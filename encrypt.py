class Encryptor:
    block_size = 8

    @classmethod
    def write_key_files(cls, name, public_key, private_key):
        with open(f"{name}.pub", "wb") as file:
            file.write(b'PUB0')
            file.write(public_key[0].to_bytes(8, byteorder="little"))
            file.write(public_key[1].to_bytes(8, byteorder="little"))

        with open(f"{name}.prv", "wb") as file:
            file.write(b'PRIV')
            file.write(private_key[0].to_bytes(8, byteorder="little"))
            file.write(private_key[1].to_bytes(8, byteorder="little"))

    @classmethod
    def encrypt(cls, key, plaintext):
        e_key, n = key

        cipher = [int.to_bytes(pow(char, e_key, n), cls.block_size, byteorder="little") for char in plaintext]
        return cipher
