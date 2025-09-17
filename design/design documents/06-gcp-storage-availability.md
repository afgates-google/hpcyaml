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

When creating an instance, you must specify a zone using the --location flag. Google Drive icon

Parallelstore Similarly, to find out where Parallelstore is available, you can use the locations list command for that service.

To list the supported locations for Parallelstore:

bash gcloud parallelstore locations list Parallelstore is a zonal service available in the following regions: asia-east1, asia-southeast1, europe-north1, europe-west1, europe-west4, us-central1, us-east1, us-east4, us-east5, us-west1, us-west2, us-west3, and us-west4. Google Drive icon

Using APIs For programmatic access, you can use the REST APIs for each service to query for available locations. This is useful for building automation or custom tools. Google Drive icon

Filestore API: You can make a GET request to the https://file.googleapis.com/v1/projects/{projectId}/locations endpoint.

Managed Lustre API: Use a GET request to the https://lustre.googleapis.com/v1/projects/{projectId}/locations endpoint.

Parallelstore API: A GET request to the https://parallelstore.googleapis.com/v1/projects/{projectId}/locations endpoint will list the available locations.

Consulting the Official Documentation Google Cloud provides official documentation that lists the supported regions and zones for its services. This is a reliable way to get up-to-date information.

Google Cloud Managed Lustre Supported Locations: This document provides a complete list of available regions and zones.

Parallelstore Supported Locations: This page details the specific regions and zones where Parallelstore can be provisioned.

Google Cloud NetApp Volumes Locations: For users of NetApp Volumes, this document lists the supported regions.

By using a combination of gcloud commands and checking the official documentation, you can accurately determine the availability of these high-performance storage services for your desired Google Cloud regions and zones.
