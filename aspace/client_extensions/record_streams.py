import re

from aspace import base_client


class RecordStreams(object):
    """
    Contains methods that can be used to stream all records from an instance
    of ArchivesSpace of a particular record type.
    """

    def __init__(self, client: base_client.BaseASpaceClient):
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

        assert not any(filter(lambda uri: type(uri) is not str, repo_uris)), (
            'All repository uris must be strings'
        )

        def invalid_repo_uri(repo_uri):
            return not re.match(r'/repositories/\d+', repo_uri)

        assert not any(filter(invalid_repo_uri, repo_uris)), (
            r'All Repository URIs must be of the form /repositories/\d+"'
        )

        return repo_uris

    def uris(self, plural_record_type: str,) -> iter:
        """
        Streams all URIs of a specific type from the ArchivesSpace instance,
        assuming that a `/:plural_record_type` endpoint exists, and supports
        the `all_ids=true` parameter.

        :plural_record_type: The desired record type, formatted as it
        appears in the documentation for the related API endpoint.
        """
        return (
            '/%s/%d' % (plural_record_type, rec_id)

            for rec_id in self._client.get(
                '/%s?all_ids=true' % plural_record_type
            ).json()
        )

    def repository_relative_uris(self, plural_record_type: str,
                                 repository_uris: list = None,
                                 endpoint_extension: str = None,):
        """
        Streams all URIs of a specific type from the ArchivesSpace
        instance, assuming that a
        `/repositories/:repo_id/:plural_record_type` endpoint
        exists, and supports the `all_ids=true` parameter.

        :plural_record_type: The desired record type, formatted as it
        appears in the documentation for the related API endpoint.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.

        :endpoint_extension: Optional extension to put at the end of each
        record URI. For example, specifying 'resources' and 
        endpoint_extension='tree' supports the
        '/repositories/:repo_id/resources/:id/tree' endpoint.
        """
        return (
            '%s/%s/%d%s' %
            (
                repo_uri, 
                plural_record_type, 
                rec_id,
                '' if endpoint_extension is None else
                '/%s' % endpoint_extension.strip('/'),
            )

            for repo_uri in self._get_repo_uris(repository_uris)

            for rec_id in self._client.get(
                '%s/%s?all_ids=true' %
                (repo_uri, plural_record_type)
            ).json()
        )

    def records(self, plural_record_type: str,):
        """
        Streams all records of a specific type from the ArchivesSpace instance,
        assuming that a `/:plural_record_type` endpoint exists, and supports
        the `all_ids=true` parameter.

        :plural_record_type: The desired record type, formatted as it
        appears in the documentation for the related API endpoint.
        """
        return (
            self._client.get(uri).json()
            for uri in self.uris(plural_record_type)
        )

    def repository_records(self, plural_record_type: str,
                           repository_uris: list = None,
                           endpoint_extension: str = None,):
        """
        Streams all records of a specific type from the ArchivesSpace 
        instance, assuming that a 
        `/repositories/:repo_id/:plural_record_type` endpoint
        exists, and supports the `all_ids=true` parameter.

        :plural_record_type: The desired record type, formatted as it
        appears in the documentation for the related API endpoint.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.

        :endpoint_extension: Optional extension to put at the end of each
        record URI. For example, specifying 'resources' and 
        endpoint_extension='tree' supports the
        '/repositories/:repo_id/resources/:id/tree' endpoint.
        """

        return (
            self._client.get(uri).json()

            for uri in self.repository_relative_uris(
                plural_record_type,
                repository_uris=repository_uris,
                endpoint_extension=endpoint_extension,
            )
        )

    def resources(self, repository_uris: list = None, 
                  endpoint_extension: str = None,):
        """
        Streams all resources from the ArchivesSpace instance.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.

        :endpoint_extension: Optional extension to put at the end of each
        record URI, supporting endpoints such as
        `/repositories/:repo_id/resources/:id/tree`
        """

        return self.repository_records(
            plural_record_type='resources',
            repository_uris=repository_uris,
            endpoint_extension=endpoint_extension,
        )

    def resource_trees(self, repository_uris: list = None,):
        """
        Streams all resource trees from the ArchivesSpace instance.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """

        return self.resources(
            repository_uris=repository_uris,
            endpoint_extension='tree',
        )

    def resource_ordered_records(self, repository_uris: list = None,):
        """
        Streams all resource ordered_records from the ArchivesSpace instance.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """

        return self.resources(
            repository_uris=repository_uris,
            endpoint_extension='ordered_records',
        )

    def accessions(self, repository_uris: list = None,):
        """
        Streams all accession records from the ArchivesSpace instance.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """

        return self.repository_records(
            plural_record_type='accessions',
            repository_uris=repository_uris,
        )

    def archival_objects(self, repository_uris: list = None,):
        """
        Streams all archival object records from the ArchivesSpace instance.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """

        return self.repository_records(
            plural_record_type='archival_objects',
            repository_uris=repository_uris,
        )

    def users(self):
        """
        Streams all user records from the ArchivesSpace instance.
        """
        return self.records('users')

    def people(self):
        """
        Streams all person agents from the ArchivesSpace instance.
        """
        return self.records('agents/people')

    def corporate_entities(self):
        """
        Streams all corporate entity agents from the ArchivesSpace instance.
        """
        return self.records('agents/corporate_entities')

    def families(self):
        """
        Streams all family agents from the ArchivesSpace instance.
        """
        return self.records('agents/families')

    def software(self):
        """
        Streams all software agents from the ArchivesSpace instance.
        """
        return self.records('agents/software')

    def all_agents(self):
        """
        Streams all agent records from the ArchivesSpace instance.
        """

        return (
            record

            for stream in [
                self.people,
                self.corporate_entities,
                self.families,
                self.software,
            ]

            for record in stream()
        )

    def top_containers(self, repository_uris: list = None,):
        """
        Streams all top_container records from the ArchivesSpace instance.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """

        return self.repository_records(
            plural_record_type='top_containers',
            repository_uris=repository_uris,
        )

    def subjects(self):
        return self.records(
            plural_record_type='subjects'
        )
