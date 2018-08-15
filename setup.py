# encoding: utf-8

from setuptools import setup, find_packages

version = '0.2'

setup(
    name='ckanext-jsonpatch',
    version=version,
    description='An extension enabling arbitrary patching of model output dictionaries',
    url='https://github.com/SAEONData/ckanext-jsonpatch',
    author='Mark Jacobson',
    author_email='mark@saeon.ac.za',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='CKAN JSON Patch',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    namespace_packages=['ckanext'],
    install_requires=[
        # CKAN extensions should list dependencies in requirements.txt, not here
    ],
    include_package_data=True,
    package_data={},
    entry_points='''
        [ckan.plugins]
        jsonpatch = ckanext.jsonpatch.plugin:JSONPatchPlugin

        [paste.paster_command]
        jsonpatch = ckanext.jsonpatch.command:JSONPatchCommand

        [babel.extractors]
        ckan = ckan.lib.extract:extract_ckan
    ''',
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    }
)
