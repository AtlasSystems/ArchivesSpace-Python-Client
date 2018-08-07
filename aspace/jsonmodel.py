"""
Contains functions and classes that can be used when construction common
components of ArchivesSpace's JsonModel objects.
"""


def _ref(ref: str):
    """
    ```
    {'ref': ref}
    ```
    """
    return {'ref': ref}


ref = _ref


def instance_sub_container(instance_type: str, ref: str,
                           type_2: str = None, indicator_2: str = None,
                           type_3: str = None, indicator_3: str = None,
                           ) -> dict:
    """
    The type and indicator parameters apply to the 'sub_container' object.

    ```
    {
        'instance_type': instance_type,
        'sub_container': {'top_container': {'ref': ref}}
    }
    ```
    """
    
    sub_container = {
        'top_container': _ref(ref)
    }

    if type_2 is not None: sub_container['type_2']
    if indicator_2 is not None: sub_container['indicator_2']

    if type_3 is not None: sub_container['type_3']
    if indicator_3 is not None: sub_container['indicator_3']

    return {
        'instance_type': instance_type,
        'sub_container': sub_container
    }


def instance_digital_object(ref: str) -> dict:
    """
    ```
    {
        'instance_type': 'digital_object',
        'digital_object': {'ref': ref}
    }
    ```
    """
    return {
        'instance_type': 'digital_object',
        'digital_object': _ref(ref)
    }
