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

Example API Request Filtering: To get a list of SKUs for Compute Engine, you can use a GET request like the following, where YOUR_API_KEY is your API key:

GET https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus?key=YOUR_API_KEY To further refine the results, you can use the filter parameter. For instance, to find SKUs related to a specific machine type in a particular region, you would need to parse the descriptions of the returned SKUs.

Alternative: Using Third-Party Tools For a more streamlined approach, you can consider using open-source tools like Infracost.

Infracost is designed to work with Infrastructure as Code (IaC) tools like Terraform and can analyze your configuration files to provide cost estimates.

While it primarily supports Terraform, its underlying logic for mapping resources to prices can serve as a valuable reference. Infracost can be integrated into your CI/CD pipeline to automatically show the cost impact of infrastructure changes.

By following these steps, you can programmatically and accurately estimate the monthly costs of your HPC resources on Google Cloud, enabling better budget planning and cost management.
