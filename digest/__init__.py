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
"""

from __future__ import print_function

__docformat__ = 'restructuredtext'

# Info about the module
__version__   = '1.0.8.1'
__author__    = 'Brian M. Clapper'
__email__     = 'bmc@clapper.org'
__url__       = 'http://software.clapper.org/digest/'
__copyright__ = '2008-2022 Brian M. Clapper'
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
from typing import NoReturn, BinaryIO

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ALGORITHMS = hashlib.algorithms_available
BUFSIZE = 1024 * 16

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def die(msg: str) -> NoReturn:
    print(msg, file=sys.stderr)
    sys.exit(1)

def digest(f: BinaryIO, algorithm: str, bufsize: int) -> str:
    try:
        h = hashlib.new(algorithm)
    except ValueError as ex:
        die('%s: %s' % (algorithm, str(ex)))

    buf = bytearray(bufsize)
    while True:
        n = f.readinto(buf)
        if n <= 0:
            break
        h.update(buf[:n])

    return h.hexdigest()

def parse_params() -> argparse.Namespace:
    def positive_number(s: str) -> int:
        n = int(s)
        if n <= 0:
            raise ValueError(f'"{s}" is not a positive number.')

        return n

    parser = argparse.ArgumentParser(
        description="Generate a message digest (cryptohash) of one or more "
                    "files, or of standard input. Files are read as binary "
                    "data, even if they're text files. Files are read "
                    f"{BUFSIZE:,} bytes at a time, by default. Use -b to "
                    "change that buffer size."
    )
    parser.add_argument('-b', '--bufsize', metavar='N', type=positive_number,
                        default=BUFSIZE,
                        help="Buffer size (in bytes) to use when reading. "
                             "Defaults to %(default)d.")
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
        print(digest(sys.stdin.buffer, args.algorithm, args.bufsize))

    else:
        u_algorithm = args.algorithm.upper()
        for filename in args.file:
            if not os.path.isfile(filename):
                print(f'*** Skipping non-file "{filename}".')
                continue

            with open(filename, mode='rb') as f:
                d = digest(f, args.algorithm, args.bufsize)
                print(f'{u_algorithm} ({filename}): {d}')

    return 0

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main())
