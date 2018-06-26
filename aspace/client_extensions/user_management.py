from . import RecordStreams

from aspace import BaseASpaceClient


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
            _user for _user in
            self._record_streams.users()
        ]

    def stream_user_records(self) -> iter:
        """
        Streams all non-system user records from the ArchivesSpace instance.
        Please see the RecordStreams extensions for other streaming methods.
        """
        return self._record_streams.users()

    def change_all_passwords(self, new_password: str) -> list:
        """
        Changes the passwords for all of the users in the ArchivesSpace 
        instance:
        
        - incuding the admin user
        - not including any other system users

        Returns a list of all of the JSON responses.
        """

        invalid = new_password is None
        invalid = invalid or len(new_password) == 0
        invalid = invalid or new_password.isspace()

        if invalid:
            raise ValueError('A new password must be specified.')

        return [
            self._client.post(
                user['uri'], json=user,
                params={'password': new_password}
            ).json()

            for user in self._record_streams.users()

            # Don't update any system users, unless they are 'admin'
            if (user.get('is_admin') or not user.get('is_system_user'))
        ]
