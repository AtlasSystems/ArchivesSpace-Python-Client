"""
This module contains classes that extend the functionality of the ASpaceClient
class, in order to prevent the core functionality of the ASpaceClient class
from exploding with too many features.
"""

from ._record_stream import RecordStream
from ._record_pages import RecordPages
