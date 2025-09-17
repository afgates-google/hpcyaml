import click
import os
import yaml
from src.gcp_client import GcpClient
from src.validator import Validator
from src.yaml_builder import YamlBuilder
from google.cloud import compute_v1  # For machine type details
from google.api_core.exceptions import NotFound, GoogleAPIError


@click.group()
def cli():
    """
    A CLI tool for generating and validating Google Cloud HPC deployment configurations.
    """
    pass


@cli.command()
@click.option("--blueprint-name", help="The name of the blueprint.")
@click.option("--deployment-name", help="The name of the deployment.")
@click.option("--project-id", help="The Google Cloud project ID.")
@click.option("--region", help="The Google Cloud region.")
@click.option("--zone", help="The Google Cloud zone for the cluster.")
@click.option("--machine-type", help="The machine type for compute nodes.")
@click.option("--node-count", type=int, help="The number of compute nodes.")
@click.option("--gpu-type", help="The type of GPU to attach (e.g., nvidia-tesla-t4).")
@click.option("--gpu-count", type=int, help="The number of GPUs to attach.")
@click.option("--storage-type", help="The type of storage (e.g., lustre, filestore).")
@click.option("--storage-capacity-gb", type=int, help="The capacity of storage in GB.")
@click.option(
    "--output-file",
    default="hpc-blueprint.yaml",
    help="The name of the output YAML file.",
)
@click.option("--interactive", is_flag=True, help="Enable interactive wizard mode.")
@click.option(
    "--template", help="Use a predefined template from the templates directory."
)
def generate(
    blueprint_name: str,
    deployment_name: str,
    project_id: str,
    region: str,
    zone: str,
    machine_type: str,
    node_count: int,
    gpu_type: str,
    gpu_count: int,
    storage_type: str,
    storage_capacity_gb: int,
    output_file: str,
    interactive: bool,
    template: str,
):
    """
    Generates a new HPC blueprint YAML file.
    """
    template_values = {}
    if template:
        template_path = os.path.join(
            os.path.dirname(__file__), "..", "templates", f"{template}.yaml"
        )
        if not os.path.exists(template_path):
            click.echo(f"Error: Template '{template}' not found.")
            exit(1)
        with open(template_path, "r") as f:
            template_values = yaml.safe_load(f)

    # Override template values with CLI options if provided
    blueprint_name = (
        blueprint_name
        if blueprint_name is not None
        else template_values.get("blueprint_name")
    )
    deployment_name = (
        deployment_name
        if deployment_name is not None
        else template_values.get("deployment_name")
    )
    project_id = (
        project_id if project_id is not None else template_values.get("project_id")
    )
    region = (
        region if region is not None else template_values.get("region", "us-central1")
    )
    zone = zone if zone is not None else template_values.get("zone", "us-central1-a")
    machine_type = (
        machine_type
        if machine_type is not None
        else template_values.get("machine_type", "n2-standard-2")
    )
    node_count = (
        node_count if node_count is not None else template_values.get("node_count", 2)
    )
    gpu_type = gpu_type if gpu_type is not None else template_values.get("gpu_type")
    gpu_count = (
        gpu_count if gpu_count is not None else template_values.get("gpu_count", 0)
    )
    storage_type = (
        storage_type
        if storage_type is not None
        else template_values.get("storage_type")
    )
    storage_capacity_gb = (
        storage_capacity_gb
        if storage_capacity_gb is not None
        else template_values.get("storage_capacity_gb", 0)
    )

    # Ensure required fields are present after template and CLI options
    if not all([blueprint_name, deployment_name, project_id]):
        click.echo(
            "Error: Missing required options. Please provide --blueprint-name, --deployment-name, and --project-id, or use a template that defines them."
        )
        exit(1)

    if interactive:
        click.echo("Entering interactive blueprint generation wizard...")
        blueprint_name = click.prompt("Enter blueprint name", default=blueprint_name)
        deployment_name = click.prompt("Enter deployment name", default=deployment_name)
        project_id = click.prompt("Enter GCP project ID", default=project_id)
        region = click.prompt("Enter GCP region", default=region)
        zone = click.prompt("Enter GCP zone", default=zone)
        machine_type = click.prompt(
            "Enter machine type for compute nodes", default=machine_type
        )
        node_count = click.prompt(
            "Enter number of compute nodes", type=int, default=node_count
        )
        if click.confirm("Do you want to add GPUs?"):
            gpu_type = click.prompt(
                "Enter GPU type (e.g., nvidia-tesla-t4)",
                default=gpu_type if gpu_type else "",
            )
            gpu_count = click.prompt(
                "Enter number of GPUs", type=int, default=gpu_count
            )
        if click.confirm("Do you want to add storage?"):
            storage_type = click.prompt(
                "Enter storage type (e.g., lustre, filestore)",
                default=storage_type if storage_type else "",
            )
            storage_capacity_gb = click.prompt(
                "Enter storage capacity in GB", type=int, default=storage_capacity_gb
            )
        output_file = click.prompt("Enter output YAML file name", default=output_file)

    builder = YamlBuilder()
    builder.build_and_write_yaml(
        output_file=output_file,
        blueprint_name=blueprint_name,
        deployment_name=deployment_name,
        project_id=project_id,
        region=region,
        zone=zone,
        machine_type=machine_type,
        node_count=node_count,
        gpu_type=gpu_type,
        gpu_count=gpu_count,
        storage_type=storage_type,
        storage_capacity_gb=storage_capacity_gb,
    )


