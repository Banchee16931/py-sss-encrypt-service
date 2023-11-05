from typing import List
from connectors import Connectors
from cryptography import encryption, hashing
from cryptography.sss import ShamirSecretSharing
from db.client import Client
from utils.http import HTTPException, Status

def get_session_key(client: Client, service_name: str, account_id: str, user_passwords: dict[str, str]) -> str:
    shares: List[str] = []
    
    print("getting data")
    for user_id in user_passwords.keys():
        next_pass = client.get_password(service_name, account_id, user_id)
        if not hashing.same(user_passwords[user_id], next_pass.hashed_password):
            raise HTTPException(Status.Unauthorized, "incorrect password given")
        
        shares.append(encryption.decrypt(user_passwords[user_id], next_pass.encrypted_share))     
    
    print("recreating master password")
    master_password = ShamirSecretSharing.combine(shares)
    
    print(f"getting session key from service {service_name}")
    return Connectors().get_session_token(service_name, account_id, master_password)