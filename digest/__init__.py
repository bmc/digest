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
__version__   = '1.1.0'
__author__    = 'Brian M. Clapper'
__email__     = 'bmc@clapper.org'
__url__       = 'http://software.clapper.org/digest/'
__copyright__ = '2008-2023 Brian M. Clapper'
__license__   = 'Apache Software License Version 2.0'

# Package stuff

__all__     = ['digest', 'main']

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import sys
import os
import argparse
import hashlib
from dataclasses import dataclass
from typing import NoReturn, BinaryIO, Optional, Sequence as Seq

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ALGORITHMS = hashlib.algorithms_available
BUFSIZE = 1024 * 16
DIGEST_LENGTH_REQUIRED = {'shake_128', 'shake_256'}

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Params:
    buffer_size: int
    digest_length: Optional[int]
    algorithm: str
    paths: Seq[str]

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def die(msg: str) -> NoReturn:
    print(msg, file=sys.stderr)
    sys.exit(1)

def parse_params() -> Params:
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
    length_required = ', '.join(sorted(DIGEST_LENGTH_REQUIRED))
    parser.add_argument('-l', '--digest-length', type=positive_number,
                        help='Length to use, for variable-length digests. '
                             f'Required for: {length_required}')
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}')
    parser.add_argument('algorithm', action='store', metavar='algorithm',
                        choices=ALGORITHMS,
                        help='The digest algorithm to use, one of: ' +
                             ', '.join(ALGORITHMS))
    parser.add_argument('path', action='store', nargs='*',
                        help='Input file(s) to process. If not specified, '
                             'standard input is read.')

    args = parser.parse_args()
    if ((args.algorithm in DIGEST_LENGTH_REQUIRED) and
        (args.digest_length is None)):
        die(f'Digest algorithm {args.algorithm} requires that you specify a '
            'digest length via -l or --digest-length.')
    elif ((args.algorithm not in DIGEST_LENGTH_REQUIRED) and
          (args.digest_length is not None)):
        print(f'WARNING: Digest length (-l) is ignored for {args.algorithm}.',
              file=sys.stderr)
        args.digest_length = None

    return Params(
        buffer_size=args.bufsize,
        digest_length=args.digest_length,
        algorithm=args.algorithm,
        paths=args.path
    )

def digest(f: BinaryIO,
           algorithm: str,
           bufsize: int,
           digest_length: Optional[int] = None) -> str:
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

    return h.hexdigest(digest_length) if digest_length else h.hexdigest()


def main():
    params: Params = parse_params()

    if len(params.paths) == 0:
        # Standard input.
        print(digest(f=sys.stdin.buffer,
                     algorithm=params.algorithm,
                     bufsize=params.buffer_size,
                     digest_length=params.digest_length))

    else:
        u_algorithm = params.algorithm.upper()
        for path in params.paths:
            if not os.path.isfile(path):
                print(f'*** Skipping non-file "{path}".')
                continue

            with open(path, mode='rb') as f:
                d = digest(f=f,
                           algorithm=params.algorithm,
                           bufsize=params.buffer_size,
                           digest_length=params.digest_length)
                print(f'{u_algorithm} ({path}): {d}')

    return 0

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main())
