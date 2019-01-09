# encoding: utf-8

import jsonpointer
import json

import ckan.plugins.toolkit as tk
from ckan.common import _


def jsonpatch_operation_validator(operation_dict):
    """
    Checks that the supplied value is a valid JSON patch operation dictionary.
    """
    valid = (type(operation_dict) is dict) and \
            ({'op', 'path'} <= set(operation_dict.keys())) and \
            (operation_dict['op'] in ('add', 'remove', 'replace', 'move', 'copy', 'test'))

    if valid:
        try:
            jsonpointer.JsonPointer(operation_dict['path'])
        except:
            valid = False

    if valid and (operation_dict['op'] in ('move', 'copy')):
        valid = 'from' in operation_dict
        if valid:
            try:
                jsonpointer.JsonPointer(operation_dict['from'])
            except:
                valid = False

    if valid and (operation_dict['op'] in ('add', 'replace', 'test')):
        valid = 'value' in operation_dict
        if valid:
            try:
                json.dumps(operation_dict['value'])
            except:
                valid = False

    if not valid:
        raise tk.Invalid(_("Invalid JSON patch operation"))

    return operation_dict


def model_reference_validator(key, data, errors, context):
    """
    Checks that a 'model_name_show' action exists and that an object is gettable with the supplied id/name.
    Also converts object name to id if applicable.
    """
    model_name = data.get(key[:-1] + ('model_name',))
    object_id = data.get(key[:-1] + ('object_id',))
    show_func_name = '{}_show'.format(model_name)
    try:
        show_func = tk.get_action(show_func_name)
    except:
        raise tk.Invalid(_("Invalid model name: action function '{}' does not exist".format(show_func_name)))

    try:
        object_dict = show_func(context, {'id': object_id})
        data[key[:-1] + ('object_id',)] = object_dict['id']
    except Exception, e:
        raise tk.Invalid(_("Unable to get object with id '{}' using action function '{}': {}".
                           format(object_id, show_func_name, e.message)))
