You can get a list of available GPU and TPU types in a specific Google Cloud zone using the gcloud command-line tool or the Google Cloud Compute API. Here’s a breakdown of how to accomplish this for both accelerator types.

Graphics Processing Units (GPUs) To accelerate your machine learning, data processing, and graphics-intensive workloads, Google Cloud offers a variety of NVIDIA GPU models. You can determine their availability in specific zones through the following methods.

Using the gcloud Command-Line Tool The gcloud compute accelerator-types list command is the primary way to discover available GPU types. You can filter the results by a specific zone to see what is offered in that location.

Command:

bash gcloud compute accelerator-types list --filter="zone:( us-central1-a )" Example Output: This command will return a table with details about the accelerator types available in the specified zone, including their name and description.

You can also view a broader list of GPU availability across different regions and zones.

Using the Google Cloud Compute API For programmatic access, you can use the acceleratorTypes.list method from the Compute Engine API. This method retrieves a list of accelerator types available to your project in a specified zone.

API Request: Make a GET request to the following URI, replacing my-project and us-central1-a with your project ID and desired zone:

https://compute.googleapis.com/compute/v1/projects/my-project/zones/us-central1-a/acceleratorTypes Response Body: The response will be a JSON object containing a list of accelerator types for the given zone. Each entry will include details such as the name, description, and maximumCardsPerInstance.

Tensor Processing Units (TPUs) Google Cloud's custom-designed TPUs are built to accelerate machine learning workloads. Discovering their availability is slightly different from GPUs.

Using the gcloud Command-Line Tool To see the available TPU types and their details within a specific zone, you can use the gcloud compute tpus tpu-vm commands. While there isn't a single command to list all types in a zone, you can list existing TPUs or check locations.

A more direct way to see what is offered is to consult the official Google Cloud documentation, which provides tables detailing the availability of different TPU versions (like v2, v3, v4, and v5e) in various zones.

To list available TPU locations, you can use:

bash gcloud compute tpus locations list And to list your existing TPU nodes in a specific zone:

bash gcloud compute tpus list --zone=us-central1-a When creating a TPU, you specify the accelerator type. If the type is not available in that zone, the command will fail, indirectly indicating availability.

Using the Google Cloud Compute API Similar to the gcloud tool, the Compute Engine API for TPUs focuses more on managing existing resources and discovering locations rather than listing available types in a zone directly.

You can list available locations for TPUs by making a GET request to:

https://tpu.googleapis.com/v2/projects/my-project/locations This will return a list of regions and zones where TPUs are available. To determine the specific types available in each zone, you would typically refer to the Google Cloud documentation, which maintains an updated list of TPU availability by region and zone.

You can get a list of available GPU and TPU types in a specific Google Cloud zone using the gcloud command-line tool and the Google Cloud API. Here are the methods for each:

Graphics Processing Units (GPUs) You can list available GPU types, which are referred to as accelerator types in Google Cloud.

Using the gcloud command-line tool To get a list of available GPU accelerator types for a specific zone, use the gcloud compute accelerator-types list command with a filter for the desired zone.

Command:

bash gcloud compute accelerator-types list --filter="zone:(ZONE)" Replace ZONE with the name of the zone you are interested in, for example, us-central1-a.

This command will return a table of the accelerator types available in that zone, including a description of the GPU model.

Using the Google Cloud Compute API You can programmatically retrieve a list of available GPU types by making a GET request to the acceleratorTypes.list method of the Compute Engine API. You will need to specify the project and the zone.

API Request:

GET https://compute.googleapis.com/compute/v1/projects/PROJECT_ID/zones/ZONE/acceleratorTypes Replace PROJECT_ID with your project ID and ZONE with the desired zone.

You can also use the aggregatedList method to get a list of all accelerator types across all zones.

Tensor Processing Units (TPUs) Similarly, you can list the available TPU types for a specific zone.

Using the gcloud command-line tool To list the available TPU accelerator types in a specific zone, you can use the gcloud compute tpus accelerator-types list command.

Command:

bash gcloud compute tpus accelerator-types list --zone=ZONE Replace ZONE with the name of the zone you want to check.

This will provide a list of the TPU types available for provisioning in that zone.

For TPU VMs, you can also use the following command:

bash gcloud compute tpu-vm accelerator-types list --zone=ZONE Using the Google Cloud TPU API To get a list of available TPU types via the API, you can use the acceleratorTypes.list method from the Cloud TPU API.

API Request (v2):

GET https://tpu.googleapis.com/v2/projects/PROJECT_ID/locations/ZONE/acceleratorTypes Replace PROJECT_ID with your project ID and ZONE with the desired zone.

This API endpoint will return a list of the accelerator types available in the specified location. The TPU API also provides methods to list available TensorFlow and runtime versions.
