# encoding: utf-8

import jsonpatch
import logging
from paste.deploy.converters import asbool

import ckan.plugins.toolkit as tk
from ckan.common import _
from ckanext.jsonpatch.logic import schema
from ckanext.jsonpatch.lib.dictization import jsonpatch_dict_save, jsonpatch_dictize
from ckanext.jsonpatch.model.jsonpatch import JSONPatch

log = logging.getLogger(__name__)


def jsonpatch_create(context, data_dict):
    """
    Create a new JSON Patch for some object. This consists of a single patch "operation" as
    per `Section 4`_ of `RFC6902`_.

    The structure of the returned dictionary may be customized by passing 'schema' in the context.

    :param model_name: this is the 'xyz' part of an 'xyz_show' action to which the patch will be applied
    :type model_name: string
    :param object_id: the id or name of the 'xyz' object
    :type object_id: string
    :param operation: the JSON Patch operation, e.g. { "op": "add", "path": "/a/b/c", "value": "foo" }
    :type operation: dictionary
    :param qualifier: may be used to filter the patches that get applied under different scenarios (optional)
    :type qualifier: string
    :param ordinal: set the order of the patch within the list of patches to be applied (optional: default ``0``);
        patches with equivalent ordinal values will be applied in timestamp (creation) order
    :type ordinal: integer
    :param data: any additional information about the patch (optional)
    :type data: dictionary

    :returns: the newly created JSON Patch (unless 'return_id_only' is set to True
              in the context, in which case just the JSON Patch id will be returned)
    :rtype: dictionary

    .. _`RFC6902`: https://tools.ietf.org/html/rfc6902
    .. _`Section 4`: https://tools.ietf.org/html/rfc6902#section-4
    """
    log.info("Creating JSON Patch: %r", data_dict)
    tk.check_access('jsonpatch_create', context, data_dict)

    model = context['model']
    user = context['user']
    session = context['session']
    defer_commit = context.get('defer_commit', False)
    return_id_only = context.get('return_id_only', False)

    data, errors = tk.navl_validate(data_dict, schema.jsonpatch_create_schema(), context)
    if errors:
        session.rollback()
        raise tk.ValidationError(errors)

    jsonpatch = jsonpatch_dict_save(data, context)

    rev = model.repo.new_revision()
    rev.author = user
    if 'message' in context:
        rev.message = context['message']
    else:
        rev.message = _(u'REST API: Create JSON Patch %s') % jsonpatch.id

    if not defer_commit:
        model.repo.commit()

    output = jsonpatch.id if return_id_only \
        else tk.get_action('jsonpatch_show')(context, {'id': jsonpatch.id})
    return output


def jsonpatch_update(context, data_dict):
    """
    Update a JSON Patch.

    It is recommended to call
    :py:func:`ckan.logic.action.get.jsonpatch_show`, make the desired changes to
    the result, and then call ``jsonpatch_update()`` with it.

    For further parameters see
    :py:func:`~ckanext.jsonpatch.logic.action.jsonpatch_create`.

    Note: model_name and object_id cannot be modified.

    The structure of the returned dictionary may be customized by passing 'schema' in the context.

    :param id: the id of the JSON Patch to update
    :type id: string

    :returns: the updated JSON Patch (unless 'return_id_only' is set to True
              in the context, in which case just the JSON Patch id will be returned)
    :rtype: dictionary
    """
    log.info("Updating JSON Patch: %r", data_dict)

    model = context['model']
    user = context['user']
    session = context['session']
    defer_commit = context.get('defer_commit', False)
    return_id_only = context.get('return_id_only', False)

    jsonpatch_id = tk.get_or_bust(data_dict, 'id')
    jsonpatch = JSONPatch.get(jsonpatch_id)
    if jsonpatch is not None:
        jsonpatch_id = jsonpatch.id
    else:
        raise tk.ObjectNotFound('%s: %s' % (_('Not found'), _('JSON Patch')))

    tk.check_access('jsonpatch_update', context, data_dict)

    data_dict.update({
        'id': jsonpatch_id,
    })
    context.update({
        'jsonpatch': jsonpatch,
        'allow_partial_update': True,
    })

    data, errors = tk.navl_validate(data_dict, schema.jsonpatch_update_schema(), context)
    if errors:
        session.rollback()
        raise tk.ValidationError(errors)

    jsonpatch = jsonpatch_dict_save(data, context)

    rev = model.repo.new_revision()
    rev.author = user
    if 'message' in context:
        rev.message = context['message']
    else:
        rev.message = _(u'REST API: Update JSON Patch %s') % jsonpatch_id

    if not defer_commit:
        model.repo.commit()

    output = jsonpatch_id if return_id_only \
        else tk.get_action('jsonpatch_show')(context, {'id': jsonpatch_id})
    return output


