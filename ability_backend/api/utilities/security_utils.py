import secrets
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64
from Cryptodome.Cipher import AES

class SecurityUtils:
    def decrypt_password_(encrypted_password, key):
        key = '123456$#@$^@1ERF'
        key = key.encode('utf-8')
        encrypted_password = base64.b64decode(encrypted_password)
        cipher = Cipher(algorithms.AES(key), modes.CBC(16 * b'\x00'), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()  # Use 128 for key size
        unpadded_password = unpadder.update(decrypted_password) + unpadder.finalize()
        return unpadded_password.decode('utf-8')

    def un_pad(s):
        # un_padding the encrypted password
        return s[:-ord(s[len(s) - 1:])]

    def decrypt_password(password, key):
        try:
            # encoding the Key
            key = key.encode('utf-8')

            enc = base64.b64decode(password)
            
            mode = AES.MODE_CBC
            # getting the initialization vector
            iv = enc[:AES.block_size]
            
            cipher = AES.new(key, mode, iv)
            
            # decoding the password
            data = cipher.decrypt(enc[AES.block_size:])
            
            if len(data) == 0:
                raise ValueError("Decrypted data is empty")
            
            padding_length = data[-1]
            data = data[:-padding_length]
            
            return data.decode('utf-8')
        except Exception as e:
            print("Exception occurred while decrypting password: ", e)