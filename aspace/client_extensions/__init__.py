r"""
This module contains classes that leverage existing endpoints of the 
ArchivesSpace API to extend its functionality. Examples of the types
of utilities included in this package are

- Streaming Records 1 by 1 from the API, using the `all_ids` flag.
- Providing paging controls for GET endpoints that support paging.
- Updating user passwords.

These components can be accessed through the ASpaceClient class.
"""

from .record_stream import RecordStream
from .record_pages import RecordPages
from .user_management import UserManagement
