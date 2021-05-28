# Contributing

To contribute, [fork](https://www.dynatrace.com/support/help/dynatrace-api) this repository and clone it.  

### Setting up your environment 


```shell
git clone git@github.com:<your_username>/api-client-python.git
cd api-client-python.git
```

After that, create a python virtual environment, this project needs at minimum `python 3.6`.  
Your favorite IDE can also do this for you, to do it manually you could run:  

```shell
python -m venv .venv
source .venv/bin/activate # On linux
# On Windows Poweshell:  .venv/Scripts/Activate.ps1
# On Windows cmd: .venv/Scripts/activate.bat
```

Install the dev requirements:

```shell
pip install -r requirements_dev.txt
```

Make sure tests pass:

```shell
pytest -v 
```

### Adding new endpoints

The project is structured in mainly three folders, one for each Dynatrace REST API.

```
dynatrace/configuration_v1
dynatrace/environment_v1
dynatrace/environment_v2
```

If you would like to add a new endpoint, first create a file in the appropriate API folder, **use plural for the file name**

Example: `activegates` under `environment_v2` will handle the [Activegate endpoints](https://www.dynatrace.com/support/help/dynatrace-api/environment-api/activegates/)
 

Each file should map to a `tag` in our schema, or a `doc session` if you are looking at the Swagger docs.  

For example, the `activegates` file should implement `GET /api/v2/activegates` and `GET /api/v2/activegates/{activegate_id}`

Each tag implements a `service`, such as: `ActivegateService`, and the methods are defined inside this service.

Example:

`ActiveGateService.list() -> Implements the /api/v2/activegates request`  
`ActiveGateService.get(activegate_id: str) -> Implements the /api/v2/activegates/{activegate_id} request`

Then, on `main.py` the `Dynatrace` class needs to expose this service for our users:

`self.activegates: ActiveGateService = ActiveGateService(self.__http_client)`

### Typing

The whole point of this client is to be easy to use and have good type annotations, so that users that are not familiar with our API schemas can still use it.

Always create classes that match directly to the Dynatrace schema definitions, we suggest that you download the schema specs at 

* `https://your_tenant_url/rest/v2/rest-api-docs/config/v1/spec3.json`
* `https://your_tenant_url/rest/v2/rest-api-docs/v1/spec3.json`
* `https://your_tenant_url/rest/v2/rest-api-docs/v2/spec3.json`

So that you can easily access them during development, copy classes names, etc, another option is to use the Swagger pages. 
**Do not use the Dynatrace docs as the source of the data**  
  
You can take a look at the activegate implementation mentioned above for how to implement types.

### Generating test data

While developing, you can copy the `dev_helper.py` script to locally test your code.  
This script uses `wrapt` to implement extra functionality to the http client, it makes it spit the raw json responses you get from Dynatrace to `test/mock_data`  

This makes it easier to write your tests, as you will generate mock data automatically as you are using your methods.

This script expects two environment variables to be set to work:

* `DYNATRACE_TENANT_URL`
* `DYNATRACE_API_TOKEN`

You can also hardcode these values in your own local copy if you prefer, **just be sure NOT to commit this file to Github and expose your credentials**

### Writing tests

Create a file called `test_{file_name}` in the appropriate folder under `test`, it follows the same structure as the `dynatrace` folder  
The goal is to test that your code correctly parses the json responses, and create valid objects of the correct types.  
  
Every test receives a `dt` fixture automatically, this is a Dynatrace instance that reads from `test/mock_data` instead of making http requests 


Example for a test for the `list` method of `ActivegateService`:

```python
def test_list(dt: Dynatrace):
    activegates = dt.activegates.list()
    assert isinstance(activegates, PaginatedList)

    for activegate in activegates:
        assert isinstance(activegate, Activegate)
        assert activegate.id == "my_id"
        assert activegate.os_type == OSType.LINUX
        ...
```

Write tests for all methods you have implemented, be sure to test all possible variations of the parameters you accept, example if you accept a `datetime` or a `str` for a parameter, test both.

When it is done, you can create a pull request with your changes, we will review it, maybe ask for changes and approve it!

### Thanks for contributing!