# encoding: utf-8

import ckan.plugins.toolkit as tk
from ckanext.jsonpatch.logic import validators as v

empty = tk.get_validator('empty')
not_empty = tk.get_validator('not_empty')
not_missing = tk.get_validator('not_missing')
ignore = tk.get_validator('ignore')
ignore_empty = tk.get_validator('ignore_empty')
ignore_missing = tk.get_validator('ignore_missing')
empty_if_not_sysadmin = tk.get_validator('empty_if_not_sysadmin')
int_validator = tk.get_validator('int_validator')


def jsonpatch_create_schema():
    schema = {
        'id': [empty_if_not_sysadmin, ignore_missing, unicode, v.jsonpatch_id_does_not_exist],
        'model_name': [not_missing, not_empty, unicode],
        'object_id': [not_missing, not_empty, unicode],
        'operation': [not_missing, not_empty, v.jsonpatch_operation_validator],
        'qualifier': [ignore_empty, ignore_missing, unicode],
        'ordinal': [ignore_missing, int_validator],
        'timestamp': [ignore],
        'data': [ignore_empty, ignore_missing],
        '__after': [v.model_reference_validator, ignore],
    }
    return schema


def jsonpatch_update_schema():
    schema = {
        'id': [],
        'model_name': [empty],
        'object_id': [empty],
        'operation': [not_missing, not_empty, v.jsonpatch_operation_validator],
        'qualifier': [ignore_empty, ignore_missing, unicode],
        'ordinal': [ignore_missing, int_validator],
        'timestamp': [ignore],
        'data': [ignore_empty, ignore_missing],
    }
    return schema


def jsonpatch_show_schema():
    schema = dict.fromkeys(jsonpatch_create_schema(), [])
    schema['revision_id'] = []
    del schema['__after']
    return schema
