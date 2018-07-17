from aspace.base_client import BaseASpaceClient

from aspace.client_extensions.record_streams import RecordStreams


class UserManagement(object):
    """
    Contains methods that can be used to perform batch updates on user records
    using different components of the ArchivesSpace API.
    """

    def __init__(self, client: BaseASpaceClient):
        self._client = client
        self._record_streams = RecordStreams(client)

    def all_user_records(self) -> list:
        """
        Dowloads a list of all of the non-system user records in the
        ArchivesSpace instance.
        """
        return [
            user for user in
            self._record_streams.users()
        ]

    def stream_user_records(self) -> iter:
        """
        Streams all non-system user records from the ArchivesSpace instance.
        Please see the RecordStreams extensions for other streaming methods.
        """
        return self._record_streams.users()

    def change_all_passwords(self, new_password: str, 
                             include_admin=False) -> list:
        """
        Changes the passwords for all of the users in the ArchivesSpace
        instance, not including any of the system users. 

        Returns a list of all of the JSON responses.

        `:new_password:` The new password to set for all users.
        TODO: Make new_password support callable(user_record)

        `:include_admin:` Determines whether the `admin` user should be
        included in the global password reset.
        """

        if new_password is None:
            raise ValueError('new_password is required.')

        return [
            self._client.post(
                user['uri'], json=user,
                params={'password': new_password}
            ).json()

            for user in self._record_streams.users()

            # Don't update any system users, unless they are 'admin'
            if (
                (user.get('is_admin') and include_admin)
                or not user.get('is_system_user')
            )
        ]
