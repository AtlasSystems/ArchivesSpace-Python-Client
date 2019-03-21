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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._streams = client_extensions.record_streams.RecordStreamingService(self)
        self._users = client_extensions.user_management.UserManagementService(self)
        self._enumerations = client_extensions.enum_management.EnumerationManagementService(self)
        self._schemas = client_extensions.schema_query.SchemaQueryingService(self)

    @property
    def streams(self) -> client_extensions.record_streams.RecordStreamingService:
        """

        Returns an instance of the RecordStreamingService class, providing
        methods that allow a more fluent interface for streaming records and
        URIs from ArchivesSpace, via the ArchivesSpace API.

        """
        return self._streams

    @property
    def users(self) -> client_extensions.user_management.UserManagementService:
        """

        Returns an instance of the UserManagementService class, providing
        methods that allow more fluent access to the `/users` endpoint of the
        ArchivesSpace API.
        
        """
        return self._users

    @property
    def enumerations(self) -> client_extensions.enum_management.EnumerationManagementService:
        """
        
        Returns an instance of the EnumerationManagementService class, providing
        methods that allow more fluent access to managing ArchivesSpace's lists
        of controlled value.

        """
        return self._enumerations

    @property
    def schemas(self) -> client_extensions.schema_query.SchemaQueryingService:
        """

        Returns an instance of the SchemaQueryingService class, providing
        methods that allow more fluent read access for ArchivesSpace's JSON
        model schemas.

        """
        return self._schemas
