# ArchivesSpace Python Client

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


## Contributing

If you have any suggestions or bug reports please feel free to report them in
the issues tab or email me at [schaffer.austin.t@gmail.com](mailto:schaffer.austin.t@gmail.com).

Please note that pull requests are welcome, but will subject to a review
process. Please . Also, please feel free to call me out on anything currently
in this package that does not conform to any style guide.
