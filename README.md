# ArchivesSpace Python Client

[![Build Status](https://travis-ci.org/AustinTSchaffer/ArchivesSpace-Python-Client.svg?branch=master)](https://travis-ci.org/AustinTSchaffer/ArchivesSpace-Python-Client)

The `aspace-client` Python package provides web client functionality that
targets the API of ArchivesSpace v2.X and up. This package was developed
to aid ongoing and future ArchivesSpace migrations.

## About

The `aspace` module primarily extends the functionality of the `Session` class
from the `requests` Python library, and attempts to provide access to many of
ArchivesSpace's commonly used endpoints, while also preserving backwards
compatibility and supporting development tools such as Pylint. ArchivesSpace
currently (June 2018) has over 250 API endpoints. Supporting and maintaining
all of those endpoints is quite an undertaking, so features are being
prioritized based on their value to performing ongoing ArchivesSpace
migrations, as well as supporting and researching aspects related to those
ArchivesSpace migrations.


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
client = ASpaceClient(
    base_url='http://localhost:8089', # Base url for connecting to your ASpace's API.
    username='admin',
    password='admin',
    auto_authenticate=False,
)
```

Failed authentications raise an error, so if the script is still running,
you're ready to query the API! These operations use both

1. the syntax layed out by the `requests` Python library that we all love and
2. the endpoint structure layed out by the ArchivesSpace API docs

```python
# Get the system info
client.get('/').json()
```

```python
# Manage your repositories
repositories = client.get('/repositories').json()

for repo in repositories:
    print(repo)

new_repo_response = client.post(
    '/repositories',
    {
        'repo_code': 'test_repo', 
        'name': 'Test Repository'
    }).json()

new_repo = client.get(new_repo_response['uri']).json()
new_repo['name'] += '!!!'

update_repo_response = client.post(
    new_repo['uri'], new_repo).json()
```

This syntax can be used to interact with all of ArchivesSpace's endpoints, as
long as the response comes back as JSON. Most do. There are also some
extensions to ArchivesSpace's API functionality that are currently provided.

```python
for resource in client.stream_records().resources():
    # Print the URI for every resource
    print(resource['uri'])

    # Make all of your resources really excited
    resource['title'] += '!!!'
    update_result = client.post(resource['uri'], resource)
    print(update_result)

# Clean up your excitement from earlier
for resource in client.stream_records().resources():
    # Manage your resource records one at a time, no matter how many there are
    pass
```

```python
# Change all of your user's passwords to "something really complicated"
client.manage_users().change_all_passwords(
    'pa$$w0rd', 
    include_admin=True
)

# Randomize all of your non-admin user's passwords
import string
import random

client.manage_users().change_all_passwords(
    include_admin=False,
    new_password=''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(25)
    ),
```

## Installation

This project has a listing on PyPI and can be installed using pip.

```bash
pip install aspace-client
```

Below are instructions for installing this package in "editable" mode. This
will allow you to make changes to the package in real time.

```bash
AS_CLIENT_DIR="/path/to/aspace-client"
git clone https://github.com/AustinTSchaffer/ArchivesSpace-Python-Client.git "$AS_CLIENT_DIR"

# In your python project directory, or in your venv
pip install -e "$AS_CLIENT_DIR"
```


## Contributing

If you have any suggestions or bug reports please feel free to report them in
[the issues tab](https://github.com/AustinTSchaffer/ArchivesSpace-Python-Client/issues) 
or email me at [schaffer.austin.t@gmail.com](mailto:schaffer.austin.t@gmail.com).

Pull requests are welcome, but they will subject to a review process.
Consistent code style is a goal for this project, as it currently 
attemps to follow the coding standards layed out in the 
[PEP8 Python style guide](https://www.python.org/dev/peps/pep-0008/).
Please keep this in mind when submitting or requesting contributions,
but also keep in mind that PEP is a flexible standard and that I'm 
willing to make exceptions.

Also, please feel free to call me out on anything currently in this 
package that is poorly styled or just generally bad code.
