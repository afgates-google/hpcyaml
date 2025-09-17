import yaml
from src.gcp_client import GcpClient
from typing import List, Dict, Any
from google.api_core.exceptions import NotFound, GoogleAPIError


class Validator:
    """
    A validator to check HPC blueprint YAML files against Google Cloud resource availability and constraints.
    """

    def __init__(self, gcp_client: GcpClient):
        self.gcp_client = gcp_client
        self.validation_errors = []

    def _add_error(self, message: str):
        self.validation_errors.append(message)

    def _extract_resources(self, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts resource definitions from the blueprint YAML for validation and cost estimation.
        """
        extracted_resources = {
            "compute_instances": [],
            "storage_instances": [],
        }

        for group in blueprint.get("deployment_groups", []):
            for module in group.get("modules", []):
                settings = module.get("settings", {})
                module_id = module.get("id", "unknown_module")
                module_source = module.get("source", "").lower()

                # Extract Compute Instances
                if "machine_type" in settings:
                    node_count = settings.get("node_count_dynamic_max", settings.get("node_count_static", 1))
                    accelerators = []
                    
                    if isinstance(settings.get("gpu"), dict):
                        gpu_info = settings["gpu"]
                        if gpu_info.get("type") and gpu_info.get("count") is not None:
                            accelerators.append({"type": gpu_info["type"], "count": gpu_info["count"], "family": "GPU"})
                    
                    if isinstance(settings.get("tpu"), dict):
                        tpu_info = settings["tpu"]
                        if tpu_info.get("type") and tpu_info.get("count") is not None:
                            accelerators.append({"type": tpu_info["type"], "count": tpu_info["count"], "family": "TPU"})

                    extracted_resources["compute_instances"].append({
                        "machine_type": settings["machine_type"],
                        "node_count": node_count,
                        "accelerators": accelerators,
                    })

                # Extract Storage
                storage_capacity_gb = settings.get("capacity_gb")
                if not storage_capacity_gb:
                     # HPC toolkit modules sometimes use 'local_mount' to imply a filesystem
                     if "local_mount" in settings and ("filestore" in module_source or "lustre" in module_source):
                         # If capacity isn't specified, we can't validate storage but we don't error
                         pass

                if storage_capacity_gb and storage_capacity_gb > 0:
                    storage_type = None
                    if "lustre" in module_source or "lustre" in module_id:
                        storage_type = "lustre"
                    elif "filestore" in module_source or "filestore" in module_id:
                        storage_type = "filestore"
                    elif "parallelstore" in module_source or "parallelstore" in module_id:
                        storage_type = "parallelstore"
                    
                    if storage_type:
                        extracted_resources["storage_instances"].append({
                            "storage_type": storage_type,
                            "capacity_gb": storage_capacity_gb,
                        })

        return extracted_resources

    def validate_yaml_content(self, yaml_content: str, region: str, zone: str) -> bool:
        """
        Parses YAML content and validates its resources against GCP availability and constraints.
        """
        self.validation_errors = []

        try:
            blueprint = yaml.safe_load(yaml_content)
            if not blueprint:
                self._add_error("Error: YAML content is empty or invalid.")
                return False
        except yaml.YAMLError as e:
            self._add_error(f"Error parsing YAML content: {e}")
            return False

        extracted_resources = self._extract_resources(blueprint)

        available_machine_types = self.gcp_client.get_available_machine_types(zone)
        available_gpus = self.gcp_client.get_available_gpus(zone)
        
        # 1. Validate Machine Types & GPUs
        for instance in extracted_resources["compute_instances"]:
            mt = instance["machine_type"]
            if mt not in available_machine_types:
                self._add_error(f"Machine type '{mt}' is not available in zone '{zone}'.")

            for acc in instance["accelerators"]:
                if acc["family"] == "GPU" and acc["type"] not in available_gpus:
                    self._add_error(f"GPU type '{acc['type']}' is not available in zone '{zone}'.")

        # 2. Validate Storage Types
        for storage in extracted_resources["storage_instances"]:
            storage_type = storage["storage_type"]
            if storage_type == "filestore" and region not in self.gcp_client.get_available_filestore_regions():
                self._add_error(f"Filestore is not available in region '{region}'.")
            elif storage_type == "lustre" and region not in self.gcp_client.get_available_lustre_regions():
                self._add_error(f"Managed Lustre is not available in region '{region}'.")
            elif storage_type == "parallelstore" and region not in self.gcp_client.get_available_parallelstore_regions():
                self._add_error(f"Parallelstore is not available in region '{region}'.")

        # 3. Validate VM-Accelerator Pairings
        vm_accelerator_pairings = self.gcp_client.get_vm_accelerator_pairings(zone)
        for instance in extracted_resources["compute_instances"]:
            vm_type = instance["machine_type"]
            if not instance["accelerators"]:
                continue

            supported_configs = vm_accelerator_pairings.get(vm_type)
            if not supported_configs:
                self._add_error(f"VM type '{vm_type}' does not support any accelerators in zone '{zone}'.")
                continue

            for req_acc in instance["accelerators"]:
                is_supported = any(
                    supported_acc["accelerator_type"] == req_acc["type"] and
                    supported_acc["accelerator_count"] == req_acc["count"]
                    for supported_acc in supported_configs
                )
                if not is_supported:
                    self._add_error(f"VM type '{vm_type}' does not support attaching {req_acc['count']}x '{req_acc['type']}' in zone '{zone}'.")

        # 4. Quota Checks
        # --- FIX: Added nvidia-tesla-a100 to the map and corrected CPU quota name ---
        GPU_QUOTA_MAP = {
            "nvidia-tesla-a100": "GPUS_NVIDIA_A100",
            "nvidia-tesla-p4": "GPUS_NVIDIA_TESLA_P4",
            "nvidia-tesla-v100": "GPUS_NVIDIA_TESLA_V100",
            "nvidia-tesla-k80": "GPUS_NVIDIA_K80",
        }
        
        cpu_req = 0
        gpu_req = {}
        for instance in extracted_resources["compute_instances"]:
            mt_details = self.gcp_client.get_machine_type_details(zone, instance["machine_type"])
            if mt_details:
                cpu_req += mt_details.guest_cpus * instance["node_count"]
            else:
                self._add_error(f"Could not retrieve details for machine type '{instance['machine_type']}' for quota check.")
                continue

            for acc in instance["accelerators"]:
                if acc["family"] == "GPU":
                    # Normalize the GPU type for map lookup
                    normalized_gpu = acc["type"].lower().replace(" ", "-")
                    quota_name = GPU_QUOTA_MAP.get(normalized_gpu)
                    if quota_name:
                        gpu_req[quota_name] = gpu_req.get(quota_name, 0) + acc["count"] * instance["node_count"]
                    else:
                        self._add_error(f"Quota check skipped: Unknown quota name for GPU type '{acc['type']}'.")
        
        # Use a more generic quota name for CPUs, as it can vary. 'CPUS' is common for regional quotas.
        if cpu_req > 0 and not self.gcp_client.check_project_quotas(region, "CPUS", cpu_req):
            self._add_error(f"Insufficient CPU quota in region '{region}'. Required: {cpu_req}.")

        for quota_name, count in gpu_req.items():
            if not self.gcp_client.check_project_quotas(region, quota_name, count):
                self._add_error(f"Insufficient quota for '{quota_name}' in region '{region}'. Required: {count}.")

        return not self.validation_errors

    def get_errors(self) -> List[str]:
        return self.validation_errors