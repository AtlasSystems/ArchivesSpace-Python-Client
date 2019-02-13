r"""
Contains the ASpaceClient class.
"""

from aspace import base_client

from aspace import client_extensions


class ASpaceClient(base_client.BaseASpaceClient):
    """
    Wraps the Session class from the requests package. Extends the 
    functionality of the BaseASpaceClient, by including instances
    of classes that leverage multiple endpoints of the ArchivesSpace
    API.
    """

    def stream_records(self):
        """
        Initializes an instance of the RecordStreams extension class, providing
        methods that allow records to be streamed from ArchivesSpace.
        """

        return client_extensions.record_streams.RecordStreams(self)

    def manage_users(self):
        """
        Initializes an instance of the UserManagement extension class, 
        providing methods that allow batch updates for user records.
        """

        return client_extensions.user_management.UserManagement(self)

    def manage_enumerations(self):
        """
        Initializes an instance of the EnumManagement extension class, 
        providing methods that allow batch updates for ArchivesSpace's
        controlled value lists.
        """

        return client_extensions.enum_management.EnumManagement(self)

    def query_schemas(self):
        """
        Initializes an instance of the SchemaQuery extension class, 
        providing methods that allow schema records to be retrieved
        through the API.
        """

        return client_extensions.schema_query.SchemaQuery(self)
