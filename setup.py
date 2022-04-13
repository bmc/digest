#!/usr/bin/env python

import sys
import os
sys.path += [os.getcwd()]

from setuptools import setup, find_packages
import re
import imp

PKG = 'digest'
DESCRIPTION = 'Calculate message digests of files or standard input'

def load_info():
    # Look for identifiers beginning with "__" at the beginning of the line.

    result = {}
    pattern = re.compile(r'^(__\w+__)\s*=\s*[\'"]([^\'"]*)[\'"]')
    here = os.path.dirname(os.path.abspath(sys.argv[0]))
    for line in open(os.path.join(here, PKG, '__init__.py'), 'r'):
        match = pattern.match(line)
        if match:
            result[match.group(1)] = match.group(2)

    sys.path = [here] + sys.path
    mf = os.path.join(here, PKG, '__init__.py')
    try:
        m = imp.load_module(PKG, open(mf), mf,
                            ('__init__.py', 'r', imp.PY_SOURCE))
        result['long_description'] = m.__doc__
    except:
        result['long_description'] = DESCRIPTION
    return result

info = load_info()

# Now the setup stuff.

DOWNLOAD_URL = ('http://pypi.python.org/packages/source/d/%s/%s-%s.tar.gz' %
                (PKG, PKG, info['__version__']))

setup (name                          = PKG,
       version                       = info['__version__'],
       description                   = DESCRIPTION,
       long_description              = info['long_description'],
       long_description_content_type = 'text/x-rst',
       packages                      = find_packages(),
       url                           = info['__url__'],
       license                       = info['__license__'],
       author                        = info['__author__'],
       author_email                  = info['__email__'],
       entry_points                  = {
           'console_scripts' : 'digest=digest:main'
        },
       classifiers                   = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Filters',
        'Topic :: Utilities',
]
)
