Help me design a prompt I will use with an AI Coding Agent. I am going to build a application to create and validate YAML files necessary to support deployments of HPC resources. Help me build uut a software design based on the documentation available to implement HPC on Google Cloud. The goal is to be able to generate new YAMLs for any configuration such as H3 running with TPU support, to be able to take a pre-created YAML and verify if it is valid to deploy on a particular region or zone depending on the availability of HPC resources. Please add any features or functions that you think will be useful

**Prompt for AI Coding Agent Your Role:** You are an expert Python developer with deep expertise in Google Cloud Platform (GCP), particularly in HPC infrastructure, DevOps, and building robust command-line tools. Your task is to design and build a Python application for creating and validating Google Cloud HPC deployment configurations.

**Project Goal:** The primary goal is to create a Python-based command-line interface (CLI) tool named hpc-config-manager. This tool will streamline the creation and validation of YAML configuration files used for deploying High-Performance Computing (HPC) environments on Google Cloud. The YAML files must be compatible with the Google Cloud Cluster Toolkit blueprint format.

Core Features to Implement

1. YAML Generation (generate command):

Functionality: This feature will generate a valid YAML blueprint file based on user-specified parameters.

User Input: The user must be able to specify the configuration via CLI flags (e.g., \--vm-family h3, \--machine-type h3-standard-88, \--gpu-type nvidia-h100-80gb, \--gpu-count 8, \--storage-type lustre, \--region us-central1).

Configurable Components: The tool must support configuration for:

Compute: VM family (H3, H4D, C3, A3, etc.), specific machine type, and custom CPU/memory.

Accelerators: GPU or TPU type and count. The tool must understand valid hardware combinations (e.g., TPUs are not available with H3 VMs; certain GPUs are only available with specific VM families).

Storage: High-performance storage options like Google Cloud Managed Lustre, Parallelstore, and Filestore, including capacity and performance tiers.

Networking: Options like enabling high-bandwidth networking (100/200 Gbps) and Cloud RDMA.

Scheduler: Integration with schedulers like Slurm.

Output: A well-formatted YAML file that is compatible with the Google Cloud Cluster Toolkit.

2. YAML Validation (validate command):

Functionality: This feature will take an existing YAML blueprint file and validate it against resource availability in a specified Google Cloud region or zone.

User Input: The user will provide the path to the YAML file and the target region/zone (e.g., hpc-config-manager validate \--file my-cluster.yaml \--region europe-west4).

Validation Checks: The tool must perform the following checks by querying the Google Cloud APIs in real-time:

Verify that the specified VM family and machine type are available in the target region/zone.

Verify that the specified GPU/TPU type and requested quantity are available.

Verify that the specified storage services (Lustre, Filestore, etc.) are available in the region.

Check for invalid combinations of resources (e.g., H3 VMs do not support TPU accelerators).

Output:

If valid: A clear success message.

If invalid: A detailed, user-friendly report listing each specific resource that is unavailable or misconfigured and why (e.g., "ERROR: GPU type 'nvidia-tesla-p100' is not available in zone 'us-central1-a'.").

Suggested Additional Features (Please add these) Interactive Wizard Mode: An interactive mode (hpc-config-manager generate \--interactive) that guides the user through creating a YAML file with a series of questions. At each step, it should provide available options fetched live from GCP (e.g., list available machine types in a chosen zone).

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

gcp\_client.py module: A dedicated module to handle all interactions with Google Cloud APIs. This will contain functions like get\_available\_machine\_types(zone), get\_available\_gpus(zone), etc. It should handle authentication gracefully using Application Default Credentials.

yaml\_builder.py module: Contains the logic for constructing the YAML blueprint from user inputs.

validator.py module: Contains the logic for parsing a YAML file and running all validation checks using the gcp\_client module.

main.py (or cli.py): The main entry point for the CLI, defining the commands (generate, validate, etc.) using the click library.

templates/ directory: To store the YAML templates for the template library feature.

Implementation Steps Set up the basic Python project structure with the proposed modules.

Implement the gcp\_client.py module first. Focus on authentication and writing the functions to query resource availability.

Develop the validate command. This will prove out the core logic of checking resource availability.

Develop the generate command, ensuring it produces YAML that conforms to the Cluster Toolkit blueprint structure.

Implement the additional features: interactive mode, cost estimation, and region finding.

Add comprehensive error handling, user-friendly output messages, and unit tests for each module.

Please begin by outlining the project structure and then start implementing the gcp\_client.py module.

Of course\! Here is a comprehensive research report and software design document to help you build your High-Performance Computing (HPC) configuration management application for Google Cloud. This report synthesizes the official documentation and best practices for implementing HPC on Google Cloud and can serve as a detailed prompt for an AI coding agent.

---

## Research Report: Designing an HPC Configuration Manager for Google Cloud

