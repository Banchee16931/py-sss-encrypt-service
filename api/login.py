from typing import List
from cryptography import encryption, hashing
from cryptography.sss import ShamirSecretSharing
from db.client import Client
from utils.http import HTTPException, Status

class LoginRequest:
    def __init__(self, user_passwords: dict[str, str]) -> None:
        self.user_passwords = user_passwords
        
    def validate(self):
        if (len(self.user_passwords) <= 0):
            raise HTTPException(Status.BadRequest, "amount of user passwords was zero or below")
        
        if not isinstance(self.user_passwords, dict):
            raise HTTPException(Status.BadRequest, "user_passwords is not a map/dictionary")
        
        for user_id, user_password in self.user_passwords.items():
            if (user_id.strip() == ""):
                raise HTTPException(Status.BadRequest, "a user id is empty")
            
            if (user_password.strip() == ""):
                raise HTTPException(Status.BadRequest, "a user password is empty")

def get_master_password(client: Client, service_name: str, account_id: str, req: LoginRequest) -> str:
    shares: List[str] = []
    
    print("getting data: ", req)
    for user_id in req.user_passwords.keys():
        print("in loop")
        next_pass = client.get_password(service_name, account_id, user_id)
        if not hashing.same(req.user_passwords[user_id], next_pass.hashed_password):
            raise HTTPException(Status.Unauthorized, "incorrect password given")
        
        shares.append(encryption.decrypt(req.user_passwords[user_id], next_pass.encrypted_share))     
    
    print("recreating master password")
    master_password = ShamirSecretSharing.combine(shares)
