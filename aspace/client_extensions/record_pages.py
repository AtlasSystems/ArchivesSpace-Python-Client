from .. import BaseASpaceClient


class RecordPages(object):
    """
    Contains methods that can be used to paginate through the various ASpace
    API endpoints that support pagination
    """

    def __init__(self, client: BaseASpaceClient):
        self._client = client
