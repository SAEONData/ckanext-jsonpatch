# encoding: utf-8

import ckan.lib.dictization as d
from ckanext.jsonpatch.model.jsonpatch import JSONPatch


def jsonpatch_dict_save(jsonpatch_dict, context):
    jsonpatch = context.get('jsonpatch')
    if jsonpatch:
        jsonpatch_dict['id'] = jsonpatch.id
    return d.table_dict_save(jsonpatch_dict, JSONPatch, context)


def jsonpatch_dictize(jsonpatch, context):
    return d.table_dictize(jsonpatch, context)
