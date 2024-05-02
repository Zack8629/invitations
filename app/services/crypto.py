class Crypto:
    def __init__(self, fernet):
        self.fernet = fernet

    key_mask = 3

    def encrypt_data(self, data):
        key = self.fernet.generate_key()
        len_key = f'{len(key):0{self.key_mask}d}'
        cipher = self.fernet(key)
        encrypted_data = cipher.encrypt(str(data).encode())

        return len_key + key.decode() + encrypted_data.decode()

    def decrypt_data(self, encrypted_data: str):
        len_key = self.key_mask + int(encrypted_data[:self.key_mask])
        key = encrypted_data[self.key_mask:len_key]
        encrypted_data_bytes = encrypted_data[len_key:].encode()

        cipher = self.fernet(key)
        decrypted_data = cipher.decrypt(encrypted_data_bytes).decode()

        return decrypted_data
