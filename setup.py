#!/usr/bin/python3

from distutils.core import setup

'''Here we are defining where should be placed each file'''
install_data = [
    ('share/applications', ['data/com.github.malothebault.latitude.desktop']),
    ('share/metainfo', ['data/com.github.malothebault.latitude.appdata.xml']),
    ('share/icons/hicolor/128x128/apps', ['data/com.github.malothebault.latitude.svg']),
    ('/usr/share/glib-2.0/schemas', ["data/com.github.malothebault.latitude.gschema.xml"]),
    ('bin/escapade', ['src/constants.py']),
    ('bin/escapade', ['src/coordinate_systems/dms.py']),
    ('bin/escapade', ['src/handler.py']),
    ('bin/escapade', ['src/main.py']),
    ('bin/escapade', ['src/window.py']),
    ('bin/escapade', ['src/__init__.py']),
]

'''Let's go and infuse our application into the system.'''
setup(
    name='Latitude',
    version='0.1',
    author='Malo Thebault',
    description='Open and create GPX files. Plan your future adventure.',
    url='https://github.com/malothebault/latitude',
    license='GNU GPL3',
    scripts=['com.github.malothebault.latitude'],
    packages=['src'],
    data_files=install_data
)
