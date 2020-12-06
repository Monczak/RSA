# RSA
Basic RSA encryptor/decryptor, made in Python

# How to use

### Encryption
To encrypt a file, type `python rsa.py -e path/to/file` in a command interpreter.

This will create a "(file name with extension).encrypted" file in the location of the original file, as well as files containing the public key and the private key.

### Decryption
To decrypt a file, type `python rsa.py -d path/to/file` in a command interpreter.

Decrypting a file requires a private key file present in the same directory as the encrypted file, which should be named like the encrypted file, except with a .prv extension.
