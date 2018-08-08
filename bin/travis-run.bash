#!/bin/bash
set -e

nosetests --ckan \
          --nologcapture \
          --with-pylons=subdir/test.ini \
          --with-coverage \
          --cover-package=ckanext.jsonpatch \
          --cover-inclusive \
          --cover-erase \
          --cover-tests \
          ckanext/jsonpatch/tests
