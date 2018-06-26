# ArchivesSpace Python Client

[![Build Status](https://travis-ci.org/AustinTSchaffer/ArchivesSpace-Python-Client.svg?branch=master)](https://travis-ci.org/AustinTSchaffer/ArchivesSpace-Python-Client)

The `aspace-client` Python package provides web client functionality that
targets the API of ArchivesSpace v2.X and up. This package was developed
to aid ongoing and future ArchivesSpace migrations.

## About

This `aspace` module primarily extends the functionality of the `Session`
class from the `requests` Python library, and attempts to provide access to
many of ArchivesSpace's commonly used endpoints, while also preserving
backwards compatibility and supporting development tools such as Pylint.
ArchivesSpace currently (June 2018) has over 250 API endpoints. Supporting
and maintaining all of those endpoints is quite an undertaking, so features
are being prioritized based on their value to performing ongoing ArchivesSpace
migrations, as well as supporting and researching aspects related to those
ArchivesSpace migrations.


## Installation

This project is currently in development and does not yet exist on PyPi.
Install this package into your virtual environment by cloning this repository
and installing the package in editable mode.

```bash
AS_CLIENT_DIR="/path/to/aspace-python-client"
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
