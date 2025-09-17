Blueprint for High-Performance, Tightly-Coupled Training on Google Cloud For organizations leveraging Google Cloud for demanding, multi-node, tightly-coupled training workloads, the Google Cloud Cluster Toolkit provides a streamlined method for deploying complex, high-performance computing environments. This is achieved through a declarative YAML blueprint that defines the entire cluster configuration.

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

    capacity\_gb: 12288 # 12 TiB deployment\_type: "SCRATCH\_SSD" # Options include "SCRATCH\_SSD" and "PERSISTENT\_SSD\_250" use:

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

  - id: slurm\_partition source: modules/scheduler/slurm-partition settings: partition\_name: "a3-highgpu" machine\_type: "a3-highgpu-8g" # A3 VM with 8 H100 GPUs

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

    node\_count: static: 2 # Example: 2 nodes for a total of 16 H100 GPUs use:



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

# These should be overridden at deployment time using a deployment file or --vars flag.

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

  - id: private\_service\_access source: community/modules/network/private-service-access use: [network]

  # Module for a shared home directory using Filestore.

  - id: homefs source: modules/file-system/filestore use: [network, private\_service\_access] settings: local\_mount: /home

  # Module for a high-performance Lustre file system for scratch space.

  # This requires a license from the Google Cloud Marketplace.

  - id: scratchfs source: community/modules/file-system/DDN-EXAScaler use: [network] settings: local\_mount: /scratch

  # Defines the compute nodes for the A3 partition.

  - id: a3\_nodeset source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset use: [network] settings: machine\_type: a3-highgpu-8g node\_count\_dynamic\_max: 16 # Maximum number of nodes to autoscale to. node\_count\_static: 0 # Number of nodes to be always on. placement\_policy: "COMPACT" # Minimizes latency between nodes. bandwidth\_tier: "tier\_1\_enabled" # Enables high-bandwidth networking. instance\_image: family: "hpc-rocky-linux-8" # Using a standard HPC-optimized image. project: "cloud-hpc-image-public"

  # Defines the Slurm partition for the A3 compute nodes.

  - id: a3\_partition source: community/modules/compute/schedmd-slurm-gcp-v6-partition use: [a3\_nodeset] settings: partition\_name: a3 is\_default: true

  # Defines the login node for the cluster.

  - id: slurm\_login source: community/modules/scheduler/schedmd-slurm-gcp-v6-login use: [network] settings: machine\_type: n2-standard-4 enable\_login\_public\_ips: true # Set to false if using a bastion host or IAP.

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

    cloud\_parameters: resume\_timeout: 1200 # Increased timeout for A3 node startup. suspend\_timeout: 600

How to Deploy Save the blueprint: Save the YAML content above into a file named a3-lustre-slurm-blueprint.yaml.

Create a deployment file: It is a best practice to create a separate deployment file to specify variables for a particular deployment. Create a file named my-a3-cluster.yaml with the following content, replacing the placeholder values with your specific information:

yaml vars: project\_id: "your-gcp-project-id" deployment\_name: "a3-training-cluster-01" region: "us-central1" zone: "us-central1-a" Create the deployment folder: Run the gctcli create command to generate the Terraform deployment files from your blueprint. Google Drive icon

bash ./gcluster create my-a3-cluster.yaml -b a3-lustre-slurm-blueprint.yaml Deploy the cluster: Use the gctcli deploy command to provision the resources on Google Cloud. This process will take several minutes.

bash ./gcluster deploy a3-training-cluster-01 Access and use the cluster: Once the deployment is complete, you can SSH into the login node and start submitting jobs to the Slurm scheduler. The A3 compute nodes will be automatically created and provisioned as jobs are submitted to the a3 partition.

This blueprint provides a robust and scalable foundation for the most demanding multi-node, tightly-coupled training jobs on Google Cloud, leveraging the full power of A3 VMs with H100 GPUs, high-speed networking, and a parallel file system.
