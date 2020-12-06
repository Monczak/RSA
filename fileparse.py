from rsacore import RSACore


class FileParser:
    # Returns a byte string with the encrypted data
    @classmethod
    def parse_encrypted_file(cls, file_path):
        with open(file_path, "rb") as file:
            magic_num = file.read(4)
            assert magic_num == b"$RSA", f"Bad magic number in encrypted file: " \
                                         f"expected b'$RSA', got {magic_num}"

            orig_length = int.from_bytes(file.read(4), byteorder="little")

            encrypted_data = file.read()
            split_data = [encrypted_data[i * RSACore.integer_size:i * RSACore.integer_size + RSACore.integer_size] for i in range(0, orig_length)]
            return orig_length, split_data

    # Returns a tuple with the parsed key (n, d/e)
    @classmethod
    def parse_key_file(cls, file_path, magic_number):
        with open(file_path, "rb") as file:
            magic_num = file.read(4)
            assert magic_num == magic_number, f"Bad magic number in key file {file_path}: " \
                                              f"expected {magic_number}, got {magic_num}"

            n = int.from_bytes(file.read(8), byteorder="little")
            de = int.from_bytes(file.read(8), byteorder="little")

            return n, de
