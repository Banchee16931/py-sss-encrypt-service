from sqlite3 import Cursor

class Client:
    _cur: Cursor
    
    def __init__(self, cur: Cursor):
        self._cur = cur
        
    def store_password(self, id: str, user_id: str, hashed_password: str, encrypted_share: str):
        self._cur.execute("insert into passwords (id, user_id, hashed_password, encrypted_share) values (?, ?, ?, ?)",
            (id, user_id, hashed_password, encrypted_share))