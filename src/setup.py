#!/usr/bin/python3

import os

from setuptools import setup

setup(name='DataDating',
    version='0.0.0',
    description='A Peer 2 Peer dating application.',
    author='Denis Salem',
    author_email='denissalem@tuxfamily.org',
    url='https://framagit.org/denissalem/DataDating',
    packages=['DataDating', 'DataDating.Controler'],
    license="GNU/GPLv3",
    platforms="Linux",
    long_description="A Peer 2 Peer dating application. Meet your soulmate, new friends or collaborators!",
    classifiers=[
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable"
    ],
    install_requires=[
    ],
    scripts=['datadating'],
    data_files=[ 
        (
            os.path.expanduser("~")+'/.local/share/DataDating/gui/css',
            [ 'gui/css/'+f for f in os.listdir('gui/css') ]
        ),
        (
            os.path.expanduser("~")+'/.local/share/DataDating/gui/css',
            [ 'gui/chunks/'+f for f in os.listdir('gui/chunks') ]
        ),
        (
            os.path.expanduser("~")+'/.local/share/DataDating/gui/fonts',
            [ 'gui/fonts/'+f for f in os.listdir('gui/fonts') ]
        ),
        (
            os.path.expanduser("~")+'/.local/share/DataDating/gui/images',
            [ 'gui/images/'+f for f in os.listdir('gui/images') ]
        ),
        (
            os.path.expanduser("~")+'/.local/share/DataDating/gui/script',
            [ 'gui/script/'+f for f in os.listdir('gui/script') ]
        )
    ]
)
