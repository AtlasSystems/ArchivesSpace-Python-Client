r"""
Contains the ASpaceClient class.
"""

from . import BaseASpaceClient
import aspace.client_extensions as extensions


class ASpaceClient(BaseASpaceClient):
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

        return extensions.RecordPages(self)

    def stream_records(self):
        """
        Initializes an instance of the RecordStream extension class, providing
        methods that allow records to be streamed from ArchivesSpace.
        """

        return extensions.RecordStream(self)

    def manage_users(self):
        """
        Initializes an instance of the UserManagement extension class, 
        providing methods that allow batch updates for user records.
        """

        return extensions.UserManagement(self)
