from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from random import SystemRandom
import base64

from utils.http import HTTPException, Status

def encrypt(password: str, data: str):
    encoded_message = data.encode()

    key = SHA256.new(password.encode()).digest()
    IV = SystemRandom.randbytes(SystemRandom, AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(encoded_message) % AES.block_size
    encoded_message += bytes([padding]) * padding
    data = IV + encryptor.encrypt(encoded_message)
    encrypted_message = base64.b64encode(data).decode("latin-1") if encoded_message else data
    
    return encrypted_message

def decrypt(password: str, encrypted_data: str):
    encrypted_message = base64.b64decode(encrypted_data.encode("latin-1"))
    key = SHA256.new(password.encode()).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = encrypted_message[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(encrypted_message[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end;
    if data[-padding:] != bytes([padding]) * padding:
        raise HTTPException(Status.InternalServerError, "invalid padding attached to password")
        
    return data[:-padding].decode()