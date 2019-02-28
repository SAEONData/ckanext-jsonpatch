# encoding: utf-8

from sqlalchemy import types, Table, Column
import vdm.sqlalchemy
import datetime

from ckan.model import meta, core, types as _types, domain_object


jsonpatch_table = Table(
    'jsonpatch', meta.metadata,
    Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
    Column('model_name', types.UnicodeText, nullable=False),
    Column('object_id', types.UnicodeText, nullable=False),
    Column('operation', _types.JsonDictType),
    Column('scope', types.UnicodeText),
    Column('ordinal', types.Integer, nullable=False, default=0),
    Column('timestamp', types.DateTime, nullable=False, default=datetime.datetime.utcnow),
    Column('data', _types.JsonDictType),
)

vdm.sqlalchemy.make_table_stateful(jsonpatch_table)
jsonpatch_revision_table = core.make_revisioned_table(jsonpatch_table)


class JSONPatch(vdm.sqlalchemy.RevisionedObjectMixin,
                vdm.sqlalchemy.StatefulObjectMixin,
                domain_object.DomainObject):

    @classmethod
    def get(cls, reference):
        """
        Returns a JSONPatch object referenced by its id.
        """
        if not reference:
            return None

        return meta.Session.query(cls).get(reference)


meta.mapper(JSONPatch, jsonpatch_table,
            extension=[vdm.sqlalchemy.Revisioner(jsonpatch_revision_table)])

vdm.sqlalchemy.modify_base_object_mapper(JSONPatch, core.Revision, core.State)
JSONPatchRevision = vdm.sqlalchemy.create_object_version(
    meta.mapper, JSONPatch, jsonpatch_revision_table)
