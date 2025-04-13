from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import requests

def get_secrets(scope):
    url = "http://localhost:8000/get_secrets?scope="+scope
    payload = {"scope": scope}
    response = requests.get(url, json=payload)
    response.raise_for_status()
    return response.json()

def generate_key():
    secrets = get_secrets("credentials")
    print(secrets)
    password = password = secrets["password"].encode()
    salt = secrets["salt"].encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA1(),
        salt=salt,
        iterations=secrets["iteration"],
        length=secrets["length"],
        backend=default_backend()
    )
    print(type(password))
    key = kdf.derive(password)
    return key

def encrypt(raw):
    secrets = get_secrets("credentials")
    key = generate_key()
    iv = secrets["iv"].encode()
    print(iv)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Apply PKCS7 padding
    block_size = algorithms.AES.block_size // 8
    padded_data = raw.encode('utf-8') + (block_size - len(raw) % block_size) * bytes([block_size - len(raw) % block_size])
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.urlsafe_b64encode(ciphertext)

def decrypt(encrypted):
    secrets = get_secrets("credentials")
    key = generate_key()
    iv = secrets["iv"].encode()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    ciphertext = base64.urlsafe_b64decode(encrypted)
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_data[:-decrypted_data[-1]].decode('utf-8')

