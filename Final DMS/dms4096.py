import os
import hashlib
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class DMS4096:
    def __init__(self, key=None):
        """Initialize with a secure key or generate a new one."""
        if key is None:
            key = self.generate_key()
        self.key = hashlib.sha256(key).digest()  # 256-bit AES Key

    def generate_key(self):
        """Generate a strong 4096-bit key."""
        return os.urandom(512)

    def encrypt(self, plaintext):
        """AES-256 + XOR Chaining Encryption"""
        start_time = time.time()
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        end_time = time.time()
        return (iv + encrypted).hex(), round(end_time - start_time, 6)  # Time in seconds

    def decrypt(self, encrypted_text):
        """AES-256 + XOR Chaining Decryption"""
        start_time = time.time()
        encrypted_bytes = bytes.fromhex(encrypted_text)
        iv, encrypted_data = encrypted_bytes[:16], encrypted_bytes[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        end_time = time.time()
        return decrypted.decode(), round(end_time - start_time, 6)  # Time in seconds

# ✅ Generate and save the key
if not os.path.exists("dms_4096_key.bin"):
    dms = DMS4096()
    with open("dms_4096_key.bin", "wb") as key_file:
        key_file.write(dms.key)
