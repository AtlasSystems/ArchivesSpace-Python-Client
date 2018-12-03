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

    def page_records(self):
        """
        NOT CURRENTLY IMPLEMENTED. WILL THROW.

        Initializes an instance of the RecordPages extension class, providing
        methods that allow records to be paged from ArchivesSpace.
        """

        return client_extensions.record_pages.RecordPages(self)

    @property
    def record_pages(self):
        """
        NOT CURRENTLY IMPLEMENTED. WILL THROW.

        Initializes an instance of the RecordPages extension class, providing
        methods that allow records to be paged from ArchivesSpace.
        """

        return self.page_records()

    def stream_records(self):
        """
        Initializes an instance of the RecordStreams extension class, providing
        methods that allow records to be streamed from ArchivesSpace.
        """

        return client_extensions.record_streams.RecordStreams(self)

    @property
    def record_streams(self):
        """
        Initializes an instance of the RecordStreams extension class, providing
        methods that allow records to be streamed from ArchivesSpace.
        """
        return self.stream_records()

    def manage_users(self):
        """
        Initializes an instance of the UserManagement extension class, 
        providing methods that allow batch updates for user records.
        """

        return client_extensions.user_management.UserManagement(self)

    @property
    def user_management(self):
        """
        Initializes an instance of the UserManagement extension class, 
        providing methods that allow batch updates for user records.
        """

        return self.manage_users()

    def manage_enumerations(self):
        """
        Initializes an instance of the EnumManagement extension class, 
        providing methods that allow batch updates for ArchivesSpace's
        controlled value lists.
        """

        return client_extensions.enum_management.EnumManagement(self)

    @property
    def enum_management(self):
        """
        Initializes an instance of the EnumManagement extension class, 
        providing methods that allow batch updates for ArchivesSpace's
        controlled value lists.
        """

        return self.manage_enumerations()
