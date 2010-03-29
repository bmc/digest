---
title: digest — Command to calculate message digests
layout: withTOC
---

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

This program is modeled on the FreeBSD [*digest*][] port (written by
Alistair G. Crooks). This Python version is an independently implemented
program based on the manual page and on output from Crooks' program.

[*digest*]: http://www.freebsd.org/cgi/url.cgi?ports/security/digest/pkg-descr

## Usage

> digest *algorithm* \[file\] ...

If you run *digest* without any parameters, it will give you a usage message
and will display the supported message digest algorithms for your installation.

## Getting and installing *digest*

### Installing via EasyInstall

Because *digest* is available via [PyPI][], if you have [EasyInstall][]
installed on your system, installing *digest* is as easy as running this
command (usually as `root` or the system administrator):

    easy_install digest

### Installing from source

You can also install *digest* from source. Either download the source
(as a zip or tarball) from <http://github.com/bmc/digest/downloads>, or
you can make a local read-only clone of the [Git repository][] using one of
the following commands:

    $ git clone git://github.com/bmc/digest.git
    $ git clone http://github.com/bmc/digest.git

[EasyInstall]: http://peak.telecommunity.com/DevCenter/EasyInstall
[PyPI]: http://pypi.python.org/pypi
[Git repository]: http://github.com/bmc/digest

Once you have a local `digest` source directory, change your working directory
to the source directory, and type:

    python setup.py install

To install it somewhere other than the default location (such as in your
home directory) type:

    python setup.py install --prefix=$HOME

## Author

Brian M. Clapper, [bmc@clapper.org][]

[bmc@clapper.org]: mailto:bmc@clapper.org

## Copyright

Copyright &copy; 2008-2010 Brian M. Clapper

## License

BSD-style license. See the accompanying [license][] file.

[license]: license.html
