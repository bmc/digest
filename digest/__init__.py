#!/usr/bin/env python
# ---------------------------------------------------------------------------

"""
Calculate a cryptohash on a file or standard input.

Usage:

    **digest** -h
    **digest** [-e encoding] *algorithm* [file] ...

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

from __future__ import print_function

__docformat__ = 'restructuredtext'

# Info about the module
__version__   = '1.0.5'
__author__    = 'Brian M. Clapper'
__email__     = 'bmc@clapper.org'
__url__       = 'http://software.clapper.org/digest/'
__copyright__ = '2008-2011 Brian M. Clapper'
__license__   = 'BSD-style license'

# Package stuff

__all__     = ['digest', 'main']

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import sys
import os
import argparse
import hashlib
from typing import NoReturn

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ALGORITHMS = ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512')

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def die(msg: str) -> NoReturn:
    print(msg, file=sys.stderr)
    sys.exit(1)

def digest(f: str, algorithm: str, encoding: str) -> str:
    try:
        h = hashlib.new(algorithm)
    except ValueError as ex:
        die('%s: %s' % (algorithm, str(ex)))

    s = f.read()
    h.update(s.encode(encoding))
    return h.hexdigest()

def parse_params() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a message digest (cryptohash) of one or more "
                    "files, or of standard input."
    )
    parser.add_argument('-e', '--encoding', action='store', default='utf-8',
                        help='Specify the encoding of the input(s). Defaults '
                             'to "%(default)s".')
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}')
    parser.add_argument('algorithm', action='store', metavar='algorithm',
                        choices=ALGORITHMS,
                        help='The digest algorithm to use, one of: ' +
                             ', '.join(ALGORITHMS))
    parser.add_argument('file', action='store', nargs='*',
                        help='Input file(s) to process. If not specified, '
                             'standard input is read.')
    return parser.parse_args()

def main():
    args: argparse.Namespace = parse_params()

    if len(args.file) == 0:
        # Standard input.
        print(digest(sys.stdin, args.algorithm, args.encoding))

    else:
        u_algorithm = args.algorithm.upper()
        for filename in args.file:
            with open(filename, mode='r', encoding=args.encoding) as f:
                d = digest(f, args.algorithm, args.encoding)
                print(f'{u_algorithm} ({filename}): {d}')

    return 0

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main())
