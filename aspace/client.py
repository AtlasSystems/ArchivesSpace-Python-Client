r"""
Contains the ASpaceClient class.
"""

import aspace.base_client
import aspace.client_extensions as client_extensions


class ASpaceClient(aspace.base_client.BaseASpaceClient):
    """
    Wraps the Session class from the requests package. Extends the 
    functionality of the BaseASpaceClient, by including instances
    of classes that leverage multiple endpoints of the ArchivesSpace
    API.
    """

    def page_records(self):
        """
        Initializes an instance of the RecordPages extension class, providing
        methods that allow records to be paged from ArchivesSpace.
        """

        return client_extensions.record_pages.RecordPages(self)

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
