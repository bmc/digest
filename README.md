# digest

## Introduction

The *digest* utility calculates message digests of files or, if no file is
specified, standard input. The set of supported digests depends on the
current Python interpreter and the version of OpenSSL present on the
system. However, at a minimum, *digest* supports the following algorithms:

* md5: The MD5 algorithm
* sha1: The SHA1 algorithm
* sha224: The SHA224 algorithm
* sha256: The SHA256 algorithm
* sha384: The SHA384 algorithm
* sha512: The SHA512 algorithm

Type `digest -h` to see a full list of algorithms available to your
installation.

[home page]: http://software.clapper.org/digest/

## Copyright and License

Digest is copyright © 2008-2023 Brian M. Clapper.

Prior to version 1.1.0, *digest* was released under a 3-clause BSD license.
As of version 1.1.0 *digest* is released under the Apache Software License,
version 2.0. See [the license file](LICENSE.md) and
<https://www.apache.org/licenses/LICENSE-2.0> for more details.
