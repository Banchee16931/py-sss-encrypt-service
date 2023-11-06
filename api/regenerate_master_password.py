
from typing import Any
from api.login import LoginRequest, get_master_password
from connectors import Connectors
from db.client import DBClient
from api.create_master_password import CreateMasterPasswordRequest, create_master_password
from db.database import Database
from db.decorators import with_dtclient
from db.transaction import transaction
from utils.http import HTTPException, Status


class RegenerateMasterPasswordRequest:
    """ The data format for the body of a request to the regenerate master password endpoint. """
    def __init__(self, user_passwords: dict[str, str], new: dict[str, Any]) -> None:
        self.user_passwords = user_passwords
        self.new = CreateMasterPasswordRequest(**new)
        
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

        self.new.validate()
        

def regenerate_master_password(service_name: str, account_id: str, req: RegenerateMasterPasswordRequest):   
    """ If the user has authorisation, replaces a master password for a given service account with the new one given in the request. """
    print("user_pass:", req.user_passwords)
    print("new_thres:", req.new.password_threshold)
    print("new_user_pass:", req.new.user_passwords)
    req.validate()
    
    print("getting old password")
    old_master_password = with_dtclient(Database())(transaction(get_master_password))(service_name, account_id, LoginRequest(req.user_passwords))
    
    print("authenticating old password")
    Connectors().get_session_token(service_name, account_id, old_master_password)
    print("old password was correct")
    
    print("creating new master password")
    new_master_password, user_passwords = create_master_password(req.new)
    
    print("updating old password")
    Connectors().update_account_password(service_name, account_id, old_master_password, new_master_password)
    
    @with_dtclient(Database())
    @transaction
    def replace_passwords(client: DBClient):
        client.delete_passwords(service_name, account_id)
        
        for password in user_passwords:
            client.store_password(service_name, account_id,
                password.user_id, password.hashed_password, password.encrypted_share)
            
    replace_passwords()
