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

## Usage

> digest -v
> digest -h
> digest *algorithm* \[file\] ...

Run `digest -h` to see a list of algorithms supported by your Python installation.

## Getting and installing *digest*

Easiest:

```
pip install digest
```

### Installing from source

Clone the repo, and run the setup:

```bash
$ git clone https://github.com/bmc/digest
$ cd digest
$ python setup.py install
```

But `pip` is easier...

## Author

Brian M. Clapper, [bmc@clapper.org][]

[bmc@clapper.org]: mailto:bmc@clapper.org

## Copyright

Copyright &copy; 2008-2022 Brian M. Clapper

## License

BSD-style license. See the accompanying [license][] file.

## Patches

I gladly accept patches from their original authors. Feel free to email
patches to me or to fork the [GitHub repository][] and send me a pull
request. Along with any patch you send:

* Please state that the patch is your original work.
* Please indicate that you license the work to the *digest*
  project under a [BSD License][license].

[GitHub repository]: http://github.com/bmc/javaeditline
[license]: license.html
