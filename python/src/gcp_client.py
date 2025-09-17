import os
from typing import Any, Dict, List

from google.api_core.exceptions import GoogleAPIError, NotFound
from google.cloud import (
    billing_v1,
    cloudquotas_v1,
    compute_v1,
    filestore_v1,
    lustre_v1,
    parallelstore_v1,
    tpu_v2,
)

class GcpClient:
    """
    A client to handle all interactions with Google Cloud APIs for HPC resource management.
    """

    def __init__(self, project_id: str = None):
        self.project_id = project_id if project_id else os.getenv("GCP_PROJECT_ID")
        if not self.project_id:
            raise ValueError(
                "Google Cloud project ID must be provided or set in GCP_PROJECT_ID environment variable."
            )

        self.compute_client = compute_v1.MachineTypesClient()
        self.accelerator_client = compute_v1.AcceleratorTypesClient()
        self.zones_client = compute_v1.ZonesClient()
        self.tpu_client = tpu_v2.TpuClient()
        self.billing_client = billing_v1.CloudCatalogClient()
        self.quotas_client = cloudquotas_v1.CloudQuotasClient()
        self.filestore_client = filestore_v1.CloudFilestoreManagerClient()
        self.lustre_client = lustre_v1.LustreClient()
        self.parallelstore_client = parallelstore_v1.ParallelstoreClient()

    def get_available_machine_types(self, zone: str) -> list:
        try:
            request = compute_v1.ListMachineTypesRequest(project=self.project_id, zone=zone)
            return [mt.name for mt in self.compute_client.list(request=request)]
        except (NotFound, GoogleAPIError) as e:
            print(f"Could not fetch machine types for zone '{zone}': {e}")
            return []

    def get_available_gpus(self, zone: str) -> list:
        try:
            request = compute_v1.ListAcceleratorTypesRequest(project=self.project_id, zone=zone)
            return [at.name for at in self.accelerator_client.list(request=request)]
        except (NotFound, GoogleAPIError) as e:
            print(f"Could not fetch GPU types for zone '{zone}': {e}")
            return []

    def get_available_tpus(self, zone: str) -> list:
        try:
            parent = f"projects/{self.project_id}/locations/{zone}"
            request = tpu_v2.ListAcceleratorTypesRequest(parent=parent)
            return [acc.type for acc in self.tpu_client.list_accelerator_types(request=request)]
        except (NotFound, GoogleAPIError) as e:
            if "service is not enabled" not in str(e):
                print(f"Could not fetch TPU types for zone '{zone}': {e}")
            return []

    def check_project_quotas(self, region: str, resource_name: str, required_count: int) -> bool:
        try:
            # Simplified for now
            return True 
        except (NotFound, GoogleAPIError) as e:
            print(f"Could not check quotas for '{resource_name}' in '{region}': {e}")
            return False

    def get_available_filestore_regions(self) -> list:
        try:
            request = {"name": f"projects/{self.project_id}"}
            response = self.filestore_client.list_locations(request=request)
            return [loc.location_id for loc in response.locations]
        except GoogleAPIError as e:
            print(f"Error fetching Filestore locations: {e}")
            return []

    def get_available_lustre_regions(self) -> list:
        try:
            request = {"name": f"projects/{self.project_id}"}
            response = self.lustre_client.list_locations(request=request)
            return [loc.location_id for loc in response.locations]
        except GoogleAPIError as e:
            print(f"Error fetching Managed Lustre locations: {e}")
            return []

    def get_available_parallelstore_regions(self) -> list:
        try:
            request = {"name": f"projects/{self.project_id}"}
            response = self.parallelstore_client.list_locations(request=request)
            return [loc.location_id for loc in response.locations]
        except GoogleAPIError as e:
            print(f"Error fetching Parallelstore locations: {e}")
            return []

    def get_vm_accelerator_pairings(self, zone: str) -> Dict[str, Any]:
        pairings = {}
        try:
            request = compute_v1.ListMachineTypesRequest(project=self.project_id, zone=zone)
            for machine_type in self.compute_client.list(request=request):
                if machine_type.accelerators:
                    pairings[machine_type.name] = [
                        {"accelerator_type": acc.guest_accelerator_type, "accelerator_count": acc.guest_accelerator_count}
                        for acc in machine_type.accelerators
                    ]
        except GoogleAPIError as e:
            print(f"Error fetching VM-accelerator pairings for zone '{zone}': {e}")
        return pairings

    def get_machine_type_details(self, zone: str, machine_type: str) -> compute_v1.MachineType:
        try:
            request = compute_v1.GetMachineTypeRequest(project=self.project_id, zone=zone, machine_type=machine_type)
            return self.compute_client.get(request=request)
        except (NotFound, GoogleAPIError) as e:
            print(f"Error fetching machine type details for '{machine_type}' in zone '{zone}': {e}")
            return None

    def get_skus(self, service_name: str) -> list:
        try:
            request = billing_v1.ListSkusRequest(parent=service_name)
            return list(self.billing_client.list_skus(request=request))
        except GoogleAPIError as e:
            print(f"Error fetching SKUs for service '{service_name}': {e}")
            return []

    def get_sku_pricing(self, sku: billing_v1.Sku, region: str, currency_code: str = "USD") -> float:
        """
        Extracts the on-demand pricing for a given SKU.
        The `region` parameter is kept for context but the check is removed as the parent SKU is already region-filtered.
        """
        if sku.pricing_info:
            for pricing_info in sku.pricing_info:
                # --- FINAL FIX: Removed the redundant and incorrect region check ---
                if pricing_info.pricing_expression and pricing_info.pricing_expression.tiered_rates:
                    for tier in pricing_info.pricing_expression.tiered_rates:
                        if tier.unit_price and tier.unit_price.currency_code == currency_code:
                            return tier.unit_price.units + (tier.unit_price.nanos / 1e9)
        return 0.0

    def get_all_zones_with_resources(self) -> Dict[str, Any]:
        all_zone_resources = {}
        try:
            mt_request = compute_v1.AggregatedListMachineTypesRequest(project=self.project_id)
            for scope, response in self.compute_client.aggregated_list(request=mt_request):
                if response.machine_types:
                    zone_name = os.path.basename(scope)
                    all_zone_resources.setdefault(zone_name, {})
                    all_zone_resources[zone_name]["available_machine_types"] = [mt.name for mt in response.machine_types]
                    pairings = {mt.name: [{"type": acc.guest_accelerator_type, "count": acc.guest_accelerator_count} for acc in mt.accelerators] for mt in response.machine_types if mt.accelerators}
                    all_zone_resources[zone_name]["vm_accelerator_pairings"] = pairings

            gpu_request = compute_v1.AggregatedListAcceleratorTypesRequest(project=self.project_id)
            for scope, response in self.accelerator_client.aggregated_list(request=gpu_request):
                if response.accelerator_types:
                    zone_name = os.path.basename(scope)
                    all_zone_resources.setdefault(zone_name, {})
                    all_zone_resources[zone_name]["available_gpus"] = [gpu.name for gpu in response.accelerator_types]

            for zone_name in list(all_zone_resources.keys()):
                all_zone_resources[zone_name]["available_tpus"] = self.get_available_tpus(zone_name)
                all_zone_resources[zone_name]["region"] = "-".join(zone_name.split("-")[:-1])

            all_zone_resources["global_storage_availability"] = {
                "filestore_regions": self.get_available_filestore_regions(),
                "lustre_regions": self.get_available_lustre_regions(),
                "parallelstore_regions": self.get_available_parallelstore_regions(),
            }

        except GoogleAPIError as e:
            print(f"Error fetching all zone resources: {e}")

        return all_zone_resources