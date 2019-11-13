import io
import json
import os
from typing import Union, List, Dict

from aspace import constants, base_client, enums, client_extensions


class JobManagementService(object):
    """
    Contains methods that can be used to create and modify ArchivesSpace jobs.
    """

    def __init__(self, client: base_client.BaseASpaceClient):
        self._client = client
        self._record_streams = (
            client_extensions.record_streams.RecordStreamingService(client)
        )

    def import_types(self, repo_uri) -> List[dict]:
        """
        Returns the JSON result from
        `GET /repositories/:repo_id/jobs/import_types`, which should be a list
        of objects with the schema:

        ```
        {
            'description': str,
            'name': str,
        }
        ```
        """
        resp = self._client.get('{}/jobs/import_types'.format(repo_uri))
        assert resp.ok, resp.text
        return resp.json()

    def _create_file_import_job(self, repo_uri: str,
                                import_type: Union[str, enums.DataImportTypes],
                                files: Dict[str, io.TextIOBase],) -> dict:
        """
        Creates a new data import job from a dictionary that maps file names to
        the contents of those files. Requires a repository URI and a data import
        type (explicit string from `/repositories/:repo_id/jobs/import_types` or
        value from `enums.DataImportTypes`).

        Asserts that the response from the API is a good response, then returns
        the JSON response.
        """

        _import_type = (
            import_type.value
            if isinstance(import_type, enums.DataImportTypes) else
            import_type
            if isinstance(import_type, str) else
            None
        )

        assert _import_type, (
            "Invalid value for 'import_type': {}".format(import_type)
        )

        _job = {
            'job_type': 'import_job',
            'job': {
                'jsonmodel_type': 'import_job',
                'filenames': list(files.keys()),
                'import_type': _import_type,
            }
        }

        _files = [
            ('files[]', filedata)
            for filedata in
            files.values()
        ]

        resp = self._client.post(
            '{}/jobs_with_files'.format(repo_uri),
            files=_files,
            data={'job': json.dumps(_job)},
        )

        assert resp.ok, resp.text
        return resp.json()

    def create_with_files(self, repo_uri: str,
                          import_type: Union[str, enums.DataImportTypes],
                          filepaths: List[str],
                          one_job_per_file: bool = False) -> dict:
        """

        Creates a new job that operates on a list of input files, taking a list
        of local file paths. Requires a repository URI and a data import type
        (explicit string from `/repositories/:repo_id/jobs/import_types` or
        value from `enums.DataImportTypes`).

        Asserts that the response from the API is a good response, then returns
        the JSON response.

        If `:one_job_per_file:` is set to true, returns a list of the JSON
        responses.

        """

        if one_job_per_file:
            return [
                self._create_file_import_job(
                    repo_uri=repo_uri,
                    import_type=import_type,
                    files={filedata: open(filedata, 'r')},
                )
                for filedata in
                filepaths
            ]

        return self._create_file_import_job(
            repo_uri=repo_uri,
            import_type=import_type,
            files={
                filedata: open(filedata, 'r')
                for filedata in
                filepaths
            },
        )

    def create_with_data(self, repo_uri: str,
                         import_type: Union[str, enums.DataImportTypes],
                         filedata: Dict[str, Union[str, io.TextIOBase]],
                         one_job_per_file: bool = False) -> dict:
        """
        Creates a new job that operates on a list of input files, taking a
        dictionary that maps the original file names to the contents of those
        files. Requires a repository URI and a data import type (explicit string
        from `/repositories/:repo_id/jobs/import_types` or value from
        `enums.DataImportTypes`).

        Asserts that the response from the API is a good response, then returns
        the JSON response.

        If `:one_job_per_file:` is set to true, returns a list of the JSON
        responses.
        """

        _files = {
            filename: (
                io.StringIO(data)
                if isinstance(data, str) else
                data
            )
            for filename, data in
            filedata.items()
        }

        if one_job_per_file:
            return [
                self._create_file_import_job(
                    repo_uri=repo_uri,
                    import_type=import_type,
                    files={filename: data},
                )
                for filename, data in
                _files.items()
            ]

        return self._create_file_import_job(
            repo_uri=repo_uri,
            import_type=import_type,
            files=_files
        )

    @staticmethod
    def _to_uri(job) -> str:
        """
        :job: Either a job's URI or the JSON representation of a job as a dict.
        """

        uri = (
            job if isinstance(job, str) else
            job.get('uri', None) if isinstance(job, dict) else
            None
        )

        if not uri:
            raise ValueError('Format of job parameter not recognized')

        return uri

    def get_output_files(self, job: Union[str, dict]) -> list:
        """
        Gets a list of a job's output files.

        :job: Either a job's URI or the JSON representation of a job as a dict.
        """

        uri = JobManagementService._to_uri(job)
        resp = self._client.get('{}/output_files'.format(uri))
        assert resp.ok, resp.text
        return resp.json()

    def get_log(self, job: Union[str, dict]) -> list:
        """
        Gets a job's output log.

        :job: Either a job's URI or the JSON representation of a job as a dict.
        """

        uri = JobManagementService._to_uri(job)
        resp = self._client.get('{}/log'.format(uri))
        assert resp.ok, resp.text
        return resp.text

    def get(self, job: Union[str, dict]) -> dict:
        """
        Gets a job.

        :job: Either a job's URI or the JSON representation of a job as a dict.
        """

        uri = JobManagementService._to_uri(job)
        resp = self._client.get(uri)
        assert resp.ok, resp.text
        return resp.json()

    def cancel(self, job: Union[str, dict]) -> dict:
        """
        Cancels a job.

        :job: Either a job's URI or the JSON representation of a job as a dict.
        """

        uri = JobManagementService._to_uri(job)
        resp = self._client.post('{}/cancel'.format(uri))
        assert resp.ok, resp.text
        return resp.json()

    def delete(self, job: Union[str, dict]) -> dict:
        """
        Deletes a job.

        :job: Either a job's URI or the JSON representation of a job as a dict.
        """

        uri = JobManagementService._to_uri(job)
        resp = self._client.delete(uri)
        assert resp.ok, resp.text
        return resp.json()

    def get_active(self, repository_uris: list = None,) -> List[dict]:
        """
        Gets a list of all the job records from the ArchivesSpace instance that
        have a status of "running" or "queued". Can be limitied to a set of
        repositories.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """
        return self.get_by_status(
            status=[
                enums.JobStatus.RUNNING,
                enums.JobStatus.QUEUED,
            ],
            repository_uris=repository_uris
        )

    def get_archived(self, repository_uris: list = None,) -> List[dict]:
        """
        Gets a list of all the job records from the ArchivesSpace instance that
        are either completed, cancelled, or failed. Can be limitied to a set of
        repositories.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """
        return self.get_by_status(
            status=[
                enums.JobStatus.COMPLETED,
                enums.JobStatus.CANCELED,
                enums.JobStatus.FAILED,
            ],
            repository_uris=repository_uris
        )

    def get_completed(self, repository_uris: list = None,) -> List[dict]:
        """
        Gets a list of all the job records from the ArchivesSpace instance that
        have a status of "completed". Can be limitied to a set of repositories.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """
        return self.get_by_status(
            status=[
                enums.JobStatus.COMPLETED,
            ],
            repository_uris=repository_uris
        )

    def get_failed(self, repository_uris: list = None,) -> List[dict]:
        """
        Gets a list of all the job records from the ArchivesSpace instance that
        have a status of "failed". Can be limitied to a set of repositories.

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """
        return self.get_by_status(
            status=[
                enums.JobStatus.FAILED,
            ],
            repository_uris=repository_uris
        )

    def get_by_status(self, status, repository_uris: list = None,) -> List[dict]:
        """
        Gets a list of all the job records from the ArchivesSpace instance that
        match the input status. Can be limitied to a set of repositories.

        :status: Can be a value from the `enums.JobStatus` enumeration, a
        string value, or a list containing values of either type. This will
        filter the list of jobs based on each job's status property.fail

        :repository_uris: Optional list of repository URIs, which limits the
        records that are downloaded. If omitted, records will be pulled from
        all repositories.
        """
        statuses = [
            (
                _status.value if isinstance(_status, enums.JobStatus) else
                _status
            )
            for _status in
            (
                [status] if isinstance(status, str) else
                [status] if isinstance(status, enums.JobStatus) else
                status
            )
        ]

        jobs = []
        for job in self._record_streams.jobs(repository_uris=repository_uris):
            if job["status"] in statuses:
                jobs.append(job)

        return jobs
