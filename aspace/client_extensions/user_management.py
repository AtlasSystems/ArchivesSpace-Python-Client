from typing import Union

from aspace import base_client
from aspace.client_extensions import record_streams


class UserManagement(object):
    """
    Contains methods that can be used to perform batch updates on user records
    using different components of the ArchivesSpace API.
    """

    def __init__(self, client: base_client.BaseASpaceClient):
        self._client = client
        self._record_streams = record_streams.RecordStreams(client)

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

    def change_all_passwords(self, new_password: Union[str, callable],
                             include_admin=False) -> list:
        """
        Changes the passwords for all of the users in the ArchivesSpace
        instance, not including any of the system users.

        Returns a list of all of the responses from the ArchivesSpace server.

        `:new_password:` The new password to set for all users. If a string is
        passed, that string will be used to set the password for all users. If
        new_password is callable, new_password should accept a user record 
        dict and should return a string, which can be used to set a unique 
        password for each user.

        `:include_admin:` Determines whether the `admin` user should be
        included in the global password reset.
        """

        return [
            self.change_password(user['uri'], new_password)

            for user in self._record_streams.users()

            if (not user.get('is_admin')) or include_admin
        ]

    def change_password(self, user_uri: str,
                        new_password: Union[str, callable],):
        """
        Changes the passwords for all of the users in the ArchivesSpace
        instance, not including any of the system users.

        Returns the response from the server.

        `:user_uri:` The uri for the user record that will receive the new 
        password. NOTE: The user record will be downloaded and reuploaded, 
        which will increment the user's `lock_version`.

        `:new_password:` The new password to set for all users. If a string is
        passed, that string will be used to set the password for all users. If
        new_password is callable, new_password should accept a user record 
        dict and should return a string, which can be used to set a unique 
        password for each user.
        """
        user = self._client.get(user_uri).json()

        password = (
            new_password(user) if callable(new_password) else
            new_password
        )

        assert password is not None

        return self._client.post(
            user['uri'],
            json=user,
            params={'password': password}
        )
