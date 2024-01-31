## Cowshed Project(Flask + Azure Function)


### endpoint

- Retrieve all

    GET /cows

    Return a list of all cows.
    
```json
    [
        {
            "name": "Betty",
            "sex": "Male",
            "birthdate": "2019-02-11T03:21:00.000000",
            "condition": "Healthy",
            "weight": {
                "mass_kg": 1100,
                "last_measured": "2022-11-02T11:15:00.000000"
            },
            "feeding": {
                "amount_kg": 5,
                "cron_schedule": "0 */6 * * *",
                "last_measured": "2022-11-02T11:00:00.000000"
            },
            "milk_production": {
                "last_milk": "2022-11-02T09:00:00.000000",
                "cron_schedule": "0 8,12,16,20 * * *",
                "amount_l": 5
            },
            "has_calves": true
        },
    ]
```
- Retrieve one

    GET /cow/{cow_id}

    Return a specific cow by cow_id.

```json
    {
        "name": "Betty",
        "sex": "Male",
        "birthdate": "2019-02-11T03:21:00.000000",
        "condition": "Healthy",
        "weight": {
            "mass_kg": 1100,
            "last_measured": "2022-11-02T11:15:00.000000"
        },
        "feeding": {
            "amount_kg": 5,
            "cron_schedule": "0 */6 * * *",
            "last_measured": "2022-11-02T11:00:00.000000"
        },
        "milk_production": {
            "last_milk": "2022-11-02T09:00:00.000000",
            "cron_schedule": "0 8,12,16,20 * * *",
            "amount_l": 5
        },
        "has_calves": true
    },
```

- Create one

    POST /cow
    
    Add the info of new cow to database.

- Update one

    POST /cow/{cow_id}
    
    update a specific cow's info by cow_id.

- Delete one

    DELETE /cow/{cow_id}
    
    update a specific cow's info by cow_id.

### Settings

Attach your own postres uri on .env file.

```
    DATABASE_URL = "postgresql://USERNAME:PASSWORD@ADDRESS:5432/DATABASE_NAME"
```


### How to test in local environment.

1. Create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate it.

2. Run the command below to install the necessary requirements.

    ```log
    python3 -m pip install -r requirements.txt
    ```

3. If you are using VS Code for development, click the "Run and Debug" button or follow [the instructions for running a function locally](https://docs.microsoft.com/azure/azure-functions/create-first-function-vs-code-python#run-the-function-locally). Outside of VS Code, follow [these instructions for using Core Tools commands directly to run the function locally](https://docs.microsoft.com/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Cpython%2Cportal%2Cbash#start).

4. Once the function is running, test the function at the local URL displayed in the Terminal panel:

    ```log
    Functions:
            http_app_func: [GET,POST,DELETE,HEAD,PATCH,PUT,OPTIONS] http://localhost:7071//{*route}
    ```

    ```log
    Functions:
            WrapperFunction: [GET,POST] http://localhost:7071/{*route}
    ```

    Try out URLs corresponding to the handlers in the app, both the simple path and the parameterized path:

    ```
    http://localhost:7071/cows
    ```
    
    Or you can use swagger to test endpoint with following urls.

    ```
    http://localhost:7071/docs
    ```
    

### How to Deploy to Azure

There are three main ways to deploy this to Azure:

* [Deploy with the VS Code Azure Functions extension](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python#publish-the-project-to-azure). 
* [Deploy with the Azure CLI](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser#create-supporting-azure-resources-for-your-function).
* Deploy with the Azure Developer CLI: After [installing the `azd` tool](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd?tabs=localinstall%2Cwindows%2Cbrew), run `azd up` in the root of the project. You can also run `azd pipeline config` to set up a CI/CD pipeline for deployment.

All approaches will provision a Function App, Storage account (to store the code), and a Log Analytics workspace.

[Azure resources created by the deployment: Function App, Storage Account, Log Analytics workspace]

### Testing in Azure

Once deployed, test different paths on the deployed URL, using either a browser or a tool like Postman.

```
 http://<FunctionAppName>.azurewebsites.net/cow
```