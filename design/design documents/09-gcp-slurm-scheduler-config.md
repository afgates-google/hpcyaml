Configuring a Slurm Scheduler in Google Cloud Cluster Toolkit Configuring a Slurm scheduler within a Google Cloud Cluster Toolkit blueprint YAML file involves defining a set of modules that specify the behavior and resources for the Slurm controller and its associated compute partitions. This powerful infrastructure-as-code approach allows for reproducible and customizable HPC environments on Google Cloud.

The central component of this setup is the blueprint YAML file, which outlines the architecture of your cluster. To integrate a Slurm scheduler, you will primarily use the slurm_controller module and one or more partition modules (e.g., compute_partition).

Key Components of a Slurm Blueprint A typical Slurm blueprint YAML is structured with the following key sections:

terraform_backend_defaults: This section is recommended for production environments to store the Terraform state in a Google Cloud Storage bucket, ensuring better state management and collaboration.

vars: This section defines variables that can be used throughout the blueprint, such as project_id, deployment_name, region, and zone.

deployment_groups: This is the core of the blueprint where you define the modules that will be deployed. For a Slurm cluster, this will include modules for networking, the Slurm controller, and compute partitions.

Configuring the Slurm Controller The slurm_controller module is responsible for deploying the virtual machine that will run the slurmctld daemon, which manages the entire cluster. Here is an example of how to configure the slurm_controller module within your blueprint:

```yaml

- group: slurm_cluster
  modules:
    - id: slurm_controller
      source: "./modules/scheduler/slurm_controller"
      settings:
        machine_type: "n2-standard-2"
        enable_public_ips: true
        partitions:
          - name: "compute"
            nodeset: "compute_nodes"
```

In this example:

machine_type: Specifies the Google Compute Engine machine type for the controller VM.

enable_public_ips: When set to true, it assigns a public IP address to the controller, allowing direct SSH access for administration and job submission.

partitions: This crucial setting links the controller to the compute partitions it will manage. Each entry in this list should correspond to a defined partition module.

Setting up Compute Partitions Compute partitions define the groups of nodes where Slurm jobs will actually run. Each partition is typically configured as a separate module. Here's an example of a compute_partition configuration:

```yaml
- id: compute_partition
  source: "./modules/scheduler/slurm_partition"
  settings:
    name: "compute"
    nodeset: "compute_nodes"
    is_default: true
```

```yaml
- id: compute_nodes
  source: "./modules/compute/schedmd_slurm_gcp_v6_nodeset"
  settings:
    machine_type: "c2-standard-60"
    node_count_dynamic_max: 10
```

Key settings for a compute partition include:

name: A unique name for the partition. This is the name users will specify when submitting jobs (e.g., sbatch -p compute).

nodeset: This links the partition to a specific nodeset module that defines the properties of the compute nodes.

is_default: Setting this to true makes this partition the default for jobs submitted without a specific partition request.

machine_type: The machine type for the compute nodes in this partition.

node_count_dynamic_max: This enables autoscaling for the partition, defining the maximum number of nodes that can be created to handle the job queue.

Putting It All Together: A Complete Example To get started, you can use or adapt the hpc-slurm.yaml example found in the official Cluster Toolkit GitHub repository.

This example provides a solid foundation for a basic Slurm cluster.

Here is a simplified, conceptual example of a complete blueprint YAML for a Slurm cluster:

```yaml
# Example hpc-slurm.yaml

terraform_backend_defaults:
  type: gcs
  configuration:
    bucket: "your-terraform-state-bucket"

vars:
  project_id: "your-gcp-project-id"
  deployment_name: "my-slurm-cluster"
  region: "us-central1"
  zone: "us-central1-a"

deployment_groups:
  - group: network
    modules:
      - id: network
        source: "./modules/network/vpc"

  - group: slurm_cluster
    modules:
      - id: slurm_controller
        source: "./modules/scheduler/slurm_controller"
        use: [network]
        settings:
          machine_type: "n2-standard-2"
          enable_public_ips: true
          partitions:
            - name: "c2-standard"
              nodeset: "c2_nodes"

      - id: c2_partition
        source: "./modules/scheduler/slurm_partition"
        use: [slurm_controller]
        settings:
          name: "c2-standard"
          nodeset: "c2_nodes"
          is_default: true

      - id: c2_nodes
        source: "./modules/compute/schedmd_slurm_gcp_v6_nodeset"
        use: [network]
        settings:
          machine_type: "c2-standard-60"
          node_count_dynamic_max: 20
```

After creating your blueprint file, you use the gcluster command-line tool to generate the Terraform deployment files and then deploy your cluster. This process automates the provisioning of all the defined resources, from VPC networks to the Slurm controller and compute instances. Configuring a Slurm scheduler within a Google Cloud HPC Toolkit blueprint involves defining a set of interconnected modules in a YAML file. These modules specify the network, storage, compute resources, and the Slurm components themselves.

Key Components of a Slurm Blueprint A typical Slurm cluster blueprint is structured with the following components:

Blueprint Name (blueprint_name): A name for your blueprint, which is used as a label on the deployed cloud resources for tracking and cost monitoring.

Variables (vars): A section for defining variables that can be used throughout the blueprint, such as project_id, deployment_name, region, and zone. This allows for easy customization of deployments.

Deployment Groups (deployment_groups): This section organizes the modules that will be deployed together. A blueprint can have one or more groups.

