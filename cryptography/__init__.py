from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from random import SystemRandom
import base64
import secrets
import string
import bcrypt
from cryptography.sss import _ShamirSecretSharing


from utils.http import HTTPException, Status

class Crypt:
    """ Contains all functions relating to cryptography for this system. """
    
    def generate_password() -> str:
        __PASSWORD_LEN = 30
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(__PASSWORD_LEN))
    
    def encrypt(password: str, data: str):
        """ 
        Performs AES encryption on the data with password as the password.
        """
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
        """ Performs AES decryption on the encrypted_data with password as the password. """
        encrypted_message = base64.b64decode(encrypted_data.encode("latin-1"))
        key = SHA256.new(password.encode()).digest()  # use SHA-256 over our key to get a proper-sized AES key
        IV = encrypted_message[:AES.block_size]  # extract the IV from the beginning
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        data = decryptor.decrypt(encrypted_message[AES.block_size:])  # decrypt
        padding = data[-1]  # pick the padding value from the end;
        if data[-padding:] != bytes([padding]) * padding:
            raise HTTPException(Status.InternalServerError, "invalid padding attached to password")
            
        return data[:-padding].decode()
    
    def hash(password: str):
        """ Hashes a password using bcrypt. """
        return bcrypt.hashpw(password.encode("latin-1"), bcrypt.gensalt()).decode("latin-1")
        
    def check_hash(password: str, hash: str):
        """ Checks if a bycrpt hash is the hash of a given password. """
        return bcrypt.checkpw(password.encode("latin-1"), hash.encode("latin-1"))
    
    def split(minimum: int, share_count: int, password: str) -> list[str]:
        """ Uses SSS to split a password into shares. """
        return _ShamirSecretSharing.create(minimum, share_count, password)
        
    def combine(shares: list[str]) -> str:
        """ Uses SSS to combine a set of shared back into a password. """
        return _ShamirSecretSharing.combine(shares)