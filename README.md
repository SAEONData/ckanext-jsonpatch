# ckanext-jsonpatch

[![Travis CI](https://travis-ci.org/SAEONData/ckanext-jsonpatch.svg?branch=master)](https://travis-ci.org/SAEONData/ckanext-jsonpatch)
[![Coverage](https://coveralls.io/repos/SAEONData/ckanext-jsonpatch/badge.svg)](https://coveralls.io/r/SAEONData/ckanext-jsonpatch)

An extension for [CKAN](https://ckan.org) enabling arbitrary, on-the-fly patching of JSON output
dictionaries, using the JSON Patch mechanism described by [RFC6902](https://tools.ietf.org/html/rfc6902).

## Requirements

This extension has been developed and tested with CKAN version 2.8.2.

## Installation

Activate your CKAN virtual environment:

    . /usr/lib/ckan/default/bin/activate

Install the latest development version of _ckanext-jsonpatch_ and its dependencies:

    cd /usr/lib/ckan/default
    pip install -e 'git+https://github.com/SAEONData/ckanext-jsonpatch.git#egg=ckanext-jsonpatch'
    pip install -r src/ckanext-jsonpatch/requirements.txt

In a production environment, you'll probably want to pin a specific
[release version](https://github.com/SAEONData/ckanext-jsonpatch/releases) instead, e.g.:

    pip install -e 'git+https://github.com/SAEONData/ckanext-jsonpatch.git@v1.0.0#egg=ckanext-jsonpatch'

Create the required database tables:

    cd /usr/lib/ckan/default/src/ckanext-jsonpatch
    paster jsonpatch initdb -c /etc/ckan/default/development.ini

Open your CKAN configuration file (e.g. `/etc/ckan/default/production.ini`) and
add `jsonpatch` to the list of plugins :

    ckan.plugins = ... jsonpatch

Restart your CKAN instance.
