import re

from aspace import BaseASpaceClient


class RecordStream(object):
    """
    Contains methods that can be used to stream all records from an instance
    of ArchivesSpace of a particular record type.
    """

    def __init__(self, client: BaseASpaceClient):
        self._client = client

    def repositories(self):
        """
        Streams all repository records from the ArchivesSpace instance.
        """
        return (
            repo for repo in
            self._client.get('/repositories').json()
        )

    def _get_repo_uris(self, repository_uris: list = None):
        """
        Returns a list of valid repository URIs in the ArchivesSpace
        instance, or raises an error.
        """
        repo_uris = (
            repository_uris
            if repository_uris is not None else
            [repo['uri'] for repo in self.repositories()]
        )

        def invalid_repo_uri(repo_uri):
            return not re.match(r'/repositories/\d+', repo_uri)

        if any(filter(lambda uri: type(uri) is not str, repo_uris)):
            raise TypeError('All repository uris must be strings')

        if any(filter(invalid_repo_uri, repo_uris)):
            raise ValueError(r'All Repository URIs must be of the form \
            "/repositories/\d+"')

        return repo_uris

    def stream_records(self, plural_record_type: str,):
        """
        Streams all records of a specific type from the ArchivesSpace instance,
        assuming that a `/:plural_record_type` endpoint exists, and supports
        the `all_ids=true` parameter.
        """
        return (
            self._client.get(rec_uri).json()

            for rec_id in self._client.get(
                '/%s?all_ids=true' % plural_record_type).json()

            for rec_uri in ['/%s/%d' % (plural_record_type, rec_id)]
        )

    def stream_repository_records(self, plural_record_type: str,
                                  repository_uris: list = None,):
        """
        Streams all records of a specific type from the ArchivesSpace instance,
        assuming that a `/repositories/:repo_id/:plural_record_type` endpoint
        exists, and supports the `all_ids=true` parameter.

        `:plural_record_type:` The desired record type, formatted as it appears
        in the documentation for the related API endpoint.

        `:repository_uris:` Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """

        return (
            self._client.get(
                '%s/%s/%d' %
                (repo_uri, plural_record_type, rec_id)
            ).json()

            for repo_uri in self._get_repo_uris(repository_uris)

            for rec_id in self._client.get(
                '%s/%s?all_ids=true' %
                (repo_uri, plural_record_type)
            ).json()

        )

    def resources(self, repository_uris: list = None,):
        """
        Streams all resources from the ArchivesSpace instance.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """

        return self.stream_repository_records(
            plural_record_type='resources',
            repository_uris=repository_uris,
        )

    def archival_objects(self, repository_uris: list = None,):
        """
        Streams all archival object records from the ArchivesSpace instance.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """

        return self.stream_repository_records(
            plural_record_type='archival_objects',
            repository_uris=repository_uris,
        )

    def users(self):
        """
        Streams all user records from the ArchivesSpace instance.
        """
        return self.stream_records('users')

    def agents(self, plural_agent_type: str):
        """
        Streams all agent records from the ArchivesSpace instance, of the
        specified agent type.

        `:plural_agent_type:` The desired type of agent
        """
        return self.stream_records('agents/%s' % plural_agent_type)

    def people(self):
        """
        Streams all person agents from the ArchivesSpace instance.
        """
        return self.agents('people')

    def corporate_entities(self):
        """
        Streams all corporate entity agents from the ArchivesSpace instance.
        """
        return self.agents('corporate_entities')

    def families(self):
        """
        Streams all family agents from the ArchivesSpace instance.
        """
        return self.agents('families')

    def software(self):
        """
        Streams all software agents from the ArchivesSpace instance.
        """
        return self.agents('software')
