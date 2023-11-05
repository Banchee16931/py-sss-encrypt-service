class user_password_data:
    def __init__(self, user_id: str, hashed_password: str, encrypted_share: str):
        self.user_id = user_id
        self.hashed_password = hashed_password
        self.encrypted_share = encrypted_share