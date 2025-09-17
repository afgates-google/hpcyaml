Uncovering Valid VM and Accelerator Pairings in Google Cloud To programmatically determine the valid combinations of Virtual Machine (VM) types and accelerator types (GPU/TPU) available in a specific Google Cloud zone, you can leverage the Google Cloud CLI (gcloud) and the Google Cloud API. The approach differs slightly for GPUs and TPUs due to their distinct provisioning models.

Graphics Processing Units (GPUs) For GPUs, the key is to inspect the properties of machine types within a given zone. Some machine families, known as accelerator-optimized, come with pre-attached GPUs, while general-purpose machine types may support attaching specific GPU models.

Using the gcloud Command-Line Tool You can achieve this by combining two gcloud commands: gcloud compute machine-types list and gcloud compute machine-types describe.

List all machine types in a specific zone: To get a list of all available machine types in a desired zone, you can use the following command. This is useful for iterating through each machine type to check for accelerator compatibility.

bash gcloud compute machine-types list --filter="zone:( us-central1-a )" Describe a specific machine type to find compatible GPUs: For each machine type obtained from the list, you can use the describe command with the --format flag to display its properties in a machine-readable format like JSON. The output will contain an accelerators field if the machine type supports any GPUs.

bash gcloud compute machine-types describe n1-standard-8 --zone us-central1-a --format="json(name, accelerators)" If the n1-standard-8 machine type in us-central1-a supports GPUs, the output will look something like this, indicating the type and maximum number of GPUs that can be attached:

JSON { "accelerators": [ { "guestAcceleratorCount": 1, "guestAcceleratorType": "nvidia-tesla-k80" }, { "guestAcceleratorCount": 2, "guestAcceleratorType": "nvidia-tesla-k80" }, ... ], "name": "n1-standard-8" } For accelerator-optimized machine types like the A2, A3, and G2 series, the GPUs are pre-attached and an integral part of the machine type itself.

Describing these machine types will show the specific GPU model and count.

Using the Google Cloud API Programmatically, you can achieve the same result by making calls to the Compute Engine API.

List Machine Types: Use the machineTypes.list method to retrieve a list of machine types for a specific zone.

Get Machine Type Details: For each machine type, use the machineTypes.get method. The response object will contain an accelerators array, which lists the supported GPU configurations for that machine type.

Tensor Processing Units (TPUs) TPUs in Google Cloud are provisioned as nodes (for the legacy TPU Node architecture) or as TPU VMs. With TPU VMs, you get direct SSH access to the host machine. To find valid combinations, you need to identify the available TPU types and their corresponding supported VM configurations in a zone.

Using the gcloud Command-Line Tool List available TPU types in a zone: You can list the TPU accelerator types available in a specific zone using the gcloud compute tpus accelerator-types list command.

bash gcloud compute tpus accelerator-types list --zone=us-central1-a This will return a table of available accelerator types, including their name and the number of TPU chips and cores.

List available TPU VM runtime versions: When creating a TPU VM, you also need to specify a software version. You can list the available runtime versions for TPUs in a zone.

bash gcloud compute tpus versions list --zone=us-central1-a Determine compatible VM types: The specific VM type (e.g., n2-standard-4) is often tied to the TPU type and is managed by the Cloud TPU service. When you create a TPU VM, you specify the accelerator type, and Google Cloud provisions the appropriate underlying VM. The documentation for each TPU version and type often specifies the host machine's characteristics.

Using the Google Cloud API You can interact with the Cloud TPU API to get information about available TPU types and locations.

List Locations and Available TPUs: Use the tpu.projects.locations.list and tpu.projects.locations.acceleratorTypes.list methods to discover which TPU types are available in which zones.

Get Accelerator Type Details: The tpu.projects.locations.acceleratorTypes.get method can provide more details about a specific TPU type.

By combining the information from these commands and API calls, you can build a comprehensive map of the valid VM and accelerator combinations available in any given Google Cloud zone. You can programmatically determine the valid combinations of VM types and accelerator (GPU/TPU) types available in a specific Google Cloud zone by using a combination of gcloud command-line tool commands and referencing the official Google Cloud documentation. There isn't a single command that provides this information directly, but you can follow this two-step process:

Step 1: List Available Accelerator Types in a Zone First, identify the accelerator types (GPUs and TPUs) available in the specific zone you are interested in. You can achieve this using the gcloud compute accelerator-types list command with a filter for the desired zone.

For example, to list all accelerator types available in the us-central1-a zone, run the following command:

bash gcloud compute accelerator-types list --filter="zone:( us-central1-a )" This command will return a list of accelerator types, such as nvidia-tesla-t4, nvidia-tesla-v100, etc., that are available in that zone. Google Drive icon

Step 2: Determine Compatible Machine Types Once you have the list of available accelerator types, you need to determine which VM machine types are compatible with them.

For Accelerator-Optimized Machine Types (A-series, G-series) Some machine series, known as accelerator-optimized machine types (like A4, A3, A2, and G2), come with a specific GPU model pre-attached. To find the availability of these, you can list the machine types for the zone.

For example, to find if the a3-highgpu-8g machine type (which has NVIDIA H100 GPUs) is available in us-central1-a, you can run:

bash gcloud compute machine-types list --filter="name=a3-highgpu-8g AND zone:( us-central1-a )" For General-Purpose N1 Machine Types For the N1 machine series, you can attach a variety of GPU models. To find the valid combinations, you need to cross-reference the available accelerator types from Step 1 with the list of N1 machine types in that zone.

First, list the N1 machine types in the zone:

bash gcloud compute machine-types list --filter="name:n1- AND zone:( us-central1-a )" Then, you can consult the GPU machine types documentation to see the compatibility between the N1 series and the available GPUs you found in Step 1. The documentation provides detailed tables showing which N1 machine types support which GPUs and in what quantity.

Putting It All Together Programmatically To automate this, you can create a script that:

Executes gcloud compute accelerator-types list for a given zone and parses the output to get a list of accelerator names.

For each accelerator name, queries the GPU regions and zones documentation or a cached version of it to find the compatible machine series (e.g., N1, A2).

Executes gcloud compute machine-types list for the same zone, filtering by the compatible machine series.

The result is the list of valid VM and accelerator combinations for that zone.

Using the API For a more programmatic approach without relying on parsing gcloud output, you can use the Google Cloud API directly. The equivalent API calls would be:

acceleratorTypes.list to get available accelerator types in a zone.

machineTypes.list to get available machine types in a zone.

You would still need to implement the logic to cross-reference the compatibility based on the information from the Google Cloud documentation. There is no "Does this combination of features exist?" API. Yaqs icon