@cli.command()
@click.argument("blueprint_path", type=click.Path(exists=True))
@click.option("--region", required=True, help="The Google Cloud region for validation.")
@click.option("--zone", required=True, help="The Google Cloud zone for validation.")
@click.option("--project-id", required=True, help="The Google Cloud project ID.")
def validate(blueprint_path: str, region: str, zone: str, project_id: str):
    """
    Validates an existing HPC blueprint YAML file against GCP resource availability and constraints.
    """
    gcp_client = GcpClient(project_id=project_id)
    validator = Validator(gcp_client)

    if validator.validate_blueprint(blueprint_path, region, zone):
        click.echo(
            f"Blueprint '{blueprint_path}' is valid for deployment in '{region}'/'{zone}'."
        )
    else:
        click.echo(f"Blueprint '{blueprint_path}' has validation errors:")
        for error in validator.get_errors():
            click.echo(f"- {error}")
        exit(1)


@cli.command()
@click.argument("blueprint_path", type=click.Path(exists=True))
@click.option("--project-id", required=True, help="The Google Cloud project ID.")
@click.option(
    "--region", required=True, help="The Google Cloud region for cost estimation."
)
def estimate_cost(blueprint_path: str, project_id: str, region: str):
    """
    Estimates the monthly cost of resources defined in an HPC blueprint YAML file.
    """
    gcp_client = GcpClient(project_id=project_id)
    validator = Validator(gcp_client)  # Use validator to extract resources

    extracted_resources = validator.get_extracted_resources_for_cost_estimation(
        blueprint_path
    )
    if not extracted_resources:
        click.echo("Could not extract resources from blueprint for cost estimation.")
        exit(1)

    # Define Google Cloud Service IDs for billing
    COMPUTE_ENGINE_SERVICE_ID = "services/6F81-5844-456A"
    # These are example service IDs, actual IDs might vary and need to be looked up
    FILESTORE_SERVICE_ID = "services/0000-0000-0000-0001"  # Placeholder
    LUSTRE_SERVICE_ID = "services/0000-0000-0000-0002"  # Placeholder
    PARALLELSTORE_SERVICE_ID = "services/0000-0000-0000-0003"  # Placeholder

    total_estimated_cost = 0.0
    cost_breakdown = {
        "Compute (CPUs)": 0.0,
        "Compute (RAM)": 0.0,
        "Accelerators (GPUs)": 0.0,
        "Accelerators (TPUs)": 0.0,
        "Storage": 0.0,
    }

    # Helper to get machine type details for CPU/RAM
    machine_type_client = compute_v1.MachineTypesClient()

    # Process Compute Instances
    for instance in extracted_resources.get("compute_instances", []):
        machine_type_name = instance["machine_type"]
        node_count = instance["node_count"]
        accelerators = instance["accelerators"]

        try:
            mt_details = machine_type_client.get(
                project=project_id, zone=region + "-a", machine_type=machine_type_name
            )  # Assuming zone for machine type details
            cpus = mt_details.guest_cpus
            memory_gb = mt_details.memory_mb / 1024

            # Estimate CPU cost
            cpu_filter = f"resourceFamily=Compute AND resourceGroup=CPU AND serviceRegions={region} AND description:'{machine_type_name.split('-')[0].upper()}'"
            cpu_skus = gcp_client.get_skus(COMPUTE_ENGINE_SERVICE_ID, cpu_filter)
            if cpu_skus:
                cpu_price_per_hour = gcp_client.get_sku_pricing(cpu_skus[0], region)
                cost_breakdown["Compute (CPUs)"] += (
                    cpu_price_per_hour * cpus * node_count * 730
                )  # 730 hours/month
            else:
                click.echo(
                    f"Warning: Could not find CPU SKU for {machine_type_name} in {region}."
                )

            # Estimate RAM cost
            ram_filter = f"resourceFamily=Compute AND resourceGroup=RAM AND serviceRegions={region} AND description:'{machine_type_name.split('-')[0].upper()}'"
            ram_skus = gcp_client.get_skus(COMPUTE_ENGINE_SERVICE_ID, ram_filter)
            if ram_skus:
                ram_price_per_gb_hour = gcp_client.get_sku_pricing(ram_skus[0], region)
                cost_breakdown["Compute (RAM)"] += (
                    ram_price_per_gb_hour * memory_gb * node_count * 730
                )
            else:
                click.echo(
                    f"Warning: Could not find RAM SKU for {machine_type_name} in {region}."
                )

            # Estimate Accelerator cost
            for acc in accelerators:
                acc_type = acc["type"]
                acc_count = acc["count"]
                if acc["resource_family"] == "GPU":
                    gpu_filter = f"resourceFamily=Compute AND resourceGroup=GPU AND serviceRegions={region} AND description:'{acc_type}'"
                    gpu_skus = gcp_client.get_skus(
                        COMPUTE_ENGINE_SERVICE_ID, gpu_filter
                    )
                    if gpu_skus:
                        gpu_price_per_hour = gcp_client.get_sku_pricing(
                            gpu_skus[0], region
                        )
                        cost_breakdown["Accelerators (GPUs)"] += (
                            gpu_price_per_hour * acc_count * node_count * 730
                        )
                    else:
                        click.echo(
                            f"Warning: Could not find GPU SKU for {acc_type} in {region}."
                        )
                elif acc["resource_family"] == "TPU":
                    # TPU pricing might be more complex, using a simplified filter for now
                    tpu_filter = f"resourceFamily=Cloud TPU AND serviceRegions={region} AND description:'{acc_type}'"
                    tpu_skus = gcp_client.get_skus(
                        COMPUTE_ENGINE_SERVICE_ID, tpu_filter
                    )  # Assuming TPU SKUs are under Compute Engine service ID for now
                    if tpu_skus:
                        tpu_price_per_hour = gcp_client.get_sku_pricing(
                            tpu_skus[0], region
                        )
                        cost_breakdown["Accelerators (TPUs)"] += (
                            tpu_price_per_hour * acc_count * node_count * 730
                        )
                    else:
                        click.echo(
                            f"Warning: Could not find TPU SKU for {acc_type} in {region}."
                        )

        except NotFound:
            click.echo(
                f"Warning: Machine type '{machine_type_name}' not found for cost estimation in {region}."
            )
        except GoogleAPIError as e:
            click.echo(f"Error fetching machine type details for cost estimation: {e}")

    # Process Storage Instances
    for storage_instance in extracted_resources.get("storage_instances", []):
        storage_type = storage_instance["storage_type"]
        capacity_gb = storage_instance["capacity_gb"]
        service_id = None
        storage_filter = None

        if storage_type == "filestore":
            service_id = FILESTORE_SERVICE_ID
            storage_filter = f"resourceFamily=Storage AND resourceGroup=Filestore AND serviceRegions={region}"
        elif storage_type == "lustre":
            service_id = LUSTRE_SERVICE_ID
            storage_filter = f"resourceFamily=Storage AND resourceGroup=Lustre AND serviceRegions={region}"
        elif storage_type == "parallelstore":
            service_id = PARALLELSTORE_SERVICE_ID
            storage_filter = f"resourceFamily=Storage AND resourceGroup=Parallelstore AND serviceRegions={region}"

        if service_id and storage_filter:
            storage_skus = gcp_client.get_skus(service_id, storage_filter)
            if storage_skus:
                storage_price_per_gb_month = gcp_client.get_sku_pricing(
                    storage_skus[0], region
                )
                cost_breakdown["Storage"] += storage_price_per_gb_month * capacity_gb
            else:
                click.echo(
                    f"Warning: Could not find storage SKU for {storage_type} in {region}."
                )
        else:
            click.echo(
                f"Warning: Unknown storage type '{storage_type}' for cost estimation."
            )

    click.echo("\n--- Estimated Monthly Cost ---")
    for component, cost in cost_breakdown.items():
        click.echo(f"{component}: ${cost:.2f}")
        total_estimated_cost += cost
    click.echo("------------------------------")
    click.echo(f"Total Estimated Cost: ${total_estimated_cost:.2f}")