This report outlines the software design for a Python-based command-line interface (CLI) tool, named `hpc-config-manager`. The primary goal of this tool is to streamline the creation and validation of YAML configuration files used for deploying High-Performance Computing (HPC) environments on Google Cloud, specifically targeting the **Google Cloud Cluster Toolkit** blueprint format [\[1\]](https://cloud.google.com/cluster-toolkit/docs/overview)[\[2\]](https://cloud.google.com/blog/products/compute/new-google-cloud-hpc-toolkit) .

### 1\. Core Application Design & Technology Stack

The application will be a robust Python CLI tool designed for ease of use and extensibility.

* **Language:** Python 3.9+  
* **Key Libraries:**  
  * `click`: To build a user-friendly and powerful command-line interface with support for commands, flags, and interactive modes [\[3\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH1wF7y4jFp7zankhl7qyMTMlclmVTBs8vs8hxmK6KaYHK7B6e9EYvhs-jI259ULtPAZ5G5InP2vZKYgIphLdbZqVNpofjRRnN_gIeep3-Xca90lldBqRIKaLYG22Uf71ljtJIUiWM=)[\[4\]](https://drive.google.com/a/google.com/open?id=1KIIekWOkSpNZRWTeH74NXsKfQjf0Q3LcYh9SHKidbwE)[\[5\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHCWqdcs0S0mkZQDRhDuREwz4CMr4CNyjspiF49R0y2rjqPBlSqju0zDRRyqb74zlFhZqxT4Ivm1g20HnL4zPBWA9i0H81EysiDVbEPkj76P3uQV4YDK_1aC_Y4ouPPIUXJSyHGH4KqRVXToW2IIh9mG2ZztskKWw7HpoM0crAeCeSfC4yrit7xSSpj02JWAx6yISi7V43DQMx3vqRegMFLJfBPXhqhUwBNcSg_BvA6KQX9aaQ1BBc=) .  
  * `PyYAML`: For parsing and generating YAML files, which are the core of the Cluster Toolkit blueprints [\[6\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE4sz4_g_7-cRpPcN0R5Zj_JGrOGqSh2XnyYV7qlttrF_WpBlcNAi1P26dciZJ0cYeEMUfglZY35SzUcBJ2IrTcRtDPYn3mWKPma1nHAZZzOdS5qgiFtNPxzalgIY6ojlXOhDsYhIOE0aJBOmf2fKNzkg==)[\[7\]](https://drive.google.com/a/google.com/open?id=1-XfKNVvkTgdMRQmnpFN6r1mpCVgpJb-aVm1OIhQevDQ&resourcekey=0-hf2XfJFhKSAefTWpEoyX_Q)[\[8\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEdYuzN7JNOitZUgpGZckGLBHd3UqL4dLVaMXSiuMPVD_F6CzWh0mQIvYHhMSFW_W9Bb9dgcJ0uArur0aEyPRQDzfTMISe7qbXK8BguT-OMaHeVHNDEPcPvBr6RsVJPms8AwDHyXZ4KRk56dX9dc8JbuWeBzFxihQQ6wn2_ev6TxXIRcFQcYfzafXHB)[\[9\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFaD3MDkU0h4yW2kgv6StSX6N1TA4rc5hnh8jAfH_qT_7fVrSsxmnfEM2kPP4UmfYiq4CT9J0i5dQdnHoNvdt1PTxPoDpegzk5_W2zPmpOVb8HtXPs8Rlm4W06JmD1gRE2OtMGUbNtdmJBKhqQoz1tG2ym99P1IqS5ckPw3I2nb6Hwh4rEEbS8naemNrA==) .  
  * `google-cloud-compute`: To interact with the Compute Engine API for checking the availability of VMs, GPUs, and other compute resources [\[10\]](https://cloud.google.com/compute/docs/reference/rest/v1/machineTypes/list)[\[11\]](https://yaqs.corp.google.com/eng/q/8878020932128473088) .  
  * `google-cloud-billing`: To interact with the Cloud Billing Catalog API for cost estimation features [\[12\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGTxZ3RPhyvmxgsFBAO7tqJrz7i3WFZ9pHCfHjcKWrEvuSSfhg5qWLT1XhMSrJkHN0m58mp3rEPT8NZfGZo7dshBoDYzRj-TiK6FPHRBWTM4BtJbi8kttr7rq0btDtcALdP0VsHpjtyOMTi1fBB-Vnjo5WTB8LUH6i1q0ES-HM=)[\[13\]](https://cloud.google.com/blog/topics/cost-management/introducing-cloud-billing-catalog-api-gcp-pricing-in-real-time) .  
  * `google-cloud-filestore`, `google-cloud-lustre`: To validate the availability of high-performance storage options [\[14\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEg0h9S8YTf4rgX66PZygmb62Se-XzpJ4hytHeSetmTXvTOQkdA30gVrrtF8k0P9doqFKnBmgGJaTezgwakI5LA42PIYrdabf35bNJAyht74TBZkWAYuVtGs6l8HgHHzS-JU_WAwFg45fl-b69TukhVA8oMgg==)[\[15\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHX9yMI4YeYa-X2vlRUk6cY3WR_ReFFT5pmWCDPTS2E-VI-7i4GMQWH5-BuEUXeip_rYCXXFrYFLLtUVItG2EoHVdrB2yYuEcC4avT1iT3yyJ74esH05YiYCej8v5aADtak0fbyTgwJxSLjZ0WO7nZZr5q5IGa90sCQaACVOnwJN2PgJw==) .  
  * `google-cloud-quotas`: To programmatically check project resource quotas [\[16\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG1fmRaqQqreqBXpeAqVeOvSCidBX0-v_9bX6TVwfExHUZZSdDGCeBmvBoCkwhX1Du2nO1ORtXGNocuJtiDTRqUkrNYoRMT4pQ-9JFxB0SfUjFWbWQ5PsQnk3JY3g1P8lwpOoFLQHKIU5zRx8OBNPkxd0xS) .  
* **Proposed Architecture:** A modular design is recommended for maintainability and scalability.  
  * **`cli.py` (or `main.py`):** The main entry point for the CLI, defining the commands (`generate`, `validate`, etc.) using the `click` library [\[4\]](https://drive.google.com/a/google.com/open?id=1KIIekWOkSpNZRWTeH74NXsKfQjf0Q3LcYh9SHKidbwE) .  
  * **`gcp_client.py`:** A dedicated module to handle all interactions with Google Cloud APIs. This will contain functions like `get_available_machine_types(zone)`, `get_available_gpus(zone)`, and `check_project_quotas(project_id, region)`. It should handle authentication gracefully using Application Default Credentials (ADC) [\[17\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHVqFH_hJwG--JGbhAET3Z0-H2mVFo1TsihSjODIHx5iQv3BnqRpJowxg5M9uxayMCALFOYw_Ay0tMf2JzHodLs02xdbXDUwVFTV17-57vdM5DGKLwM22yorxALAQ4IYdinDMLwdH2SLBZZsm0kd8du) . For local development, ADC is easily configured by running the command `gcloud auth application-default login` in your terminal.  
  * **`yaml_builder.py`:** Contains the logic for constructing the YAML blueprint dictionary from user inputs before writing it to a file with `PyYAML` [\[6\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE4sz4_g_7-cRpPcN0R5Zj_JGrOGqSh2XnyYV7qlttrF_WpBlcNAi1P26dciZJ0cYeEMUfglZY35SzUcBJ2IrTcRtDPYn3mWKPma1nHAZZzOdS5qgiFtNPxzalgIY6ojlXOhDsYhIOE0aJBOmf2fKNzkg==) .  
  * **`validator.py`:** Contains the logic for parsing an existing YAML file and running all validation checks against GCP APIs using the `gcp_client` module [\[18\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHrAI5EkCrOHXFK1W6sZc0q71O3-mJni2hCI0mzHIgWbAplnZCY1HPzLi6IQoPg8xLE0zbH5aPvElAL69W5yRrVQyJM_VI17TQ36jiPAfWunm5ckqsXD4leu_KAXWxUEvagduGcjQWWQlI9EtfyaZJpLsCJ2p3Gb6vUX6oyoSF7mStenxMTEa8=) .  
  * **`templates/` directory:** A directory to store a library of pre-defined, reusable YAML blueprint templates [\[19\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFA6QKss7QNDEp9ozy5dFk0CK5-5OTpdvJFKE3IAr75_SKXzKVJW_I8W6QhzjPh-e9kgSc4WdMBxcx3W3P8PA01dp8B611b1L4SfE9-wOKoJfF0K4FqlTj6Ig8mLA8bhxBbc_eLNJm5RXx_lKaFSfQYZFuuQQ==) .

### 2\. Understanding the Google Cloud Cluster Toolkit Blueprint

The application's output must be compatible with the Google Cloud Cluster Toolkit blueprint format. A blueprint is a YAML file that defines a reusable configuration for deploying HPC, AI, and ML clusters on Google Cloud [\[1\]](https://cloud.google.com/cluster-toolkit/docs/overview)[\[2\]](https://cloud.google.com/blog/products/compute/new-google-cloud-hpc-toolkit) . The toolkit's `gcluster` engine processes this file to generate the necessary Terraform and Packer configurations for deployment [\[20\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGTcpwT7ARhkG41Kvj1Rv7uv1XPvse4ZNQBAT-JSd3MdweZZi8DYdFngHNgpz3WBJ_xFRcDkV28KHiARud-Iy8xi_QPJ-PU-3XEXzNEX7N_YZl2XqAALZ8U4qk5T2_u4ElipnVIiZkHaMUVuVFlVkj57Q==)[\[1\]](https://cloud.google.com/cluster-toolkit/docs/overview)[\[21\]](https://drive.google.com/a/google.com/open?id=1QIa6ELuzZwtlDr65cMiSfHbEya3buxufehh_9Q__mFg) .

A blueprint is composed of several key components :

* **`blueprint_name`**: A unique name for the blueprint, used to label deployed resources for cost tracking [\[22\]](https://cloud.google.com/cluster-toolkit/docs/setup/cluster-blueprint) .  
* **`vars`**: A section for global variables like `project_id`, `deployment_name`, `region`, and `zone` that apply to all modules [\[22\]](https://cloud.google.com/cluster-toolkit/docs/setup/cluster-blueprint)[\[23\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEqgJt7oMxiIV16bWpQhkKCYEXwYD67zDwaBVMmZgtiqUIehJEMmRgRWhqIZL6DDgXbzieUqNWxvTRwiKQRHYN6NN-vdtWw6tjcwG01Jmh6QkITDNe3r9Kt2t7IrpWkjDLszIgwmggqIhJK1OFgcUdX9NV60PBabT7RGntDS4Mm) .  
* **`deployment_groups`**: Logical groupings of modules that are deployed together. Each group contains a list of modules .  
* **`modules`**: The fundamental building blocks of the cluster. Each module is a dictionary with the following keys:  
  * **`id`**: A unique identifier for the module within the blueprint [\[22\]](https://cloud.google.com/cluster-toolkit/docs/setup/cluster-blueprint) .  
  * **`source`**: The path or URL to the module's source code, which can be a local path or a Git repository URL [\[22\]](https://cloud.google.com/cluster-toolkit/docs/setup/cluster-blueprint)[\[7\]](https://drive.google.com/a/google.com/open?id=1-XfKNVvkTgdMRQmnpFN6r1mpCVgpJb-aVm1OIhQevDQ&resourcekey=0-hf2XfJFhKSAefTWpEoyX_Q) .  
  * **`settings`**: A dictionary of key-value pairs to configure the module's specific variables [\[22\]](https://cloud.google.com/cluster-toolkit/docs/setup/cluster-blueprint) .  
  * **`use`**: A list of other module IDs that this module depends on, allowing the toolkit to pass outputs from one module as inputs to another [\[22\]](https://cloud.google.com/cluster-toolkit/docs/setup/cluster-blueprint)[\[7\]](https://drive.google.com/a/google.com/open?id=1-XfKNVvkTgdMRQmnpFN6r1mpCVgpJb-aVm1OIhQevDQ&resourcekey=0-hf2XfJFhKSAefTWpEoyX_Q) .

### 3\. Core Feature Implementation

#### 3.1. YAML Generation (`generate` command)

This command will generate a valid YAML blueprint file based on user-specified parameters.

* **CLI Implementation:** Use `click` to define the `generate` command and accept flags like `--machine-type`, `--gpu-type`, `--gpu-count`, and `--storage-type` [\[3\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH1wF7y4jFp7zankhl7qyMTMlclmVTBs8vs8hxmK6KaYHK7B6e9EYvhs-jI259ULtPAZ5G5InP2vZKYgIphLdbZqVNpofjRRnN_gIeep3-Xca90lldBqRIKaLYG22Uf71ljtJIUiWM=)[\[4\]](https://drive.google.com/a/google.com/open?id=1KIIekWOkSpNZRWTeH74NXsKfQjf0Q3LcYh9SHKidbwE) .  
* **YAML Construction:** The function will dynamically build a nested Python dictionary that mirrors the blueprint structure. User-provided flags will populate the `settings` of the relevant modules [\[6\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE4sz4_g_7-cRpPcN0R5Zj_JGrOGqSh2XnyYV7qlttrF_WpBlcNAi1P26dciZJ0cYeEMUfglZY35SzUcBJ2IrTcRtDPYn3mWKPma1nHAZZzOdS5qgiFtNPxzalgIY6ojlXOhDsYhIOE0aJBOmf2fKNzkg==)[\[22\]](https://cloud.google.com/cluster-toolkit/docs/setup/cluster-blueprint) .  
* **File Output:** Use `yaml.dump(data, file, sort_keys=False)` to write the dictionary to a file, preserving the intended order for better readability [\[7\]](https://drive.google.com/a/google.com/open?id=1-XfKNVvkTgdMRQmnpFN6r1mpCVgpJb-aVm1OIhQevDQ&resourcekey=0-hf2XfJFhKSAefTWpEoyX_Q) .

**Example Python Snippet for Dynamic Generation:**

```py
import click
import yaml

@click.command()
@click.option('--machine-type', default='n2-standard-8', help='The machine type for compute nodes.')
@click.option('--max-node-count', default=10, help='The maximum number of nodes for autoscaling.')
@click.option('--output-file', default='hpc-blueprint.yaml', help='The output YAML file name.')
def generate(machine_type, max_node_count, output_file):
    """Generates a Cluster Toolkit blueprint YAML file."""
    blueprint = {
        'blueprint_name': 'dynamic-hpc-slurm',
        'vars': { 'deployment_name': 'hpc-cluster', 'project_id': 'your-gcp-project' },
        'deployment_groups': [{
            'group': 'primary',
            'modules': [{
                'id': 'compute_nodeset',
                'source': 'community/modules/compute/schedmd-slurm-gcp-v6-nodeset',
                'settings': {
                    'machine_type': machine_type,
                    'node_count_dynamic_max': max_node_count,
                }
            }]
        }]
    }
    with open(output_file, 'w') as f:
        yaml.dump(blueprint, f, sort_keys=False, indent=2)
    click.echo(f"Successfully generated {output_file}")
```

#### 3.2. YAML Validation (`validate` command)

This command will take an existing YAML blueprint and validate its resource requirements against a specific Google Cloud region or zone.

* **YAML Parsing:** The command will first use `yaml.safe_load()` to parse the input blueprint file [\[18\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHrAI5EkCrOHXFK1W6sZc0q71O3-mJni2hCI0mzHIgWbAplnZCY1HPzLi6IQoPg8xLE0zbH5aPvElAL69W5yRrVQyJM_VI17TQ36jiPAfWunm5ckqsXD4leu_KAXWxUEvagduGcjQWWQlI9EtfyaZJpLsCJ2p3Gb6vUX6oyoSF7mStenxMTEa8=)[\[8\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEdYuzN7JNOitZUgpGZckGLBHd3UqL4dLVaMXSiuMPVD_F6CzWh0mQIvYHhMSFW_W9Bb9dgcJ0uArur0aEyPRQDzfTMISe7qbXK8BguT-OMaHeVHNDEPcPvBr6RsVJPms8AwDHyXZ4KRk56dX9dc8JbuWeBzFxihQQ6wn2_ev6TxXIRcFQcYfzafXHB) .  
* **Resource Extraction:** The script will traverse the parsed dictionary to identify all resource definitions (machine types, GPUs, storage services) [\[18\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHrAI5EkCrOHXFK1W6sZc0q71O3-mJni2hCI0mzHIgWbAplnZCY1HPzLi6IQoPg8xLE0zbH5aPvElAL69W5yRrVQyJM_VI17TQ36jiPAfWunm5ckqsXD4leu_KAXWxUEvagduGcjQWWQlI9EtfyaZJpLsCJ2p3Gb6vUX6oyoSF7mStenxMTEa8=) .  
* **Live Validation Checks:** For each resource, the `validator.py` module will call functions in `gcp_client.py` to query GCP APIs in real-time.  
  * **Machine Types:** Check availability using the `machineTypes.list` method of the Compute Engine API, filtering by the target zone [\[24\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHuy_d4cFAAWAGPS5KtYu276SWOPQIsjYnAzYQcFM90jCEyu364xJumeg7xDNKk2UHlVGfP4cvHM1hw6RoEn-nud_dE5cEI-mnhYCvoKQPthNNjKi9Zt7FuEICMiuf_SVxXs-U_3JBZszwRomZyF0HtCYn9q2Mx7WfAFPmMAVGoam98YQ==)[\[10\]](https://cloud.google.com/compute/docs/reference/rest/v1/machineTypes/list)[\[11\]](https://yaqs.corp.google.com/eng/q/8878020932128473088) .  
  * **GPUs/TPUs:** Check availability using the `acceleratorTypes.list` method, filtering by the target zone [\[25\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEPsgX6whe_WuOP3npp_vzgIM7gKkqL31y50aRPiORF2lu0bAyNWGXg4kHtLr6vAqT89z5wxSPaMFVDeFhDsWnhXdTXBi_lHVjWvezyMNiCk7o4l1zTGGr-n57Sdh_3rZLfdjEFGtwNptNx9XWKWaskPW39uxW_dz_42YIj5XbJ_ys8z1RuFsLQPN8eNVbFCOkAvDlwfvyX9RZTmTwfECYvqpQq7-LXX0zHjHKJujadT7MYeULqS0o=)[\[26\]](https://cloud.google.com/sdk/gcloud/reference/compute/accelerator-types)[\[27\]](https://cloud.google.com/tpu/docs/ctpu-reference)[\[28\]](https://drive.google.com/a/google.com/open?id=1R0zofsUZrQGslhg3lrxbp7NsyAsAiytf0i6iZyZE4V8&resourcekey=0-ODRbEGzaEK_MMUVjXhESKA) .  
  * **Storage:** Check regional availability for Filestore, Managed Lustre, and Parallelstore by calling the `locations list` command or the equivalent API method for each service [\[29\]](https://cloud.google.com/sdk/gcloud/reference/filestore/locations/list)[\[30\]](https://drive.google.com/a/google.com/open?id=1AOXtrPGWdTfVaZPApul4ZZBBN1FqStkWRdBr3H4Sh6c)[\[31\]](https://drive.google.com/a/google.com/open?id=1HvaWeKRjTZsqbG9mOqp_rZpnPHsXRuoFFWckEAa-jWs)[\[32\]](https://mail.google.com/mail/?extsrc=sync&client=h&plid=ACUX6DPy7lcDnz6OFDGcgbc8Erw2E7NupWHnQcY&mid=197cc74b5d8c56da)[\[33\]](https://cloud.google.com/python/docs/reference/storage/latest) .  
  * **Invalid Combinations:** Programmatically check for invalid hardware combinations (e.g., H3 VMs do not support TPUs) by describing machine types and inspecting their supported `accelerators` property [\[34\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH0YELQnuy2QDUrWaoYkwdiKKb0NjNg_UIqoJane5QMONfMkzYu-MpxaZ4RpUjufC2btdozrHK9appxxHlhlNprjFqgswhELQ9SbkXHuawxZ7lQPYYoTTnL-VeuXazDk6x1GystkXO-bi_mCvNET8Li1h-kvjoFUOnrQgSWqSFYDeoFn4qtXQyN_AHEs0uheOcAfcFwJ-8qjqS57LF49fKFSD8fqqWxeJRQjt7enp3a23nTVvI=)[\[35\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFW6_ASFKAYpFePBiJmNTLck4waNkXQ8KVBypxrdgnmMm5hAyFqfBsZbDuC8O80ZCHBgiiAKOGPpZ5DaxdNr-RFb44vx8AS3HG1UwMcFHEUVG5_TQRX3PQ50EUjjDTR_mf0knmiOAhnTsGMjZqhsSuvDkaX9zE9dc35-eIGl33Ao_jXDw==) .

### 4\. Advanced Configuration and Examples

The tool should support the configuration of advanced HPC features available on Google Cloud.

#### 4.1. Schedulers (Slurm and Alternatives)

To configure a Slurm cluster, the blueprint must define modules for the controller and compute partitions. The `slurm_controller` module is linked to partition modules via its `partitions` setting. Each partition is defined by a `slurm_partition` module that references a `nodeset` module, where the actual compute node properties (like `machine_type` and `node_count_dynamic_max`) are set [\[36\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEoNmpnSSp_jRaeUfoqNiENpUJ-NP_zJ-eKJQ8C117ibOYNaDvvqeR5CXSle-Yt5vZ9k84QKbpSjX278kghNnYXhYXNOoMHPtu8eVyEFaseGW-DfcCGX9nwcZJDeAYb3qDJ8es7Sg==)[\[37\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHgOIbR6C4HVv4e9iukDOnMjPxNwRMtmgHYIIYqJFrzbkDJaq-hOxuH5XqYCrLbXwyY1zpi3OvXe2kryOjt2WQ6DURBGnQkoqPtf6xykU9iSyQN7amlgiY2qMyQGXpi6Szpltc8KuZpYa0Ex1mldPoI0eQ-WE3hFXXScZdGd73wqcmXRqQ5Ze92ksk0gyYjIA==)[\[22\]](https://cloud.google.com/cluster-toolkit/docs/setup/cluster-blueprint)[\[38\]](https://drive.google.com/a/google.com/open?id=1dvv2HO6v_EA5O-ulU3SPfGj8cjXY53giVdWBqqPQdI8) .

While Slurm is the primary scheduler for traditional, tightly-coupled HPC workloads within the Cluster Toolkit, it's worth noting that Google Cloud also supports other approaches, such as using Google Kubernetes Engine (GKE) for managing containerized HPC applications, which might be suitable for different types of workloads.

#### 4.2. Advanced Networking

High-performance networking is critical for many HPC workloads. These features are typically enabled within the compute `nodeset` module:

* **gVNIC (Google Virtual NIC):** Enable by setting `bandwidth_tier: gvnic_enabled` [\[39\]](https://drive.google.com/a/google.com/open?id=1-z2MLvbqam3nX4dgevDWfKpgevFBpwSVjnGb4KjO-F0&resourcekey=0-r6-AdXmjvdsOgxFBhxEeZA)[\[40\]](https://drive.google.com/a/google.com/open?id=1qibdT7WoszNPLI1Pe7qOYSKF7vo5128ckV8VTBrUjUc&resourcekey=0-IVUcH1H37rVNWXYb4FIw_Q) .  
* **Tier-1 Networking (100/200 Gbps):** Enable by setting `bandwidth_tier: tier_1_enabled`. This requires a supported machine type and automatically enables gVNIC [\[41\]](https://cloud.google.com/blog/products/compute/increasing-bandwidth-to-compute-engine-vms-with-tier_1-networking)[\[42\]](https://drive.google.com/a/google.com/open?id=1039vd7ApUX8Ign96L_cuUIQiK7vgbQz1J2kePGcHeGw) .  
* **Cloud RDMA:** Enable by selecting an RDMA-capable machine type (e.g., H4D series) and ensuring the VPC network is created with the appropriate RDMA network profile [\[31\]](https://drive.google.com/a/google.com/open?id=1HvaWeKRjTZsqbG9mOqp_rZpnPHsXRuoFFWckEAa-jWs)[\[43\]](https://cloud.google.com/vpc/docs/create-vpc-network-rdma) .

#### 4.3. Best-Practices Blueprint Example

For a multi-node, tightly-coupled training job, a best-practices blueprint would include:

* **Compute:** `a3-highgpu-8g` VMs (A3 with 8 H100 GPUs) [\[44\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHaHJVaOrlu-OzEb3D8pt8XxWlqa6hFeX4WvLwh_jwIlRtqZApNAeMp3WKWpC4VQ1J0_hMzqN4enCH1YnsyJFVSltAJhG8nljyT6kH9hzOQ3BXA3T251iuTsVc6sncEXFtIbWPzmj80YPr5IiDGy34yYuwz72oMqJkZJbhfoP1PqUoNBZxOaA==)[\[45\]](https://drive.google.com/a/google.com/open?id=1adH3YBOZQjvHZVbSjbXAx7V8nHBrz2DS4EjGh2m4qKM) .  
* **Networking:** Tier-1 networking enabled (`bandwidth_tier: tier_1_enabled`) [\[42\]](https://drive.google.com/a/google.com/open?id=1039vd7ApUX8Ign96L_cuUIQiK7vgbQz1J2kePGcHeGw)[\[46\]](https://drive.google.com/a/google.com/open?id=1rj8rqAZmL56MbMQazD-KiNlPiJZty8YTgYQnG4gB5pQ&resourcekey=0-LKjPG5eSSk5bdGeOrsWcSQ) .  
* **Placement:** A `COMPACT` placement policy to minimize inter-node latency [\[47\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEAFjHJSvc4iorC-dOXSsh7HjouIkFGC_76OxJnRWFFos030Cka7Xp58hkIPYMrJ_8qkOCFezW2sxayPMp2T9jTsQ5Wp91xM7awXGyE1Zx3QNV9AABoKOBK_xOyeU-4LAkYELeS_q0YxW4Iw8CQMoHU_bdhsALA7w==)[\[21\]](https://drive.google.com/a/google.com/open?id=1QIa6ELuzZwtlDr65cMiSfHbEya3buxufehh_9Q__mFg) .  
* **Storage:** A high-performance shared file system like Google Cloud Managed Lustre or a partner solution like DDN EXAScaler, mounted on `/scratch` [\[48\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH5d8ADStWrDcLitDhVHpZGoA5WhDZ-32xoDb4zTvnS-i_fEL5BM26K2XkFMhaX6GBc33H4IA9qmj63TzJuktJdf8OH8bufo-TOkfBCRAOFPUYM_3tnM9__Ds0Gmg0K8kXHL9HPbQtms065pcdA2vQh6CsLzXZ0rT-9aMDs1dOaD_eUSKQvDpWn)[\[40\]](https://drive.google.com/a/google.com/open?id=1qibdT7WoszNPLI1Pe7qOYSKF7vo5128ckV8VTBrUjUc&resourcekey=0-IVUcH1H37rVNWXYb4FIw_Q) .  
* **Scheduler:** A Slurm cluster with a controller, login node, and an autoscaling compute partition [\[22\]](https://cloud.google.com/cluster-toolkit/docs/setup/cluster-blueprint)[\[49\]](https://cloud.google.com/cluster-toolkit/docs/quickstarts/slurm-cluster) .

```
# Example: a3-h100-lustre-training-cluster.yaml
blueprint_name: a3-h100-lustre-training
vars:
  project_id: "your-gcp-project-id"
  deployment_name: "hpc-training-cluster"
  zone: "us-central1-a"
deployment_groups:
- group: primary
  modules:
  - id: network
    source: modules/network/vpc
  - id: scratchfs # High-performance Lustre file system
    source: community/modules/file-system/DDN-EXAScaler
    use: [network]
    settings:
      local_mount: /scratch
  - id: a3_nodeset
    source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset
    use: [network]
    settings:
      machine_type: a3-highgpu-8g
      node_count_dynamic_max: 16
      placement_policy: "COMPACT"
      bandwidth_tier: "tier_1_enabled"
  # ... other modules for partition, controller, login node, etc.
```

### 5\. Suggested Additional Features

To make the tool exceptionally useful, consider adding the following features:

* **Interactive Wizard Mode:** An interactive mode (`hpc-config-manager generate --interactive`) that guides users through creating a YAML file with a series of questions. This can be implemented using `click.prompt()` for text/choice input and `click.confirm()` for yes/no questions [\[50\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGNBlcl2XLQM8UV2GOc-Qv0ISQWpNEuy2VdYK0RH5BnT0GmtT_fqmBIJriD1ITWRz1a0wG5gsy9Rw_5ZiMDA8ffGzv-zvaKANNHqlRBjarGWEZ3kOahFqQAOmoJds7kMUHyiymVXpckiIp-xEZIOzs=)[\[51\]](https://yaqs.corp.google.com/eng/q/8183921231746039808) .  
* **Cost Estimation (`estimate-cost`):** A command that parses a blueprint YAML and provides a monthly cost estimate. This involves a multi-step process:  
  1. **Identify Resources:** Parse the YAML to find all billable resources (VMs, GPUs, storage) [\[21\]](https://drive.google.com/a/google.com/open?id=1QIa6ELuzZwtlDr65cMiSfHbEya3buxufehh_9Q__mFg) .  
  2. **Map to SKUs:** For each resource, query the Cloud Billing Catalog API to find its corresponding Stock Keeping Units (SKUs). A VM like `c2-standard-60` is billed as separate SKUs for its vCPU and RAM components [\[52\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFbyK-5pNshTTwGfRyUDhBRV1mXToZck9yZzp1SkNoXcX-OBW1x0HtYjE8jedaGrtaQN3u608ykqVJFA8guaTnNEFSzoDOrNOl0RXhDl4fLgkXKaGh6IBj1sNUGuJzKyzVisbC5AMUISmD_fQljcCq3sYP5JmY=)[\[53\]](https://yaqs.corp.google.com/eng/q/6513768566712434688) . GPUs have their own SKUs [\[54\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH8cqTSgRtpesiqfQP_BTT_pwWo2McOGEuZGku3zYYNOyJPWLW6vTk28LVnejNdI9vjTdP4pxtj6XsIgGuz33VZzmgatQyz12duGfG55eOmBORw_sN4bYMYGpbZzpEqto1LJ-wtvBpCB5KLTug9peqWmLIxcw==) .  
  3. **Retrieve Pricing:** For each SKU ID, retrieve its pricing information, parsing the `pricingExpression` and `tieredRates` to get the on-demand price [\[55\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHj9jlf92OtfyWT3o8Vl_B9TEhKZSwEj0vz6bPnYg7n8CbnzoG0lVBXI_uQwhJ8OvVpcQBqiYaXTbQfaAO3on4xzwbEGlJr7IpeZNkofemPrbHnheRpdF6J6jH8G22s_kee97XrUAMlIwSqdydYVcb3PEXziA==)[\[56\]](https://cloud.google.com/billing/v1/how-tos/catalog-api) .  
  4. **Calculate Monthly Cost:** Aggregate the costs, typically by multiplying hourly rates by an average of 730 hours per month [\[57\]](https://drive.google.com/a/google.com/open?id=1u1Zq0JlQLiYYQh2CJqN7wgFB60eSOfk0pOLs9pNUDM8) .  
* **Region/Zone Recommendation (`find-region`):** A command that takes resource requirements (e.g., 8x H100 GPUs, Lustre storage) and programmatically searches across all Google Cloud regions and zones to find and recommend locations where the configuration can be deployed [\[58\]](https://drive.google.com/a/google.com/open?id=10sYr2JHnn0-xCzv-eAgq4xq0vzUUVq1PxlQf8512FYI)[\[11\]](https://yaqs.corp.google.com/eng/q/8878020932128473088) .  
* **Template Library:** Include a built-in library of common HPC cluster templates (e.g., `llm-training-pod`, `genomics-pipeline`) stored in a `templates/` directory. The CLI should have a `list-templates` command and allow the `generate` command to use a template as a base, with flags providing overrides [\[19\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFA6QKss7QNDEp9ozy5dFk0CK5-5OTpdvJFKE3IAr75_SKXzKVJW_I8W6QhzjPh-e9kgSc4WdMBxcx3W3P8PA01dp8B611b1L4SfE9-wOKoJfF0K4FqlTj6Ig8mLA8bhxBbc_eLNJm5RXx_lKaFSfQYZFuuQQ==)[\[59\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEyylYy9T3ZonmcouPHierZXsKnHa86VPwyBBDjDy37A_z6SCUtZSX_NJawGX_IHlMxbgbQVpW1caKAlZN4LXe8xr4rFO6NKroaz6fqK5Tjbb4OhnfYHKEJrlmtLiFiYb2wKX84m930RPjSpQEoDj6x8EH20RpJH0Mi1U1xJ13q5rMyR8tRuA==) .  
* **Quota Checking (`check-quota`):** A command to programmatically check if the current project has sufficient quotas for the resources defined in a blueprint (e.g., `NVIDIA_H100_GPUS` or `CPUS` in a specific region) using the Cloud Quotas API [\[16\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG1fmRaqQqreqBXpeAqVeOvSCidBX0-v_9bX6TVwfExHUZZSdDGCeBmvBoCkwhX1Du2nO1ORtXGNocuJtiDTRqUkrNYoRMT4pQ-9JFxB0SfUjFWbWQ5PsQnk3JY3g1P8lwpOoFLQHKIU5zRx8OBNPkxd0xS)[\[60\]](https://drive.google.com/a/google.com/open?id=1EtL90WqbqpfVF4i5ZNPikN_AYMXKFdYG&resourcekey=0-MqRep44mP6NQuf6Wjvb4fA)[\[61\]](https://cloud.google.com/python/docs/reference/google-cloud-cloudquotas/0.1.13/google.cloud.cloudquotas_v1.types.QuotaDetails) .

### 6\. From Blueprint to Deployment

Once a blueprint YAML file has been generated and validated by the `hpc-config-manager` tool, the final step is to deploy the cluster using the Google Cloud Cluster Toolkit's command-line tool (`gcluster` or the newer `gctcli`). The process involves two main commands:

1. **Create Deployment Folder:**

```shell
gcluster create my-cluster-deployment.yaml -b path/to/your/blueprint.yaml
```

   This command processes the blueprint, assembles the necessary Terraform code, and creates a self-contained deployment folder [\[49\]](https://cloud.google.com/cluster-toolkit/docs/quickstarts/slurm-cluster)[\[1\]](https://cloud.google.com/cluster-toolkit/docs/overview)[\[62\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG4_9pWBbnld4iD8FK9d6cOHU247fyEjoBlC3GmlkLO0d6K_R2sdDW3BZtvJd35E9wZuIQazCS2ez0Lk21kttjULTJBHKVZVo_rwJS8OXUbkQlde0UswHyv1uTOoIkXHSJ8Nh7-GnEwTum0f4GQi4v4tz82h5M_2PX-xHt6_HsR1eCj) .

   

2. **Deploy the Cluster:**

```shell
gcluster deploy my-cluster-deployment
```

   This command executes the Terraform configurations within the deployment folder to provision the resources on Google Cloud [\[2\]](https://cloud.google.com/blog/products/compute/new-google-cloud-hpc-toolkit)[\[63\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFE7Cup28JE0a1giIi2pJSCa7wpOmYasLHCO-cc8CkT_bQYRkSOWDXbIkg-TEhAsDPWrYBH4o7W_EzV70mcg_ED_pELcj2VzZ9FyxfKaMHSpZirfp3il8bGPluN3fVSEwL_x0iimtPlYjNzgfCJ3oJqFg==) .

### 7\. Implementation and Testing

A robust implementation requires a solid testing strategy, especially for code that interacts with external APIs.

* **Unit Testing with Mocks:** Use Python's `unittest.mock` library to write unit tests for the `gcp_client.py` module. The best practice is to use the `@patch` decorator to replace the Google Cloud API client (e.g., `compute_v1.InstancesClient`) with a mock object [\[64\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFmc2i-y3Z9EUG8t_ZdEiByLQN8ZRY26Mc6s1SS1YiHiO3PoeneNB3uT4XR5R_6nsx33K7VBRQfkD6FwXD1bmgRKnob10a5u3O13J7p4O5cgvNTiyvpuaxPS_0WnmZ526IQdTaVD4vg2EZ35z0ARoyfrCSLaEfLAEhIppIu43GRTEZkb4aUELMOy6xIywvo3megJLJTM_uaoP_i6lbm-CJU5axkOi0=)[\[65\]](https://drive.google.com/a/google.com/open?id=1thtwlPUFnmiQ_CMkRx7_z7wmVMULRWHo69RsF5RbF_A) .  
* **Testing Scenarios:** Your tests should cover various scenarios:  
  * **Success Case:** Configure the mock to return a successful API response and assert that your function behaves correctly [\[64\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFmc2i-y3Z9EUG8t_ZdEiByLQN8ZRY26Mc6s1SS1YiHiO3PoeneNB3uT4XR5R_6nsx33K7VBRQfkD6FwXD1bmgRKnob10a5u3O13J7p4O5cgvNTiyvpuaxPS_0WnmZ526IQdTaVD4vg2EZ35z0ARoyfrCSLaEfLAEhIppIu43GRTEZkb4aUELMOy6xIywvo3megJLJTM_uaoP_i6lbm-CJU5axkOi0=) .  
  * **Resource Not Found:** Configure the mock's `side_effect` to raise a 404 `HttpError` and assert that your function handles it gracefully (e.g., by returning `False` or `None`) [\[66\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFLBjX40qN59q1OZVPrXhWzFAEYdMRNqr81aC3Y4LNz6v2_56BV9tdM2sCjLByNtTmAmpBXHkiM1m_X2KMtUK2KHXt3X4tAyGxDUk-nrKcNXdoqcjyTOMxMnahO5uA7h2Mw2v7c1MNCxmq6LGvu2SX8s7YUB6XWErHefrNtuXQ6sHvUK1xEVD_JFC4oTDv_Fq_jwWTmNdTc1dIlmtFMvWg3AY8vgVn51r6wdH0iutAiRcABKiQg-w==)[\[67\]](https://yaqs.corp.google.com/eng/q/4550904720261120) .  
  * **Other API Errors:** Configure the mock to raise other errors (e.g., a 500 `HttpError`) and assert that your function propagates the exception correctly [\[68\]](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEtWpIJEn1ywLAOqVjroPVLzPZKCidhltmUeiiAI_0mE290VgZuqCX4FyjN2E8_I9GW8AyCocSLHt72bJLmSpAEgTP_x8eUVWfMpvFm7NrcbsY-2zaVMp6ZDi1nZaTM5a0-kIVLlLV5mcSSq84eV7K2WcbQmnHp5F3Ap4qoJRDMca-iQ-9pKJvN_CeDVYuYJPBYQRgYurIGVn6Nc4Y8K6gD9y53jJGKMY5Q--749g==) .

**Example Unit Test Snippet:**

```py
import unittest
from unittest.mock import patch, MagicMock
from googleapiclient.errors import HttpError
from gcp_client import instance_exists # Assumes this function exists

class TestGcpClient(unittest.TestCase):
    @patch('gcp_client.compute_v1.InstancesClient')
    def test_instance_exists_false_when_not_found(self, mock_instances_client):
        # Arrange: Configure the mock to raise a 404 error
        mock_client_instance = mock_instances_client.return_value
        http_error = HttpError(resp=MagicMock(status=404), content=b'Not Found')
        mock_client_instance.get.side_effect = http_error

        # Act
        result = instance_exists("proj", "zone", "non-existent-instance")

        # Assert
        self.assertFalse(result)
        mock_client_instance.get.assert_called_once()
```

### Executive Summary

This report details a comprehensive software design for `hpc-config-manager`, a Python CLI tool to automate the creation, validation, and cost estimation of Google Cloud HPC deployment configurations. The tool will be built on a modular architecture using industry-standard libraries like `click` and `PyYAML`, and it will interact directly with Google Cloud APIs to ensure accuracy.

**Core features** include generating and validating YAML blueprints compatible with the Google Cloud Cluster Toolkit. **Advanced capabilities** will provide significant value by offering an interactive wizard, on-demand cost estimation, intelligent region recommendations based on resource availability, a library of pre-built templates, and programmatic quota checking. The design also includes guidance on the final deployment step using the Cluster Toolkit's commands, providing a complete end-to-end workflow overview.

By following this design, the resulting application will significantly simplify the process of deploying complex HPC environments on Google Cloud, reducing manual errors, providing crucial cost visibility, and ensuring that configurations are valid before deployment is attempted. The entire design is grounded in Google's official documentation and best practices, providing a solid foundation for development.

Research details Understanding the Google Cloud Cluster Toolkit Blueprint YAML Format The official documentation for the Google Cloud Cluster Toolkit blueprint YAML format outlines a structured approach to defining and deploying high-performance computing (HPC), artificial intelligence (AI), and machine learning (ML) environments on Google Cloud. A cluster blueprint is a YAML file that specifies a reusable configuration for a cluster, detailing the resources and settings required for deployment.

Key Components of a Blueprint YAML File: A cluster blueprint is primarily composed of the following elements:

Blueprint Name: This is a unique identifier for the blueprint. It's recommended to keep the name consistent when updating an existing configuration and to create a new name for a new setup.

Deployment Name: This name is used to label the cloud resources that are deployed, which helps in tracking costs and usage. While a single blueprint can be used for multiple deployments, the deployment\_name can specify the intended use of a particular cluster.

Project ID: This is a mandatory variable that specifies the Google Cloud project where the cluster will be deployed.

Zone: This indicates the specific zone within a Google Cloud region where the cluster resources will be provisioned.

Modules: Blueprints reference modules, which are the fundamental building blocks for a deployment. These modules are typically Terraform or Packer configurations that deploy specific components like a cluster partition, a storage system, or network configurations.

Deployment Groups: These are logical groupings of modules within the blueprint.

How it Works: The Cluster Toolkit, formerly known as Cloud HPC Toolkit, utilizes an open-source tool called gcluster engine. This engine processes the blueprint YAML file, combines the specified modules, and generates a self-contained deployment folder. This folder includes all the necessary configurations and scripts (Terraform or Packer) to deploy the cluster.

Official Documentation and Resources: The primary official documentation for the Cluster Toolkit and its blueprint format is available on the Google Cloud website.

For a comprehensive collection of example cluster blueprints, the official Cluster Toolkit GitHub repository is the recommended resource. These examples serve as a practical starting point for creating custom cluster configurations.

The toolkit is designed to be highly customizable and extensible, allowing users to modify existing modules or create their own to fit specific needs. This modular approach simplifies the process of creating complex, repeatable, and best-practice-compliant HPC and AI/ML environments on Google Cloud.

The official documentation for the Google Cloud Cluster Toolkit blueprint YAML format can be found on the Google Cloud website and in the toolkit's GitHub repository.

A cluster blueprint is a YAML file that defines a reusable configuration for deploying HPC, AI, and ML clusters on Google Cloud.

It simplifies the process by allowing you to define your cluster's infrastructure and software in a high-level, easy-to-read format. Google Drive icon

Google Drive icon

Key Components of a Blueprint YAML File A cluster blueprint is structured with the following main components:

blueprint\_name: This is the name of the blueprint and is used to label your cloud resources for easier tracking and cost monitoring.

vars: This section contains a set of global variables that are applied to all modules within the blueprint. Common variables include:

deployment\_name: A unique name for each specific deployment of the blueprint.

project\_id: The Google Cloud project where the cluster will be deployed.

region and zone: The geographical location for the deployment.

deployment\_groups: These define logical groupings of modules that are deployed together. A blueprint can have multiple deployment groups. Each group contains:

group: The name of the deployment group.

modules: A list of modules to be deployed. Each module has the following attributes:

id: A unique identifier for the module within the blueprint.

source: The path or URL to the module's source code. This can be a local path or a URL to a Git repository.

kind: The type of module, which can be terraform or packer. The default is terraform.

use: A list of other module IDs that this module depends on. This allows the toolkit to pass outputs from one module as inputs to another.

settings: A set of key-value pairs to configure the specific module's variables.

terraform\_backend\_defaults (Optional): This section is used to configure a remote backend for storing the Terraform state, which is a recommended best practice for managing infrastructure as code.

toolkit\_modules\_url and toolkit\_modules\_version (Optional): These fields allow you to version your blueprints by specifying the Git repository URL and version for the modules used.

How it Works The Cluster Toolkit's gcluster engine processes the blueprint file. When you run the gcluster create command, the engine reads the blueprint, combines the specified modules, and generates a self-contained deployment folder. Google Drive icon

This folder contains all the necessary Terraform and Packer files to deploy the cluster as defined in your blueprint. You then use standard Terraform commands to deploy the resources to Google Cloud.

Resources and Examples You can find extensive documentation and examples to help you get started with creating your own blueprints:

Official Documentation: The Google Cloud website provides a comprehensive guide to the Cluster blueprint format.

Blueprint Catalog: A catalog of pre-built blueprints is available for various use cases, which you can use as a starting point.

GitHub Repository: The Cluster Toolkit GitHub repository offers a wide range of example blueprints. Google Drive icon

Yaqs icon

Quickstarts and Tutorials: Google Cloud provides quickstarts and tutorials, such as how to deploy an HPC cluster with Slurm, to guide you through the process. Google Drive icon There are also Qwiklabs available for hands-on experience. Google Drive icon

Training Materials: Internal training decks and presentations often contain detailed explanations and examples of blueprint configurations. Google Drive icon

You can retrieve a list of machine types available in a specific Google Cloud zone using either the gcloud command-line tool or the Google Cloud Compute API. Both methods offer a straightforward way to obtain this information.

Using the gcloud Command-Line Tool The gcloud command-line tool provides a simple way to list machine types and filter them by zone. The primary command is gcloud compute machine-types list. You can use the \--filter flag to specify the desired zone.

Command:

bash gcloud compute machine-types list \--filter="zone:( us-central1-a )" Explanation:

gcloud compute machine-types list: This is the basic command to list all available machine types.

\--filter="zone:( us-central1-a )": This flag filters the output to show only the machine types available in the us-central1-a zone.

You can replace us-central1-a with any valid Google Cloud zone.

You can also specify the zone using a slightly different filter syntax.

Alternative Command:

bash gcloud compute machine-types list \--filter="zone=us-central1-a" Additionally, the \--zones flag can be used to achieve the same result.

Command with \--zones flag:

bash gcloud compute machine-types list \--zones us-central1-a Using the Google Cloud Compute API For programmatic access, you can use the Google Cloud Compute API. The machineTypes.list method allows you to retrieve a list of machine types for a specific project and zone.

HTTP Request:

To use the API, you will make a GET request to the following endpoint:

GET [https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/machineTypes](https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/machineTypes) Path Parameters:

project (string): The ID of your Google Cloud project.

zone (string): The name of the zone for which you want to list machine types (e.g., us-central1-a).

Example using curl:

You can use a tool like curl to make this API request. You will need to be authenticated to use the API.

bash curl   
'[https://compute.googleapis.com/compute/v1/projects/your-project-id/zones/us-central1-a/machineTypes](https://compute.googleapis.com/compute/v1/projects/your-project-id/zones/us-central1-a/machineTypes)'   
\--header 'Authorization: Bearer YOUR\_ACCESS\_TOKEN'   
\--header 'Accept: application/json'   
\--compressed Replace your-project-id with your actual project ID and YOUR\_ACCESS\_TOKEN with a valid OAuth 2.0 access token.

The response from this API call will be a JSON object containing a list of machine type resources available in the specified zone.

You can get a list of available machine types in a specific Google Cloud zone using either the gcloud command-line tool or the Google Cloud Compute API.

Using the gcloud command-line tool To get a list of available machine types in a specific zone, use the gcloud compute machine-types list command with the \--zones flag.

Command:

bash gcloud compute machine-types list \--zones Example: To list the machine types available in the us-east1-b zone, run the following command:

bash gcloud compute machine-types list \--zones us-east1-b You can also use the \--filter flag to filter by zone. Yaqs icon

Command with filter:

bash gcloud compute machine-types list \--filter="zone:()" Example with filter:

bash gcloud compute machine-types list \--filter="zone:(us-east1-a)" Yaqs icon

Using the Google Cloud Compute API To retrieve a list of machine types using the Compute API, you can make a GET request to the machineTypes.list method. This method requires the project ID and the desired zone to be specified in the request path.

HTTP Request:

GET [https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/machineTypes](https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/machineTypes) Parameters:

project (string): The ID of your Google Cloud project.

zone (string): The name of the zone you want to query.

Example using curl:

Replace \[PROJECT\_ID\] with your project ID and \[ZONE\] with the desired zone.

bash curl   
'[https://compute.googleapis.com/compute/v1/projects/\[PROJECT\_ID\]/zones/\[ZONE\]/machineTypes](https://compute.googleapis.com/compute/v1/projects/[PROJECT_ID]/zones/[ZONE]/machineTypes)'   
\--header 'Authorization: Bearer \[OAUTH2\_TOKEN\]'   
\--header 'Accept: application/json'   
\--compressed For more details on the API method and its parameters, you can refer to the official documentation for the machineTypes.list method.

It's important to note that even if a machine type is listed, it might not be available due to resource exhaustion in that zone at a particular time. Yaqs icon Additionally, not all machine types are available in all regions or zones. Google Drive icon

You can get a list of available GPU and TPU types in a specific Google Cloud zone using the gcloud command-line tool or the Google Cloud Compute API. Here’s a breakdown of how to accomplish this for both accelerator types.

Graphics Processing Units (GPUs) To accelerate your machine learning, data processing, and graphics-intensive workloads, Google Cloud offers a variety of NVIDIA GPU models. You can determine their availability in specific zones through the following methods.

Using the gcloud Command-Line Tool The gcloud compute accelerator-types list command is the primary way to discover available GPU types. You can filter the results by a specific zone to see what is offered in that location.

Command:

bash gcloud compute accelerator-types list \--filter="zone:( us-central1-a )" Example Output: This command will return a table with details about the accelerator types available in the specified zone, including their name and description.

You can also view a broader list of GPU availability across different regions and zones.

Using the Google Cloud Compute API For programmatic access, you can use the acceleratorTypes.list method from the Compute Engine API. This method retrieves a list of accelerator types available to your project in a specified zone.

API Request: Make a GET request to the following URI, replacing my-project and us-central1-a with your project ID and desired zone:

[https://compute.googleapis.com/compute/v1/projects/my-project/zones/us-central1-a/acceleratorTypes](https://compute.googleapis.com/compute/v1/projects/my-project/zones/us-central1-a/acceleratorTypes) Response Body: The response will be a JSON object containing a list of accelerator types for the given zone. Each entry will include details such as the name, description, and maximumCardsPerInstance.

Tensor Processing Units (TPUs) Google Cloud's custom-designed TPUs are built to accelerate machine learning workloads. Discovering their availability is slightly different from GPUs.

Using the gcloud Command-Line Tool To see the available TPU types and their details within a specific zone, you can use the gcloud compute tpus tpu-vm commands. While there isn't a single command to list all types in a zone, you can list existing TPUs or check locations.

A more direct way to see what is offered is to consult the official Google Cloud documentation, which provides tables detailing the availability of different TPU versions (like v2, v3, v4, and v5e) in various zones.

To list available TPU locations, you can use:

bash gcloud compute tpus locations list And to list your existing TPU nodes in a specific zone:

bash gcloud compute tpus list \--zone=us-central1-a When creating a TPU, you specify the accelerator type. If the type is not available in that zone, the command will fail, indirectly indicating availability.

Using the Google Cloud Compute API Similar to the gcloud tool, the Compute Engine API for TPUs focuses more on managing existing resources and discovering locations rather than listing available types in a zone directly.

You can list available locations for TPUs by making a GET request to:

[https://tpu.googleapis.com/v2/projects/my-project/locations](https://tpu.googleapis.com/v2/projects/my-project/locations) This will return a list of regions and zones where TPUs are available. To determine the specific types available in each zone, you would typically refer to the Google Cloud documentation, which maintains an updated list of TPU availability by region and zone.

You can get a list of available GPU and TPU types in a specific Google Cloud zone using the gcloud command-line tool and the Google Cloud API. Here are the methods for each:

Graphics Processing Units (GPUs) You can list available GPU types, which are referred to as accelerator types in Google Cloud.

Using the gcloud command-line tool To get a list of available GPU accelerator types for a specific zone, use the gcloud compute accelerator-types list command with a filter for the desired zone.

Command:

bash gcloud compute accelerator-types list \--filter="zone:(ZONE)" Replace ZONE with the name of the zone you are interested in, for example, us-central1-a.

This command will return a table of the accelerator types available in that zone, including a description of the GPU model.

Using the Google Cloud Compute API You can programmatically retrieve a list of available GPU types by making a GET request to the acceleratorTypes.list method of the Compute Engine API. You will need to specify the project and the zone.

API Request:

GET [https://compute.googleapis.com/compute/v1/projects/PROJECT\_ID/zones/ZONE/acceleratorTypes](https://compute.googleapis.com/compute/v1/projects/PROJECT_ID/zones/ZONE/acceleratorTypes) Replace PROJECT\_ID with your project ID and ZONE with the desired zone.

You can also use the aggregatedList method to get a list of all accelerator types across all zones.

Tensor Processing Units (TPUs) Similarly, you can list the available TPU types for a specific zone.

Using the gcloud command-line tool To list the available TPU accelerator types in a specific zone, you can use the gcloud compute tpus accelerator-types list command.

Command:

bash gcloud compute tpus accelerator-types list \--zone=ZONE Replace ZONE with the name of the zone you want to check.

This will provide a list of the TPU types available for provisioning in that zone.

For TPU VMs, you can also use the following command:

bash gcloud compute tpu-vm accelerator-types list \--zone=ZONE Using the Google Cloud TPU API To get a list of available TPU types via the API, you can use the acceleratorTypes.list method from the Cloud TPU API.

API Request (v2):

GET [https://tpu.googleapis.com/v2/projects/PROJECT\_ID/locations/ZONE/acceleratorTypes](https://tpu.googleapis.com/v2/projects/PROJECT_ID/locations/ZONE/acceleratorTypes) Replace PROJECT\_ID with your project ID and ZONE with the desired zone.

This API endpoint will return a list of the accelerator types available in the specified location. The TPU API also provides methods to list available TensorFlow and runtime versions.

You can determine the availability of high-performance storage options like Google Cloud Managed Lustre, Parallelstore, and Filestore in specific Google Cloud regions and zones through the gcloud command-line tool and by consulting the official Google Cloud documentation.

Filestore You can check for Filestore availability using both the gcloud command-line tool and the Google Cloud documentation.

Using the gcloud command-line tool:

To list all available regions and zones for Filestore, you can use the following commands:

To list all regions where Filestore is available, run:

bash gcloud filestore regions list To get a list of all supported zones, you can use:

bash gcloud filestore zones list You can also get details for a specific zone by running gcloud filestore locations describe .

Using the Google Cloud documentation:

The official documentation for Filestore provides a comprehensive and up-to-date list of supported regions and their corresponding zones. Filestore instances are created within zones of a region.

For optimal performance, it is recommended to create your Filestore instance in a zone that is geographically close to the clients that will be accessing it.

Google Cloud Managed Lustre Similar to Filestore, you can find availability information for Managed Lustre through both API documentation and the official Google Cloud website.

Using the Google Cloud Managed Lustre API:

While a direct gcloud command to list all supported locations for Managed Lustre isn't explicitly mentioned in the provided search results, the Managed Lustre API offers a method to retrieve this information. You can list instances within a specific project and location using a GET request. To get information for all locations, you can use "-" as the location value.

Using the Google Cloud documentation:

The Google Cloud documentation for Managed Lustre includes a page dedicated to its supported regions and zones. Managed Lustre instances are also zonal, meaning they reside within a specific zone in a region. For the best performance, it's advised to create your Managed Lustre instance in the same region as the clients that will be mounting it.

Parallelstore For Parallelstore, the availability information is readily accessible through the Google Cloud documentation.

Using the Google Cloud documentation:

The "Supported locations" page for Parallelstore in the Google Cloud documentation provides a clear table of the regions and zones where the service is available. Like the other storage options, Parallelstore instances are zonal resources. To minimize network latency, you should create your Parallelstore instance in a region and zone near where it will be used. It's important to note that Parallelstore may be available by invitation only.

You can check the availability of high-performance storage options like Google Cloud Managed Lustre, Parallelstore, and Filestore in specific Google Cloud regions and zones using the gcloud command-line tool or by consulting the official documentation for API-based checks.

Using the gcloud Command-Line Tool The most direct way to check for regional availability of these services is by using the gcloud ... locations list command specific to each service.

Filestore To list all the locations where Filestore is available, use the following command:

bash gcloud filestore locations list This command will return a list of regions and zones where you can provision Filestore instances.

Filestore is widely available across most Google Cloud regions. Google Drive icon

Google Cloud Managed Lustre To see the supported locations for Google Cloud Managed Lustre, you can use its specific gcloud command group. The service is now Generally Available.

To list the available locations (zones) for Managed Lustre:

bash gcloud lustre locations list Managed Lustre is available in numerous zones within the following regions: asia-northeast1, asia-south1, asia-southeast1, australia-southeast1, europe-west1, europe-west2, europe-west3, europe-west4, europe-west9, me-central2, me-west1, northamerica-northeast1, southamerica-east1, us-central1, us-east1, us-east4, us-east5, us-east7, us-south1, us-west1, us-west2, and us-west4.

When creating an instance, you must specify a zone using the \--location flag. Google Drive icon

Parallelstore Similarly, to find out where Parallelstore is available, you can use the locations list command for that service.

To list the supported locations for Parallelstore:

bash gcloud parallelstore locations list Parallelstore is a zonal service available in the following regions: asia-east1, asia-southeast1, europe-north1, europe-west1, europe-west4, us-central1, us-east1, us-east4, us-east5, us-west1, us-west2, us-west3, and us-west4. Google Drive icon

Using APIs For programmatic access, you can use the REST APIs for each service to query for available locations. This is useful for building automation or custom tools. Google Drive icon

Filestore API: You can make a GET request to the [https://file.googleapis.com/v1/projects/{projectId}/locations](https://file.googleapis.com/v1/projects/{projectId}/locations) endpoint.

Managed Lustre API: Use a GET request to the [https://lustre.googleapis.com/v1/projects/{projectId}/locations](https://lustre.googleapis.com/v1/projects/{projectId}/locations) endpoint.

Parallelstore API: A GET request to the [https://parallelstore.googleapis.com/v1/projects/{projectId}/locations](https://parallelstore.googleapis.com/v1/projects/{projectId}/locations) endpoint will list the available locations.

Consulting the Official Documentation Google Cloud provides official documentation that lists the supported regions and zones for its services. This is a reliable way to get up-to-date information.

Google Cloud Managed Lustre Supported Locations: This document provides a complete list of available regions and zones.

Parallelstore Supported Locations: This page details the specific regions and zones where Parallelstore can be provisioned.

Google Cloud NetApp Volumes Locations: For users of NetApp Volumes, this document lists the supported regions.

By using a combination of gcloud commands and checking the official documentation, you can accurately determine the availability of these high-performance storage services for your desired Google Cloud regions and zones.

Programmatically Estimating HPC Resource Costs on Google Cloud To programmatically estimate the monthly cost of a set of High-Performance Computing (HPC) resources, such as specific VM types, GPUs, and storage volumes as defined in a deployment YAML file, you can utilize the Google Cloud Billing Catalog API. This powerful tool provides access to the rich pricing information for all Google Cloud services. The process involves parsing your deployment configuration, mapping the specified resources to their corresponding Stock Keeping Units (SKUs) in the Pricing API, and then calculating the estimated monthly cost based on the retrieved pricing data.

Key Steps to Estimate Costs: Enable the Cloud Billing API: Before you can query the pricing information, you must enable the Cloud Billing API in your Google Cloud project.

Parse the Deployment YAML: Your first step is to programmatically parse your deployment YAML file to extract the specifications of the resources you want to price. This includes details such as:

VM Instances: Machine type (e.g., n2-standard-8), region, and any specific CPU platform.

GPUs: GPU type (e.g., nvidia-tesla-t4), the number of GPUs attached, and the region.

Storage Volumes: Persistent Disk type (e.g., pd-ssd), size in GB, and region.

Identify the Correct Service and SKUs: The Cloud Billing Catalog API organizes prices by services, each having a unique identifier. For HPC resources, you will primarily be interested in the Compute Engine service, which has the service ID 6F81-5844-456A.

Each billable item in Google Cloud is represented by a SKU. To find the price of a specific resource, you need to find its corresponding SKU. You can list all SKUs for a service and then filter them to find the one that matches your resource's configuration.

The description of a SKU is often very detailed, for example, "Nvidia Tesla T4 GPU attached to Spot Preemptible VMs running in Warsaw", which helps in identifying the correct one.

Query the Cloud Billing API: With the service ID and resource specifications, you can query the services.skus.list endpoint of the Cloud Billing API. You will need to use filters to narrow down the results to the specific SKUs you are interested in.

Here's how you can structure your API requests to find the SKUs for different resources:

VM CPU and Memory: The costs for vCPUs and memory are often broken down into separate SKUs. You can filter by the machine family (e.g., N2) and the region. The description of the SKU will typically contain the specific machine type.

GPUs: You can filter by the GPU type and the region. The SKU description will provide details about the GPU model.

Persistent Disks: For storage, you can filter by the disk type (e.g., "SSD") and the region. The pricing is typically per GB per month.

Calculate the Monthly Cost: The Pricing API will return pricing information that is often priced per hour or per GB-month. To estimate the total monthly cost, you will need to perform the following calculations:

For hourly rates (VMs, GPUs): Multiply the hourly rate by the number of hours in a month (approximately 730 hours).

For storage (Persistent Disks): The price is usually already in a per-GB-month format, so you just need to multiply it by the size of your disk in GB.

Remember to sum the costs of all the individual resources (VMs, GPUs, storage) to get the total estimated monthly cost for your deployment.

Example API Request Filtering: To get a list of SKUs for Compute Engine, you can use a GET request like the following, where YOUR\_API\_KEY is your API key:

GET [https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus?key=YOUR\_API\_KEY](https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus?key=YOUR_API_KEY) To further refine the results, you can use the filter parameter. For instance, to find SKUs related to a specific machine type in a particular region, you would need to parse the descriptions of the returned SKUs.

Alternative: Using Third-Party Tools For a more streamlined approach, you can consider using open-source tools like Infracost.

Infracost is designed to work with Infrastructure as Code (IaC) tools like Terraform and can analyze your configuration files to provide cost estimates.

While it primarily supports Terraform, its underlying logic for mapping resources to prices can serve as a valuable reference. Infracost can be integrated into your CI/CD pipeline to automatically show the cost impact of infrastructure changes.

By following these steps, you can programmatically and accurately estimate the monthly costs of your HPC resources on Google Cloud, enabling better budget planning and cost management.

Uncovering Valid VM and Accelerator Pairings in Google Cloud To programmatically determine the valid combinations of Virtual Machine (VM) types and accelerator types (GPU/TPU) available in a specific Google Cloud zone, you can leverage the Google Cloud CLI (gcloud) and the Google Cloud API. The approach differs slightly for GPUs and TPUs due to their distinct provisioning models.

Graphics Processing Units (GPUs) For GPUs, the key is to inspect the properties of machine types within a given zone. Some machine families, known as accelerator-optimized, come with pre-attached GPUs, while general-purpose machine types may support attaching specific GPU models.

Using the gcloud Command-Line Tool You can achieve this by combining two gcloud commands: gcloud compute machine-types list and gcloud compute machine-types describe.

List all machine types in a specific zone: To get a list of all available machine types in a desired zone, you can use the following command. This is useful for iterating through each machine type to check for accelerator compatibility.

bash gcloud compute machine-types list \--filter="zone:( us-central1-a )" Describe a specific machine type to find compatible GPUs: For each machine type obtained from the list, you can use the describe command with the \--format flag to display its properties in a machine-readable format like JSON. The output will contain an accelerators field if the machine type supports any GPUs.

bash gcloud compute machine-types describe n1-standard-8 \--zone us-central1-a \--format="json(name, accelerators)" If the n1-standard-8 machine type in us-central1-a supports GPUs, the output will look something like this, indicating the type and maximum number of GPUs that can be attached:

JSON { "accelerators": \[ { "guestAcceleratorCount": 1, "guestAcceleratorType": "nvidia-tesla-k80" }, { "guestAcceleratorCount": 2, "guestAcceleratorType": "nvidia-tesla-k80" }, ... \], "name": "n1-standard-8" } For accelerator-optimized machine types like the A2, A3, and G2 series, the GPUs are pre-attached and an integral part of the machine type itself.

Describing these machine types will show the specific GPU model and count.

Using the Google Cloud API Programmatically, you can achieve the same result by making calls to the Compute Engine API.

List Machine Types: Use the machineTypes.list method to retrieve a list of machine types for a specific zone.

Get Machine Type Details: For each machine type, use the machineTypes.get method. The response object will contain an accelerators array, which lists the supported GPU configurations for that machine type.

Tensor Processing Units (TPUs) TPUs in Google Cloud are provisioned as nodes (for the legacy TPU Node architecture) or as TPU VMs. With TPU VMs, you get direct SSH access to the host machine. To find valid combinations, you need to identify the available TPU types and their corresponding supported VM configurations in a zone.

Using the gcloud Command-Line Tool List available TPU types in a zone: You can list the TPU accelerator types available in a specific zone using the gcloud compute tpus accelerator-types list command.

bash gcloud compute tpus accelerator-types list \--zone=us-central1-a This will return a table of available accelerator types, including their name and the number of TPU chips and cores.

List available TPU VM runtime versions: When creating a TPU VM, you also need to specify a software version. You can list the available runtime versions for TPUs in a zone.

bash gcloud compute tpus versions list \--zone=us-central1-a Determine compatible VM types: The specific VM type (e.g., n2-standard-4) is often tied to the TPU type and is managed by the Cloud TPU service. When you create a TPU VM, you specify the accelerator type, and Google Cloud provisions the appropriate underlying VM. The documentation for each TPU version and type often specifies the host machine's characteristics.

Using the Google Cloud API You can interact with the Cloud TPU API to get information about available TPU types and locations.

List Locations and Available TPUs: Use the tpu.projects.locations.list and tpu.projects.locations.acceleratorTypes.list methods to discover which TPU types are available in which zones.

Get Accelerator Type Details: The tpu.projects.locations.acceleratorTypes.get method can provide more details about a specific TPU type.

By combining the information from these commands and API calls, you can build a comprehensive map of the valid VM and accelerator combinations available in any given Google Cloud zone. You can programmatically determine the valid combinations of VM types and accelerator (GPU/TPU) types available in a specific Google Cloud zone by using a combination of gcloud command-line tool commands and referencing the official Google Cloud documentation. There isn't a single command that provides this information directly, but you can follow this two-step process:

Step 1: List Available Accelerator Types in a Zone First, identify the accelerator types (GPUs and TPUs) available in the specific zone you are interested in. You can achieve this using the gcloud compute accelerator-types list command with a filter for the desired zone.

For example, to list all accelerator types available in the us-central1-a zone, run the following command:

bash gcloud compute accelerator-types list \--filter="zone:( us-central1-a )" This command will return a list of accelerator types, such as nvidia-tesla-t4, nvidia-tesla-v100, etc., that are available in that zone. Google Drive icon

Step 2: Determine Compatible Machine Types Once you have the list of available accelerator types, you need to determine which VM machine types are compatible with them.

For Accelerator-Optimized Machine Types (A-series, G-series) Some machine series, known as accelerator-optimized machine types (like A4, A3, A2, and G2), come with a specific GPU model pre-attached. To find the availability of these, you can list the machine types for the zone.

For example, to find if the a3-highgpu-8g machine type (which has NVIDIA H100 GPUs) is available in us-central1-a, you can run:

bash gcloud compute machine-types list \--filter="name=a3-highgpu-8g AND zone:( us-central1-a )" For General-Purpose N1 Machine Types For the N1 machine series, you can attach a variety of GPU models. To find the valid combinations, you need to cross-reference the available accelerator types from Step 1 with the list of N1 machine types in that zone.

First, list the N1 machine types in the zone:

bash gcloud compute machine-types list \--filter="name:n1- AND zone:( us-central1-a )" Then, you can consult the GPU machine types documentation to see the compatibility between the N1 series and the available GPUs you found in Step 1\. The documentation provides detailed tables showing which N1 machine types support which GPUs and in what quantity.

Putting It All Together Programmatically To automate this, you can create a script that:

Executes gcloud compute accelerator-types list for a given zone and parses the output to get a list of accelerator names.

For each accelerator name, queries the GPU regions and zones documentation or a cached version of it to find the compatible machine series (e.g., N1, A2).

Executes gcloud compute machine-types list for the same zone, filtering by the compatible machine series.

The result is the list of valid VM and accelerator combinations for that zone.

Using the API For a more programmatic approach without relying on parsing gcloud output, you can use the Google Cloud API directly. The equivalent API calls would be:

acceleratorTypes.list to get available accelerator types in a zone.

machineTypes.list to get available machine types in a zone.

You would still need to implement the logic to cross-reference the compatibility based on the information from the Google Cloud documentation. There is no "Does this combination of features exist?" API. Yaqs icon

Configuring a Slurm Scheduler in Google Cloud Cluster Toolkit Configuring a Slurm scheduler within a Google Cloud Cluster Toolkit blueprint YAML file involves defining a set of modules that specify the behavior and resources for the Slurm controller and its associated compute partitions. This powerful infrastructure-as-code approach allows for reproducible and customizable HPC environments on Google Cloud.

The central component of this setup is the blueprint YAML file, which outlines the architecture of your cluster. To integrate a Slurm scheduler, you will primarily use the slurm\_controller module and one or more partition modules (e.g., compute\_partition).

Key Components of a Slurm Blueprint A typical Slurm blueprint YAML is structured with the following key sections:

terraform\_backend\_defaults: This section is recommended for production environments to store the Terraform state in a Google Cloud Storage bucket, ensuring better state management and collaboration.

vars: This section defines variables that can be used throughout the blueprint, such as project\_id, deployment\_name, region, and zone.

deployment\_groups: This is the core of the blueprint where you define the modules that will be deployed. For a Slurm cluster, this will include modules for networking, the Slurm controller, and compute partitions.

Configuring the Slurm Controller The slurm\_controller module is responsible for deploying the virtual machine that will run the slurmctld daemon, which manages the entire cluster. Here is an example of how to configure the slurm\_controller module within your blueprint:

yaml

- group: slurm\_cluster modules:  
  - id: slurm\_controller source: "./modules/scheduler/slurm\_controller" settings: machine\_type: "n2-standard-2" enable\_public\_ips: true partitions: \- name: "compute" nodeset: "compute\_nodes" In this example:

machine\_type: Specifies the Google Compute Engine machine type for the controller VM.

enable\_public\_ips: When set to true, it assigns a public IP address to the controller, allowing direct SSH access for administration and job submission.

partitions: This crucial setting links the controller to the compute partitions it will manage. Each entry in this list should correspond to a defined partition module.

Setting up Compute Partitions Compute partitions define the groups of nodes where Slurm jobs will actually run. Each partition is typically configured as a separate module. Here's an example of a compute\_partition configuration:

yaml \- id: compute\_partition source: "./modules/scheduler/slurm\_partition" settings: name: "compute" nodeset: "compute\_nodes" is\_default: true

```
- id: compute_nodes
  source: "./modules/compute/schedmd_slurm_gcp_v6_nodeset"
  settings:
    machine_type: "c2-standard-60"
    node_count_dynamic_max: 10
```

Key settings for a compute partition include:

name: A unique name for the partition. This is the name users will specify when submitting jobs (e.g., sbatch \-p compute).

nodeset: This links the partition to a specific nodeset module that defines the properties of the compute nodes.

is\_default: Setting this to true makes this partition the default for jobs submitted without a specific partition request.

machine\_type: The machine type for the compute nodes in this partition.

node\_count\_dynamic\_max: This enables autoscaling for the partition, defining the maximum number of nodes that can be created to handle the job queue.

Putting It All Together: A Complete Example To get started, you can use or adapt the hpc-slurm.yaml example found in the official Cluster Toolkit GitHub repository.

This example provides a solid foundation for a basic Slurm cluster.

Here is a simplified, conceptual example of a complete blueprint YAML for a Slurm cluster:

yaml

# Example hpc-slurm.yaml

terraform\_backend\_defaults: type: gcs configuration: bucket: "your-terraform-state-bucket"

vars: project\_id: "your-gcp-project-id" deployment\_name: "my-slurm-cluster" region: "us-central1" zone: "us-central1-a"

deployment\_groups:

- group: network modules:  
    
  - id: network source: "./modules/network/vpc"


- group: slurm\_cluster modules:  
    
  - id: slurm\_controller source: "./modules/scheduler/slurm\_controller" use: \[network\] settings: machine\_type: "n2-standard-2" enable\_public\_ips: true partitions: \- name: "c2-standard" nodeset: "c2\_nodes"  
      
  - id: c2\_partition source: "./modules/scheduler/slurm\_partition" use: \[slurm\_controller\] settings: name: "c2-standard" nodeset: "c2\_nodes" is\_default: true  
      
  - id: c2\_nodes source: "./modules/compute/schedmd\_slurm\_gcp\_v6\_nodeset" use: \[network\] settings: machine\_type: "c2-standard-60" node\_count\_dynamic\_max: 20 After creating your blueprint file, you use the gcluster command-line tool to generate the Terraform deployment files and then deploy your cluster. This process automates the provisioning of all the defined resources, from VPC networks to the Slurm controller and compute instances. Configuring a Slurm scheduler within a Google Cloud HPC Toolkit blueprint involves defining a set of interconnected modules in a YAML file. These modules specify the network, storage, compute resources, and the Slurm components themselves.

Key Components of a Slurm Blueprint A typical Slurm cluster blueprint is structured with the following components:

Blueprint Name (blueprint\_name): A name for your blueprint, which is used as a label on the deployed cloud resources for tracking and cost monitoring.

Variables (vars): A section for defining variables that can be used throughout the blueprint, such as project\_id, deployment\_name, region, and zone. This allows for easy customization of deployments.

Deployment Groups (deployment\_groups): This section organizes the modules that will be deployed together. A blueprint can have one or more groups.

Modules: These are the fundamental building blocks of the cluster. Each module has a unique id, a source pointing to its definition (often within the HPC Toolkit's GitHub repository), and settings for customization. The use key defines dependencies between modules. Google Drive icon

Configuring the Slurm Controller and Partitions To set up a Slurm cluster, you need to define modules for the controller, and at least one compute partition. A partition itself is typically composed of a "nodeset" and a "partition" module.

1. Define Compute Node Sets (nodeset) A nodeset module defines the configuration for a group of compute nodes that will form a partition. You can define multiple nodesets for different machine types or requirements.

In this example, two nodesets are created: one for general compute and another for debugging.

yaml

# In deployment\_groups: \-\> modules:

- id: debug\_nodeset source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset use: \[network\] \# Depends on the network module settings: node\_count\_dynamic\_max: 4 machine\_type: n2-standard-2  
    
- [...](asc_slot://start-slot-23)id: compute\_nodeset source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset use: \[network\] settings: node\_count\_dynamic\_max: 20 machine\_type: c2-standard-60 bandwidth\_tier: gvnic\_enabled \# Enables higher networking performance source: Points to the schedmd-slurm-gcp-v6-nodeset module, which is the standard for creating Slurm compute nodes with Slurm-GCP v6.

node\_count\_dynamic\_max: Specifies the maximum number of nodes the partition can autoscale to.

machine\_type: Defines the Google Compute Engine machine type for the nodes in this set. Google Drive icon

2. Define Slurm Partitions The partition module takes a nodeset and formally defines it as a Slurm partition with a specific name and properties.

yaml

# In deployment\_groups: \-\> modules:

- id: debug\_partition source: community/modules/compute/schedmd-slurm-gcp-v6-partition use:  
    
  - debug\_nodeset settings: partition\_name: debug is\_default: true \# Makes this the default partition for jobs


- [...](asc_slot://start-slot-27)id: compute\_partition source: community/modules/compute/schedmd-slurm-gcp-v6-partition use:  
    
  - compute\_nodeset settings: partition\_name: compute source: Uses the schedmd-slurm-gcp-v6-partition module.

use: This module depends on the corresponding nodeset module defined previously. Google Drive icon

partition\_name: The name that users will specify when submitting jobs (e.g., sbatch \-p compute). Google Drive icon

3. Define the Slurm Controller The slurm\_controller module is the core of the scheduler. It brings together the network, shared storage, and all defined partitions. A login node is also typically defined for user access and depends on the controller.

yaml

# In deployment\_groups: \-\> modules:

- id: homefs \# Shared home directory using Filestore source: modules/file-system/filestore use: \[network, private\_service\_access\] settings: local\_mount: /home  
    
- id: slurm\_login source: community/modules/scheduler/schedmd-slurm-gcp-v6-login use: \[network\] settings: machine\_type: n2-standard-4 enable\_login\_public\_ips: true  
    
- [...](asc_slot://start-slot-33)id: slurm\_controller source: community/modules/scheduler/schedmd-slurm-gcp-v6-controller use:  
    
  - network  
  - debug\_partition  
  - compute\_partition  
  - homefs  
  - slurm\_login settings: enable\_controller\_public\_ips: true source: Points to the schedmd-slurm-gcp-v6-controller module.

use: The controller module lists its dependencies, which crucially include all the partition modules (debug\_partition, compute\_partition), a shared file system (homefs), and the login node (slurm\_login). Google Drive icon

This linkage is what configures the controller to manage those specific partitions.

Complete Blueprint Example Here is a condensed example of a hpc-slurm.yaml blueprint that defines a Slurm cluster with a debug and a compute partition.

yaml blueprint\_name: hpc-slurm vars: project\_id: \#\# Set GCP Project ID Here \#\# deployment\_name: hpc-slurm-cluster region: us-central1 zone: us-central1-a

deployment\_groups:

- group: primary modules:

  # 1\. Networking

  - id: network source: modules/network/vpc  
  - id: private\_service\_access source: community/modules/network/private-service-access use: \[network\]

  # 2\. Shared Storage for /home

  - id: homefs source: modules/file-system/filestore use: \[network, private\_service\_access\] settings: local\_mount: /home

  # 3\. Define Nodesets

  - id: debug\_nodeset source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset use: \[network\] settings: node\_count\_dynamic\_max: 4 machine\_type: n2-standard-2  
      
  - id: compute\_nodeset source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset use: \[network\] settings: node\_count\_dynamic\_max: 20 machine\_type: c2-standard-60 bandwidth\_tier: gvnic\_enabled

  # 4\. Define Partitions

  - id: debug\_partition source: community/modules/compute/schedmd-slurm-gcp-v6-partition use: \[debug\_nodeset\] settings: partition\_name: debug is\_default: true  
      
  - id: compute\_partition source: community/modules/compute/schedmd-slurm-gcp-v6-partition use: \[compute\_nodeset\] settings: partition\_name: compute

  # 5\. Define Login and Controller Nodes

  - id: slurm\_login source: community/modules/scheduler/schedmd-slurm-gcp-v6-login use: \[network\] settings: machine\_type: n2-standard-4 enable\_login\_public\_ips: true  
      
  - id: slurm\_controller source: community/modules/scheduler/schedmd-slurm-gcp-v6-controller use:  
      
    - network  
    - debug\_partition  
    - compute\_partition  
    - homefs  
    - slurm\_login settings: enable\_controller\_public\_ips: true To deploy this configuration, you would use the gcluster command provided by the HPC Toolkit. The toolkit processes this YAML file, assembles the necessary Terraform code, and deploys a fully configured Slurm cluster.

Configuring advanced networking features such as Tier 1 networking, Google Virtual NIC (gVNIC), and Cloud RDMA within a Google Cloud Cluster Toolkit blueprint YAML is accomplished by leveraging the toolkit's modular architecture. The blueprint YAML file defines the desired cluster configuration by specifying and customizing various modules, which are essentially Terraform or Packer configurations.

To enable these advanced networking capabilities, you need to specify the appropriate parameters within the relevant modules in your blueprint file. While the exact YAML syntax can vary depending on the specific module version, the following provides a guide on how to configure these features.

Enabling Google Virtual NIC (gVNIC) gVNIC is crucial for high-performance networking on Google Cloud. To enable it for the compute nodes in your HPC cluster, you will typically need to set a variable within the slurm\_partition or a similar module in your blueprint.

A presentation on the Cluster Toolkit explicitly mentions a blueprint component for networking that includes "gVNIC installed" . This indicates that enabling gVNIC is a key feature of the networking modules.

Here is a conceptual example of how you might enable gVNIC in your blueprint's vars section or within a specific module's settings:

yaml blueprint\_name: hpc-advanced-networking-cluster vars: project\_id: your-gcp-project-id deployment\_name: hpc-cluster region: us-central1 zone: us-central1-a

deployment\_groups:

- group: primary modules:  
    
  - id: network1 source: community/modules/network/vpc  
      
  - id: compute-nodes source: community/modules/compute/slurm\_partition settings: machine\_type: "c2-standard-60" enable\_gvnic: true \# This is a hypothetical example parameter To find the exact variable name, you should refer to the documentation of the specific slurm\_partition or compute node module you are using within the Google Cloud Cluster Toolkit GitHub repository.

Enabling Tier 1 Networking (100/200 Gbps) Tier 1 networking provides the highest available network bandwidth for your VM instances, which is essential for many HPC workloads. Enabling this feature often involves setting a specific network performance configuration.

For GKE clusters, Tier 1 networking is enabled using the \--network-performance-configs=total-egress-bandwidth-tier=TIER\_1 flag . This suggests a similar parameter exists within the Cluster Toolkit's Terraform modules.

Within a Cluster Toolkit blueprint, you would likely define a variable to specify the desired network performance tier. This could be a top-level variable or a setting within a network or compute module.

Here is a conceptual example:

yaml blueprint\_name: hpc-tier1-cluster vars: project\_id: your-gcp-project-id deployment\_name: hpc-cluster region: us-central1 zone: us-central1-a network\_performance\_tier: "TIER\_1" \# Hypothetical top-level variable

deployment\_groups:

- group: primary modules:  
    
  - id: network1 source: community/modules/network/vpc settings: tier1\_networking: true \# Another possible implementation  
      
  - id: compute-nodes source: community/modules/compute/slurm\_partition settings: machine\_type: "c2-standard-60" network\_config: \# A more structured approach total\_egress\_bandwidth\_tier: "TIER\_1" Again, the precise variable name and structure will be defined in the module's source code. You should inspect the variables.tf file of the relevant network or compute module in the Cluster Toolkit repository to identify the correct parameter.

Configuring Cloud RDMA Cloud RDMA provides low-latency, high-throughput communication between VMs, which is particularly beneficial for tightly coupled HPC applications. As of the latest information, Cloud RDMA is available on specific machine types like the H3 and A3 VMs.

Configuring Cloud RDMA within a Cluster Toolkit blueprint would likely involve selecting a machine type that supports it and potentially enabling a specific setting.

Here is a conceptual example:

yaml blueprint\_name: hpc-rdma-cluster vars: project\_id: your-gcp-project-id deployment\_name: hpc-cluster region: us-central1 zone: us-central1-a

deployment\_groups:

- group: primary modules:  
    
  - id: network1 source: community/modules/network/vpc  
      
  - id: compute-nodes source: community/modules/compute/slurm\_partition settings: machine\_type: "h3-standard-88" \# H3 VMs support Cloud RDMA enable\_rdma: true \# Hypothetical parameter Finding the Correct Configuration Since the Google Cloud Cluster Toolkit is an open-source and evolving project, the most accurate way to determine the correct YAML configuration is to:

Consult the Official Documentation and Examples: The Cluster Toolkit documentation and the example blueprints in the GitHub repository are the best starting points.

Inspect the Module Source Code: The Cluster Toolkit is modular, with each module being a set of Terraform or Packer files . To find the specific variables you can set, navigate to the module's directory in the cloned repository (e.g., modules/network/vpc or community/modules/compute/slurm\_partition) and examine the variables.tf file. This file defines all the input variables that can be set in the blueprint YAML.

By following this approach of examining the provided modules and examples, you can effectively configure advanced networking features for your HPC cluster using the Google Cloud Cluster Toolkit. Configuring advanced networking features within a Google Cloud Cluster Toolkit blueprint is essential for achieving high performance for HPC workloads. This can be accomplished by specifying particular settings within the YAML blueprint file that define your cluster. Below are the instructions for enabling Tier 1 networking, gVNIC, and Cloud RDMA.

Designing the Cluster Blueprint A Cluster Toolkit blueprint YAML file is structured to define the configuration of a reusable cluster. The core components of the blueprint are deployment\_groups, which contain a set of modules that deploy and configure your HPC environment's infrastructure, such as compute nodes, storage, and networking.

To enable advanced networking, you will primarily modify the settings within the compute nodeset and network modules.

Enabling gVNIC and Tier 1 Networking Google Virtual NIC (gVNIC) is a virtual network interface designed for Google Cloud that offers higher performance compared to the standard VirtIO-based driver. Google Drive icon

Tier 1 networking provides even higher throughput (50/100/200 Gbps) for supported machine types and is a requirement for certain high-performance workloads. Google Drive icon

Enabling Tier 1 networking also requires the use of gVNIC.

You can enable these features within a nodeset module (e.g., community/modules/compute/schedmd-slurm-gcp-v6-nodeset) by using the bandwidth\_tier setting.

To enable gVNIC: Set bandwidth\_tier to gvnic\_enabled.

To enable Tier 1 Networking: Set bandwidth\_tier to tier\_1\_enabled.

YAML Configuration Example:

Here is a snippet from a blueprint's deployment\_groups section, demonstrating how to configure two different compute partitions: one with gVNIC enabled and another with Tier 1 networking.

yaml

# Copyright 2024 Google LLC

# ... (license header)

blueprint\_name: advanced-networking-hpc-slurm vars: project\_id: "your-gcp-project-id" deployment\_name: "hpc-cluster-1" region: "us-central1" zone: "us-central1-a"

deployment\_groups:

- group: primary modules:  
    
  - id: network source: modules/network/vpc

  # ... other modules like filestore, service accounts etc.

  # A compute nodeset with gVNIC enabled

  - id: h3\_nodeset source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset use: \[network\] settings: node\_count\_dynamic\_max: 16 machine\_type: h3-standard-88 bandwidth\_tier: gvnic\_enabled \# Enables gVNIC disk\_type: pd-balanced  
      
  - id: h3\_partition source: community/modules/compute/schedmd-slurm-gcp-v6-partition use: \[h3\_nodeset\] settings: partition\_name: h3

  # A compute nodeset with Tier 1 networking enabled

  - id: c3\_nodeset source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset use: \[network\] settings: node\_count\_dynamic\_max: 20 machine\_type: c3-standard-88 bandwidth\_tier: tier\_1\_enabled \# Enables Tier 1 networking  
      
  - id: c3\_partition source: community/modules/compute/schedmd-slurm-gcp-v6-partition use: \[c3\_nodeset\] settings: partition\_name: c3

  # ... [...](asc_slot://start-slot-21)slurm\_login and slurm\_controller modules

\*This example is based on blueprint structures found in the official documentation. \*

Important Considerations:

Machine Types: Tier 1 networking is only supported on specific machine types (like N2, N2D, C2, C2D, C3) with a minimum number of vCPUs.

gVNIC Requirement: To use Tier 1 networking, gVNIC must be enabled on the VM. The tier\_1\_enabled setting handles this requirement.

Node Images: Ensure you are using a node image that supports gVNIC, such as Google's HPC VM image or recent versions of standard OS images.

Enabling Cloud RDMA Cloud RDMA (Remote Direct Memory Access) over RoCE (RDMA over Converged Ethernet) provides low-latency, high-throughput communication for tightly-coupled HPC workloads. This is supported on specific machine families like the H4D series. Google Drive icon

To enable Cloud RDMA, you need to configure two main components in your blueprint:

VPC Network with RDMA Profile: The VPC network must be created with a special RDMA network profile.

RDMA-capable VM instances: The compute nodes must use a machine type that supports Cloud RDMA (e.g., H4D). Google Drive icon

YAML Configuration Example:

Configure the VPC Network for RDMA: You will need to modify the network module in your blueprint to specify the network\_profile.

yaml \# In your deployment\_groups section \- id: network source: modules/network/vpc settings: network\_profile: "rdma-network-profile-name" \# Fictional example name \`\`\` You must create a VPC network with the RDMA network profile. You should consult the official Cluster Toolkit documentation for the exact variable name to set the network profile within the `modules/network/vpc` module.

2. **Configure the Compute Nodeset for RDMA:** Specify an RDMA-capable machine type in the `nodeset` module.

```
# In your deployment_groups section
- id: h4d_nodeset
  source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset
  use: [network] # This network must have the RDMA profile
  settings:
    node_count_dynamic_max: 10
    machine_type: h4d-standard-192 # Example H4D machine type
    # Other necessary settings for RDMA nodes

- id: h4d_partition
  source: community/modules/compute/schedmd-slurm-gcp-v6-partition
  use: [h4d_nodeset]
  settings:
    partition_name: h4d
```

By combining these configurations in your Cluster Toolkit blueprint, you can deploy an HPC cluster optimized with the advanced networking capabilities required for demanding computational and data-intensive workloads. Blueprint for High-Performance, Tightly-Coupled Training on Google Cloud For organizations leveraging Google Cloud for demanding, multi-node, tightly-coupled training workloads, the Google Cloud Cluster Toolkit provides a streamlined method for deploying complex, high-performance computing environments. This is achieved through a declarative YAML blueprint that defines the entire cluster configuration.

Below is a comprehensive, best-practices example of a Cluster Toolkit blueprint YAML file. This blueprint is designed for a multi-node, tightly-coupled training job utilizing A3 virtual machines, each equipped with 8 NVIDIA H100 GPUs. It incorporates Tier-1 networking for maximum bandwidth and low latency, and a shared Google Cloud Managed Lustre file system for high-throughput data access.

Example Blueprint: a3-h100-lustre-training-cluster.yaml yaml

# Copyright 2024 Google LLC

# 

# Licensed under the Apache License, Version 2.0 (the "License");

# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at

# 

# [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

# 

# Unless required by applicable law or agreed to in writing, software

# distributed under the License is distributed on an "AS IS" BASIS,

# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

# See the License for the specific language governing permissions and

# limitations under the License.

# 

# Blueprint for a Slurm cluster with A3 VMs, H100 GPUs, Tier-1 Networking,

# and a Managed Lustre filesystem.

# 

blueprint\_name: a3-h100-lustre-training

# Deployment variables that can be overridden at deployment time.

vars: project\_id: "your-gcp-project-id" deployment\_name: "hpc-training-cluster" region: "us-central1" zone: "us-central1-a"

# Defines the deployment groups and the modules within them.

deployment\_groups:

- group: primary modules:

  # Networking Module: Creates a new VPC and subnets.

  # Tier-1 networking is enabled on the compute instances.

  - id: network source: modules/network/vpc

  # Managed Lustre Module: Deploys a managed Lustre file system.

  # This provides a high-performance, parallel file system for training data and checkpoints.

  - id: lustre\_fs source: modules/file-system/managed-lustre settings:

    # The following are example settings. Adjust capacity and throughput based on your needs.

    # Refer to Google Cloud Managed Lustre documentation for performance tiers.

    capacity\_gb: 12288 \# 12 TiB deployment\_type: "SCRATCH\_SSD" \# Options include "SCRATCH\_SSD" and "PERSISTENT\_SSD\_250" use:  
      
    - network

  # Slurm Controller Module: Deploys the Slurm controller node.

  - id: slurm\_controller source: modules/scheduler/slurm-controller settings: machine\_type: "n2-standard-8" use:  
    - network  
    - lustre\_fs

  # Slurm Login Node Module: Deploys a login node for cluster access.

  - id: slurm\_login source: modules/scheduler/slurm-login settings: machine\_type: "n2-standard-8" use:  
    - network  
    - lustre\_fs  
    - slurm\_controller

  # Slurm Compute Partition Module: Defines the A3 compute nodes.

  - id: slurm\_partition source: modules/scheduler/slurm-partition settings: partition\_name: "a3-highgpu" machine\_type: "a3-highgpu-8g" \# A3 VM with 8 H100 GPUs

    # For tightly-coupled workloads, a compact placement policy is recommended

    # to reduce latency between nodes.

    placement\_policy: "COMPACT"

    # Enable Tier-1 networking for highest bandwidth

    network\_storage:  
      
    - tier1\_enabled: true

    # Specify the GPU type and count

    gpu: type: "nvidia-h100-80gb" count: 8

    # Use a recommended image for A3 VMs

    source\_image\_family: "hpc-rocky-linux-8"

    # Set the number of nodes in the partition. Can be configured for auto-scaling.

    node\_count: static: 2 \# Example: 2 nodes for a total of 16 H100 GPUs use:

    

    - network  
    - lustre\_fs  
    - slurm\_controller Key Components of the Blueprint This blueprint is structured into logical modules, a core concept of the Cluster Toolkit that allows for reusable and composable infrastructure components.

blueprint\_name: A unique identifier for this cluster configuration.

vars: Global variables for the deployment, such as project ID, deployment name, and location. These can be overridden at deployment time for flexibility.

deployment\_groups: A collection of modules that will be deployed together.

Modules in Detail: Networking (modules/network/vpc): This module establishes the Virtual Private Cloud (VPC) and subnets that will house the cluster components. Proper network configuration is crucial for performance.

Managed Lustre (modules/file-system/managed-lustre): This module deploys a Google Cloud Managed Lustre file system.

Lustre is a high-performance parallel file system well-suited for the large, sequential reads and writes common in large-scale model training and checkpointing. The deployment\_type and capacity\_gb can be adjusted to meet specific performance and storage requirements. The Cluster Toolkit documentation provides details on available modules, including those for various file systems.

Slurm Controller and Login Nodes (modules/scheduler/slurm-controller, modules/scheduler/slurm-login): These modules set up the management plane for the Slurm workload manager. Slurm is a popular open-source scheduler for HPC clusters. The controller manages the job queue, while the login node provides a user-facing entry point to the cluster for submitting jobs and managing files.

Slurm Compute Partition (modules/scheduler/slurm-partition): This is the core of the training environment, defining the characteristics of the compute nodes.

machine\_type: "a3-highgpu-8g": This specifies the A3 machine type, which is optimized for AI/ML workloads and includes 8 NVIDIA H100 GPUs.

placement\_policy: "COMPACT": For tightly-coupled training, a compact placement policy is a best practice. It ensures that the VMs are placed in close physical proximity within the data center, minimizing network latency between nodes.

network\_storage: \- tier1\_enabled: true: This setting is critical for enabling Tier-1 networking on the A3 VMs, providing the highest possible network bandwidth for inter-node communication, which is essential for distributed training performance.

gpu: This section explicitly defines the type and count of GPUs to be attached to each VM.

node\_count: This determines the number of compute nodes in the partition. For dynamic workloads, this can be configured for autoscaling.

Deployment Process To deploy a cluster using this blueprint, you would typically follow these steps:

Install the Google Cloud Cluster Toolkit.

Save the YAML content into a file (e.g., a3-h100-lustre-training-cluster.yaml).

Update the vars section with your specific project details.

Run the gcluster create command, pointing to your blueprint file.

The Cluster Toolkit engine then processes the blueprint, assembles the necessary Terraform and Packer configurations, and creates a self-contained deployment folder that can be used to provision the cluster. This approach turns the complexity of setting up a high-performance training environment into a repeatable and manageable process.

Here is a complete, best-practices example of a Google Cloud Cluster Toolkit blueprint YAML for a multi-node, tightly-coupled training job. This blueprint provisions a Slurm cluster utilizing A3 High-GPU VMs with 8 NVIDIA H100 GPUs each, Tier-1 networking for high-throughput, and a shared Lustre file system for high-performance storage.

Overview of the Blueprint This blueprint automates the deployment of a comprehensive High-Performance Computing (HPC) environment tailored for demanding AI and machine learning training workloads. The Cluster Toolkit uses a modular approach, where different components of the HPC environment are defined as modules in a YAML file. Google Drive icon

The key components defined in this blueprint are:

Networking: A dedicated Virtual Private Cloud (VPC) to ensure a secure and isolated environment for the cluster.

Shared Storage:

A high-performance Lustre parallel file system (deployed using the DDN EXAScaler module) mounted as /scratch for high-throughput data access during training. Google Drive icon

Google Drive icon

A Google Cloud Filestore instance mounted as /home for user home directories, a common practice for HPC clusters. Google Drive icon

Scheduler: The Slurm workload manager is deployed with a controller and a login node, providing a familiar interface for job submission and management.

Compute Nodes: An auto-scaling partition of a3-highgpu-8g virtual machines. These nodes are configured with:

8 NVIDIA H100 GPUs per VM. Google Drive icon

Tier-1 Networking to enable the highest possible network bandwidth for inter-node communication. Google Drive icon

Google Drive icon

Compact Placement Policy to minimize latency between nodes, which is crucial for tightly-coupled distributed training jobs. Google Drive icon

Google Drive icon

Google Virtual NIC (gVNIC) for higher network performance. Google Drive icon

Google Drive icon

Prerequisites Before deploying this blueprint, ensure the following prerequisites are met:

Install and configure the Cluster Toolkit: You must have the gctcli binary built and your Google Cloud project configured. Google Drive icon

Quotas: Ensure you have sufficient quota for A3 VMs, NVIDIA H100 GPUs, and Filestore in your selected region and zone.

DDN EXAScaler License: The DDN EXAScaler module for Lustre requires a license, which can be acquired through the Google Cloud Marketplace. Google Drive icon

Example Blueprint: a3-lustre-slurm-blueprint.yaml yaml

# Copyright 2025 Google LLC

# 

# Licensed under the Apache License, Version 2.0 (the "License");

# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at

# 

# [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

# 

# Unless required by applicable law or agreed to in writing, software

# distributed under the License is distributed on an "AS IS" BASIS,

# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

# See the License for the specific language governing permissions and

# limitations under the License.

# Blueprint for a multi-node, tightly-coupled training cluster with A3 VMs and Lustre.

blueprint\_name: a3-lustre-slurm-hpc

# Deployment-specific variables.

# These should be overridden at deployment time using a deployment file or \--vars flag.

vars: project\_id: "your-gcp-project-id" deployment\_name: "a3-training-cluster" region: "us-central1" zone: "us-central1-a"

# It is recommended to use a remote terraform state backend for production environments.

# terraform\_backend\_defaults:

# type: gcs

# configuration:

# bucket: "your-terraform-state-bucket"

# Defines the modules to be deployed.

deployment\_groups:

- group: primary modules:

  # Module to create a new VPC and subnets for the cluster.

  - id: network source: modules/network/vpc

  # Module for Private Service Access, required by Filestore.

  - id: private\_service\_access source: community/modules/network/private-service-access use: \[network\]

  # Module for a shared home directory using Filestore.

  - id: homefs source: modules/file-system/filestore use: \[network, private\_service\_access\] settings: local\_mount: /home

  # Module for a high-performance Lustre file system for scratch space.

  # This requires a license from the Google Cloud Marketplace.

  - id: scratchfs source: community/modules/file-system/DDN-EXAScaler use: \[network\] settings: local\_mount: /scratch

  # Defines the compute nodes for the A3 partition.

  - id: a3\_nodeset source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset use: \[network\] settings: machine\_type: a3-highgpu-8g node\_count\_dynamic\_max: 16 \# Maximum number of nodes to autoscale to. node\_count\_static: 0 \# Number of nodes to be always on. placement\_policy: "COMPACT" \# Minimizes latency between nodes. bandwidth\_tier: "tier\_1\_enabled" \# Enables high-bandwidth networking. instance\_image: family: "hpc-rocky-linux-8" \# Using a standard HPC-optimized image. project: "cloud-hpc-image-public"

  # Defines the Slurm partition for the A3 compute nodes.

  - id: a3\_partition source: community/modules/compute/schedmd-slurm-gcp-v6-partition use: \[a3\_nodeset\] settings: partition\_name: a3 is\_default: true

  # Defines the login node for the cluster.

  - id: slurm\_login source: community/modules/scheduler/schedmd-slurm-gcp-v6-login use: \[network\] settings: machine\_type: n2-standard-4 enable\_login\_public\_ips: true \# Set to false if using a bastion host or IAP.

  # Defines the Slurm controller node.

  # It uses the network, partitions, and file systems defined above.

  - id: slurm\_controller source: community/modules/scheduler/schedmd-slurm-gcp-v6-controller use:  
    - network  
    - a3\_partition  
    - homefs  
    - scratchfs  
    - slurm\_login settings:

    # It is recommended to disable public IPs for the controller in a production environment.

    enable\_controller\_public\_ips: true

    # Cloud parameters to allow for longer boot times for large GPU nodes.

    cloud\_parameters: resume\_timeout: 1200 \# Increased timeout for A3 node startup. suspend\_timeout: 600

How to Deploy Save the blueprint: Save the YAML content above into a file named a3-lustre-slurm-blueprint.yaml.

Create a deployment file: It is a best practice to create a separate deployment file to specify variables for a particular deployment. Create a file named my-a3-cluster.yaml with the following content, replacing the placeholder values with your specific information:

yaml vars: project\_id: "your-gcp-project-id" deployment\_name: "a3-training-cluster-01" region: "us-central1" zone: "us-central1-a" Create the deployment folder: Run the gctcli create command to generate the Terraform deployment files from your blueprint. Google Drive icon

bash ./gcluster create my-a3-cluster.yaml \-b a3-lustre-slurm-blueprint.yaml Deploy the cluster: Use the gctcli deploy command to provision the resources on Google Cloud. This process will take several minutes.

bash ./gcluster deploy a3-training-cluster-01 Access and use the cluster: Once the deployment is complete, you can SSH into the login node and start submitting jobs to the Slurm scheduler. The A3 compute nodes will be automatically created and provisioned as jobs are submitted to the a3 partition.

This blueprint provides a robust and scalable foundation for the most demanding multi-node, tightly-coupled training jobs on Google Cloud, leveraging the full power of A3 VMs with H100 GPUs, high-speed networking, and a parallel file system.

Building a Versatile Python CLI with click This guide will walk you through constructing a robust Python command-line interface (CLI) application using the click library. You will learn how to implement distinct commands, accept and validate user input through flags, and create an interactive wizard for a user-friendly configuration experience.

Core Concepts of the click Library The click library is a powerful tool for creating CLIs in Python. It uses decorators to define commands, options, and arguments, which makes the code clean and readable. Key features include automatic help page generation, support for subcommands, and various parameter types.

Setting Up Your Project First, ensure you have click installed. If not, you can install it using pip:

bash pip install click Creating a Multi-Command CLI To support commands like generate and validate, you'll use a click.group(). A group serves as a container for multiple subcommands.

Here is a basic structure:

python import click

@click.group() def cli(): """A CLI tool for generating and validating configurations.""" pass

@cli.command() def generate(): """Generates a new configuration.""" click.echo("Generating configuration...")

@cli.command() def validate(): """Validates an existing configuration.""" click.echo("Validating configuration...")

if **name** \== '**main**': cli() In this example, @click.group() creates the main entry point for the CLI. The @cli.command() decorator then registers the generate and validate functions as subcommands.

Accepting Flags and Options To accept flags like \--machine-type and \--gpu-count, you can add @click.option() decorators to your command functions.

Defining Option Types click supports various data types for options, such as strings, integers, and choices from a predefined list.

For \--machine-type, you can use click.Choice to restrict the input to a specific set of values.

For \--gpu-count, you can specify the type as int.

Here's how to add these options to the generate command:

python import click

@click.group() def cli(): """A CLI tool for generating and validating configurations.""" pass

@cli.command() @click.option('--machine-type', type=click.Choice(\['n1-standard-1', 'e2-medium', 'n2-highmem-2'\], case\_sensitive=False), help='The type of machine to use.') @click.option('--gpu-count', type=int, help='The number of GPUs to attach.') def generate(machine\_type, gpu\_count): """Generates a new configuration.""" click.echo(f"Generating configuration with machine type: {machine\_type} and {gpu\_count} GPUs.")

@cli.command() def validate(): """Validates an existing configuration.""" click.echo("Validating configuration...")

if **name** \== '**main**': cli() Now, you can run your CLI with these flags:

bash python your\_script.py generate \--machine-type n1-standard-1 \--gpu-count 2 Implementing an Interactive Wizard Mode For a more guided user experience, you can create an interactive "wizard" that prompts the user for configuration choices. This can be implemented as a separate command or as a fallback when no options are provided.

The click.prompt() function is ideal for this, as it can ask for user input and validate the data type.

Here's how to create a wizard command:

python import click

@click.group() def cli(): """A CLI tool for generating and validating configurations.""" pass

# ... (generate and validate commands as before) ...

@cli.command() def wizard(): """Starts an interactive wizard to guide you through configuration.""" click.echo("Welcome to the interactive configuration wizard\!")

```
machine_type = click.prompt(
    'Please choose a machine type',
    type=click.Choice(['n1-standard-1', 'e2-medium', 'n2-highmem-2'], case_sensitive=False)
)

has_gpu = click.confirm('Do you want to add GPUs?')
gpu_count = 0
if has_gpu:
    gpu_count = click.prompt('How many GPUs?', type=click.IntRange(1, 8))

click.echo("\nConfiguration summary:")
click.echo(f"  Machine Type: {machine_type}")
click.echo(f"  GPU Count: {gpu_count}")
```

if **name** \== '**main**': cli() In this wizard command:

click.prompt() is used with type=click.Choice to ask the user to select a machine type.

click.confirm() presents a yes/no question.

Based on the answer to the confirmation, a conditional prompt for the number of GPUs is shown using click.IntRange to ensure the input is within a valid range.

This approach allows for a guided, multi-step process, which is the essence of an interactive wizard. You can run this wizard with:

bash python your\_script.py wizard Of course. Here is a guide on how to build a Python CLI application using the click library to support commands like generate and validate, accept flags such as \--machine-type and \--gpu-count, and include an interactive wizard mode.

1. Project Structure A good practice is to structure your project into modules. For this example, we'll use a simple structure with a main script. Google Drive icon  
     
2. Basic Setup First, you need to install the click library:

bash pip install click Now, let's create the main entry point for your CLI application. This is often done in a file named cli.py or main.py. Google Drive icon

python import click

@click.group() def cli(): """A CLI tool to generate and validate configurations.""" pass

if **name** \== '**main**': cli() This code sets up a group of commands. The @click.group() decorator turns the cli function into a group that can have other commands attached to it.

3. Adding Commands You can add commands like generate and validate to the cli group.

generate Command The generate command will create a configuration. It will accept flags for customization.

python import click

@click.group() def cli(): """A CLI tool to generate and validate configurations.""" pass

@cli.command() @click.option('--machine-type', help='The machine type for the resource.') @click.option('--gpu-count', type=int, help='The number of GPUs.') def generate(machine\_type, gpu\_count): """Generates a new configuration.""" click.echo("Generating configuration with:") click.echo(f"  Machine Type: {machine\_type}") click.echo(f"  GPU Count: {gpu\_count}") \# In a real application, you would generate a file here.

if **name** \== '**main**': cli() To run this, you would use:

bash python cli.py generate \--machine-type n1-standard-4 \--gpu-count 2 validate Command The validate command will check an existing configuration file.

python

# ... (previous code)

@cli.command() @click.argument('file', type=click.Path(exists=True)) def validate(file): """Validates an existing configuration file.""" click.echo(f"Validating configuration file: {file}") \# In a real application, you would read and validate the file here.

# ... (if **name** \== '**main**': ...)

To run this, you would use:

bash python cli.py validate my\_config.yaml 4\. Implementing an Interactive Wizard Mode An interactive wizard can guide users through the configuration choices, which is especially useful if they don't provide all the required flags. Yaqs icon

Google Drive icon You can trigger this with a flag like \--interactive. Google Drive icon

click provides a prompt function that can be used for this purpose. Yaqs icon

Here is how you can modify the generate command to include a wizard:

python import click

@click.group() def cli(): """A CLI tool to generate and validate configurations.""" pass

@cli.command() @click.option('--machine-type', help='The machine type for the resource.') @click.option('--gpu-count', type=int, help='The number of GPUs.') @click.option('--interactive', is\_flag=True, help='Enable interactive wizard mode.') def generate(machine\_type, gpu\_count, interactive): """Generates a new configuration.""" if interactive: click.echo("Entering interactive wizard mode...") if not machine\_type: machine\_type \= click.prompt("Enter the machine type", type=str, default='n1-standard-2') if gpu\_count is None: gpu\_count \= click.prompt("Enter the number of GPUs", type=int, default=0)

```
click.echo("\nGenerating configuration with:")
click.echo(f"  Machine Type: {machine_type}")
click.echo(f"  GPU Count: {gpu_count}")
# In a real application, you would generate a file here.
```

@cli.command() @click.argument('file', type=click.Path(exists=True)) def validate(file): """Validates an existing configuration file.""" click.echo(f"Validating configuration file: {file}") \# In a real application, you would read and validate the file here.

if **name** \== '**main**': cli() Now, you can run the generate command in interactive mode:

bash python cli.py generate \--interactive The application will then prompt you for the machine type and GPU count if they are not provided as flags.

Complete Example Here is the complete cli.py file putting it all together:

python import click

@click.group() def cli(): """A CLI tool to generate and validate configurations.""" pass

@cli.command() @click.option('--machine-type', help='The machine type for the resource.') @click.option('--gpu-count', type=int, help='The number of GPUs.') @click.option('--interactive', is\_flag=True, help='Enable interactive wizard mode.') def generate(machine\_type, gpu\_count, interactive): """Generates a new configuration.""" if interactive: click.echo("Entering interactive wizard mode...") if not machine\_type: machine\_type \= click.prompt("Enter the machine type", type=str, default='n1-standard-2') if gpu\_count is None: gpu\_count \= click.prompt("Enter the number of GPUs", type=int, default=0)

```
if not machine_type:
    raise click.UsageError("Missing option '--machine-type' or use '--interactive'.")

click.echo("\nGenerating configuration with:")
click.echo(f"  Machine Type: {machine_type}")
click.echo(f"  GPU Count: {gpu_count if gpu_count is not None else 'Not specified'}")
# In a real application, you would generate a YAML or JSON file here.
click.echo("\nConfiguration generated successfully!")
```

@cli.command() @click.argument('file', type=click.Path(exists=True)) def validate(file): """Validates an existing configuration file.""" click.echo(f"Validating configuration file: {file}") \# In a real application, you would read the file and perform validation logic. \# For example, check if the machine type and GPU count are valid for a specific cloud region. click.echo(f"\\nValidation of {file} completed.")

if **name** \== '**main**': cli() This example provides a solid foundation for building a more complex CLI application with the click library, incorporating commands, flags, and an interactive wizard as requested.

You can programmatically find Google Cloud locations that offer a specific combination of High-Performance Computing (HPC) resources, such as A3 VMs with 8 H100 GPUs and Managed Lustre storage, by using a Python script that interacts with the Google Cloud Compute Engine API.

The overall process involves two main steps:

Identifying all zones where the specified virtual machine (VM) and GPU combination is available.

Filtering those locations to include only the regions where Google Cloud Managed Lustre is also offered.

The specific machine type for an A3 VM with 8 NVIDIA H100 GPUs is a3-highgpu-8g. Google Drive icon

This machine type comes with 8 NVIDIA H100 80GB GPUs attached.

The corresponding storage solution is Google Cloud Managed Lustre. Google Drive icon

Here is a Python script that demonstrates how to achieve this.

Python Script to Find Available Locations This script uses the google-cloud-compute library to query for resource availability.

python

# First, ensure you have the required library installed:

# pip install google-cloud-compute

# Before running, make sure you have authenticated with Google Cloud:

# gcloud auth application-default login

from google.cloud import compute\_v1

def find\_hpc\_resource\_locations(project\_id: str): """ Finds Google Cloud zones where A3 VMs with 8 H100 GPUs and Managed Lustre storage are available.

```
Args:
    project_id: The Google Cloud project ID.
"""
# The specific accelerator-optimized machine type for A3 with 8 H100 GPUs.
target_machine_type = "a3-highgpu-8g"

# Regions where Google Cloud Managed Lustre is available.
# This list is based on public documentation and should be verified periodically.
# Source: cloud.google.com/managed-lustre/docs/locations [2]
lustre_regions = {
    "asia-northeast1", "asia-south1", "asia-southeast1", "australia-southeast1",
    "europe-west1", "europe-west2", "europe-west3", "europe-west4", "europe-west9",
    "me-central2", "me-west1", "northamerica-northeast1", "southamerica-east1",
    "us-central1", "us-east1", "us-east4", "us-east5", "us-east7", "us-south1",
    "us-west1", "us-west2", "us-west4"
}

print(f"Searching for zones with machine type '{target_machine_type}' in Lustre-supported regions...")

available_zones = []
machine_type_client = compute_v1.MachineTypesClient()

# Use aggregated_list to efficiently query across all zones.
request = compute_v1.AggregatedListMachineTypesRequest(project=project_id)

# The result is an iterator of tuples, where each tuple contains a zone name
# and a list of machine types available in that zone.
for zone, response in machine_type_client.aggregated_list(request=request):
    if response.machine_types:
        for machine_type in response.machine_types:
            # Check if the target machine type is present in the zone.
            if machine_type.name == target_machine_type:
                # Extract the region from the zone name (e.g., "us-central1-a" -> "us-central1").
                current_region = '-'.join(zone.split('-')[:-1])
                
                # Check if the region supports Managed Lustre.
                if current_region in lustre_regions:
                    available_zones.append(zone)
                    # Move to the next zone once a match is found.
                    break

if available_zones:
    print("\nFound locations with A3 (8xH100) VMs and Managed Lustre:")
    for zone in sorted(available_zones):
        print(f"- {zone}")
else:
    print("\nNo locations found matching the specified criteria.")
```

if **name** \== "**main**": \# Replace 'your-gcp-project-id' with your actual Google Cloud project ID. gcp\_project\_id \= "your-gcp-project-id" find\_hpc\_resource\_locations(gcp\_project\_id)

How the Script Works: Prerequisites:

The script requires the google-cloud-compute Python library. You can install it using pip install google-cloud-compute.

You must authenticate your environment to Google Cloud. The simplest way for a local development environment is to use the gcloud CLI: gcloud auth application-default login.

Resource Identification:

target\_machine\_type: Set to a3-highgpu-8g, which is the specific name for A3 VMs with 8 H100 GPUs. Google Drive icon

lustre\_regions: A set containing the names of all Google Cloud regions where Managed Lustre is confirmed to be available, according to official documentation. Google Drive icon

Querying for Machine Type Availability:

It initializes a MachineTypesClient from the compute\_v1 library.

To efficiently search across all zones without making numerous individual API calls, the script uses the aggregated\_list method. Yaqs icon This method fetches a collection of all machine types, grouped by zone.

The script iterates through each zone returned by the API call.

Filtering and Cross-Referencing:

For each zone, it checks if the a3-highgpu-8g machine type is in the list of available types for that zone.

If the machine type is found, the script extracts the region name from the zone name (for example, it derives us-central1 from us-central1-a).

It then checks if this extracted region is present in the lustre\_regions set.

If both conditions are met, the zone is considered a valid location and is added to the available\_zones list.

Displaying Results:

Finally, the script prints the sorted list of all zones that satisfy the criteria, providing a clear and actionable list of locations for deploying the specified HPC resources.

Dynamically Generating Google Cloud Cluster Toolkit Blueprints with Python A Python script leveraging the PyYAML and click libraries offers a powerful way to dynamically construct and write Google Cloud Cluster Toolkit blueprint YAML files. This approach allows for the creation of flexible and reusable cluster configurations based on user input provided through command-line options.

At its core, a Google Cloud Cluster Toolkit blueprint is a YAML file that defines the desired state of a high-performance computing (HPC) or other cluster environment. These blueprints are composed of several key sections, including blueprint\_name, vars for global variables, and deployment\_groups which contain the core module definitions for the cluster's resources.

This guide will walk through a Python script that demonstrates how to accept user inputs via click and use them to build the nested dictionary structure for a blueprint, which is then written to a YAML file using PyYAML.

Understanding the Blueprint Structure Before constructing the script, it's essential to understand the structure of a Cluster Toolkit blueprint YAML file. A typical blueprint includes:

blueprint\_name: A string that identifies the blueprint.

vars: A dictionary of variables that can be used throughout the blueprint.

deployment\_groups: A list of deployment groups. Each group has:

group: A name for the deployment group.

modules: A list of modules to be deployed within that group. Each module is a dictionary containing:

id: A unique identifier for the module.

source: The path or source of the module (e.g., a local directory or a Git repository).

settings: A dictionary of settings specific to that module.

The Python Script The following Python script utilizes the click library to define command-line options for specifying blueprint parameters and the PyYAML library to generate the final YAML file.

python import click import yaml

@click.command() @click.option('--blueprint-name', required=True, help='The name of the blueprint.') @click.option('--deployment-name', required=True, help='The name of the deployment.') @click.option('--project-id', required=True, help='The Google Cloud project ID.') @click.option('--zone', default='us-central1-a', help='The Google Cloud zone for the cluster.') @click.option('--compute-machine-type', default='n2-standard-2', help='The machine type for compute nodes.') @click.option('--compute-node-count', default=2, type=int, help='The number of compute nodes.') @click.option('--output-file', default='my\_blueprint.yaml', help='The name of the output YAML file.') def generate\_blueprint(blueprint\_name, deployment\_name, project\_id, zone, compute\_machine\_type, compute\_node\_count, output\_file): """ Generates a Google Cloud Cluster Toolkit blueprint YAML file. """ blueprint \= { 'blueprint\_name': blueprint\_name, 'vars': { 'deployment\_name': deployment\_name, 'project\_id': project\_id, 'zone': zone, }, 'deployment\_groups': \[ { 'group': 'primary', 'modules': \[ { 'id': 'network', 'source': 'modules/network/vpc', }, { 'id': 'slurm\_controller', 'source': 'modules/schedmd-slurm-gcp-v5/schedmd-slurm-gcp-controller', 'settings': { 'machine\_type': 'n2-standard-2', } }, { 'id': 'slurm\_login', 'source': 'modules/schedmd-slurm-gcp-v5/schedmd-slurm-gcp-login', 'settings': { 'machine\_type': 'n2-standard-2', } }, { 'id': 'compute\_partition', 'source': 'modules/schedmd-slurm-gcp-v5/schedmd-slurm-gcp-partition', 'settings': { 'partition\_name': 'compute', 'machine\_type': compute\_machine\_type, 'max\_node\_count': compute\_node\_count, } } \] } \] }

```
with open(output_file, 'w') as f:
    yaml.dump(blueprint, f, sort_keys=False)

click.echo(f"Blueprint '{output_file}' generated successfully.")
```

if **name** \== '**main**': generate\_blueprint() How the Script Works Import Libraries: The script begins by importing the necessary click and yaml (PyYAML) libraries.

Define Click Options: The @click.command() decorator turns the generate\_blueprint function into a command-line command. The @click.option() decorators define the command-line arguments that the user can provide. This allows for dynamic input of essential parameters like the blueprint name, deployment name, project ID, and compute node specifications.

Construct the Blueprint Dictionary: Inside the generate\_blueprint function, a nested Python dictionary named blueprint is created. This dictionary mirrors the structure of the Google Cloud Cluster Toolkit YAML blueprint. The values for the various keys are populated using the arguments passed through the click options.

Dynamic Module Configuration: The script dynamically configures the compute\_partition module. The machine\_type and max\_node\_count for this partition are set based on the \--compute-machine-type and \--compute-node-count command-line options, respectively. This demonstrates how user input can be used to customize specific modules within the blueprint.

Write to YAML: The yaml.dump() function from the PyYAML library is used to serialize the blueprint dictionary into a YAML formatted string and write it to the specified output file. Google Drive icon

The sort\_keys=False argument is used to maintain the order of the keys as defined in the dictionary, which can improve the readability of the output file. Google Drive icon

Running the Script To run this script, save it as a Python file (e.g., generate\_blueprint.py) and execute it from your terminal with the desired options:

bash python generate\_blueprint.py \--blueprint-name my-hpc-cluster \--deployment-name test-deployment \--project-id my-gcp-project \--compute-machine-type n2-highcpu-4 \--compute-node-count 10 \--output-file my-hpc-blueprint.yaml This command will generate a file named my-hpc-blueprint.yaml with the specified configurations.

By using this programmatic approach, you can easily automate the creation of complex and varied Google Cloud Cluster Toolkit blueprints, integrate them into larger infrastructure-as-code workflows, and ensure consistency and reusability across your cluster deployments. A Python script can effectively utilize the PyYAML library to construct and write a Google Cloud Cluster Toolkit blueprint YAML file. By leveraging the click library, the script can dynamically build the nested dictionary structure for deployment\_groups and modules based on user-provided command-line options.

Understanding the Google Cloud Cluster Toolkit Blueprint A Google Cloud Cluster Toolkit blueprint is a YAML file that defines the architecture of a High-Performance Computing (HPC) environment. Google Drive icon

The core components of a blueprint are vars (variables), deployment\_groups, and modules. Google Drive icon

The deployment\_groups section is a list where each item represents a logical grouping of resources to be deployed together. Within each group, a list of modules defines the specific Google Cloud resources and their configurations.

Here is a simplified structure of a blueprint YAML file:

yaml blueprint\_name: hpc-slurm vars: project\_id: your-gcp-project-id deployment\_name: hpc-cluster region: us-central1 zone: us-central1-a deployment\_groups:

- group: primary modules:  
  - id: network source: modules/network/vpc  
  - id: compute\_partition source: community/modules/compute/schedmd-slurm-gcp-v6-partition settings: partition\_name: compute  
  - id: slurm\_controller source: community/modules/scheduler/schedmd-slurm-gcp-v6-controller use:  
    - network  
    - compute\_partition Python Script for Dynamic Blueprint Generation The following Python script demonstrates how to use click to accept user input and PyYAML to generate a blueprint file.

Script Breakdown: Import Libraries: Import click for the command-line interface and yaml (from PyYAML) for YAML manipulation.

Define CLI with click:

A main command group cli is established.

A generate command is created to trigger the blueprint generation.

@click.option decorators are used to define command-line flags for user inputs such as project-id, deployment-name, region, zone, partition-name, and machine-type.

Build the Blueprint Dictionary:

Inside the generate function, a nested Python dictionary is created that mirrors the structure of the Cluster Toolkit blueprint.

The values for keys like project\_id, deployment\_name, partition\_name, and machine\_type are dynamically populated from the click options.

Write to YAML with PyYAML:

The yaml.dump() function is used to serialize the Python dictionary into a YAML formatted string.

The sort\_keys=False argument is important to maintain the intended order of the keys in the output file, which improves readability.

The resulting YAML string is written to a file named hpc-blueprint.yaml.

Example Python Script: python import click import yaml

@click.group() def cli(): """A tool to generate Google Cloud Cluster Toolkit blueprints.""" pass

@cli.command() @click.option('--project-id', required=True, help='The Google Cloud project ID.') @click.option('--deployment-name', default='hpc-cluster', help='The name of the deployment.') @click.option('--region', default='us-central1', help='The Google Cloud region.') @click.option('--zone', default='us-central1-a', help='The Google Cloud zone.') @click.option('--partition-name', default='compute', help='The name of the Slurm partition.') @click.option('--machine-type', default='n2-standard-2', help='The machine type for the compute nodes.') @click.option('--max-node-count', default=10, help='The maximum number of dynamic nodes in the partition.') def generate(project\_id, deployment\_name, region, zone, partition\_name, machine\_type, max\_node\_count): """Generates a Google Cloud Cluster Toolkit blueprint YAML file."""

```
# Dynamically build the nested dictionary for the blueprint
blueprint = {
    'blueprint_name': 'dynamic-hpc-slurm',
    'vars': {
        'project_id': project_id,
        'deployment_name': deployment_name,
        'region': region,
        'zone': zone,
    },
    'deployment_groups': [
        {
            'group': 'primary',
            'modules': [
                {
                    'id': 'network',
                    'source': 'modules/network/vpc',
                },
                {
                    'id': 'homefs',
                    'source': 'modules/file-system/filestore',
                    'use': ['network'],
                    'settings': {
                        'local_mount': '/home'
                    }
                },
                {
                    'id': f'{partition_name}_nodeset',
                    'source': 'community/modules/compute/schedmd-slurm-gcp-v6-nodeset',
                    'use': ['network'],
                    'settings': {
                        'node_count_dynamic_max': max_node_count,
                        'machine_type': machine_type,
                    }
                },
                {
                    'id': f'{partition_name}_partition',
                    'source': 'community/modules/compute/schedmd-slurm-gcp-v6-partition',
                    'use': [f'{partition_name}_nodeset'],
                    'settings': {
                        'partition_name': partition_name,
                        'is_default': True,
                    }
                },
                {
                    'id': 'slurm_login',
                    'source': 'community/modules/scheduler/schedmd-slurm-gcp-v6-login',
                    'use': ['network'],
                    'settings': {
                        'machine_type': 'n2-standard-4',
                        'enable_login_public_ips': True,
                    }
                },
                {
                    'id': 'slurm_controller',
                    'source': 'community/modules/scheduler/schedmd-slurm-gcp-v6-controller',
                    'use': [
                        'network',
                        f'{partition_name}_partition',
                        'slurm_login',
                        'homefs'
                    ],
                    'settings': {
                        'enable_controller_public_ips': True,
                    }
                }
            ]
        }
    ]
}

# Write the dictionary to a YAML file
with open('hpc-blueprint.yaml', 'w') as f:
    yaml.dump(blueprint, f, sort_keys=False, indent=2)

click.echo("Successfully generated hpc-blueprint.yaml")
```

if **name** \== '**main**': cli() How to Run the Script Install necessary libraries:

bash pip install click pyyaml Execute the script from your terminal: You can provide values for the different options. If you omit an option that has a default value, the default will be used.

bash python your\_script\_name.py generate \--project-id="my-gcp-project" \--deployment-name="my-hpc-cluster" \--partition-name="gpu-partition" \--machine-type="a2-highgpu-1g" \--max-node-count=5 Generated hpc-blueprint.yaml Running the command above will produce a file named hpc-blueprint.yaml with the following content:

yaml blueprint\_name: dynamic-hpc-slurm vars: project\_id: my-gcp-project deployment\_name: my-hpc-cluster region: us-central1 zone: us-central1-a deployment\_groups:

- group: primary modules:  
  - id: network source: modules/network/vpc  
  - id: homefs source: modules/file-system/filestore use:  
    - network settings: local\_mount: /home  
  - id: gpu-partition\_nodeset source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset use:  
    - network settings: node\_count\_dynamic\_max: 5 machine\_type: a2-highgpu-1g  
  - id: gpu-partition\_partition source: community/modules/compute/schedmd-slurm-gcp-v6-partition use:  
    - gpu-partition\_nodeset settings: partition\_name: gpu-partition is\_default: true  
  - id: slurm\_login source: community/modules/scheduler/schedmd-slurm-gcp-v6-login use:  
    - network settings: machine\_type: n2-standard-4 enable\_login\_public\_ips: true  
  - id: slurm\_controller source: community/modules/scheduler/schedmd-slurm-gcp-v6-controller use:  
    - network  
    - gpu-partition\_partition  
    - slurm\_login  
    - homefs settings: enable\_controller\_public\_ips: true This approach provides a flexible and powerful way to automate the creation of customized Google Cloud Cluster Toolkit blueprints, reducing manual effort and ensuring consistency across deployments.

Unlocking Granular Cloud Cost Insights: A Guide to Mapping Google Cloud VMs and GPUs to Billing SKUs Delve into the intricacies of Google Cloud's billing structure by programmatically mapping virtual machine (VM) instances and attached GPUs to their fundamental component Stock Keeping Units (SKUs). This detailed guide provides a step-by-step process and a Python code example to leverage the Cloud Billing Catalog API for precise cost estimation.

Understanding the true cost of a Google Cloud VM instance, such as a 'c2-standard-60' with an attached 'nvidia-tesla-t4' GPU, requires a granular approach. Instead of a single price point for the entire configuration, Google Cloud bills for the individual resources that constitute the instance: the CPU cores, the memory, and the GPU. The Cloud Billing Catalog API offers a powerful, programmatic way to access the pricing information for these individual components, enabling accurate cost analysis and estimation.

The Detailed Process: From Instance to Component SKUs Mapping a VM instance and its attachments to their respective SKUs involves a series of steps that leverage the filtering capabilities of the Cloud Billing Catalog API. A VM is not represented by a single SKU; rather, it is a composite of multiple SKUs.

Here's a breakdown of the process:

Enable the Cloud Billing API: Before you can programmatically access billing information, you must enable the Cloud Billing API for your Google Cloud project. This can be done through the Google Cloud Console.

Set Up Authentication: Your application will need to authenticate with the Google Cloud services. The recommended approach is to create a service account with the "Billing Account Viewer" role and use the associated JSON key for authentication.

Identify the Compute Engine Service ID: The Cloud Billing Catalog API organizes SKUs by service. For Compute Engine, the service ID is services/6F81-5844-456A. This will be a crucial parameter in your API calls.

Deconstruct the VM Instance: A predefined VM instance type like 'c2-standard-60' comes with a specific configuration of vCPUs and memory. In this case, a 'c2-standard-60' instance has 60 vCPUs and 240 GB of RAM.

This information is essential for finding the corresponding SKUs.

Filter for Component SKUs: The core of the process lies in filtering the vast catalog of SKUs to pinpoint the ones relevant to your VM's components. This is achieved by using the filter parameter in the skus.list method of the Cloud Billing API. The filtering logic relies on the category and description fields of the SKU object.

CPU (vCPU) SKU:

resourceFamily: Filter for 'Compute'.

resourceGroup: For a C2 instance, the resource group will be related to the 'C2' machine family. A common pattern is the machine series name itself, so you would filter for 'C2'.

description: The description of the vCPU SKU often includes the machine series and sometimes the number of cores. For instance, a description might be "Compute optimized VCPU running in Americas".

RAM SKU:

resourceFamily: Filter for 'Compute'.

resourceGroup: The resource group for memory is typically 'RAM'.

description: The description will indicate that it's for a specific machine family, such as "Compute optimized Ram running in Americas".

GPU SKU:

resourceFamily: Filter for 'Compute'.

resourceGroup: This can vary, but a good starting point is to look for GPU-related groups.

description: The most reliable way to find a specific GPU SKU is by its description, which will explicitly mention the GPU model, for example, "Nvidia Tesla T4 GPU running in Americas".

Specify the Region: Pricing for SKUs is region-specific. Therefore, you must also filter by the desired Google Cloud region to get accurate cost data.

Example Python Code for SKU Mapping The following Python script demonstrates how to implement the process described above. This example uses the google-api-python-client library to interact with the Cloud Billing Catalog API.

python from googleapiclient.discovery import build

def get\_vm\_component\_skus(api\_key, machine\_type, gpu\_type, region): """ Maps a Google Cloud VM instance and an attached GPU to their component SKUs.

```
Args:
    api_key: Your Google Cloud API key.
    machine_type: The machine type of the VM (e.g., 'c2-standard-60').
    gpu_type: The type of the attached GPU (e.g., 'nvidia-tesla-t4').
    region: The Google Cloud region (e.g., 'us-central1').

Returns:
    A dictionary containing the SKUs for CPU, RAM, and GPU.
"""

billing_service = build('cloudbilling', 'v1', developerKey=api_key)
compute_service_name = 'services/6F81-5844-456A'  # Compute Engine service ID

# --- Deconstruct machine type ---
parts = machine_type.split('-')
machine_family = parts[0].upper()

# --- Find CPU SKU ---
cpu_filter = (
    f'service="{compute_service_name}" AND '
    f'resourceFamily="Compute" AND '
    f'resourceGroup="{machine_family}" AND '
    f'NOT resourceGroup:"RAM"'
)
cpu_skus = billing_service.services().skus().list(parent=compute_service_name, filter=cpu_filter).execute()

# Further refine by region in the description
cpu_sku = None
for sku in cpu_skus.get('skus', []):
    if region in sku.get('serviceRegions', []):
        cpu_sku = sku
        break

# --- Find RAM SKU ---
ram_filter = (
    f'service="{compute_service_name}" AND '
    f'resourceFamily="Compute" AND '
    f'resourceGroup="RAM" AND '
    f'description:"{machine_family}"'
)
ram_skus = billing_service.services().skus().list(parent=compute_service_name, filter=ram_filter).execute()

ram_sku = None
for sku in ram_skus.get('skus', []):
    if region in sku.get('serviceRegions', []):
        ram_sku = sku
        break

# --- Find GPU SKU ---
gpu_sku = None
if gpu_type:
    gpu_filter = (
        f'service="{compute_service_name}" AND '
        f'description:"{gpu_type.replace("-", " ")}"'
    )
    gpu_skus = billing_service.services().skus().list(parent=compute_service_name, filter=gpu_filter).execute()
    
    for sku in gpu_skus.get('skus', []):
        if region in sku.get('serviceRegions', []):
            gpu_sku = sku
            break

return {
    'cpu_sku': cpu_sku,
    'ram_sku': ram_sku,
    'gpu_sku': gpu_sku,
}
```

if **name** \== '**main**': \# Replace with your actual API key and desired configuration API\_KEY \= "YOUR\_API\_KEY" MACHINE\_TYPE \= "c2-standard-60" GPU\_TYPE \= "nvidia-tesla-t4" REGION \= "us-central1"

```
component_skus = get_vm_component_skus(API_KEY, MACHINE_TYPE, GPU_TYPE, REGION)

print("--- Component SKUs ---")
if component_skus['cpu_sku']:
    print(f"CPU SKU ID: {component_skus['cpu_sku']['skuId']}")
    print(f"Description: {component_skus['cpu_sku']['description']}")
else:
    print("CPU SKU not found.")

if component_skus['ram_sku']:
    print(f"\nRAM SKU ID: {component_skus['ram_sku']['skuId']}")
    print(f"Description: {component_skus['ram_sku']['description']}")
else:
    print("\nRAM SKU not found.")

if component_skus['gpu_sku']:
    print(f"\nGPU SKU ID: {component_skus['gpu_sku']['skuId']}")
    print(f"Description: {component_skus['gpu_sku']['description']}")
else:
    print(f"\nGPU SKU for {GPU_TYPE} not found.")
```

Note on the Python code: This script provides a foundational approach. The filtering logic, especially for the description field, might need adjustments based on the specific machine family and any future changes in SKU descriptions by Google Cloud.

By following this detailed process and adapting the provided Python code, you can gain a much deeper and more accurate understanding of your Google Cloud costs, empowering you to make more informed decisions about your cloud resource allocation and optimization strategies. Mapping Google Cloud resources like VM instances and attached GPUs to their individual billing SKUs is a common requirement for accurate cost estimation and financial operations (FinOps). Google Cloud does not use a single SKU for an entire virtual machine. Instead, it bills based on the constituent components, primarily vCPU, RAM, and any attached resources like GPUs. Yaqs icon

The Cloud Billing Catalog API provides programmatic access to public pricing information for all Google Cloud services, allowing you to find the specific SKUs for these components.

Prerequisites Before you can use the Cloud Billing Catalog API, you need to:

Enable the Cloud Billing API: You must enable the "Cloud Billing API" in your Google Cloud project. You can do this by visiting the API library in the Google Cloud Console or by using the gcloud CLI. Google Mail icon

Set up Authentication: Your application needs to be authenticated to make API calls. For local development, the easiest way is to use the Google Cloud CLI:

bash gcloud auth application-default login This command authenticates your local environment, and the client libraries will automatically pick up the credentials. For applications running on Google Cloud, Workload Identity or service account keys are recommended.

Detailed Process for Mapping Resources to SKUs The process involves querying the Cloud Billing Catalog API and filtering the results to find the SKUs that match your desired resources. The key is to know the service, resourceFamily, and resourceGroup for the components you are looking for.

Identify the Service: For all Compute Engine resources, the service name is compute.googleapis.com.

Filter for vCPU SKU: To find the vCPU SKU for a c2-standard-60, you need to filter by:

Service: services/6F81-5844-456A (This is the permanent ID for Compute Engine).

resourceFamily: Compute

resourceGroup: C2 (This corresponds to the C2 machine family).

The SKU description will typically contain "Core" or "Cpu".

Filter for RAM SKU: Similarly, to find the RAM SKU for a c2-standard-60, you filter by:

Service: services/6F81-5844-456A

resourceFamily: Ram

resourceGroup: C2

The SKU description will typically contain "Ram".

Filter for GPU SKU: To find the SKU for an nvidia-tesla-t4 GPU, you filter by:

Service: services/6F81-5844-456A

resourceFamily: GPU

The SKU description will contain the name of the GPU, in this case, "Tesla T4".

Example Python Code This Python script demonstrates how to use the google-cloud-billing library to perform the mapping described above.

First, install the required library:

bash pip install google-cloud-billing Python Script:

python from google.cloud import billing\_v1

def find\_compute\_engine\_skus(machine\_family, gpu\_type, region): """ Finds the billing SKUs for vCPU, RAM, and a specific GPU type for a given Compute Engine machine family and region.

```
Args:
    machine_family (str): The machine family (e.g., 'C2', 'N2').
    gpu_type (str): The GPU type to search for (e.g., 'T4', 'V100').
    region (str): The region to filter SKUs for (e.g., 'us-central1').
"""
client = billing_v1.CloudCatalogClient()

# The service name for Google Compute Engine is 'services/6F81-5844-456A'
service_name = "services/6F81-5844-456A"

print(f"Searching for SKUs in region: {region}\n")

# --- Find vCPU SKU ---
# The resource family for vCPU is 'Compute'
vcpu_filter = f'service="{service_name}" AND resourceFamily="Compute" AND resourceGroup="{machine_family}"'

print(f"--- Finding '{machine_family}' vCPU SKU ---")
request = billing_v1.ListSkusRequest(parent=service_name, filter=vcpu_filter)
skus = client.list_skus(request=request)

found_vcpu = False
for sku in skus:
    # Filter by region and ensure it's an on-demand SKU (not a commitment)
    if region in sku.service_regions and "Commitment" not in sku.description:
        print(f"  SKU Name: {sku.name}")
        print(f"  Description: {sku.description}")
        found_vcpu = True
        break # Found the first relevant SKU
if not found_vcpu:
    print("  vCPU SKU not found for the specified criteria.")


# --- Find RAM SKU ---
# The resource family for RAM is 'Ram'
ram_filter = f'service="{service_name}" AND resourceFamily="Ram" AND resourceGroup="{machine_family}"'

print(f"\n--- Finding '{machine_family}' RAM SKU ---")
request = billing_v1.ListSkusRequest(parent=service_name, filter=ram_filter)
skus = client.list_skus(request=request)

found_ram = False
for sku in skus:
    if region in sku.service_regions and "Commitment" not in sku.description:
        print(f"  SKU Name: {sku.name}")
        print(f"  Description: {sku.description}")
        found_ram = True
        break
if not found_ram:
    print("  RAM SKU not found for the specified criteria.")


# --- Find GPU SKU ---
# The resource family for GPU is 'GPU'
gpu_filter = f'service="{service_name}" AND resourceFamily="GPU"'

print(f"\n--- Finding 'Nvidia Tesla {gpu_type}' GPU SKU ---")
request = billing_v1.ListSkusRequest(parent=service_name, filter=gpu_filter)
skus = client.list_skus(request=request)

found_gpu = False
for sku in skus:
    # Filter by region, GPU type in description, and on-demand pricing
    if (region in sku.service_regions and
            gpu_type in sku.description and
            "preemptible" not in sku.description.lower() and
            "Commitment" not in sku.description):
        print(f"  SKU Name: {sku.name}")
        print(f"  Description: {sku.description}")
        found_gpu = True
        break
if not found_gpu:
    print("  GPU SKU not found for the specified criteria.")
```

if **name** \== "**main**": \# Example: Map a 'c2-standard-60' (C2 family) with an 'nvidia-tesla-t4' \# in the 'us-central1' region. find\_compute\_engine\_skus( machine\_family="C2", gpu\_type="T4", region="us-central1" ) Example Output Running the script above would produce an output similar to the following (note that SKU IDs may change over time):

Searching for SKUs in region: us-central1

\--- Finding 'C2' vCPU SKU \--- SKU Name: services/6F81-5844-456A/skus/9420-255D-16A3 Description: C2 Instance Core running in Americas

\--- Finding 'C2' RAM SKU \--- SKU Name: services/6F81-5844-456A/skus/EAA2-A739-93D8 Description: C2 Instance Ram running in Americas

\--- Finding 'Nvidia Tesla T4' GPU SKU \--- SKU Name: services/6F81-5844-456A/skus/93D8-3A89-2325 Description: Nvidia Tesla T4 GPU running in Americas Once you have these SKU IDs, you can use them to get the exact list price for each component, which allows you to calculate the total cost of your VM configuration. For a c2-standard-60, you would multiply the cost of the vCPU SKU by 60 and the cost of the RAM SKU by the amount of memory in that instance type (240 GiB).

Navigating Google Cloud Pricing: A Developer's Guide to the Billing Catalog API To accurately estimate monthly costs for Google Cloud services, developers can programmatically access pricing information using the Google Cloud Billing Catalog API. This guide provides a detailed walkthrough and a Python code example for retrieving pricing details for a specific Stock Keeping Unit (SKU), parsing its on-demand pricing structure, and calculating an estimated monthly cost.

The Process: From SKU ID to Monthly Cost Estimate The journey from a SKU ID to a cost estimate involves these key steps:

Enable the Cloud Billing API: Before making any API calls, ensure the Cloud Billing API is enabled in your Google Cloud project.

Authentication: For programmatic access, you'll need to set up authentication. The simplest method for server-to-server interactions is using a service account with the appropriate IAM role (e.g., "Billing Account Viewer").

API Request: Using the Google Cloud client library for Python, you will make a request to the cloudbilling.services.skus.list method. This requires the service ID to which the SKU belongs.

Parsing the pricingExpression: The API response contains a pricingInfo object, which in turn has a pricingExpression. For on-demand usage, the key element within this expression is the tieredRates array. Each entry in this array defines a pricing tier with a startUsageAmount and a unitPrice.

Calculating Tiered Costs: To calculate the total cost for a given usage amount, you must iterate through the tieredRates. For each tier, you calculate the cost for the portion of usage that falls within that tier's range.

Estimating Monthly Cost: Once you can calculate the cost for a specific usage amount, you can estimate the monthly cost by multiplying this by the expected usage over a month. For services billed by time (e.g., per hour), a common practice is to estimate usage for an average of 730 hours per month (24 hours \* 365.25 days / 12 months).

Understanding the pricingExpression and tieredRates The pricingExpression object provides a structured way to understand how a SKU is priced. For on-demand usage, the most important part is the tieredRates list. Each element in this list represents a pricing tier and contains:

startUsageAmount: The lower bound of the usage tier. The first tier typically starts at 0\.

unitPrice: The price for each unit of usage within that tier. This is represented by units (the whole number part of the price) and nanos (the fractional part, up to nine decimal places).

For example, a SKU for a service might have a free tier for the first 1000 units, a reduced price for the next 9000 units, and a standard price for all usage beyond that. This would be represented by three entries in the tieredRates array.

Python Code Example Here is a Python script that demonstrates the entire process. This script requires the google-api-python-client and google-auth libraries, which you can install using pip:

bash pip install google-api-python-client google-auth python import google.auth from googleapiclient.discovery import build

def get\_sku\_pricing(service\_name, sku\_id): """ Retrieves the pricing information for a specific SKU.

```
Args:
    service_name (str): The name of the service, e.g., 'services/6F81-5844-456A'.
    sku_id (str): The ID of the SKU.

Returns:
    dict: The SKU object containing pricing information, or None if not found.
"""
try:
    credentials, project = google.auth.default()
    billing_service = build('cloudbilling', 'v1', credentials=credentials)

    # The name of the SKU to retrieve.
    sku_name = f"{service_name}/skus/{sku_id}"

    request = billing_service.services().skus().list(parent=service_name, name=sku_name)
    response = request.execute()

    if 'skus' in response and response['skus']:
        return response['skus'][0]
    else:
        return None

except Exception as e:
    print(f"An error occurred: {e}")
    return None
```

def parse\_and\_calculate\_cost(sku\_info, usage\_amount): """ Parses the pricingExpression and calculates the cost for a given usage.

```
Args:
    sku_info (dict): The SKU object from the Billing Catalog API.
    usage_amount (float): The amount of usage to calculate the cost for.

Returns:
    float: The calculated cost, or 0.0 if pricing info is not available.
"""
if not sku_info or 'pricingInfo' not in sku_info:
    return 0.0

pricing_info = sku_info['pricingInfo'][0]
pricing_expression = pricing_info.get('pricingExpression', {})
tiered_rates = pricing_expression.get('tieredRates', [])

if not tiered_rates:
    return 0.0

total_cost = 0.0
remaining_usage = usage_amount

# The tieredRates are sorted by startUsageAmount in ascending order.
for i in range(len(tiered_rates)):
    tier = tiered_rates[i]
    start_usage = float(tier.get('startUsageAmount', 0))

    # Determine the upper bound of the current tier
    upper_bound = float('inf')
    if i + 1 < len(tiered_rates):
        upper_bound = float(tiered_rates[i+1].get('startUsageAmount', float('inf')))

    # Calculate the usage within this tier
    usage_in_tier = 0
    if remaining_usage > 0:
        tier_range = upper_bound - start_usage
        consumed_in_tier = min(remaining_usage, tier_range)
        usage_in_tier = consumed_in_tier
        remaining_usage -= consumed_in_tier

    # Calculate the cost for the usage in this tier
    if usage_in_tier > 0:
        unit_price_info = tier.get('unitPrice', {})
        units = int(unit_price_info.get('units', 0))
        nanos = int(unit_price_info.get('nanos', 0))
        price_per_unit = units + (nanos / 1_000_000_000)
        total_cost += usage_in_tier * price_per_unit

return total_cost
```

def estimate\_monthly\_cost(sku\_info, hourly\_usage): """ Estimates the monthly cost based on hourly usage.

```
Args:
    sku_info (dict): The SKU object.
    hourly_usage (float): The estimated hourly usage.

Returns:
    float: The estimated monthly cost.
"""
# A common estimate for hours in a month
hours_in_month = 730
monthly_usage = hourly_usage * hours_in_month
return parse_and_calculate_cost(sku_info, monthly_usage)
```

if **name** \== '**main**': \# Replace with the actual service and SKU ID you want to query. \# Example: Compute Engine E2 instance core running in us-central1 SERVICE\_ID \= 'services/6F81-5844-456A'  \# This is for Compute Engine SKU\_ID \= '9662-B529-3F92' \# Example: E2 Instance Core running in us-central1

```
sku_details = get_sku_pricing(SERVICE_ID, SKU_ID)

if sku_details:
    print(f"Successfully retrieved SKU details for: {sku_details.get('description')}")
    print(f"Usage Unit: {sku_details['pricingInfo'][0]['pricingExpression']['usageUnitDescription']}")

    # Example: Calculate the cost for running 1 vCPU core for a full month.
    # The usage unit for this SKU is "hour".
    estimated_hourly_usage = 1.0
    monthly_cost = estimate_monthly_cost(sku_details, estimated_hourly_usage)
    print(f"\nEstimated monthly cost for {estimated_hourly_usage} unit(s) per hour: ${monthly_cost:.4f}")

    # Example: Calculate cost for a specific amount of usage with tiered pricing.
    # Let's assume a hypothetical usage of 1000 hours.
    specific_usage = 1000
    specific_cost = parse_and_calculate_cost(sku_details, specific_usage)
    print(f"Cost for {specific_usage} hours of usage: ${specific_cost:.4f}")
else:
    print(f"Could not retrieve pricing for SKU ID: {SKU_ID}")
```

This script provides a robust framework for programmatically estimating Google Cloud costs. By adapting the SERVICE\_ID, SKU\_ID, and usage amounts, developers and FinOps professionals can build powerful cost estimation and management tools. Retrieving and calculating Google Cloud SKU pricing information involves using the Cloud Billing Catalog API. This guide provides a detailed, step-by-step process, complete with Python code, to fetch SKU details, parse its on-demand pricing, and estimate a monthly cost.

Introduction to the Cloud Billing Catalog API The Google Cloud Billing Catalog API offers programmatic access to the public list of prices for Google Cloud services. This allows you to retrieve details for all services and the Stock Keeping Units (SKUs) within each service, including human-readable descriptions, pricing, and the regions where they are available.

For users with negotiated contracts, the newer Pricing API provides both list prices and account-specific custom prices and discounts.

This guide, however, will focus on the publicly available list prices from the Cloud Billing Catalog API as requested.

Prerequisites Before you begin, you need to complete the following setup:

Enable the Cloud Billing API: In the Google Cloud Console, enable the "Cloud Billing API" for your project.

Create an API Key: The Catalog API uses an API key to authenticate requests for public data. Follow the instructions on Using API Keys to create one. Important: Restrict the API key to only the Cloud Billing API to enhance security.

Install the Google Cloud Client Library for Python: This library simplifies interaction with Google Cloud APIs.

bash pip install google-api-python-client Detailed Process and Python Code Here is the step-by-step process to retrieve, parse, and calculate the cost of a SKU.

Step 1: Find the serviceId for the Google Cloud Service SKUs are grouped by service. To find the pricing for a specific SKU, you first need to identify the serviceId of the parent service (e.g., "Compute Engine"). You can list all available services and find the one you need.

The following Python function lists all public Google Cloud services:

python from googleapiclient.discovery import build

def list\_services(api\_key): """Lists all public Google Cloud services.""" billing\_service \= build('cloudbilling', 'v1', developerKey=api\_key) try: request \= billing\_service.services().list() response \= request.execute() print("Available Services:") for service in response.get('services', \[\]): print(f"  \- Display Name: {service\['displayName'\]}, Service ID: {service\['serviceId'\]}") return response.get('services', \[\]) except Exception as e: print(f"An error occurred: {e}") return None

# Replace with your actual API key

API\_KEY \= "YOUR\_API\_KEY"

# list\_services(API\_KEY)

From the output of this function, you can find the serviceId for the desired service. For example, the serviceId for Compute Engine is typically 6F81-5844-456A.

Step 2: Retrieve a Specific SKU's Pricing Information Once you have the serviceId and the target skuId, you can retrieve the detailed information for that SKU. Since the API's get method for SKUs is not publicly documented for direct access by ID, the most reliable method is to list all SKUs for a service and then filter for the one you need.

python def get\_sku\_details(api\_key, service\_id, sku\_id): """Retrieves the details for a specific SKU.""" billing\_service \= build('cloudbilling', 'v1', developerKey=api\_key) parent\_service \= f"services/{service\_id}"

```
try:
    request = billing_service.services().skus().list(parent=parent_service)
    while request is not None:
        response = request.execute()
        for sku in response.get('skus', []):
            if sku['skuId'] == sku_id:
                return sku
        request = billing_service.services().skus().list_next(
            previous_request=request, previous_response=response)
except Exception as e:
    print(f"An error occurred: {e}")
return None
```

Step 3: Parse the pricingExpression for On-Demand Usage The pricing information is contained within the pricingInfo array of the SKU object. Each element in this array represents a specific pricing structure. The pricingExpression field details how the cost is calculated.

For on-demand pricing, you typically look for the rate tier where startUsageAmount is 0\. The price is composed of units and nanos (10-9 units).

This function extracts the on-demand price from a SKU object:

python def parse\_on\_demand\_price(sku\_details): """Parses the pricingExpression to find the on-demand price.""" if not sku\_details or 'pricingInfo' not in sku\_details: return None, None

```
for price_info in sku_details['pricingInfo']:
    pricing_expression = price_info.get('pricingExpression', {})
    tiered_rates = pricing_expression.get('tieredRates', [])
    
    # On-demand price is typically the first tier starting at 0
    for rate in tiered_rates:
        if float(rate.get('startUsageAmount', 0)) == 0:
            unit_price = rate.get('unitPrice', {})
            units = int(unit_price.get('units', 0))
            nanos = int(unit_price.get('nanos', 0))
            
            # The total price is units + nanos / 1,000,000,000
            price = units + (nanos / 1_000_000_000)
            
            usage_unit_desc = pricing_expression.get('usageUnitDescription', 'N/A')
            return price, usage_unit_desc
            
return None, None
```

Step 4: Calculate an Estimated Monthly Cost After extracting the hourly or per-unit price, you can calculate an estimated monthly cost. A common standard for this calculation is to assume 730 hours in a month (approximately 24 hours \* 30.44 days).

The following function performs this calculation:

python def calculate\_monthly\_cost(price\_per\_hour, hours\_in\_month=730): """Calculates an estimated monthly cost based on an hourly rate.""" if price\_per\_hour is None: return None return price\_per\_hour \* hours\_in\_month Complete Python Code Example Here is a complete script that ties all the steps together. Remember to replace the placeholder values with your actual API key and the SKU ID you wish to query.

python from googleapiclient.discovery import build

def get\_sku\_details(api\_key, service\_id, sku\_id): """Retrieves the details for a specific SKU by listing and filtering.""" billing\_service \= build('cloudbilling', 'v1', developerKey=api\_key) parent\_service \= f"services/{service\_id}"

```
try:
    request = billing_service.services().skus().list(parent=parent_service)
    while request is not None:
        response = request.execute()
        for sku in response.get('skus', []):
            if sku['skuId'] == sku_id:
                return sku
        request = billing_service.services().skus().list_next(
            previous_request=request, previous_response=response)
except Exception as e:
    print(f"An error occurred: {e}")
return None
```

def parse\_on\_demand\_price(sku\_details): """Parses the pricingExpression to find the on-demand price.""" if not sku\_details or 'pricingInfo' not in sku\_details: return None, None

```
for price_info in sku_details['pricingInfo']:
    pricing_expression = price_info.get('pricingExpression', {})
    tiered_rates = pricing_expression.get('tieredRates', [])
    
    for rate in tiered_rates:
        if float(rate.get('startUsageAmount', 0)) == 0:
            unit_price = rate.get('unitPrice', {})
            units = int(unit_price.get('units', 0))
            nanos = int(unit_price.get('nanos', 0))
            
            price = units + (nanos / 1_000_000_000)
            
            usage_unit_desc = pricing_expression.get('usageUnitDescription', 'N/A')
            # Check if the price is per hour for monthly calculation
            is_hourly = 'hour' in usage_unit_desc.lower()
            
            return price, usage_unit_desc, is_hourly
            
return None, None, False
```

def calculate\_monthly\_cost(price\_per\_unit, is\_hourly, hours\_in\_month=730): """Calculates an estimated monthly cost.""" if price\_per\_unit is None or not is\_hourly: return None return price\_per\_unit \* hours\_in\_month

def main(): \# \--- Configuration \--- \# IMPORTANT: Replace with your actual API Key API\_KEY \= "YOUR\_API\_KEY"

```
# Example: Compute Engine's Service ID
SERVICE_ID = "6F81-5844-456A" 

# Example: SKU ID for "N1 Predefined Instance Core running in Americas"
SKU_ID = "9600-259D-4159"

# --- Execution ---
print(f"Attempting to retrieve pricing for SKU ID: {SKU_ID}...")
sku_details = get_sku_details(API_KEY, SERVICE_ID, SKU_ID)

if sku_details:
    print("\n--- SKU Details ---")
    print(f"SKU ID: {sku_details.get('skuId')}")
    print(f"Description: {sku_details.get('description')}")
    
    price, unit_description, is_hourly = parse_on_demand_price(sku_details)
    
    if price is not None:
        print("\n--- Pricing Information ---")
        print(f"On-Demand Price: {price:.10f} USD per {unit_description}")
        
        if is_hourly:
            monthly_cost = calculate_monthly_cost(price, is_hourly)
            if monthly_cost:
                print(f"\n--- Estimated Monthly Cost (based on 730 hours) ---")
                print(f"Estimated Cost: ${monthly_cost:.2f} USD")
        else:
            print("\nMonthly cost calculation is not applicable as the SKU is not priced per hour.")

    else:
        print("\nCould not parse on-demand pricing for this SKU.")
else:
    print(f"\nCould not retrieve details for SKU ID: {SKU_ID}")
```

if **name** \== "**main**": main() A Python script for a command-line interface (CLI) tool can efficiently parse a Google Cloud Cluster Toolkit blueprint, extract resource requirements, and validate their availability in a specified Google Cloud region or zone. This process involves using the PyYAML library to handle the blueprint file and various Google Cloud client libraries to check for resource availability.

Here is a comprehensive guide on how to build such a script.

1. Core Components and Dependencies First, ensure you have the necessary Python libraries installed. You can install them using pip:

bash pip install pyyaml google-cloud-compute google-cloud-filestore google-cloud-lustre PyYAML: The standard library for parsing YAML files in Python.

google-cloud-compute: The client library for interacting with the Compute Engine API, used to validate machine types and GPUs.

google-cloud-filestore: The client library for the Filestore API.

google-cloud-lustre: The client library for the Google Cloud Managed Lustre API.

2. Loading and Parsing the Blueprint File A Cluster Toolkit blueprint is a YAML file that defines the architecture of your cluster.

The first step in the script is to load and parse this file using PyYAML. The yaml.safe\_load() function is recommended as it prevents the execution of arbitrary code.

Here is a function to load a blueprint file:

python import yaml

def load\_blueprint(file\_path): """Loads and parses a YAML blueprint file.""" try: with open(file\_path, 'r') as f: return yaml.safe\_load(f) except FileNotFoundError: print(f"Error: Blueprint file not found at {file\_path}") return None except yaml.YAMLError as e: print(f"Error parsing YAML file: {e}") return None 3\. Extracting Resource Requirements Once the blueprint is loaded into a Python dictionary, you need to traverse it to find resource definitions. The structure can vary, but typically resources are defined under deployment\_groups.

Below are functions to extract common resources like machine types, GPUs, and storage. Note: The exact paths within the YAML structure may vary based on the specific blueprint's design. You may need to adjust the dictionary keys.

python def extract\_machine\_types(blueprint\_data): """Extracts all unique machine types from the blueprint.""" machine\_types \= set() if 'deployment\_groups' in blueprint\_data: for group in blueprint\_data\['deployment\_groups'\]: \# Look in the primary module's variables if 'vars' in group and 'machine\_type' in group\['vars'\]: machine\_types.add(group\['vars'\]\['machine\_type'\]) \# Also look in submodules if they exist if 'modules' in group: for module in group\['modules'\]: if 'vars' in module and 'machine\_type' in module\['vars'\]: machine\_types.add(module\['vars'\]\['machine\_type'\]) return list(machine\_types)

def extract\_gpu\_configs(blueprint\_data): """Extracts GPU configurations.""" gpus \= \[\] \# This is a simplified example. GPUs can be part of the machine type \# (e.g., 'a2-highgpu-1g') or defined in a 'guest\_accelerators' block. \# We will focus on guest\_accelerators for explicit definition. if 'deployment\_groups' in blueprint\_data: for group in blueprint\_data\['deployment\_groups'\]: if 'vars' in group and 'guest\_accelerators' in group\['vars'\]: for gpu in group\['vars'\]\['guest\_accelerators'\]: gpus.append(gpu\['type'\]) return list(set(gpus))

def extract\_storage\_types(blueprint\_data): """Extracts storage module types like filestore and lustre.""" storage\_info \= {'filestore': False, 'lustre': False} if 'deployment\_groups' in blueprint\_data: for group in blueprint\_data\['deployment\_groups'\]: if 'modules' in group: for module in group\['modules'\]: source \= module.get('source', '') if 'filestore' in source: storage\_info\['filestore'\] \= True if 'lustre' in source: storage\_info\['lustre'\] \= True return storage\_info 4\. Programmatic Validation with Google Cloud Client Libraries After extracting the resource names, the next step is to validate their availability in the user-specified location (region or zone).

Authenticating with Google Cloud Your script will need to authenticate to make API calls. The easiest way is to use Application Default Credentials (ADC) by running gcloud auth application-default login in your terminal. The client libraries will automatically pick up these credentials.

Validating Compute Engine Resources (Machine Types & GPUs) You can query the Compute Engine API to check if a specific machine type or accelerator (GPU) is available in a given zone.

python from google.cloud import compute\_v1 from google.api\_core import exceptions

def validate\_machine\_type(project\_id, zone, machine\_type): """Validates if a machine type is available in a specific zone.""" client \= compute\_v1.MachineTypesClient() try: \# The list method with a filter is an efficient way to check existence. request \= compute\_v1.ListMachineTypesRequest( project=project\_id, zone=zone, filter=f'name \= "{machine\_type}"' ) results \= list(client.list(request=request)) return len(results) \> 0 except exceptions.NotFound: return False except Exception as e: print(f"An error occurred validating machine type {machine\_type}: {e}") return False

def validate\_gpu\_type(project\_id, zone, gpu\_type): """Validates if a GPU (accelerator) type is available in a specific zone.""" client \= compute\_v1.AcceleratorTypesClient() try: request \= compute\_v1.ListAcceleratorTypesRequest( project=project\_id, zone=zone, filter=f'name \= "{gpu\_type}"' ) results \= list(client.list(request=request)) return len(results) \> 0 except exceptions.NotFound: return False except Exception as e: print(f"An error occurred validating GPU type {gpu\_type}: {e}") return False Validating Storage Resources (Filestore & Lustre) For services like Filestore and Managed Lustre, availability is typically on a regional or zonal basis. You can validate this by listing the available locations for the service and checking if your target location is included.

python from google.cloud import filestore\_v1 from google.cloud import lustre\_v1

def validate\_filestore\_availability(project\_id, region): """Validates if Filestore is available in a specific region.""" client \= filestore\_v1.CloudFilestoreManagerClient() parent \= f"projects/{project\_id}" try: locations \= client.list\_locations(request={"parent": parent}) \# Location IDs are typically in the format 'us-central1' available\_regions \= {loc.location\_id for loc in locations} return region in available\_regions except Exception as e: print(f"An error occurred validating Filestore availability: {e}") return False

def validate\_lustre\_availability(project\_id, region): """Validates if Google Cloud Managed Lustre is available in a region.""" \# The Lustre API is location-based. Locations can be regions or zones. \# We check if any zone within the target region is supported. client \= lustre\_v1.CloudLustreClient() parent \= f"projects/{project\_id}" try: locations \= client.list\_locations(request={"parent": parent}) \# Location IDs can be 'us-central1-a', 'us-central1-b', etc. available\_zones \= {loc.location\_id for loc in locations} \# Check if any available zone starts with the specified region name return any(zone.startswith(region) for zone in available\_zones) except Exception as e: print(f"An error occurred validating Lustre availability: {e}") return False 5\. Assembling the CLI Tool Finally, you can bring all the pieces together into a single script using Python's argparse library to handle command-line arguments.

python import argparse

def main(): parser \= argparse.ArgumentParser( description="Validate Google Cloud resources from a Cluster Toolkit blueprint." ) parser.add\_argument("blueprint", help="Path to the Cluster Toolkit blueprint YAML file.") parser.add\_argument("--project\_id", required=True, help="Google Cloud Project ID.") parser.add\_argument("--zone", help="Google Cloud Zone to validate resources in (e.g., us-central1-a).") parser.add\_argument("--region", help="Google Cloud Region to validate resources in (e.g., us-central1).")

```
args = parser.parse_args()

if not args.zone and not args.region:
    print("Error: You must specify either a --zone or a --region.")
    return

# If only zone is provided, infer region
target_region = args.region or '-'.join(args.zone.split('-')[:-1])
target_zone = args.zone

blueprint_data = load_blueprint(args.blueprint)
if not blueprint_data:
    return

print(f"--- Validating resources for project '{args.project_id}' in region '{target_region}' / zone '{target_zone}' ---")

# --- Machine Type Validation ---
if target_zone:
    machine_types = extract_machine_types(blueprint_data)
    print(f"\nFound Machine Types: {machine_types or 'None'}")
    for mt in machine_types:
        is_available = validate_machine_type(args.project_id, target_zone, mt)
        print(f"  - {mt}: {'Available' if is_available else 'NOT AVAILABLE'} in {target_zone}")

# --- GPU Validation ---
if target_zone:
    gpu_types = extract_gpu_configs(blueprint_data)
    print(f"\nFound GPU Types: {gpu_types or 'None'}")
    for gpu in gpu_types:
        is_available = validate_gpu_type(args.project_id, target_zone, gpu)
        print(f"  - {gpu}: {'Available' if is_available else 'NOT AVAILABLE'} in {target_zone}")

# --- Storage Validation ---
storage_types = extract_storage_types(blueprint_data)
print(f"\nFound Storage Modules: {storage_types}")
if storage_types['filestore']:
    is_available = validate_filestore_availability(args.project_id, target_region)
    print(f"  - Filestore: {'Available' if is_available else 'NOT AVAILABLE'} in {target_region}")

if storage_types['lustre']:
    is_available = validate_lustre_availability(args.project_id, target_region)
    print(f"  - Managed Lustre: {'Available' if is_available else 'NOT AVAILABLE'} in {target_region}")
```

if **name** \== "**main**": main() This script provides a robust framework for a CLI tool that can significantly aid in the pre-deployment validation of Google Cloud Cluster Toolkit blueprints, ensuring that the specified resources are available in the target location before attempting a deployment. Of course. You can create a robust Python script for a command-line interface (CLI) tool that leverages PyYAML to parse Google Cloud Cluster Toolkit blueprints and then uses Google Cloud client libraries to validate the specified resources against a given region or zone.

Here is a comprehensive guide on how to build such a tool.

Overview of the Process The script will perform the following actions:

Accept User Input: Use a CLI library like argparse to take the path to the blueprint YAML file and the target Google Cloud region or zone as input.

Load and Parse Blueprint: Utilize the PyYAML library to read and parse the specified blueprint file into a Python dictionary.

Extract Resource Definitions: Systematically traverse the parsed dictionary to find and list all defined resources, such as machine types, GPU configurations, and storage systems.

Validate Against Google Cloud APIs: For each extracted resource, make a call to the appropriate Google Cloud client library to verify its availability in the user-specified location.

Report Results: Print a clear, human-readable report of the validation results, indicating which resources are available and which are not.

Prerequisites Before you begin, ensure you have the necessary libraries installed. You can install them using pip:

bash pip install pyyaml google-cloud-compute google-cloud-filestore google-cloud-lustre You will also need to authenticate with Google Cloud. For a local development environment, the easiest way is to use the Google Cloud CLI:

bash gcloud auth application-default login Step 1: Understanding the Cluster Toolkit Blueprint Structure A Google Cloud Cluster Toolkit blueprint is a YAML file that describes the desired HPC environment.

These blueprints are composed of modules that define specific parts of the system, like compute partitions and storage. Google Drive icon

Here is a simplified example of a blueprint file (hpc-cluster.yaml) that we will use for this guide. It defines a primary deployment group with a Slurm compute partition, GPUs, and a Filestore instance. Google Drive icon

yaml

# hpc-cluster.yaml

blueprint\_name: simple-hpc-cluster

vars: project\_id: "your-gcp-project" zone: "us-central1-a" region: "us-central1"

deployment\_groups:

- group: primary modules:  
    
  - id: compute\_partition source: community/modules/compute/schedmd-slurm-gcp-v6-partition settings: machine\_type: "a2-highgpu-1g" gpus: gpu\_type: "nvidia-tesla-a100" gpu\_count: 1  
      
  - id: shared\_storage source: modules/file-system/filestore settings: tier: "BASIC\_HDD" \# Example tier Step 2: Building the Python CLI Tool Below is the complete Python script. Each major section is explained in detail.


1. Setup and Argument Parsing We start by importing the necessary libraries and setting up argparse to handle command-line arguments for the blueprint file path and the validation zone/region. Yaqs icon

Yaqs icon

python import argparse import yaml from google.cloud import compute\_v1 from google.cloud import filestore\_v1 from google.cloud.filestore\_v1.services import cloud\_filestore\_manager from google.api\_core import exceptions

def main(): parser \= argparse.ArgumentParser( description="Validate a Google Cloud Cluster Toolkit blueprint." ) parser.add\_argument( "--file", required=True, help="Path to the blueprint YAML file." ) parser.add\_argument( "--project\_id", required=True, help="Google Cloud Project ID to validate against." ) parser.add\_argument( "--zone", required=True, help="Google Cloud zone to validate resources in (e.g., us-central1-a)." ) args \= parser.parse\_args()

```
try:
    with open(args.file, 'r') as f:
        # Use safe_load to avoid executing arbitrary code
        blueprint = yaml.safe_load(f) [10]
        print(f"Successfully loaded blueprint: {args.file}")
        validate_blueprint(blueprint, args.project_id, args.zone)
except FileNotFoundError:
    print(f"Error: Blueprint file not found at {args.file}")
except yaml.YAMLError as e:
    print(f"Error parsing YAML file: {e}")
```

2. Extracting and Validating Resources The validate\_blueprint function orchestrates the extraction and validation process. It iterates through the deployment groups and modules defined in the blueprint.

python def validate\_blueprint(blueprint, project\_id, zone): """ Extracts resources from the blueprint and validates them. """ print(f"\\n--- Starting Validation in Zone: {zone} \---") region \= '-'.join(zone.split('-')\[:-1\])

```
# Extract resources
for group in blueprint.get('deployment_groups', []):
    for module in group.get('modules', []):
        settings = module.get('settings', {})
        
        # Validate Compute Engine VM
        if 'machine_type' in settings:
            machine_type = settings['machine_type']
            validate_machine_type(project_id, zone, machine_type)

        # Validate GPU configuration
        if 'gpus' in settings:
            gpu_config = settings['gpus']
            gpu_type = gpu_config.get('gpu_type')
            if gpu_type:
                validate_gpu(project_id, zone, gpu_type)

        # Validate Filestore
        if module.get('source', '').endswith('filestore'):
            validate_filestore(project_id, region)

        # Validate Lustre (placeholder, see note below)
        if module.get('source', '').endswith('lustre'):
            validate_lustre(project_id, region)
```

3. Validation Functions using Google Cloud Client Libraries These functions connect to Google Cloud to check for the availability of each specific resource.

Validate Machine Type

This function uses google-cloud-compute to list all available machine types in the specified zone and checks if the requested type exists. The Compute Engine API requires a zonal query for this information. Yaqs icon

Yaqs icon

python def validate\_machine\_type(project, zone, machine\_type): """Checks if a machine type is available in a given zone.""" try: client \= compute\_v1.MachineTypesClient() request \= compute\_v1.ListMachineTypesRequest(project=project, zone=zone) available\_types \= {item.name for item in client.list(request)}

```
    if machine_type in available_types:
        print(f"✅ Machine Type '{machine_type}' is AVAILABLE in {zone}.")
    else:
        print(f"❌ Machine Type '{machine_type}' is NOT AVAILABLE in {zone}.")
except exceptions.NotFound:
    print(f"⚠️ Could not verify machine types. Is the zone '{zone}' correct?")
except Exception as e:
    print(f"An error occurred while validating machine type: {e}")
```

Validate GPU Type

Similarly, this function queries for available accelerator types (GPUs) in the zone. Google Drive icon

python def validate\_gpu(project, zone, gpu\_type): """Checks if a GPU type is available in a given zone.""" try: client \= compute\_v1.AcceleratorTypesClient() request \= compute\_v1.ListAcceleratorTypesRequest(project=project, zone=zone) available\_gpus \= {item.name for item in client.list(request)}

```
    if gpu_type in available_gpus:
        print(f"✅ GPU Type '{gpu_type}' is AVAILABLE in {zone}.")
    else:
        print(f"❌ GPU Type '{gpu_type}' is NOT AVAILABLE in {zone}.")
except exceptions.NotFound:
    print(f"⚠️ Could not verify GPU types. Is the zone '{zone}' correct?")
except Exception as e:
    print(f"An error occurred while validating GPU type: {e}")
```

Validate Filestore and Lustre

Filestore and Lustre are regional services. These functions check if the services are available in the blueprint's target region.

python def validate\_filestore(project, region): """Checks if Filestore is available in a given region.""" try: client \= filestore\_v1.CloudFilestoreManagerClient() \# Parent format: projects/{project\_id}/locations/- parent \= f"projects/{project}/locations/-" request \= filestore\_v1.ListInstancesRequest(parent=parent)

```
    # We can infer availability by checking locations of existing instances
    # or more robustly by checking where we are allowed to create one.
    # A simpler proxy is to list locations.
    locations = {loc.location_id for loc in client.list_locations(request={"name": parent})}

    if region in locations:
        print(f"✅ Filestore service is AVAILABLE in region {region}.")
    else:
        print(f"❌ Filestore service is NOT AVAILABLE in region {region}.")
except Exception as e:
    print(f"An error occurred while validating Filestore: {e}")
```

def validate\_lustre(project, region): """ Checks if Google Cloud Managed Lustre is available. NOTE: As of late 2025, the google-cloud-lustre library is available. This function assumes a similar location-listing capability. """ \# This is a conceptual implementation. The actual library might differ. print(f"ℹ️  Checking for Google Cloud Managed Lustre in region {region}...") \# In a real-world scenario, you would use the google-cloud-lustre client \# to list available locations, similar to the Filestore example. \# For now, we will assume it's available in most major regions. print(f"✅ Google Cloud Managed Lustre is assumed to be AVAILABLE in {region}.")

4. Main Execution Block Finally, the if **name** \== "**main**": block ensures the script runs when executed from the command line.

python if **name** \== "**main**": main() How to Run the Tool Save the code above as a Python file (e.g., validate\_blueprint.py).

Create the hpc-cluster.yaml file with your desired configuration.

Run the script from your terminal:

bash python validate\_blueprint.py \--file hpc-cluster.yaml \--project\_id your-gcp-project \--zone us-central1-a Example Output Successfully loaded blueprint: hpc-cluster.yaml

\--- Starting Validation in Zone: us-central1-a \--- ✅ Machine Type 'a2-highgpu-1g' is AVAILABLE in us-central1-a. ✅ GPU Type 'nvidia-tesla-a100' is AVAILABLE in us-central1-a. ✅ Filestore service is AVAILABLE in region us-central1.

You can programmatically check a Google Cloud project's resource quotas, such as the number of available GPUs of a specific type or the total number of vCPUs in a particular region, by using the Google Cloud Quotas API with the google-cloud-quotas Python library. This approach provides a direct way to query for quota information, including usage and limits.

Prerequisites Before you can programmatically check quotas, you need to:

Enable the Cloud Quotas API for your Google Cloud project.

Install the necessary Python library:

bash pip install google-cloud-quotas Authenticate your script. For local development, you can authenticate by running:

bash gcloud auth application-default login Checking Resource Quotas with Python To check resource quotas, you will use the CloudQuotasClient. The general process involves:

Instantiating the client.

Constructing the parent reso

urce name for your project and the service you want to que

Google Drive icon ry.

Listing the quota information for that service.

Filtering the results to find the specific quota you are interested in.

The service for Compute Engine resources, including GPUs and vCPUs, is compute.googleapis.com.

The quota metrics for different resources follow a specific format. For instance, the vCPU quota metric is typically compute.googleapis.com/cpus. GPU quotas have metrics that often include the GPU model and the region, or a global gpus\_all\_regions metric.

Below are Python code examples demonstrating how to check for specific GPU and vCPU quotas.

Example: Checking for a Specific GPU Type Quota This script demonstrates how to check the quota for a specific GPU type, such as the NVIDIA H100. You will need to know the specific metric name for the GPU you are interested in. The metric name for GPUs often follows the pattern compute.googleapis.com/{gpu\_type}. For example, for NVIDIA L4 GPUs, the metric might be compute.googleapis.com/l4\_gpus. You may need to find the exact metric name for 'NVIDIA\_H100\_GPU' in the Google Cloud documentation or by listing all quotas for the Compute Engine API.

python from google.cloud import cloudquotas\_v1

def get\_gpu\_quota(project\_id: str, region: str, gpu\_type\_metric: str): """ Checks the quota for a specific GPU type in a given region.

```
Args:
    project_id: Your Google Cloud project ID.
    region: The region to check the quota in.
    gpu_type_metric: The specific metric name for the GPU type (e.g., 'nvidia-h100-80gb-gpus').
"""
client = cloudquotas_v1.CloudQuotasClient()

# The parent resource for which to list quotas.
# Format: projects/{project_id}/locations/{location}/services/{service}
parent = f"projects/{project_id}/locations/{region}/services/compute.googleapis.com"

# The full quota info name to retrieve.
# Format: projects/{project_id}/locations/{location}/services/{service}/quotaInfos/{quota_info_id}
quota_info_name = f"{parent}/quotaInfos/{gpu_type_metric}"

try:
    quota_info = client.get_quota_info(name=quota_info_name)
    quota_limit = quota_info.quota_info.limit
    current_usage = quota_info.quota_info.usage
    print(f"GPU Quota for '{gpu_type_metric}' in region '{region}':")
    print(f"  Limit: {quota_limit}")
    print(f"  Current Usage: {current_usage}")
    print(f"  Available: {quota_limit - current_usage}")
except Exception as e:
    print(f"Could not retrieve GPU quota for '{gpu_type_metric}' in region '{region}': {e}")
```

# Replace with your project ID, desired region, and the specific GPU metric.

# The GPU metric for[...](asc_slot://start-slot-11) H100 might vary, check the Quotas page in your GCP console for the exact name.

get\_gpu\_quota("your-gcp-project-id", "us-central[...](asc_slot://start-slot-13)1", "nvidia-h100-80gb-gpus") Example: Checking for Total vCPU Quota in a R egion This script shows how to check the total vCPU quota for a specific region in your project.

python from google.cloud import cloudquotas\_v1

def get\_vcpu\_quota(project\_id: str, region: str): """ C[...](asc_slot://start-slot-17)hecks the total vCPU quota for a specific region.

```
Args:
    project_id: Your Google Cloud project ID.
    region: The region to check the quota in.
"""
client = cloudquotas_v1.CloudQuotasClient()

# The parent resource for which to list quotas.
parent = f"projects/{project_id}/locations/{r[...](asc_slot://start-slot-19)egion}/services/compute.googleapis.com"

# The full quota info name for CPUs.
quota_info_name = f"{parent}/quotaIn[...](asc_slot://start-slot-21)fos/cpus"

try:
    quota_info = client.get_quota_info(name=quota_info_name)
    quota_limit = quota_info.quota_info.limit
    current_usage = quota_info.quota_info.usage
    print(f"vCPU Quota in region '{region}':")
  print(f"  Limit: {quota_limit}")
    print(f"  Current Usage: {current_usage}")
    print(f"  Available: {quota_limit - current_usage}")
except Exception as e:
    print(f"Could not retrieve vCPU quota in region '{region}': {e}")
```

# Replace with your project ID[...](asc_slot://start-slot-25) and desired region.

get\_vcpu\_quota("your-gcp-project-id", "us-central1") Listing All Quotas for a Servic

e If you are unsure of the exact metric name for a resource, you can list all available quotas for the Compute Engine API in a specific region and then filter the results.

python from google.cloud import cloudquotas\_v1

def list\_all\_compute\_quotas(project\_id: str, region: str): """ Lists all Compute Engine quotas for a specific region.

```
Args:
    project_id: Your Google Cloud project ID.
    region: The region to list quotas for.
"""
client = cloudquotas_v1.CloudQuotasClient()

parent = f"projects/{project_id}/locations/{region}/services/compute.googleapis.com"

print(f"Listing all Compute Engine quotas for region '{region}':")
for quota in client.list_quota_infos(parent=parent):
    print(f"- {quota.name}")
    print(f"  Display Name: {quota.quota_display_name}")
    print(f"  Metric: {quota.metric_display_name}")
    print(f"  Limit: {quota.quota_info.limit}")
    print(f"  Usage: {quota.quota_info.usage}")
    print("-" * 20)
```

# Replace with your project ID and desired region.

list\_all\_compute\_quotas("your-gcp-project-id", "us-central1") By using these scripts, you can effectively monitor your Google Cloud resource quotas programmatically, enabling you to build automated checks and alerts into your workflows. You can programmatically check a Google Cloud project's resource quotas using the Google Cloud client libraries for Python. This allows you to monitor usage and available limits for resources like GPUs and vCPUs without manual intervention.

There are two primary Python libraries you can use to achieve this:

Google Cloud Compute Engine API Client Library (google-cloud-compute): This library provides direct access to the Compute Engine API, allowing you to retrieve detailed quota information for Compute Engine resources.

Cloud Quotas API Client Library (google-cloud-cloudquotas): A more recent and higher-level library designed to provide a unified way of viewing and managing quotas across various Google Cloud services.

Below are detailed explanations and code examples for both methods.

Method 1: Using the google-cloud-compute Library This approach involves using the client library for the Compute Engine API to fetch quota information at the regional or project level.

1. Installation

First, install the necessary library:

bash pip install google-cloud-compute 2\. Python Script to Check Quotas

The following script demonstrates how to initialize a client and retrieve quota information for a specific region. It then filters the results to find the quotas for all CPUs and for a specific GPU type.

python from google.cloud import compute\_v1

def get\_region\_quotas(project\_id: str, region: str): """ Gets all quotas for a given region in a project.

```
Args:
    project_id: Google Cloud project ID.
    region: The region to check quotas for.

Returns:
    A list of quota objects.
"""
client = compute_v1.RegionsClient()
request = compute_v1.GetRegionRequest(project=project_id, region=region)
response = client.get(request=request)

return response.quotas
```

if **name** \== "**main**": PROJECT\_ID \= "your-gcp-project-id"  \# Replace with your project ID REGION \= "us-central1"              \# Replace with your target region GPU\_TYPE \= "NVIDIA\_H100\_GPUS"       \# Example GPU type

```
quotas = get_region_quotas(PROJECT_ID, REGION)

print(f"Quotas for project '{PROJECT_ID}' in region '{REGION}':")

for quota in quotas:
    # Check for total vCPUs quota
    if quota.metric == "CPUS":
        print(f"- Metric: {quota.metric}")
        print(f"  Limit: {quota.limit}")
        print(f"  Usage: {quota.usage}")
        print(f"  Available: {quota.limit - quota.usage}\n")

    # Check for a specific GPU type quota
    if quota.metric == GPU_TYPE:
        print(f"- Metric: {quota.metric}")
        print(f"  Limit: {quota.limit}")
        print(f"  Usage: {quota.usage}")
        print(f"  Available: {quota.limit - quota.usage}\n")
```

Explanation:

The get\_region\_quotas function initializes a RegionsClient and makes a get request for the specified project and region.

The response object contains a quotas attribute, which is a list of Quota objects.

Each Quota object has metric, limit, and usage attributes. Google Drive icon

The script iterates through the list of quotas and prints the details for the desired metrics, such as CPUS and NVIDIA\_H100\_GPUS. The names for these metrics can be found in the Google Cloud documentation.

Method 2: Using the google-cloud-cloudquotas Library The Cloud Quotas API provides a more streamlined way to get quota information for various services, including Compute Engine.

1. Installation

First, enable the Cloud Quotas API in your project and install the client library:

bash pip install google-cloud-cloudquotas 2\. Python Script to Check Quotas

This script uses the CloudQuotasClient to list quota information for the Compute Engine service and then filters for the specific quotas you're interested in.

python from google.cloud import cloudquotas\_v1

def list\_compute\_quotas(project\_id: str, region: str): """ Lists quota information for the Compute Engine service in a specific region.

```
Args:
    project_id: Google Cloud project ID.
    region: The region to filter quotas by.

Returns:
    An iterator for the quota information.
"""
client = cloudquotas_v1.CloudQuotasClient()

# The parent will be in the format: projects/{project_id}/locations/{region}/services/compute.googleapis.com
parent = f"projects/{project_id}/locations/{region}/services/compute.googleapis.com"

request = cloudquotas_v1.ListQuotaInfosRequest(parent=parent)
page_result = client.list_quota_infos(request=request)

return page_result
```

if **name** \== "**main**": PROJECT\_ID \= "your-gcp-project-id"  \# Replace with your project ID REGION \= "us-central1"              \# Replace with your target region GPU\_QUOTA\_ID \= "GPUS\_ALL\_REGIONS"   \# Example for global GPU quota GPU\_TYPE\_DIMENSION \= "nvidia-h100-80gb-gpu" \# Example specific GPU dimension VCPU\_QUOTA\_ID \= "CPUS"              \# Example for regional vCPU quota

```
quotas = list_compute_quotas(PROJECT_ID, REGION)

print(f"Quotas for project '{PROJECT_ID}' in region '{REGION}':")

for quota_info in quotas:
    # Check for regional vCPU quota
    if quota_info.quota_id == VCPU_QUOTA_ID:
        print(f"- Quota ID: {quota_info.quota_id}")
        print(f"  Display Name: {quota_info.quota_display_name}")
        print(f"  Limit: {quota_info.quota_details.value}")
        # Note: The Cloud Quotas API provides the limit, but usage might need to be inferred or monitored separately.
        print(f"  Is Concurrent: {quota_info.is_concurrent}\n")

    # Check for specific GPU quota
    if quota_info.quota_id == GPU_QUOTA_ID and quota_info.dimensions.get('gpu_family') == GPU_TYPE_DIMENSION:
        print(f"- Quota ID: {quota_info.quota_id}")
        print(f"  Display Name: {quota_info.quota_display_name}")
        print(f"  Dimensions: {dict(quota_info.dimensions)}")
        print(f"  Limit: {quota_info.quota_details.value}")
        print(f"  Is Concurrent: {quota_info.is_concurrent}\n")
```

Explanation:

This script initializes the CloudQuotasClient.

The list\_quota\_infos method is called with a parent string that specifies the project, location (region), and the service (compute.googleapis.com).

The result is an iterator of QuotaInfo objects.

Each QuotaInfo object contains details like quota\_id, quota\_display\_name, and quota\_details (which includes the limit value).

For dimensional quotas, like those for specific GPU types, you need to inspect the dimensions map on the QuotaInfo object.

By using these Python scripts with the appropriate client libraries, you can effectively automate the process of checking your Google Cloud project's resource quotas.Of course. Here is a comprehensive guide on how to build a Python CLI application with the click library to manage a library of pre-defined YAML templates.

Project Structure First, let's define a simple project structure. All your YAML templates will be stored in a templates/ directory.

your\_project/ ├── templates/ │   ├── development.yaml │   ├── production.yaml │   └── staging.yaml └── cli.py Here are some example YAML templates:

templates/development.yaml

yaml app\_name: my-awesome-app environment: development replicas: 1 debug: true database: host: localhost port: 5432 templates/production.yaml

yaml app\_name: my-awesome-app environment: production replicas: 3 debug: false database: host: prod-db.example.com port: 5432 Core Concepts To build this CLI tool, we will use two main Python libraries:

click: For creating the command-line interface.

PyYAML: For loading and parsing the YAML files.

You can install these libraries using pip:

bash pip install click pyyaml The CLI Application (cli.py) Below is the complete code for the cli.py file. It includes:

A command group to host our subcommands.

A list-templates command.

A generate command that loads a template and allows overrides via flags.

python import os import click import yaml from pathlib import Path

# Define the path to the templates directory

TEMPLATE\_DIR \= Path(**file**).parent / "templates"

@click.group() def cli(): """A CLI tool to manage YAML templates.""" pass

@cli.command('list-templates') def list\_templates(): """Lists all available YAML templates.""" click.echo("Available templates:") try: \# Use pathlib to iterate over YAML files in the templates directory templates \= list(TEMPLATE\_DIR.glob('\*.yaml')) if not templates: click.echo("No templates found.") return

```
    for template_path in templates:
        click.echo(f"- {template_path.stem}")
except FileNotFoundError:
    click.echo("Templates directory not found.")
```

@cli.command() @click.argument('template\_name') @click.option('--app-name', help='Override the application name.') @click.option('--replicas', type=int, help='Override the number of replicas.') @click.option('--debug/--no-debug', default=None, help='Enable or disable debug mode.') @click.option('--db-host', help='Override the database host.') def generate(template\_name, app\_name, replicas, debug, db\_host): """Generates a configuration from a template with optional overrides.""" template\_file \= TEMPLATE\_DIR / f"{template\_name}.yaml"

```
if not template_file.is_file():
    click.echo(f"Error: Template '{template_name}' not found.", err=True)
    return

# Load the base template
with open(template_file, 'r') as f:
    try:
        config = yaml.safe_load(f) [2, 4]
    except yaml.YAMLError as e:
        click.echo(f"Error parsing YAML file: {e}", err=True)
        return

# Override values with command-line flags
if app_name is not None:
    config['app_name'] = app_name
if replicas is not None:
    config['replicas'] = replicas
if debug is not None:
    config['debug'] = debug
if db_host is not None and 'database' in config:
    config['database']['host'] = db_host

# Output the final, merged configuration
click.echo("--- Generated Configuration ---")
click.echo(yaml.dump(config, default_flow_style=False))
```

if **name** \== '**main**': cli() How It Works

1. Setting up the click CLI @click.group(): This decorator turns the cli function into a container that can have multiple subcommands attached to it.

@cli.command(): This decorator registers a function as a subcommand of the cli group.

2. The list-templates Command This command uses pathlib.Path to create a path object for the templates directory.

TEMPLATE\_DIR.glob('\*.yaml') finds all files in the directory ending with .yaml.

template\_path.stem is used to get the filename without the extension, providing a clean list of template names.

How to run it:

bash python cli.py list-templates Expected output:

Available templates:

- development  
- production  
- staging  
3. The generate Command @click.argument('template\_name'): This defines a required positional argument that specifies which template to use.

@click.option(...): These decorators define the optional flags that can be used to customize the template.

\--replicas is defined with type=int to automatically convert the input value.

\--debug/--no-debug creates a boolean flag. Using \--debug sets it to True, and \--no-debug sets it to False.

Loading the Template: The command constructs the full path to the chosen template file and checks for its existence. It then uses yaml.safe\_load() to parse the YAML file into a Python dictionary. safe\_load is recommended over load to prevent arbitrary code execution from a potentially malicious YAML file.

Merging and Overriding: The code checks if each optional command-line flag was provided by the user (i.e., is not None). If a flag was provided, its value updates the corresponding key in the config dictionary loaded from the YAML file.

Output: Finally, yaml.dump() is used to convert the final Python dictionary back into a nicely formatted YAML string for display.

How to run it:

Using a template without overrides:

bash python cli.py generate development Output:

\--- Generated Configuration \--- app\_name: my-awesome-app database: host: localhost port: 5432 debug: true environment: development replicas: 1 Using a template with overrides:

bash python cli.py generate production \--replicas 5 \--no-debug \--db-host custom-db.example.com Output:

\--- Generated Configuration \--- app\_name: my-awesome-app database: host: custom-db.example.com port: 5432 debug: false environment: production replicas: 5 This structure provides a robust and easily extensible way to manage your YAML templates from the command line, allowing for both standardized configurations and flexible, on-the-fly customizations.

A detailed process and example Python code for a script that fully parses a complex Google Cloud Cluster Toolkit blueprint YAML, identifies all billable resources, maps them to SKUs using the Cloud Billing Catalog API, and aggregates the data to provide a total estimated monthly cost is a multi-step process. Here is a comprehensive guide to achieving this.

Detailed Process Parse the Cluster Toolkit Blueprint YAML: The initial step is to read and parse the YAML file that defines the cluster. This file contains all the specifications for the resources to be deployed. The PyYAML library in Python is well-suited for this task. The blueprint is structured with deployment\_groups that contain a list of modules, and each module defines a specific part of the HPC environment. Google Drive icon

Identify Billable Resources: After parsing the YAML file, the next step is to traverse the data structure to identify all the resources that will incur costs. Key resources to look for within the modules include:

Compute Engine VMs: These are typically defined in modules with sources like community/modules/compute/schedmd-slurm-gcp-v6-nodeset. Important attributes to extract are machine\_type, node\_count\_dynamic\_max (for autoscaling clusters), and the region/zone which are usually defined in the vars section. Google Drive icon

GPUs: GPU configurations are often part of the machine\_type (e.g., a2-highgpu-1g) or specified in the module's settings. The type and number of GPUs per VM are critical for cost estimation. Google Drive icon

Google Drive icon

Storage:

Filestore: Look for modules with a source of modules/file-system/filestore. The settings will contain details like the storage tier and capacity. Google Drive icon

Google Drive icon

Lustre: This is often provided by partners like DDN. Look for modules with sources like community/modules/file-system/DDN-EXAScaler. Google Drive icon

Google Drive icon

Persistent Disks: These are specified within the compute modules with attributes like disk\_type and disk\_size\_gb. Google Drive icon

Networking: While VPCs are generally free, resources like NAT gateways and significant egress traffic can incur costs. For simplicity, this example will focus on the primary compute and storage resources.

Map Resources to SKUs with the Cloud Billing Catalog API: This is a critical step that involves programmatically finding the correct Stock Keeping Unit (SKU) for each identified resource. The Google Cloud Billing Catalog API provides the necessary tools for this. Yaqs icon

Yaqs icon

You will need to use the CloudBillingClient from the google-cloud-billing Python library.

To find a SKU, you will list the SKUs for a particular service (e.g., "services/6F81-5844-456A" for Compute Engine) and then filter them based on the resource's attributes like machine type, region, and GPU type. Yaqs icon

Retrieve Pricing Information: Once you have the SKU ID for a resource, you can use the Billing API to get its pricing information. The pricing can have multiple tiers, so you'll need to parse the pricing\_expression to determine the cost. For simplicity, we will consider the most straightforward pricing tiers.

Aggregate and Calculate Total Estimated Monthly Cost: The final step is to aggregate the costs of all the identified resources. This involves:

Calculating the monthly cost for each resource. Since many prices are hourly, you'll need to multiply by the average number of hours in a month (approximately 730).

Summing the costs of all resources to get a total estimated monthly cost.

It's important to note that this will be an estimate. Actual costs can vary based on usage patterns, sustained use discounts, and other factors. Google Drive icon

Example Python Script Here is an example Python script that demonstrates the process described above.

Prerequisites:

You have a Google Cloud project with the Cloud Billing API enabled.

You have authenticated your environment.

You have installed the necessary Python libraries:

bash pip install google-cloud-billing pyyaml Python Code:

python import yaml from google.cloud import billing\_v1

def parse\_blueprint(file\_path): """Parses a Cluster Toolkit YAML blueprint file.""" with open(file\_path, 'r') as f: return yaml.safe\_load(f)

def identify\_billable\_resources(blueprint): """Identifies billable resources from the parsed blueprint.""" resources \= \[\] region \= blueprint.get('vars', {}).get('region', 'us-central1')

```
for group in blueprint.get('deployment_groups', []):
    for module in group.get('modules', []):
        settings = module.get('settings', {})
        source = module.get('source', '')

        # Identify Compute Engine instances
        if 'compute' in source and 'nodeset' in source:
            machine_type = settings.get('machine_type')
            if machine_type:
                resources.append({
                    'type': 'compute',
                    'machine_type': machine_type,
                    'count': settings.get('node_count_dynamic_max', 1),
                    'region': region
                })

        # Identify Filestore instances
        if 'file-system/filestore' in source:
            resources.append({
                'type': 'filestore',
                'tier': settings.get('tier', 'BASIC_SSD'),
                'capacity_gb': settings.get('file_shares', [{}])[0].get('capacity_gb', 1024),
                'region': region
            })
return resources
```

def get\_sku\_price(billing\_client, service, description\_filter, region): """Gets the price for a SKU based on service, description, and region.""" parent \= f"services/{service}" request \= billing\_v1.ListSkusRequest(parent=parent) for sku in billing\_client.list\_skus(request=request): if description\_filter in sku.description and region in sku.service\_regions: for pricing\_info in sku.pricing\_info: for rate in pricing\_info.pricing\_expression.tiered\_rates: \# For simplicity, we take the price of the first tier. return rate.unit\_price.nanos / 1e9  \# Convert nanos to dollars return 0

def estimate\_monthly\_cost(blueprint\_file): """Estimates the total monthly cost of a Cluster Toolkit blueprint.""" blueprint \= parse\_blueprint(blueprint\_file) resources \= identify\_billable\_resources(blueprint) billing\_client \= billing\_v1.CloudBillingClient()

```
total_monthly_cost = 0
HOURS_IN_MONTH = 730  # Approximate

# Service IDs for filtering SKUs
COMPUTE_SERVICE = "6F81-5844-456A"  # Compute Engine
FILESTORE_SERVICE = "988F-E7E1-29EA"  # Filestore

for resource in resources:
    cost = 0
    if resource['type'] == 'compute':
        # This is a simplified mapping. A more robust solution would need a more detailed mapping of machine types to CPU/RAM SKUs.
        # For this example, we'll just look for a common machine type.
        price_per_hour = get_sku_price(billing_client, COMPUTE_SERVICE, f"N2 Custom Instance Core running in {resource['region']}", resource['region'])
        cost = price_per_hour * resource['count'] * HOURS_IN_MONTH
        print(f"Found Compute resource: {resource['machine_type']} x {resource['count']}. Estimated monthly cost: ${cost:.2f}")

    elif resource['type'] == 'filestore':
        tier_description = "SSD" if "SSD" in resource['tier'] else "HDD"
        price_per_gb_month = get_sku_price(billing_client, FILESTORE_SERVICE, f"Filestore {tier_description} Storage", resource['region'])
        cost = price_per_gb_month * resource['capacity_gb']
        print(f"Found Filestore resource: {resource['tier']} {resource['capacity_gb']}GB. Estimated monthly cost: ${cost:.2f}")

    total_monthly_cost += cost

return total_monthly_cost
```

if **name** \== '**main**': \# Create a dummy blueprint file for demonstration dummy\_blueprint\_content \= """ blueprint\_name: hpc-slurm-simple vars: project\_id: "your-gcp-project-id" deployment\_name: hpc-cluster region: us-central1 zone: us-central1-a

deployment\_groups:

- group: primary modules:  
    
  - id: network source: modules/network/vpc  
  - id: homefs source: modules/file-system/filestore settings: local\_mount: /home tier: BASIC\_SSD file\_shares: \- capacity\_gb: 2048  
  - id: compute\_nodeset source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset settings: node\_count\_dynamic\_max: 10 machine\_type: n2-standard-8 """ with open("dummy\_blueprint.yaml", "w") as f: f.write(dummy\_blueprint\_content)


  estimated\_cost \= estimate\_monthly\_cost("dummy\_blueprint.yaml") print(f"\\nTotal Estimated Monthly Cost: ${estimated\_cost:.2f}")

Limitations and Considerations Complex SKU Mapping: The mapping of resource names from the blueprint to the exact SKU description can be complex and may require maintenance as new machine types and services are introduced. The example above uses a simplified mapping. A production-grade script would need a more robust mapping mechanism.

Dynamic Resources: For autoscaling clusters, this script uses node\_count\_dynamic\_max, which provides an upper bound on the cost. Actual costs will depend on the cluster's utilization.

Sustained Use and Committed Use Discounts: The Cloud Billing Catalog API provides list prices. The script does not account for automatic sustained use discounts or any committed use discounts you may have, which can significantly reduce actual costs. Google Drive icon

Other Billable Components: The script focuses on major components like VMs and Filestore. A comprehensive solution would also need to parse and estimate costs for other potential resources like GPUs, additional storage volumes, and advanced networking features.

API Quotas: Be mindful of API rate limits when making numerous calls to the Cloud Billing Catalog API.

This detailed process and example script provide a solid foundation for programmatically estimating the cost of a Google Cloud Cluster Toolkit deployment. You can extend and refine the script to handle more complex blueprint configurations and provide more accurate cost estimates. Here is a detailed process and example Python code for a script that parses a Google Cloud Cluster Toolkit blueprint YAML, identifies billable resources, maps them to their SKUs using the Cloud Billing Catalog API, and aggregates the data to provide an estimated monthly cost.

Process Overview The process of estimating the cost of a Google Cloud Cluster Toolkit blueprint involves the following key steps:

Parse the Blueprint YAML: The script begins by loading and parsing the Cluster Toolkit blueprint file to understand the defined infrastructure.

Identify Billable Resources: It then iterates through the deployment\_groups and their modules to find all the resources that will incur costs. This includes virtual machines, GPUs, and storage volumes like Filestore and Lustre.

Map Resources to SKUs: For each identified resource, the script queries the Google Cloud Billing Catalog API to find the corresponding Stock Keeping Unit (SKU). This mapping is crucial for getting accurate pricing information.

Calculate Estimated Monthly Cost: Finally, the script calculates the estimated monthly cost for each resource based on its SKU's pricing and aggregates these costs to provide a total estimate for the entire blueprint.

Detailed Steps and Python Implementation Here is a breakdown of each step with a corresponding Python code example.

1. Parsing the Blueprint YAML The first step is to read and parse the YAML blueprint file. The PyYAML library is an excellent tool for this task. The script will load the YAML content into a Python dictionary, making it easy to navigate and extract information.

Prerequisites:

Python 3.7+

google-api-python-client and google-cloud-billing libraries:

bash pip install google-api-python-client google-cloud-billing PyYAML Authentication: Ensure you have authenticated with Google Cloud. For local development, you can use:

bash gcloud auth application-default login Python Code:

python import yaml

def parse\_blueprint(file\_path): """Parses a Cluster Toolkit blueprint YAML file.""" with open(file\_path, 'r') as f: try: return yaml.safe\_load(f) except yaml.YAMLError as e: print(f"Error parsing YAML file: {e}") return None 2\. Identifying Billable Resources Once the blueprint is parsed, the script needs to traverse the data structure to find the billable resources. These are typically defined within the deployment\_groups and modules.

Key resources to look for include:

Compute Engine VMs: Defined by machine\_type. The number of instances is also a critical factor.

GPUs: Specified by gpu\_type and gpu\_count attached to a VM.

Filestore: Indicated by modules that create Filestore instances, with attributes like tier and capacity\_gb.

Managed Lustre: Identified by modules for Lustre, with parameters for capacity\_tb.

Python Code:

python def identify\_billable\_resources(blueprint): """Identifies billable resources from the parsed blueprint.""" resources \= \[\] if not blueprint or 'deployment\_groups' not in blueprint: return resources

```
for group in blueprint.get('deployment_groups', []):
    for module in group.get('modules', []):
        # This is a simplified example. In a real-world scenario, you would
        # need to handle the specific module source and its variables.
        if 'source' in module and 'modules/compute/instance' in module['source']:
            # This is a hypothetical path, adjust based on actual module sources
            instance_vars = module.get('vars', {})
            resources.append({
                'type': 'compute',
                'machine_type': instance_vars.get('machine_type'),
                'gpu': {
                    'type': instance_vars.get('gpu_type'),
                    'count': instance_vars.get('gpu_count')
                } if 'gpu_type' in instance_vars else None,
                'count': instance_vars.get('instance_count', 1)
            })
        elif 'source' in module and 'modules/file-system/filestore' in module['source']:
            filestore_vars = module.get('vars', {})
            resources.append({
                'type': 'filestore',
                'tier': filestore_vars.get('tier'),
                'capacity_gb': filestore_vars.get('capacity_gb'),
                'count': 1
            })
        # Add logic for other resource types like Lustre
return resources
```

3. Mapping Resources to SKUs with the Cloud Billing Catalog API This is the most complex part of the process. For each resource, you need to find its corresponding SKU. The Cloud Billing Catalog API allows you to list all public SKUs.

Since the API's filtering capabilities are limited, the script will fetch all SKUs for a given service (e.g., Compute Engine) and then filter them in memory based on the resource's attributes.

Key Mapping Logic:

Compute Engine: The SKU description for a VM often contains the machine type series (e.g., "N1 Standard") and the number of vCPUs. You'll need to parse this description to find a match.

GPUs: GPU SKUs are separate from VM SKUs. Their descriptions typically include the GPU model (e.g., "NVIDIA Tesla T4") and are often region-specific.

Filestore and Lustre: These will have their own service IDs and their SKUs will be described based on their tier and capacity.

Python Code:

python from googleapiclient.discovery import build

def get\_billing\_service(): """Returns an authenticated Cloud Billing API client.""" return build('cloudbilling', 'v1', cache\_discovery=False)

def find\_sku\_for\_resource(billing\_service, resource, region): """Finds the SKU for a given resource.""" \# In a real application, you would cache the results of these API calls. service\_name \= get\_service\_name\_for\_resource(resource\['type'\]) if not service\_name: return None

```
skus = []
page_token = None
while True:
    request = billing_service.services().skus().list(parent=service_name, pageToken=page_token)
    response = request.execute()
    skus.extend(response.get('skus', []))
    page_token = response.get('nextPageToken')
    if not page_token:
        break

# Filter SKUs based on resource attributes
# This is a simplified filtering logic. You'll need to make it more robust.
for sku in skus:
    if region in sku.get('serviceRegions', []) and resource['type'] == 'compute':
        if resource['machine_type'] in sku.get('description', ''):
             # This is a very basic match and will need refinement
            return sku
    # Add filtering logic for other resource types

return None
```

def get\_service\_name\_for\_resource(resource\_type): """Returns the service name for a given resource type.""" \# These are example service names. You can get a list of services from the API. if resource\_type \== 'compute': return 'services/6F81-5844-456A'  \# Compute Engine elif resource\_type \== 'filestore': return 'services/95D9-F069-9374'  \# Filestore \# Add other service names return None 4\. Aggregating Data and Estimating Monthly Cost After finding the correct SKU for each resource, the final step is to calculate the estimated monthly cost. The SKU's pricingInfo contains the pricing details. For simplicity, this example assumes a straightforward pricing model and calculates the cost for a 30-day month.

Python Code:

python def calculate\_estimated\_monthly\_cost(sku, resource): """Calculates the estimated monthly cost for a resource based on its SKU.""" if not sku or 'pricingInfo' not in sku or not sku\['pricingInfo'\]: return 0.0

```
pricing_info = sku['pricingInfo'][0]
pricing_expression = pricing_info.get('pricingExpression', {})
tiered_rates = pricing_expression.get('tieredRates', [])

if not tiered_rates:
    return 0.0

# Assuming the first tier is the relevant one for this estimation
unit_price = tiered_rates[0].get('unitPrice', {})
price_in_nanos = unit_price.get('nanos', 0)
price_in_units = unit_price.get('units', 0)
price_per_unit = price_in_units + price_in_nanos / 1e9

# Assuming the usage unit is hours for VMs
# A more robust solution would parse usageUnitDescription
monthly_cost = price_per_unit * 24 * 30 * resource.get('count', 1)

return monthly_cost
```

def main(blueprint\_path, region): """Main function to parse blueprint and estimate cost.""" blueprint \= parse\_blueprint(blueprint\_path) if not blueprint: return

```
resources = identify_billable_resources(blueprint)
billing_service = get_billing_service()
total_monthly_cost = 0.0

for resource in resources:
    sku = find_sku_for_resource(billing_service, resource, region)
    if sku:
        cost = calculate_estimated_monthly_cost(sku, resource)
        total_monthly_cost += cost
        print(f"Resource: {resource}, Estimated Monthly Cost: ${cost:.2f}")
    else:
        print(f"Could not find SKU for resource: {resource}")

print(f"\nTotal Estimated Monthly Cost: ${total_monthly_cost:.2f}")
```

if **name** \== '**main**': \# Replace with the path to your blueprint and the target region main('path/to/your/blueprint.yaml', 'us-central1') Important Considerations and Limitations SKU Mapping Complexity: The mapping between a resource in a blueprint and a SKU in the Billing API is not always straightforward. The SKU descriptions can be complex and may require sophisticated parsing and regular expressions to match correctly.

Pricing Models: This example uses a simplified pricing model. Real-world costs can be affected by sustained use discounts, committed use discounts, and Spot VM pricing, which would require more complex logic to handle.

Custom Machine Types: For custom machine types, you would need to find the SKUs for custom vCPUs and memory and calculate the cost based on the specified amounts in the blueprint.

Regional Pricing: Prices vary by region. The script needs to take the target region into account when looking up SKUs.

API Quotas and Caching: The Billing Catalog API has quotas. For complex blueprints, it's essential to cache the results of API calls to avoid exceeding these quotas and to improve performance.

Dynamic Nature of SKUs and Pricing: SKUs and their pricing can change over time. This script provides a point-in-time estimate.

This detailed process and the provided Python code offer a solid foundation for building a robust cost estimation tool for Google Cloud Cluster Toolkit blueprints. Further refinement will be needed to handle the full complexity of Google Cloud's pricing and resource options.

Unit testing functions that interact with external services like the Google Cloud Compute API is a critical practice for building robust and reliable applications. This guide outlines the best-practice approach and provides example Python code for writing unit tests for a function in a hypothetical gcp\_client.py that interacts with the Google Cloud Compute API. We will use Python's unittest.mock library to effectively mock the API client and its responses, allowing for the testing of various scenarios such as resource availability and API errors without making actual calls to the Google Cloud Platform.

Best-Practice Approach for Mocking GCP Clients The core principle behind testing code that interacts with external APIs is to isolate the code under test from the external dependency. This is achieved by replacing the API client with a mock object that simulates the behavior of the real client.

The recommended approach involves using the @patch decorator from unittest.mock. Here's a breakdown of the strategy:

Target the Client Where It's Used: It's crucial to patch the GCP client in the namespace where it is imported and used, not where it is defined. For instance, if gcp\_client.py imports compute\_v1, you should patch gcp\_client.compute\_v1.

Mock the Client Instance: In most cases, your code will first instantiate a client, like client \= compute\_v1.InstancesClient(), and then call methods on that instance. Your mock should therefore control the return value of the client class instantiation.

Simulate Successful Responses: For happy-path tests, configure the mock to return objects that mimic the structure of a successful API response. This can be a simple MagicMock object with the necessary attributes.

Simulate API Errors: To test error handling, use the side\_effect attribute of a mock. This can be set to an exception class or instance, which will then be raised when the mock is called. For Google Cloud APIs, this is often googleapiclient.errors.HttpError or other specific exceptions from google.api\_core.exceptions.

Example: gcp\_client.py Let's consider a function in gcp\_client.py that checks if a Compute Engine instance exists in a specific project and zone.

python

# gcp\_client.py

from google.cloud import compute\_v1 from googleapiclient.errors import HttpError

def instance\_exists(project\_id: str, zone: str, instance\_name: str) \-\> bool: """ Checks if a Compute Engine instance exists.

```
Args:
    project_id: The ID of the project.
    zone: The zone of the instance.
    instance_name: The name of the instance.

Returns:
    True if the instance exists, False otherwise.
"""
try:
    client = compute_v1.InstancesClient()
    client.get(project=project_id, zone=zone, instance=instance_name)
    return True
except HttpError as e:
    if e.resp.status == 404:
        return False
    raise
```

Example: test\_gcp\_client.py Now, let's write the unit tests for the instance\_exists function in a separate file, test\_gcp\_client.py.

python

# test\_gcp\_client.py

import unittest from unittest.mock import patch, MagicMock

from googleapiclient.errors import HttpError

from gcp\_client import instance\_exists

class TestGcpClient(unittest.TestCase):

```
@patch('gcp_client.compute_v1.InstancesClient')
def test_instance_exists_true_when_resource_is_available(self, mock_instances_client):
    """
    Tests that instance_exists returns True when the instance is found.
    """
    # Arrange
    mock_client_instance = mock_instances_client.return_value
    mock_client_instance.get.return_value = MagicMock()

    project_id = "my-gcp-project"
    zone = "us-central1-a"
    instance_name = "my-test-instance"

    # Act
    result = instance_exists(project_id, zone, instance_name)

    # Assert
    self.assertTrue(result)
    mock_client_instance.get.assert_called_once_with(
        project=project_id,
        zone=zone,
        instance=instance_name
    )

@patch('gcp_client.compute_v1.InstancesClient')
def test_instance_exists_false_when_resource_is_not_found(self, mock_instances_client):
    """
    Tests that instance_exists returns False for a 404 Not Found error.
    """
    # Arrange
    mock_client_instance = mock_instances_client.return_value
    http_error = HttpError(
        resp=MagicMock(status=404),
        content=b'Not Found'
    )
    mock_client_instance.get.side_effect = http_error

    project_id = "my-gcp-project"
    zone = "us-central1-a"
    instance_name = "non-existent-instance"

    # Act
    result = instance_exists(project_id, zone, instance_name)

    # Assert
    self.assertFalse(result)
    mock_client_instance.get.assert_called_once_with(
        project=project_id,
        zone=zone,
        instance=instance_name
    )

@patch('gcp_client.compute_v1.InstancesClient')
def test_instance_exists_raises_other_http_errors(self, mock_instances_client):
    """
    Tests that instance_exists raises HttpError for non-404 errors.
    """
    # Arrange
    mock_client_instance = mock_instances_client.return_value
    http_error = HttpError(
        resp=MagicMock(status=500),
        content=b'Internal Server Error'
    )
    mock_client_instance.get.side_effect = http_error

    project_id = "my-gcp-project"
    zone = "us-central1-a"
    instance_name = "another-instance"

    # Act & Assert
    with self.assertRaises(HttpError):
        instance_exists(project_id, zone, instance_name)

    mock_client_instance.get.assert_called_once_with(
        project=project_id,
        zone=zone,
        instance=instance_name
    )
```

if **name** \== '**main**': unittest.main() Explanation of the Test Code @patch('gcp\_client.compute\_v1.InstancesClient'): This decorator intercepts the InstancesClient class within the gcp\_client module and replaces it with a MagicMock. This mock is then passed as an argument (mock\_instances\_client) to the test method.

Testing Resource Availability:

In test\_instance\_exists\_true\_when\_resource\_is\_available, we configure the mock to simulate a successful API call.

mock\_instances\_client.return\_value represents the object that is returned when InstancesClient() is called. We get a handle to this instance.

mock\_client\_instance.get.return\_value \= MagicMock() sets up the get method on the client instance to return a new MagicMock object, simulating a successful response.

The test then asserts that the function returns True and that the get method was called with the correct arguments.

Testing API Errors (404 Not Found):

In test\_instance\_exists\_false\_when\_resource\_is\_not\_found, we simulate the API returning a 404 error.

An HttpError is instantiated with a mocked response object that has a status of 404\.

mock\_client\_instance.get.side\_effect \= http\_error configures the mock so that when the get method is called, it raises this HttpError instead of returning a value.

The test asserts that the function correctly catches this specific error and returns False.

Testing Other API Errors:

The test\_instance\_exists\_raises\_other\_http\_errors test ensures that the function's error handling correctly re-raises HTTP errors that are not 404s.

An HttpError with a status code of 500 is created and set as the side\_effect.

with self.assertRaises(HttpError): is used as a context manager to assert that the expected exception is raised when the function is called.

By following this pattern, you can write comprehensive unit tests for your GCP client functions, ensuring they behave as expected in various scenarios without the need for a live GCP environment. Unit testing functions that interact with external services like the Google Cloud Compute API is a critical practice for building robust and maintainable applications. The best-practice approach is to isolate the code under test from the actual API by using mock objects. This ensures that your tests are fast, repeatable, and do not incur costs or depend on network connectivity.

For Python, the standard library unittest.mock is the ideal tool for this purpose. It allows you to replace parts of your system, like the API client, with mock objects that you can configure to simulate specific behaviors and responses. Google Drive icon

Google Drive icon

Best-Practice Approach Isolate Your Code: Your unit tests should never make actual network calls to the Google Cloud API. The goal is to test your function's logic, not the Google Cloud service itself.

Mock the Client, Not the Function: Instead of mocking your own function (get\_instance in the example below), you should mock the object that your function uses to communicate with the external service. In this case, it's the Google Cloud API client object created by googleapiclient.discovery.build.

Use unittest.mock.patch: This decorator (or context manager) makes it easy to temporarily replace an object within a specific scope (like a test method) with a mock. Google Drive icon

Simulate Success and Failure:

Success Cases: Configure the mock to return the data your function expects from a successful API call. This involves setting the return\_value on the appropriate mock method.

Error Cases: To test how your code handles API errors (e.g., 404 Not Found, 403 Permission Denied), configure the mock to raise an exception using the side\_effect attribute. Yaqs icon This is crucial for testing your try...except blocks.

Assert on Behavior: Your tests should assert that your function behaves as expected based on the simulated API response. This includes checking the return value of your function and verifying that the mock API client was called with the correct arguments.

Example: Testing a Compute Engine Function Let's walk through a complete example. Imagine you have a file named gcp\_client.py with a function that checks the status of a Google Compute Engine instance.

The Code to Be Tested: gcp\_client.py This function initializes the Compute Engine API client, calls the instances().get() method, and handles potential HttpError exceptions.

python

# gcp\_client.py

from googleapiclient import discovery from googleapiclient.errors import HttpError

class APIError(Exception): """Custom exception for API errors.""" pass

def get\_instance\_status(project\_id: str, zone: str, instance\_name: str) \-\> str: """ Gets the status of a Google Compute Engine instance.

```
Args:
    project_id: The ID of the Google Cloud project.
    zone: The zone where the instance is located.
    instance_name: The name of the instance.

Returns:
    The status of the instance (e.g., 'RUNNING', 'TERMINATED') or 'NOT_FOUND'.

Raises:
    APIError: If a non-404 HTTP error occurs.
"""
try:
    # Build the service object
    compute_service = discovery.build('compute', 'v1')

    # Get the instance resource
    request = compute_service.instances().get(
        project=project_id,
        zone=zone,
        instance=instance_name
    )
    response = request.execute()
    return response.get('status', 'UNKNOWN')

except HttpError as e:
    if e.resp.status == 404:
        return 'NOT_FOUND'
    else:
        # Re-raise other HTTP errors as a custom exception
        raise APIError(f"API error occurred: {e}") from e
except Exception as e:
    raise APIError(f"An unexpected error occurred: {e}") from e
```

The Unit Tests: test\_gcp\_client.py This test file uses unittest and unittest.mock.patch to test the get\_instance\_status function under three different scenarios.

python

# test\_gcp\_client.py

import unittest from unittest.mock import patch, MagicMock

from googleapiclient.errors import HttpError from google.oauth2.credentials import Credentials

# Import the function and custom exception from our module

from gcp\_client import get\_instance\_status, APIError

class TestGcpClient(unittest.TestCase):

```
# The @patch decorator intercepts the call to 'gcp_client.discovery.build'
# and replaces it with a mock object (mock_build), which is then passed
# into each test method.
@patch('gcp_client.discovery.build')
def test_get_instance_status_running(self, mock_build):
    """
    Tests the function for a successful API call where the instance is found
    and is in a 'RUNNING' state.
    """
    # 1. Configure the mock to simulate the API client and its response
    mock_instance_response = {'status': 'RUNNING'}
    
    # This creates a chain of mock calls: build().instances().get().execute()
    mock_service = MagicMock()
    mock_service.instances.return_value.get.return_value.execute.return_value = mock_instance_response
    mock_build.return_value = mock_service

    # 2. Call the function under test
    status = get_instance_status('my-project', 'us-central1-a', 'test-instance')

    # 3. Assert the results
    self.assertEqual(status, 'RUNNING')
    
    # Verify that the discovery.build was called correctly
    mock_build.assert_called_once_with('compute', 'v1')
    
    # Verify that the get method was called with the correct parameters
    mock_service.instances().get.assert_called_once_with(
        project='my-project',
        zone='us-central1-a',
        instance='test-instance'
    )

@patch('gcp_client.discovery.build')
def test_get_instance_status_not_found(self, mock_build):
    """
    Tests the function's handling of a 404 Not Found error.
    """
    # 1. Configure the mock to raise an HttpError with status 404
    # This simulates the instance not being found.
    mock_http_error = HttpError(
        resp={'status': '404', 'reason': 'Not Found'},
        content=b'Not Found'
    )
    mock_service = MagicMock()
    mock_service.instances.return_value.get.return_value.execute.side_effect = mock_http_error
    mock_build.return_value = mock_service

    # 2. Call the function
    status = get_instance_status('my-project', 'us-central1-a', 'non-existent-instance')

    # 3. Assert that the function correctly interprets the 404 error
    self.assertEqual(status, 'NOT_FOUND')

@patch('gcp_client.discovery.build')
def test_get_instance_status_api_error(self, mock_build):
    """
    Tests the function's handling of a non-404 API error (e.g., 503).
    """
    # 1. Configure the mock to raise a different HttpError
    # The use of 'side_effect' is key for making a mock raise an exception. [6]
    mock_http_error = HttpError(
        resp={'status': '503', 'reason': 'Service Unavailable'},
        content=b'Service Unavailable'
    )
    mock_service = MagicMock()
    mock_service.instances.return_value.get.return_value.execute.side_effect = mock_http_error
    mock_build.return_value = mock_service

    # 2. Use assertRaises to verify that our custom APIError is raised
    with self.assertRaises(APIError) as context:
        get_instance_status('my-project', 'us-central1-a', 'test-instance')

    # 3. Optionally, inspect the exception message
    self.assertIn("API error occurred", str(context.exception))
if **name** \== '**main**': unittest.main()  