def jsonpatch_delete(context, data_dict):
    """
    Delete a JSON Patch.

    :param id: the id of the JSON Patch to delete
    :type id: string
    """
    log.info("Deleting JSON Patch: %r", data_dict)

    model = context['model']
    user = context['user']
    session = context['session']
    defer_commit = context.get('defer_commit', False)

    jsonpatch_id = tk.get_or_bust(data_dict, 'id')
    jsonpatch = JSONPatch.get(jsonpatch_id)
    if jsonpatch is not None:
        jsonpatch_id = jsonpatch.id
    else:
        raise tk.ObjectNotFound('%s: %s' % (_('Not found'), _('JSON Patch')))

    tk.check_access('jsonpatch_delete', context, data_dict)

    rev = model.repo.new_revision()
    rev.author = user
    rev.message = _(u'REST API: Delete JSON Patch %s') % jsonpatch_id

    jsonpatch.delete()
    if not defer_commit:
        model.repo.commit()


@tk.side_effect_free
def jsonpatch_show(context, data_dict):
    """
    Return a JSON Patch definition.

    The structure of the returned dictionary may be customized by passing 'schema' in the context.

    :param id: the id of the JSON Patch
    :type id: string

    :rtype: dictionary
    """
    log.debug("Retrieving JSON Patch: %r", data_dict)

    jsonpatch_id = tk.get_or_bust(data_dict, 'id')
    jsonpatch = JSONPatch.get(jsonpatch_id)
    if jsonpatch is not None:
        jsonpatch_id = jsonpatch.id
    else:
        raise tk.ObjectNotFound('%s: %s' % (_('Not found'), _('JSON Patch')))

    tk.check_access('jsonpatch_show', context, data_dict)

    output_schema = context.get('schema')
    context['jsonpatch'] = jsonpatch
    jsonpatch_dict = jsonpatch_dictize(jsonpatch, context)

    result_dict, errors = tk.navl_validate(jsonpatch_dict, output_schema or schema.jsonpatch_show_schema(), context)
    return result_dict


@tk.side_effect_free
def jsonpatch_list(context, data_dict):
    """
    Return a list of ids of an object's JSON Patches, in the order in which they will be applied.

    The structure of the returned dictionaries may be customized by passing 'schema' in the context.

    :param model_name: the 'xyz' part of the 'xyz_show' action to which the patches will be applied
    :type model_name: string
    :param object_id: the id of the 'xyz' object
    :type object_id: string
    :param qualifier: return only patches with the specified qualifier (optional, default: return all)
    :type qualifier: string
    :param all_fields: return dictionaries instead of just ids (optional, default: ``False``)
    :type all_fields: boolean

    :rtype: list of strings
    """
    log.debug("Retrieving JSON Patch list: %r", data_dict)

    model = context['model']
    session = context['session']

    model_name, object_id = tk.get_or_bust(data_dict, ['model_name', 'object_id'])
    qualifier = data_dict.get('qualifier')
    all_fields = asbool(data_dict.get('all_fields'))

    tk.check_access('jsonpatch_list', context, data_dict)

    q = session.query(JSONPatch.id) \
        .filter_by(model_name=model_name, object_id=object_id, state='active') \
        .order_by(JSONPatch.ordinal, JSONPatch.timestamp)
    if qualifier:
        q = q.filter_by(qualifier=qualifier)

    jsonpatches = q.all()
    result = []
    for (id_,) in jsonpatches:
        if all_fields:
            data_dict['id'] = id_
            result += [tk.get_action('jsonpatch_show')(context, data_dict)]
        else:
            result += [id_]

    return result


@tk.side_effect_free
def jsonpatch_apply(context, data_dict):
    """
    Return an object dictionary, modified by its list of JSON patches.

    :param model_name: the 'xyz' part of the 'xyz_show' action to which the patches will be applied
    :type model_name: string
    :param object_id: the id of the 'xyz' object
    :type object_id: string
    :param qualifier: apply only patches with the specified qualifier (optional, default: apply all)
    :type qualifier: string
    :param kwargs: additional arguments to be passed in the data_dict to the 'xyz_show' action (optional)
    :param kwargs: dictionary

    :returns: the patched object dict
    :rtype: dictionary
    """
    log.debug("Retrieving JSON-patched object: %r", data_dict)

    model = context['model']
    session = context['session']

    model_name, object_id = tk.get_or_bust(data_dict, ['model_name', 'object_id'])
    qualifier = data_dict.get('qualifier')

    tk.check_access('jsonpatch_apply', context, data_dict)

    q = session.query(JSONPatch.operation) \
        .filter_by(model_name=model_name, object_id=object_id, state='active') \
        .order_by(JSONPatch.ordinal, JSONPatch.timestamp)
    if qualifier:
        q = q.filter_by(qualifier=qualifier)

    oplist = [operation for (operation,) in q.all()]
    patch = jsonpatch.JsonPatch(oplist)

    show_params = data_dict.get('kwargs') or {}
    show_params['id'] = object_id
    object_dict = tk.get_action('{}_show'.format(model_name))(context, show_params)
    patched_dict = patch.apply(object_dict)

    return patched_dict
