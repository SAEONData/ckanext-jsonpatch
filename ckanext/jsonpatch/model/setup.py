# encoding: utf-8

import logging

from ckanext.jsonpatch.model.jsonpatch import *

log = logging.getLogger(__name__)


def init_tables():
    tables = (
        jsonpatch_table,
        jsonpatch_revision_table,
    )
    for table in tables:
        if not table.exists():
            log.debug("Creating table %s", table.name)
            table.create()
        else:
            log.debug("Table %s already exists", table.name)
