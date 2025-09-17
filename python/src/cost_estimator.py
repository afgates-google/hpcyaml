"""
This module contains the logic for estimating the cost of a blueprint.
"""

from src.gcp_client import GcpClient
from google.cloud import billing_v1
from typing import Dict, Any

# Service IDs for the Cloud Billing Catalog API
COMPUTE_ENGINE_SERVICE_ID = "6F81-5844-456A"
FILESTORE_SERVICE_ID = "9662-B51E-5089"

def _calculate_monthly_cost_from_sku(
    sku: billing_v1.Sku,
    usage_amount: float,
    region: str,
    gcp_client: "GcpClient"
) -> float:
    """
    Calculates the estimated monthly cost for a given SKU and usage amount.
    """
    if not sku:
        return 0.0

    price = gcp_client.get_sku_pricing(sku, region)
    if price == 0.0:
        return 0.0

    if sku.pricing_info and sku.pricing_info[0].pricing_expression:
        usage_unit = sku.pricing_info[0].pricing_expression.usage_unit_description.lower()
        if "hour" in usage_unit:
            # 730 hours represents a standard monthly usage
            return price * usage_amount * 730
        elif "gibibyte" in usage_unit or "gb" in usage_unit:
            return price * usage_amount

    return price * usage_amount

def _find_sku(skus: list, description_keywords: list, region: str) -> billing_v1.Sku:
    """
    Finds a SKU from a list that matches a region and all keywords in the description.
    """
    for sku in skus:
        if region in sku.service_regions and all(keyword.lower() in sku.description.lower() for keyword in description_keywords):
            return sku
    return None

def estimate_cost(extracted_resources: Dict[str, Any], region: str, zone: str, gcp_client: "GcpClient") -> tuple[float, dict]:
    """
    Estimates the monthly cost of the configuration by querying the Cloud Billing Catalog API.
    """
    total_cost = 0.0
    cost_breakdown = {}

    compute_service_name = f"services/{COMPUTE_ENGINE_SERVICE_ID}"
    compute_skus = gcp_client.get_skus(compute_service_name)

    # --- Compute Cost ---
    for instance in extracted_resources.get("compute_instances", []):
        machine_type = instance["machine_type"]
        node_count = instance.get("node_count", 1)
        
        # --- FINAL FIX: Implement smarter pricing logic for different VM types ---
        is_priced_as_unit = False

        # 1. First, try to find an all-inclusive SKU for the entire machine instance.
        #    This is common for specialized types like A2, C3, H3, etc.
        vm_instance_sku = _find_sku(compute_skus, [machine_type, "instance"], region)
        if vm_instance_sku:
            instance_cost = _calculate_monthly_cost_from_sku(vm_instance_sku, node_count, region, gcp_client)
            if instance_cost > 0:
                cost_breakdown[f"{node_count}x {machine_type} Instance"] = instance_cost
                total_cost += instance_cost
                is_priced_as_unit = True # Mark that we've priced this machine.

        # 2. If no all-inclusive SKU was found, fall back to pricing components separately.
        #    This is the standard model for general-purpose machines like N1, N2, E2.
        if not is_priced_as_unit:
            machine_details = gcp_client.get_machine_type_details(zone, machine_type)
            if machine_details:
                machine_series = machine_type.split("-")[0].upper()
                
                # vCPU cost
                cpu_sku = _find_sku(compute_skus, [machine_series, "vCPU"], region)
                if cpu_sku:
                    cpu_cost = _calculate_monthly_cost_from_sku(cpu_sku, machine_details.guest_cpus * node_count, region, gcp_client)
                    cost_breakdown[f"{node_count}x {machine_type} (vCPU)"] = cpu_cost
                    total_cost += cpu_cost
                
                # Memory cost
                memory_gb = machine_details.memory_mb / 1024
                ram_sku = _find_sku(compute_skus, [machine_series, "RAM"], region)
                if ram_sku:
                    memory_cost = _calculate_monthly_cost_from_sku(ram_sku, memory_gb * node_count, region, gcp_client)
                    cost_breakdown[f"{node_count}x {machine_type} (Memory)"] = memory_cost
                    total_cost += memory_cost

                # GPU cost (only if not priced as a unit)
                for accelerator in instance.get("accelerators", []):
                    gpu_type = accelerator["type"].replace("nvidia-", "").replace("tesla-","").strip()
                    gpu_count = accelerator["count"]
                    gpu_sku = _find_sku(compute_skus, [gpu_type, "GPU"], region)
                    if gpu_sku:
                        gpu_cost = _calculate_monthly_cost_from_sku(gpu_sku, gpu_count * node_count, region, gcp_client)
                        cost_breakdown[f"{gpu_count * node_count}x {accelerator['type']} GPU"] = gpu_cost
                        total_cost += gpu_cost
            else:
                 cost_breakdown[f"{node_count}x {machine_type}"] = "Machine Type Details Not Found"

    # --- Storage Cost ---
    filestore_service_name = f"services/{FILESTORE_SERVICE_ID}"
    filestore_skus = gcp_client.get_skus(filestore_service_name)
    
    for storage in extracted_resources.get("storage_instances", []):
        storage_type = storage["storage_type"]
        capacity_gb = storage["capacity_gb"]
        storage_key = f"Storage ({storage_type.capitalize()})"

        if storage_type == "filestore":
            filestore_sku = _find_sku(filestore_skus, ["Zonal", "Capacity"], region)
            if filestore_sku:
                storage_cost = _calculate_monthly_cost_from_sku(filestore_sku, capacity_gb, region, gcp_client)
                cost_breakdown[storage_key] = storage_cost
                total_cost += storage_cost
            else:
                cost_breakdown[storage_key] = "SKU Not Found"
        else:
            cost_breakdown[storage_key] = "Pricing model not yet implemented"

    return total_cost, cost_breakdown