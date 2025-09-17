"""
This module will contain the logic for finding suitable regions.
"""

from src import gcp_client


def find_regions(requirements: dict, project_id: str) -> list[str]:
    """
    Finds regions that can satisfy the given resource requirements.

    Args:
        requirements: A dictionary containing the resource requirements.
        project_id: The Google Cloud project ID.

    Returns:
        A list of suitable zones.
    """
    suitable_zones = []

    # This is a simplified implementation that only checks a few hardcoded regions.
    # A real implementation would need to get a list of all regions and zones
    # and iterate through them.
    regions_to_check = ["us-central1", "europe-west4"]
    zones_to_check = ["a", "b"]  # Check zones 'a' and 'b' in each region

    for region in regions_to_check:
        for zone_suffix in zones_to_check:
            zone = f"{region}-{zone_suffix}"

            # --- Machine Type Check ---
            machine_type = requirements.get("machine_type")
            if machine_type:
                available_machine_types = gcp_client.get_available_machine_types(
                    project_id, zone
                )
                if machine_type not in available_machine_types:
                    continue

            # --- GPU Check ---
            gpu_type = requirements.get("gpu_type")
            if gpu_type:
                available_gpus = gcp_client.get_available_gpus(project_id, zone)
                if gpu_type not in available_gpus:
                    continue

            # --- Storage Check ---
            storage_type = requirements.get("storage_type")
            if storage_type == "filestore":
                if not gcp_client.check_filestore_availability(project_id, region):
                    continue
            elif storage_type == "lustre":
                try:
                    if not gcp_client.check_lustre_availability(project_id, region):
                        continue
                except NotImplementedError:
                    # For now, we assume lustre is available if the check is not implemented
                    pass

            suitable_zones.append(zone)

    return suitable_zones
