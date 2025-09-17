import yaml
from typing import Dict, Any

class YamlBuilder:
    """
    A builder to construct and write HPC blueprint YAML files from user inputs.
    This version is more flexible and modular.
    """

    def build_and_write_yaml(
        self,
        output_file: str,
        blueprint_name: str,
        deployment_name: str,
        project_id: str,
        region: str,
        zone: str,
        machine_type: str,
        node_count: int,
        gpu_type: str = None,
        gpu_count: int = 0,
        tpu_type: str = None,         # --- IMPROVEMENT 3: Add TPU support ---
        tpu_count: int = 0,
        storage_configs: list = None, # --- IMPROVEMENT 2: Allow flexible storage configs ---
    ) -> None:
        """
        Constructs a YAML blueprint dictionary and writes it to a file.
        """
        # --- IMPROVEMENT 1: Build modules dynamically instead of modifying a static structure ---
        modules = []

        # 1. Network Module (static)
        modules.append({
            "id": "network",
            "source": "modules/network/vpc",
        })

        # 2. Compute Nodeset Module
        compute_settings = {
            "machine_type": machine_type,
            "node_count_dynamic_max": node_count,
        }
        # Add GPU configuration if provided
        if gpu_type and gpu_count > 0:
            compute_settings["gpu"] = {
                "type": gpu_type,
                "count": gpu_count,
            }
        # Add TPU configuration if provided
        if tpu_type and tpu_count > 0:
            compute_settings["tpu"] = {
                "type": tpu_type,
                "count": tpu_count,
            }
        
        modules.append({
            "id": "compute_nodeset",
            "source": "community/modules/compute/schedmd-slurm-gcp-v6-nodeset",
            "use": ["network"],
            "settings": compute_settings,
        })
        
        # --- IMPROVEMENT 2 (cont.): Add storage configurations from a flexible list ---
        # The `storage_configs` parameter allows for custom module sources, mounts, etc.
        # Example of storage_configs:
        # [
        #     {"type": "filestore", "capacity_gb": 1024, "id": "homefs", "mount": "/home"},
        #     {"type": "lustre", "capacity_gb": 2048, "id": "scratch", "mount": "/scratch"}
        # ]
        if storage_configs:
            for config in storage_configs:
                storage_type = config.get("type")
                capacity_gb = config.get("capacity_gb", 0)

                if not storage_type or capacity_gb <= 0:
                    continue
                
                # Use provided details or fall back to sensible defaults
                module_id = config.get("id", f"{storage_type}fs")
                mount_point = config.get("mount", f"/{module_id}")
                
                storage_module = {
                    "id": module_id,
                    "use": ["network"],
                    "settings": {
                        "local_mount": mount_point,
                        "capacity_gb": capacity_gb,
                    },
                }

                if storage_type == "filestore":
                    storage_module["source"] = config.get("source", "modules/file-system/filestore")
                elif storage_type == "lustre":
                    storage_module["source"] = config.get("source", "community/modules/file-system/DDN-EXAScaler")
                # Add other storage types like "parallelstore" here
                
                modules.append(storage_module)


        # Assemble the final blueprint
        blueprint = {
            "blueprint_name": blueprint_name,
            "vars": {
                "project_id": project_id,
                "deployment_name": deployment_name,
                "region": region,
                "zone": zone,
            },
            "deployment_groups": [
                {
                    "group": "primary",
                    "modules": modules,
                }
            ],
        }

        try:
            with open(output_file, "w") as f:
                # Use a custom dumper for better formatting if needed, but default is fine
                yaml.dump(blueprint, f, sort_keys=False, indent=2, default_flow_style=False)
            print(f"Successfully generated blueprint: {output_file}")
        except IOError as e:
            print(f"Error writing YAML file {output_file}: {e}")