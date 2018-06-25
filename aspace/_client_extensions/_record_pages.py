from aspace import ASpaceClient


class RecordPages(object):
    """
    Contains methods that can be used to paginate through the various ASpace
    API endpoints that support pagination
    """

    def __init__(self, client: ASpaceClient):
        self._client = client

    def
