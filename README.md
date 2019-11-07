# ArchivesSpace Python Client

[![PyPI version](https://badge.fury.io/py/aspace-client.svg)](https://badge.fury.io/py/aspace-client)

The `aspace-client` Python package provides web client functionality that
targets the API of ArchivesSpace v2.X and up. This package was developed
to aid ongoing and future ArchivesSpace migrations.


## About

The `aspace` module extends the functionality of the `Session` class from the
`requests` Python library, and attempts to provide access to all of
ArchivesSpace's REST API endpoints, while also preserving backwards
compatibility and supporting development tools such as Pylint. ArchivesSpace
currently (May 2019) has over 250 API endpoints. Supporting and maintaining all
of those endpoints is quite an undertaking, so new features and bug-fixes are
prioritized based on their value to performing ongoing ArchivesSpace migrations.


## Installation

[This project has a listing on PyPI!](https://pypi.org/project/aspace-client/)

```bash
pip install aspace-client
```

You can also install this project directly from the GitHub repository:

```bash
pip install https://github.com/AtlasSystems/ArchivesSpace-Python-Client/zipball/master
```


## Developer Installation

Below are instructions for installing this package in "editable" mode. This
will allow you to make changes to the package and test them in real time.

```bash
AS_CLIENT_DIR="/path/to/aspace-client"
git clone https://github.com/AtlasSystems/ArchivesSpace-Python-Client.git "$AS_CLIENT_DIR"

# In your python project directory, or in your venv
pip install -e "$AS_CLIENT_DIR"
```


## Usage

```python
from aspace.client import ASpaceClient

client = ASpaceClient('http://localhost:8089', 'admin', 'admin')
```

This will initialize a client that targets the instance of your ArchivesSpace
API. This initialization will also automatically authenticate your user. There
is an option to turn this off, if you're using this package as part of a
larger script, where interacting with ArchivesSpace is not the primary
component, and you're in an environment where it is not 100% certain that
ArchivesSpace is running and accessible. For that operation:

```python
from time import sleep
from aspace.client import ASpaceClient

client = ASpaceClient(
    base_url='http://localhost:8089', # Base url for connecting to your ASpace's API.
    username='admin',
    password='admin',
    auto_authenticate=False,
)

while client.get('/version').status_code != 200:
    print('ArchivesSpace API is not up')
    sleep(2)

client.authenticate()
```

There is also built-in support for the operation above, as well as built-in
functionality for pulling settings from an instance of ConfigParser.

In settings.ini:

```ini
[aspace_credentials]
api_host = 'http://aspace.cloudapp.eastus.azure.com'
username = 'automation-user'
password = 'automation-user-password'
```

In app.py:

```python
import configparser

import aspace

config = configparser.ConfigParser()
config.load('settings.ini')

client = (
    aspace.client.ASpaceClient
    .init_from_config(config)
    .wait_until_ready(
        check_interval=2.0,
        max_wait_time=200.0,
        authenticate_on_success=True,
    )
)
```

Failed authentications raise an error, so if any of these scripts are still
running, you're ready to query the API! This package interacts with the
ArchivesSpace API using the following considerations.

1. the syntax described by the `requests` Python library that we all love and
2. the API endpoint structure described by the docs for the ArchivesSpace API

The typical syntax of the `requests` Python library is preserved, so all HTTP
methods (POST, GET, DELETE, etc.) typically start with a URI or an endpoint,
relative to the base URL of the API. The URI is never assumed to make sure 
that all operations are predictable, and that all of the functionality of the
API is utilized correctly.

### Get ArchivesSpace System Info

```python
# Get the system info
print(client.get('/').json())
```

### Manage Repositories

```python

# Get a listing of all repositories
repositories = client.get('/repositories').json()
for repository in repositories:
    print(repository)

# Create a new repository
new_repo = {}
new_repo['repo_code'] = 'test_repo'
new_repo['name'] = 'Test Repository'
response = client.post('/repositories', json=new_repo).json()

# Update the name of that repository
repo = client.get(response['uri']).json()
repo['name'] = 'Andy Samberg University Archives - Test Repository'
client.post(repo['uri'], json=repo)

# Delete the repository
client.delete(new_repo['uri'])
```

This syntax can be used to interact with all of ArchivesSpace's endpoints, as
long as the response comes back as JSON. Most do. There are also some
extensions to ArchivesSpace's API functionality that are currently provided.

### Streaming Records

```python
# Manage your resource records one at a time, no matter how many you have
for resource in client.stream_records().resources():
    if resource['title'].endswith('!'):
        # Remove trailing spaces and 
        print('Cleaning Resource:', resource['uri'], resource['title'])
        resource['title'] = resource['title'].rstrip('!')
        update_result = client.post(resource['uri'], json=resource).json()
        print(update_result)

# Works for accessions and agents
client.stream_records().accessions()
client.stream_records().people()
client.stream_records().corporate_entities()
client.stream_records().families()
client.stream_records().software()
client.stream_records().all_agents()


# Works for endpoints that do not have an explicitly defined stream method
client.stream_records().records('container_profiles'):
    pass

# Works for endpoints that do not have an explicitly defined stream method
# and require a repository reference in the URI.
for assessment in client.stream_records().repository_records('assessments'):
    pass

# Optional limits can be placed on record streams, so that only 1 repository
# is considered, as opposed to streaming all records from all repositories,
# which is default.
assessments_stream = client.stream_records().repository_records(
    'assessments',
    repository_uris=['/repositories/2']
)

for assessment in assessments_stream:
    pass
```

### User Management

```python
# Change all of your user's passwords to "something really complicated"
client.manage_users().change_all_passwords(
    'pa$$w0rd',
    include_admin=True
)

# Randomize all of your non-admin user's passwords
import string
import random

def random_password():
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(25)
    )

# The same password for every user
client.manage_users().change_all_passwords(
    new_password=random_password(),
    include_admin=False,
)

# Different password for every user
client.manage_users().change_all_passwords(
    new_password=lambda user: random_password(),
    include_admin=False,
)
```


## Contributing

If you have any suggestions or bug reports please feel free to report them in
[the issues tab](https://github.com/AtlasSystems/ArchivesSpace-Python-Client/issues) 
or email us at [devgineers@atlas-sys.com](mailto:devgineers@atlas-sys.com).
Feel free to email us if you are new to Git, but would still like to 
contribute.

Pull requests are welcome, but they will subject to a review process.
Consistent code style is a goal for this project, as it currently 
attempts to follow the coding standards layed out in the 
[PEP8 Python style guide](https://www.python.org/dev/peps/pep-0008/).
Please keep this in mind when submitting or requesting contributions,
but also keep in mind that PEP is a flexible standard and that we are 
willing to make exceptions.
