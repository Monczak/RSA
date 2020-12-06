from rsacore import RSACore


class Encryptor:
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

        padding_start = (len(plaintext) // 4) * 4
        padding_length = len(plaintext) % 4

        cipher = [int.to_bytes(pow(int.from_bytes(plaintext[i * RSACore.block_size:i * RSACore.block_size + RSACore.block_size], byteorder="little"), e_key, n), RSACore.integer_size, byteorder="little") for i in range(len(plaintext) // RSACore.block_size)]
        cipher.append(int.to_bytes(pow(int.from_bytes(plaintext[padding_start:padding_start + padding_length], byteorder="little"), e_key, n), RSACore.integer_size, byteorder="little"))
        return cipher
