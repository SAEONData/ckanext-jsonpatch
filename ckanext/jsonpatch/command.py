# encoding: utf-8

import logging
import sys

import ckan.plugins.toolkit as tk


class JSONPatchCommand(tk.CkanCommand):
    """
    JSONPatch management commands.

    Usage:
        paster jsonpatch initdb
            - Initialize the database tables for the jsonpatch plugin
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__

    def command(self):
        if not self.args or self.args[0] in ['--help', '-h', 'help']:
            print self.usage
            sys.exit(1)

        cmd = self.args[0]
        self._load_config()

        # initialize logger after config is loaded, so that it is not disabled
        self.log = logging.getLogger(__name__)

        if cmd == 'initdb':
            self._initdb()

    def _initdb(self):
        from ckanext.jsonpatch.model import setup
        setup.init_tables()
        self.log.info("JSONPatch tables have been initialized")
