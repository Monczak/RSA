class Decryptor:
    block_size = 4
    integer_size = 8

    @classmethod
    def decrypt(cls, key, ciphertext, orig_length):
        d_key, n = key

        padding_length = cls.block_size - orig_length % cls.block_size

        plaintext = [b""] * (orig_length // cls.block_size + 1)
        for i in range(orig_length // cls.block_size + 1):
            block = ciphertext[i]
            decrypted_block = pow(int.from_bytes(block, byteorder="little"), d_key, n)
            plaintext[i] = int.to_bytes(decrypted_block, cls.block_size, byteorder="little")

        plaintext[-1] = plaintext[-1][:cls.block_size - padding_length]
        return plaintext
