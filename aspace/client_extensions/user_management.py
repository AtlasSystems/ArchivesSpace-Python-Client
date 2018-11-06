import re
from typing import Union

from aspace import base_client
from aspace import constants
from aspace.client_extensions import record_streams

VALID_USER_URI_RE = re.compile(constants.VALID_USER_URI_REGEX)


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

    def _change_password(self, user_record: dict,
                         new_password: Union[str, callable],):
        """
        Changes the password for the user record. Returns the response from
        the ArchivesSpace server. Only to be used internally.
        """
        password = (
            new_password(user_record) if callable(new_password) else
            new_password
        )

        assert (password is not None), (
            'Unable to create a new password for the current user: "%s"' %
            user_record['username']
        )

        return self._client.post(
            user_record['uri'],
            json=user_record,
            params={'password': password}
        )

    def change_all_passwords(self, new_password: Union[str, callable],
                             include_admin=False) -> list:
        """
        Changes the passwords for all of the users in the ArchivesSpace
        instance, not including any of the system users.

        Returns a list of all of the responses from the ArchivesSpace server.

        :new_password: The new password to set for all users. If a string is
        passed, that string will be used to set the password for all users. If
        new_password is callable, new_password should accept a user record 
        dict and should return a string, which can be used to set a unique 
        password for each user.

        :include_admin: Determines whether the `admin` user should be
        included in the global password reset.
        """
        return [
            self._change_password(user, new_password)

            for user in self._record_streams.users()

            if (not user['is_admin']) or include_admin
        ]

    def change_password(self, user: str,
                        new_password: Union[str, callable],):
        """
        Changes the password for the user specified by the URI. Returns the
        response from the ArchivesSpace server.

        :user: The uri or username for the user record that will receive the 
        new password. NOTE: The user record will be downloaded and reuploaded,
        which will increment the user's lock_version.

        :new_password: The new password to set for all users. If a string is
        passed, that string will be used to set the password for all users. If
        new_password is callable, new_password should accept the user record
        dict and should return a string.
        """

        if VALID_USER_URI_RE.match(user):
            user_record = self._client.get(user).json()
            return self._change_password(user_record, new_password)
        
        user_record = next(filter(
            lambda u_rec: u_rec['username'] == user,
            self.stream_user_records()
        ), None)

        assert user_record, ('Unable to find user: "%s"' % user)
        return self._change_password(user_record, new_password)

    def new_user(self, user: dict, password: str):
        """
        Creates a new user and returns he response from the server.

        :user: A dict representation of a user record. Requires
        ['username'] and ['name'] at a minimum.

        :password: The password for the new user.
        """
        assert password is not None

        return self._client.post(
            '/users',
            json=user,
            params={'password': password},
        )
