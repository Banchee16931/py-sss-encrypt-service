from typing import List
from cryptography import Crypt
from cryptography.sss import _ShamirSecretSharing
from db.client import DBClient
from utils.http import HTTPException, Status

class LoginRequest:
    """ The data format for the body of a request to the login endpoint. """
    def __init__(self, user_passwords: dict[str, str]) -> None:
        self.user_passwords = user_passwords
        
    def validate(self):
        """ Checks all the values in the class are within their parameters. """
        if (len(self.user_passwords) <= 0):
            raise HTTPException(Status.BadRequest, "amount of user passwords was zero or below")
        
        if not isinstance(self.user_passwords, dict):
            raise HTTPException(Status.BadRequest, "user_passwords is not a map/dictionary")
        
        for user_id, user_password in self.user_passwords.items():
            if (user_id.strip() == ""):
                raise HTTPException(Status.BadRequest, "a user id is empty")
            
            if (user_password.strip() == ""):
                raise HTTPException(Status.BadRequest, "a user password is empty")

def get_master_password(client: DBClient, service_name: str, account_id: str, req: LoginRequest) -> str:
    """ Gets the shares related to the login request and attempts to reconstruct them into a master password """
    shares: List[str] = []
    
    for user_id in req.user_passwords.keys():
        next_pass = client.get_password(service_name, account_id, user_id)
        if not Crypt.check_hash(req.user_passwords[user_id], next_pass.hashed_password):
            raise HTTPException(Status.Unauthorized, "incorrect password given")
        
        shares.append(Crypt.decrypt(req.user_passwords[user_id], next_pass.encrypted_share))     
    master_password = _ShamirSecretSharing.combine(shares)
    print("output master pass: ", master_password)
    
    return master_password