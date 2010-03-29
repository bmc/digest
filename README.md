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

For more information, please see the [home page][].

[*digest*]: http://www.freebsd.org/cgi/url.cgi?ports/security/digest/pkg-descr
[home page]: http://bmc.github.com/digest/
