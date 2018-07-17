from aspace import base_client


class RecordPages(object):
    """
    Contains methods that can be used to paginate through the various ASpace
    API endpoints that support pagination.
    """

    def __init__(self, client: base_client.BaseASpaceClient):
        self._client = client