Modules: These are the fundamental building blocks of the cluster. Each module has a unique id, a source pointing to its definition (often within the HPC Toolkit's GitHub repository), and settings for customization. The use key defines dependencies between modules. Google Drive icon

Configuring the Slurm Controller and Partitions To set up a Slurm cluster, you need to define modules for the controller, and at least one compute partition. A partition itself is typically composed of a "nodeset" and a "partition" module.

1. Define Compute Node Sets (nodeset) A nodeset module defines the configuration for a group of compute nodes that will form a partition. You can define multiple nodesets for different machine types or requirements.

In this example, two nodesets are created: one for general compute and another for debugging.

```yaml
# In deployment_groups: -> modules:

- id: debug_nodeset
  source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset
  use: [network] # Depends on the network module
  settings:
    node_count_dynamic_max: 4
    machine_type: n2-standard-2

- id: compute_nodeset
  source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset
  use: [network]
  settings:
    node_count_dynamic_max: 20
    machine_type: c2-standard-60
    bandwidth_tier: gvnic_enabled # Enables higher networking performance
```

source: Points to the schedmd-slurm-gcp-v6-nodeset module, which is the standard for creating Slurm compute nodes with Slurm-GCP v6.

node_count_dynamic_max: Specifies the maximum number of nodes the partition can autoscale to.

machine_type: Defines the Google Compute Engine machine type for the nodes in this set. Google Drive icon

2. Define Slurm Partitions The partition module takes a nodeset and formally defines it as a Slurm partition with a specific name and properties.

```yaml
# In deployment_groups: -> modules:

- id: debug_partition
  source: community/modules/compute/schedmd-slurm-gcp-v6-partition
  use:
    - debug_nodeset
  settings:
    partition_name: debug
    is_default: true # Makes this the default partition for jobs

- id: compute_partition
  source: community/modules/compute/schedmd-slurm-gcp-v6-partition
  use:
    - compute_nodeset
  settings:
    partition_name: compute
```

source: Uses the schedmd-slurm-gcp-v6-partition module.

use: This module depends on the corresponding nodeset module defined previously. Google Drive icon

partition_name: The name that users will specify when submitting jobs (e.g., sbatch -p compute). Google Drive icon

3. Define the Slurm Controller The slurm_controller module is the core of the scheduler. It brings together the network, shared storage, and all defined partitions. A login node is also typically defined for user access and depends on the controller.

```yaml
# In deployment_groups: -> modules:

- id: homefs # Shared home directory using Filestore
  source: modules/file-system/filestore
  use: [network, private_service_access]
  settings:
    local_mount: /home

- id: slurm_login
  source: community/modules/scheduler/schedmd-slurm-gcp-v6-login
  use: [network]
  settings:
    machine_type: n2-standard-4
    enable_login_public_ips: true

- id: slurm_controller
  source: community/modules/scheduler/schedmd-slurm-gcp-v6-controller
  use:
    - network
    - debug_partition
    - compute_partition
    - homefs
    - slurm_login
  settings:
    enable_controller_public_ips: true
```

source: Points to the schedmd-slurm-gcp-v6-controller module.

use: The controller module lists its dependencies, which crucially include all the partition modules (debug_partition, compute_partition), a shared file system (homefs), and the login node (slurm_login). Google Drive icon

This linkage is what configures the controller to manage those specific partitions.

Complete Blueprint Example Here is a condensed example of a hpc-slurm.yaml blueprint that defines a Slurm cluster with a debug and a compute partition.

```yaml
blueprint_name: hpc-slurm

vars:
  project_id: ## Set GCP Project ID Here ##
  deployment_name: hpc-slurm-cluster
  region: us-central1
  zone: us-central1-a

deployment_groups:
  - group: primary
    modules:
      # 1. Networking
      - id: network
        source: modules/network/vpc
      - id: private_service_access
        source: community/modules/network/private-service-access
        use: [network]

      # 2. Shared Storage for /home
      - id: homefs
        source: modules/file-system/filestore
        use: [network, private_service_access]
        settings:
          local_mount: /home

      # 3. Define Nodesets
      - id: debug_nodeset
        source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset
        use: [network]
        settings:
          node_count_dynamic_max: 4
          machine_type: n2-standard-2

      - id: compute_nodeset
        source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset
        use: [network]
        settings:
          node_count_dynamic_max: 20
          machine_type: c2-standard-60
          bandwidth_tier: gvnic_enabled

      # 4. Define Partitions
      - id: debug_partition
        source: community/modules/compute/schedmd-slurm-gcp-v6-partition
        use: [debug_nodeset]
        settings:
          partition_name: debug
          is_default: true

      - id: compute_partition
        source: community/modules/compute/schedmd-slurm-gcp-v6-partition
        use: [compute_nodeset]
        settings:
          partition_name: compute

      # 5. Define Login and Controller Nodes
      - id: slurm_login
        source: community/modules/scheduler/schedmd-slurm-gcp-v6-login
        use: [network]
        settings:
          machine_type: n2-standard-4
          enable_login_public_ips: true

      - id: slurm_controller
        source: community/modules/scheduler/schedmd-slurm-gcp-v6-controller
        use:
          - network
          - debug_partition
          - compute_partition
          - homefs
          - slurm_login
        settings:
          enable_controller_public_ips: true
```

To deploy this configuration, you would use the gcluster command provided by the HPC Toolkit. The toolkit processes this YAML file, assembles the necessary Terraform code, and deploys a fully configured Slurm cluster.
