# Azure Function to Convert Excel to CSV

## Prerequisites

* Install VS Code
* See the steps for creating and deploying an [Azure Python Function](https://docs.microsoft.com/en-us/azure/python/tutorial-vs-code-serverless-python-01)
  * Installing [Az Func Core Tools](https://docs.microsoft.com/en-us/azure/python/tutorial-vs-code-serverless-python-01#azure-functions-core-tools)
  * Installing the [VS Code Az Func Extension](https://docs.microsoft.com/en-us/azure/python/tutorial-vs-code-serverless-python-01#visual-studio-code-python-and-the-azure-functions-extension)
* Create an [Event Grid Subscription for your Azure Function](https://docs.microsoft.com/en-us/azure/event-grid/subscribe-through-portal).
* Create your storage account and the input and output containers for your excels and csv.
* Update your local.settings.json file to the below with values filled in.

## local.settings.json

    {
    "IsEncrypted": false,
    "Values": {
        "AzureWebJobsStorage": "",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "STORAGE_CONNECTION": "DefaultEndpointsProtocol=https;AccountName=XXXXX;AccountKey=XXXX;EndpointSuffix=core.windows.net",
        "INPUT_CONTAINER":"XXXX",
        "OUTPUT_CONTAINER":"XXX"
    }
    }
