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

        