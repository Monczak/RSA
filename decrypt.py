class Decryptor:
    @classmethod
    def decrypt(cls, key, ciphertext):
        d_key, n = key

        plaintext = [bytes(chr(pow(int.from_bytes(integer, byteorder="little"), d_key, n)), encoding="utf-8")
                     for integer in ciphertext]
        return plaintext
