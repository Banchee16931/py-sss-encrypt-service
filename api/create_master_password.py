from typing import List
from cryptography import Crypt
from cryptography.sss import _ShamirSecretSharing
from models.password import UserPassword
from utils.http import HTTPException, Status

class CreateMasterPasswordRequest:
    """ The data format for the body of a request to the create master password endpoint. """
    def __init__(self, password_threshold: int, user_passwords: dict[str, str]) -> None:
        self.password_threshold = password_threshold
        self.user_passwords = user_passwords
        
    def validate(self):
        """ Checks all the values in the class are within their parameters. """
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

def create_master_password(req: CreateMasterPasswordRequest) -> tuple[str, List[UserPassword]]:  
    """ Creates a new master password, returning both the master password and its relevant password data. """
    print("generating master password")
    master_password = Crypt.generate_password()
    
    print("creating shares")
    shares = _ShamirSecretSharing.create(
        req.password_threshold, 
        len(req.user_passwords),
        master_password
    )
    
    if len(shares) != len(req.user_passwords):
        raise HTTPException(Status.InternalServerError, "failed to create shares equal to that of user passwords")
    
    passwords: List[UserPassword] = []
    
    print("storing data")
    for i, user_id in enumerate(req.user_passwords):
        user_pass = req.user_passwords[user_id]
        
        hashed_password = Crypt.hash(user_pass)
        print("input share:", user_id, shares[i])
        encrypted_share = Crypt.encrypt(user_pass, shares[i])
        
        passwords.append(UserPassword(user_id, hashed_password, encrypted_share))  
    
    return master_password, passwords
