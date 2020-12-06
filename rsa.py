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

    with open(f"{args.file[0]}.encrypted", "wb") as output_file:
        output_file.write(b"$RSA")
        output_file.write(os.path.getsize(args.file[0]).to_bytes(4, byteorder="little"))

        print("Loading...")
        plaintext = file.read()
        print("Encrypting...")
        encrypted_text = Encryptor.encrypt(public_key, plaintext)
        output_file.write(b"".join(encrypted_text))
else:
    orig_file_name = os.path.splitext(args.file[0])[0]

    print("Loading...")
    private_key = FileParser.parse_key_file(f"{orig_file_name}.prv", b"PRIV")
    encrypted_text = FileParser.parse_encrypted_file(args.file[0])

    with open(f"{orig_file_name}.decrypted", "wb") as output_file:
        print("Decrypting...")
        decrypted_text = Decryptor.decrypt(private_key, encrypted_text)
        output_file.write(b"".join(decrypted_text))

file.close()
print("Done.")
