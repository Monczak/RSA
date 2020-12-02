import argparse
from enum import Enum
import os

from encrypt import Encryptor
from decrypt import Decryptor
from fileparse import FileParser
from rsacore import RSACore


class OperationMode(Enum):
    ENCRYPT = 0
    DECRYPT = 1


parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument("-e", "--encrypt", help="encrypt file", action="store_true")
group.add_argument("-d", "--decrypt", help="decrypt file", action="store_true")
parser.add_argument("file", type=str, nargs=1)

args = parser.parse_args()

if not (args.encrypt or args.decrypt):
    print("error: you must provide a mode of operation (encrypt or decrypt)")

mode = OperationMode.ENCRYPT if args.encrypt else OperationMode.DECRYPT

file = open(args.file[0], "rb")

if mode == OperationMode.ENCRYPT:
    public_key, private_key = RSACore.generate_key_pair()
    Encryptor.write_key_files(args.file[0], public_key, private_key)
    Encryptor.encrypt(private_key, file.read())
else:
    # Get the public key stored in the file "(file name with extension).pub"
    public_key = FileParser.parse_key_file(f"{os.path.splitext(args.file[0])[0]}.pub", b"PUB0")
    encrypted_text = FileParser.parse_encrypted_file(args.file[0])

    Decryptor.decrypt(public_key, encrypted_text)

print("Done.")
