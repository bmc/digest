#!/usr/bin/env python
#
# $Id$
# ---------------------------------------------------------------------------

"""
Calculate a cryptohash on a file or standard input.

Usage:

    **digest** *algorithm* [file] ...

The *digest* utility calculates message digests of files or, if no file
is specified, standard input. The set of supported digests depends on the
current Python interpreter and the version of OpenSSL present on the system.
However, at a minimum, *digest* supports the following algorithms:

    +-------------+--------------------------------------+
    | Argument    | Algorithm                            |
    +=============+======================================+
    | md5         | The MD5 algorithm                    |
    +-------------+--------------------------------------+
    | sha1        | The SHA-1 algorithm                  |
    +-------------+--------------------------------------+
    | sha224      | The SHA-224 algorithm                |
    +-------------+--------------------------------------+
    | sha256      | The SHA-256 algorithm                |
    +-------------+--------------------------------------+
    | sha384      | The SHA-384 algorithm                |
    +-------------+--------------------------------------+
    | sha512      | The SHA-512 algorithm                |
    +-------------+--------------------------------------+

This program is modeled on the *digest* program found in BSD Un\*x systems
and written by Alistair G. Crooks. This Python version is an independently
implemented program based on the manual page and output from the BSD *digest*
program.
"""

__docformat__ = 'restructuredtext'

# Info about the module
__version__   = '1.0'
__author__    = 'Brian M. Clapper'
__email__     = 'bmc@clapper.org'
__url__       = 'http://www.clapper.org/software/python/digest/'
__copyright__ = '2008 Brian M. Clapper'
__license__   = 'BSD-style license'

# Package stuff

__all__     = ['digest', 'main']

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import sys
import os
import hashlib

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

USAGE = '''Usage: %s algorithm [file] ...

Generate a cryptohash of one or more files, or of standard input.

"algorithm" can be one of: md5, sha1, sha224, sha384, sha512''' %\
os.path.basename(sys.argv[0])

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def die(msg):
    print >> sys.stderr, msg
    sys.exit(1)

def digest(f, algorithm):
    try:
        h = hashlib.new(algorithm)
    except ValueError, ex:
        die('%s: %s' % (algorithm, str(ex)))

    h.update(f.read())
    return h.hexdigest()

def main():
    if len(sys.argv) < 2:
        die(USAGE)

    algorithm = sys.argv[1]
    if len(sys.argv) == 2:
        # Standard input.
        print digest(sys.stdin, algorithm)

    else:
        u_algorithm = algorithm.upper()
        for filename in sys.argv[2:]:
            print '%s (%s) = %s' % \
                  (u_algorithm, filename, digest(open(filename), algorithm))

    return 0

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main())