@cli.command()
@click.option("--project-id", required=True, help="The Google Cloud project ID.")
@click.option(
    "--gpu-type", default=None, help="Required GPU type (e.g., nvidia-h100-80gb)."
)
@click.option("--gpu-count", default=0, type=int, help="Required GPU count.")
@click.option(
    "--storage-type", default=None, help="Required storage type (e.g., lustre)."
)
def find_region(project_id: str, gpu_type: str, gpu_count: int, storage_type: str):
    """
    Recommends Google Cloud regions/zones where a given set of resource requirements can be deployed.
    """
    click.echo("Region/zone recommendation is not yet implemented.")
    # Placeholder for region finding logic


@cli.command()
def list_templates():
    """
    Lists available HPC blueprint templates.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    if not os.path.exists(templates_dir) or not os.listdir(templates_dir):
        click.echo("No templates found.")
        return

    click.echo("Available templates:")
    for filename in os.listdir(templates_dir):
        if filename.endswith(".yaml"):
            click.echo(f"- {filename.replace('.yaml', '')}")


@cli.command()
@click.option(
    "--blueprint-path",
    type=click.Path(exists=True),
    required=True,
    help="The path to the blueprint YAML file.",
)
@click.option(
    "--region", required=True, help="The Google Cloud region for quota checking."
)
@click.option("--project-id", required=True, help="The Google Cloud project ID.")
def check_quota(blueprint_path: str, region: str, project_id: str):
    """
    Checks if the current project has sufficient quotas for the resources defined in a blueprint.
    """
    gcp_client = GcpClient(project_id=project_id)
    validator = Validator(gcp_client)

    # The validate_blueprint method already includes comprehensive quota checks
    # It also handles parsing the blueprint and extracting resources internally
    if validator.validate_blueprint(
        blueprint_path, region, ""
    ):  # Zone is not strictly needed for region-level quotas
        click.echo(
            f"Quota check passed for blueprint '{blueprint_path}' in region '{region}'."
        )
    else:
        click.echo(
            f"Quota check failed for blueprint '{blueprint_path}' in region '{region}'."
        )
        click.echo("Details:")
        for error in validator.get_errors():
            if "quota" in error.lower():  # Only show quota-related errors
                click.echo(f"- {error}")
        exit(1)


if __name__ == "__main__":
    cli()
