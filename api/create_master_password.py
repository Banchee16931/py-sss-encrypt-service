from typing import List
from cryptography import encryption, hashing
from cryptography.generate import generate_password
from cryptography.sss import ShamirSecretSharing
from models.password import user_password_data
from utils.http import HTTPException, Status

class CreateMasterPasswordRequest:
    def __init__(self, password_threshold: int, user_passwords: dict[str, str]) -> None:
        self.password_threshold = password_threshold
        self.user_passwords = user_passwords
        
    def validate(self):
        if (self.password_threshold <= 0):
            raise HTTPException(Status.BadRequest, "password threshold was zero or below")
        
        if (len(self.user_passwords) < self.password_threshold):
            raise HTTPException(Status.BadRequest, "amount of user passwords is greater than passowrd_threshold")
        
        if not isinstance(self.user_passwords, dict):
            raise HTTPException(Status.BadRequest, "user_passwords is not a map/dictionary")
        
        for user_id, user_password in self.user_passwords.items():
            if (user_id.strip() == ""):
                raise HTTPException(Status.BadRequest, "a user id is empty")
            
            if (user_password.strip() == ""):
                raise HTTPException(Status.BadRequest, "a user password is empty")

def create_master_password(req: CreateMasterPasswordRequest) -> tuple[str, List[str]]:  
    print("generating master password")
    master_password = generate_password()
    
    print("creating shares")
    shares = ShamirSecretSharing.create(
        req.password_threshold, 
        len(req.user_passwords),
        master_password
    )
    
    if len(shares) != len(req.user_passwords):
        raise HTTPException(Status.InternalServerError, "failed to create shares equal to that of user passwords")
    
    passwords: List[user_password_data] = []
    
    print("storing data")
    for i, user_id in enumerate(req.user_passwords):
        user_pass = req.user_passwords[user_id]
        
        hashed_password = hashing.create(user_pass)
        encrypted_share = encryption.encrypt(user_pass, shares[i])
        
        passwords.append(user_password_data(user_id, hashed_password, encrypted_share))  
    
    return master_password, passwords
