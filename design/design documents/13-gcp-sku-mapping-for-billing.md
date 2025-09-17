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

def get_vm_component_skus(api_key, machine_type, gpu_type, region):
    """ Maps a Google Cloud VM instance and an attached GPU to their component SKUs.

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
