class UserPassword:
    """ A data class that stores details about a specific user password. """
    
    def __init__(self, user_id: str, hashed_password: str, encrypted_share: str):
        self.user_id = user_id
        self.hashed_password = hashed_password
        self.encrypted_share = encrypted_share