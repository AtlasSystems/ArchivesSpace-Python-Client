import re
from typing import Union, Iterable
import enum

from aspace import base_client
from aspace import enums
from aspace import constants

VALID_ENUM_URI_RE = re.compile(constants.VALID_ENUM_URI_REGEX)


class EnumManagement(object):
    """
    Contains methods that can be used to perform batch updates and formatting
    for enumerations.
    """

    def __init__(self, client: base_client.BaseASpaceClient):
        self._client = client

    def all_enumerations(self) -> list:
        """
        Dowloads a list of all of the controlled value lists.
        """
        return self._client.get('/config/enumerations').json()

    def _get_enumeration_by_id(self, enum_id: int) -> dict:
        """
        GETs an enumeration (controlled value list) using the
        /config/enumerations/%i endpoint. For internal use only.
        """
        resp = self._client.get('/config/enumerations/%i' % enum_id)
        return resp.json()

    def get_enumeration_by_name(self, enum_name: str) -> dict:
        """
        GETs an enumeration using the `/config/enumerations/names/:enum_name`
        endpoint.
        """
        resp = self._client.get('/config/enumerations/names/%s' % enum_name)
        return resp.json()

    def get_enumeration(self, enum_id: Union[str, int, enums.Enumeration]
                       ) -> dict:
        """
        Gets an enumeration (controlled value list) using the enumeration's
        name, uri, id, or the enumeration specified in the enums module.
        """

        if isinstance(enum_id, enums.Enumeration):
            return self._get_enumeration_by_id(enum_id.value)

        if isinstance(enum_id, int):
            return self._get_enumeration_by_id(enum_id)

        if isinstance(enum_id, str):
            if VALID_ENUM_URI_RE.match(enum_id):
                resp = self._client.get(enum_id)
                return resp.json()
            return self.get_enumeration_by_name(enum_id)

        raise 'Invalid value type for parameter enum_id %s' % repr(enum_id)

    def sort_values(self, enum_id: Union[str, int, enums.Enumeration]):
        """
        Sorts all of the values of an enumeration based on their value.
        Does not return a value, but will fail if any of the HTTP requests
        fail.
        """
        enumeration = self.get_enumeration(enum_id)
        sorted_enum_vals = sorted(
            enumeration['enumeration_values'],
            lambda ev: ev['value']
        )

        for index, enum_val in enumerate(sorted_enum_vals):
            resp = self._client.post(
                '%s/position' % enum_val['uri'],
                params={'position': index}
            )
            assert resp.ok, resp.text

    @staticmethod
    def convert_to_enumeration_value(value: str) -> str:
        """
        Converts a value to the common formatting for an enumeration_value:

        1. all characters are converted to lowercase
        2. all numbers, letters, and underscores are kept
        3. all other characters are replaced by underscores
        4. extra underscores are removed from the ends
        5. continuous runs of underscore characters are shortened to "_"

        `"_1 - Some Value - w/ Formatting..."` -> `"1_some_value_w_formatting"`
        """
        value = re.sub(r'[^\w]+', '_', value)
        value = value.strip(' _')
        value = re.sub(r'_+', '_', value)
        return value or 'unknown'

    def update_enumeration(self, enum_id: Union[str, int, enums.Enumeration],
                           new_values: Iterable, cleanup_new_values=True,
                           reorder_enumeration=False):
        """
        Updates the specified enumeration using distinct values from the
        specified iterable of string. Creates a `set` for the values currently
        associated with the enumeration, and uploads a list of those results,
        so there are no issues with duplicates.

        Optionally, you can specify whether the new values are run through
        the convert_to_enumeration_value function, and whether the client
        should re-order the enumeration after updating.
        """
        new_enum_values = set(new_values)
        
        if cleanup_new_values:
            new_enum_values = {
                self.convert_to_enumeration_value(value)
                for value in new_enum_values
            }

        enumeration = self.get_enumeration(enum_id)
        enumeration['values'] = list(new_enum_values.union(enumeration['values']))
        update_resp = self._client.post(enumeration['uri'], json=enumeration)
        assert update_resp.ok, update_resp.text

        if reorder_enumeration:
            self.sort_values(enum_id)
