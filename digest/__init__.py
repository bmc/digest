#!/usr/bin/env python
# ---------------------------------------------------------------------------

"""
Calculate a cryptohash on a file or standard input.

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

For usage information, the algorithms supported by your version of Python,
and other information, run:

    digest --help

For additional information, see the README (README.md) or visit
https://github.com/bmc/digest
"""

__docformat__ = "restructuredtext"

# Info about the module
__version__ = "1.2.1"
__author__ = "Brian M. Clapper"
__email__ = "bmc@clapper.org"
__url__ = "https://github.com/bmc/digest"
__copyright__ = "2008-2026 Brian M. Clapper"
__license__ = "Apache Software License Version 2.0"

# Package stuff

__all__ = ["digest", "main"]

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import hashlib
import os
import sys
from dataclasses import dataclass, replace
from typing import BinaryIO
from typing import Sequence as Seq

import click

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ALGORITHMS = sorted(hashlib.algorithms_available)
BUFSIZE = 1024 * 16
DIGEST_LENGTH_REQUIRED = {"shake_128", "shake_256"}

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Params:
    """
    Parsed command-line parameters.
    """

    buffer_size: int
    digest_length: int | None
    algorithm: str
    paths: Seq[str]


class DigestError(Exception):
    """
    Thrown to indicate an error in processing.
    """


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------


def digest(
    f: BinaryIO,
    algorithm: str,
    bufsize: int,
    digest_length: int | None = None,
) -> str:
    """
    Calculate a digest of the contents of a file. If an error occurs, this
    function raises a DigestError.

    :param f:             The file to read.
    :param algorithm:     The algorithm to use.
    :param bufsize:       The buffer size to use when reading.
    :param digest_length: The length of the digest, for variable-length
                          algorithms.
    """
    try:
        h = hashlib.new(algorithm)
        buf = bytearray(bufsize)
        while True:
            # Pyright can't grok BinaryIO.readinto(), so just disable it for
            # this line.
            n = f.readinto(buf)  # pyright: ignore
            if n <= 0:
                break
            h.update(buf[:n])

        # Some algorithms (e.g., the SHAKE algorithms) are variable length, and
        # their hexdigest() functions take a length parameter. But the generic
        # hexdigest() function doesn't, and the typing doesn't capture this
        # difference. So, type-checkers like pyright complain about the first
        # call, below. For now, we just disable pyright for that line.
        if digest_length is not None:
            return h.hexdigest(digest_length)  # pyright: ignore

        return h.hexdigest()
    except Exception as ex:
        raise DigestError(f"{algorithm}: {ex}") from ex


def positive_integer(
    ctx: click.Context, param: str, value: int | None
) -> int | None:
    """
    Ensure that a command line parameter is a positive integer.
    """
    if value is not None and value <= 0:
        raise click.BadParameter(f"{value} is not a positive integer.")

    return value


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "-b",
    "--bufsize",
    type=int,
    default=BUFSIZE,
    show_default=True,
    callback=positive_integer,
    help="Buffer size to use when reading files.",
)
@click.option(
    "-l",
    "--digest-length",
    type=int,
    callback=positive_integer,
    show_default=True,
    help="Length of the digest for variable-length algorithms.",
)
@click.option(
    "-a",
    "--algorithm",
    type=click.Choice(ALGORITHMS, case_sensitive=False),
    required=True,
    help="Digest algorithm to use.",
)
@click.version_option(version=__version__)
@click.argument(
    "paths", nargs=-1, metavar="[PATH]...", type=click.Path(exists=True)
)
def main(
    bufsize: int, digest_length: int | None, algorithm: str, paths: list[str]
) -> int:
    """
    Generate a message digest (cryptohash) of one or more files, or of standard
    input. Files are read as binary data, even if they're text files. Files are
    read BUFSIZE bytes at a time.
    """
    params = Params(
        buffer_size=bufsize,
        digest_length=digest_length,
        algorithm=algorithm,
        paths=paths,
    )

    if (params.algorithm in DIGEST_LENGTH_REQUIRED) and (
        params.digest_length is None
    ):
        raise click.BadParameter(
            f"Digest length is required for algorithm {params.algorithm}."
        )

    if (params.algorithm not in DIGEST_LENGTH_REQUIRED) and (
        params.digest_length is not None
    ):
        print(
            f"WARNING: Digest length (-l) is ignored for {params.algorithm}",
            file=sys.stderr,
        )
        params = replace(params, digest_length=None)

    try:
        if len(params.paths) == 0:
            # Standard input.
            print(
                digest(
                    f=sys.stdin.buffer,
                    algorithm=params.algorithm,
                    bufsize=params.buffer_size,
                    digest_length=params.digest_length,
                )
            )

        else:
            u_algorithm = params.algorithm.upper()
            for path in params.paths:
                if not os.path.isfile(path):
                    print(f'*** Skipping non-file "{path}".')
                    continue

                with open(path, mode="rb") as f:
                    d = digest(
                        f=f,
                        algorithm=params.algorithm,
                        bufsize=params.buffer_size,
                        digest_length=params.digest_length,
                    )
                    print(f"{u_algorithm} ({path}): {d}")
    except DigestError as ex:
        print(f"Error: {ex}", file=sys.stderr)
        return 1

    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
