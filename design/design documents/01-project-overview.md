Help me design a prompt I will use with an AI Coding Agent. I am going to build a application to create and validate YAML files necessary to support deployments of HPC resources. Help me build uut a software design based on the documentation available to implement HPC on Google Cloud. The goal is to be able to generate new YAMLs for any configuration such as H3 running with TPU support, to be able to take a pre-created YAML and verify if it is valid to deploy on a particular region or zone depending on the availability of HPC resources. Please add any features or functions that you think will be useful

**Prompt for AI Coding Agent Your Role:** You are an expert Python developer with deep expertise in Google Cloud Platform (GCP), particularly in HPC infrastructure, DevOps, and building robust command-line tools. Your task is to design and build a Python application for creating and validating Google Cloud HPC deployment configurations.

**Project Goal:** The primary goal is to create a Python-based command-line interface (CLI) tool named hpc-config-manager. This tool will streamline the creation and validation of YAML configuration files used for deploying High-Performance Computing (HPC) environments on Google Cloud. The YAML files must be compatible with the Google Cloud Cluster Toolkit blueprint format.

Core Features to Implement

1. YAML Generation (generate command):

Functionality: This feature will generate a valid YAML blueprint file based on user-specified parameters.

User Input: The user must be able to specify the configuration via CLI flags (e.g., --vm-family h3, --machine-type h3-standard-88, --gpu-type nvidia-h100-80gb, --gpu-count 8, --storage-type lustre, --region us-central1).

Configurable Components: The tool must support configuration for:

Compute: VM family (H3, H4D, C3, A3, etc.), specific machine type, and custom CPU/memory.

Accelerators: GPU or TPU type and count. The tool must understand valid hardware combinations (e.g., TPUs are not available with H3 VMs; certain GPUs are only available with specific VM families).

Storage: High-performance storage options like Google Cloud Managed Lustre, Parallelstore, and Filestore, including capacity and performance tiers.

Networking: Options like enabling high-bandwidth networking (100/200 Gbps) and Cloud RDMA.

Scheduler: Integration with schedulers like Slurm.

Output: A well-formatted YAML file that is compatible with the Google Cloud Cluster Toolkit.

2. YAML Validation (validate command):

Functionality: This feature will take an existing YAML blueprint file and validate it against resource availability in a specified Google Cloud region or zone.

User Input: The user will provide the path to the YAML file and the target region/zone (e.g., hpc-config-manager validate --file my-cluster.yaml --region europe-west4).

Validation Checks: The tool must perform the following checks by querying the Google Cloud APIs in real-time:

Verify that the specified VM family and machine type are available in the target region/zone.

Verify that the specified GPU/TPU type and requested quantity are available.

Verify that the specified storage services (Lustre, Filestore, etc.) are available in the region.

Check for invalid combinations of resources (e.g., H3 VMs do not support TPU accelerators).

Output:

If valid: A clear success message.

If invalid: A detailed, user-friendly report listing each specific resource that is unavailable or misconfigured and why (e.g., "ERROR: GPU type 'nvidia-tesla-p100' is not available in zone 'us-central1-a'.")

Suggested Additional Features (Please add these) Interactive Wizard Mode: An interactive mode (hpc-config-manager generate --interactive) that guides the user through creating a YAML file with a series of questions. At each step, it should provide available options fetched live from GCP (e.g., list available machine types in a chosen zone).

Cost Estimation (estimate-cost command): A command that takes a YAML file and provides a monthly cost estimate for the defined resources by using the Google Cloud Pricing API. The output should break down the cost by component (Compute, Storage, etc.).

Region/Zone Recommendation (find-region command): A command that takes a set of resource requirements (e.g., 8x H100 GPUs, Lustre storage) and searches across all Google Cloud regions to find and recommend zones where this configuration can be deployed.

Template Library: Include a built-in library of common HPC cluster templates (e.g., wrf-cluster, genomics-pipeline, llm-training-pod) that users can generate and customize.

Proposed Software Design & Tech Stack Language: Python 3.9+

Key Libraries:

google-cloud-compute: To interact with the Compute Engine API for resource availability checks.

google-cloud-billing: To interact with the Cloud Billing/Pricing API for cost estimation.

PyYAML: For parsing and generating YAML files.

click: To build a user-friendly and robust CLI.

Architecture:

gcp_client.py module: A dedicated module to handle all interactions with Google Cloud APIs. This will contain functions like get_available_machine_types(zone), get_available_gpus(zone), etc. It should handle authentication gracefully using Application Default Credentials.

yaml_builder.py module: Contains the logic for constructing the YAML blueprint from user inputs.

validator.py module: Contains the logic for parsing a YAML file and running all validation checks using the gcp_client module.

main.py (or cli.py): The main entry point for the CLI, defining the commands (generate, validate, etc.) using the click library.

templates/ directory: To store the YAML templates for the template library feature.

Implementation Steps Set up the basic Python project structure with the proposed modules.

Implement the gcp_client.py module first. Focus on authentication and writing the functions to query resource availability.

Develop the validate command. This will prove out the core logic of checking resource availability.

Develop the generate command, ensuring it produces YAML that conforms to the Cluster Toolkit blueprint structure.

Implement the additional features: interactive mode, cost estimation, and region finding.

Add comprehensive error handling, user-friendly output messages, and unit tests for each module.

Please begin by outlining the project structure and then start implementing the gcp_client.py module.
