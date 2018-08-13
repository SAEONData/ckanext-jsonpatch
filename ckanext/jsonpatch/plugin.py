# encoding: utf-8

import logging
import ckan.plugins as p
import ckanext.jsonpatch.logic.action as action
import ckanext.jsonpatch.logic.auth as auth

log = logging.getLogger(__name__)


class JSONPatchPlugin(p.SingletonPlugin):
    """
    Plugin allowing model output dictionaries to be patched according to the JSON Patch specification.
    """
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)

    def get_actions(self):
        return {
            'jsonpatch_create': action.jsonpatch_create,
            'jsonpatch_update': action.jsonpatch_update,
            'jsonpatch_delete': action.jsonpatch_delete,
            'jsonpatch_show': action.jsonpatch_show,
            'jsonpatch_list': action.jsonpatch_list,
            'jsonpatch_apply': action.jsonpatch_apply,
        }

    def get_auth_functions(self):
        return {
            'jsonpatch_create': auth.jsonpatch_create,
            'jsonpatch_update': auth.jsonpatch_update,
            'jsonpatch_delete': auth.jsonpatch_delete,
            'jsonpatch_show': auth.jsonpatch_show,
            'jsonpatch_list': auth.jsonpatch_list,
            'jsonpatch_apply': auth.jsonpatch_apply,
        }
