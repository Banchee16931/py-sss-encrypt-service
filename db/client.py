from sqlite3 import Cursor

from models.password import user_password_data
from utils.http import HTTPException, Status

class Client:
    _cur: Cursor
    
    def __init__(self, cur: Cursor):
        self._cur = cur
        
    def store_password(self, service_name: str, account_id: str, user_id: str, hashed_password: str, encrypted_share: str):
        try:
            self._cur.execute("insert into passwords (service_name, account_id, user_id, hashed_password, encrypted_share) values (?, ?, ?, ?, ?)",
                (service_name, account_id, user_id, hashed_password, encrypted_share))
        except HTTPException as inst:
            raise inst
        except Exception as inst:
            inst = HTTPException(Status.InternalServerError, f"failed to store password: {inst}")
            raise inst
        
    def get_password(self, service_name: str, account_id: str, user_id: str) -> user_password_data:
        try:
            self._cur.execute("select hashed_password, encrypted_share from passwords where service_name=? and account_id=? and user_id=?",
                (service_name, account_id, user_id))
            rows = self._cur.fetchall()
            
            for row in rows:
                if len(row) != 2:
                    raise HTTPException(Status.InternalServerError, "returned amount of data from db did not match expected")
                return user_password_data(user_id, row[0], row[1])
            
            raise HTTPException(Status.NotFound, f"service_name:{service_name}, account_id:{account_id}, user_id:{user_id} does not exist")
        except HTTPException as inst:
            raise inst
        except Exception as inst:
            inst = HTTPException(Status.InternalServerError, f"failed to get password: {inst}")
            raise inst
        
    def delete_passwords(self, service_name: str, account_id: str):
        try:
            self._cur.execute("delete from passwords where service_name=? and account_id=?",
                (service_name, account_id))
        except HTTPException as inst:
            raise inst
        except Exception as inst:
            inst = HTTPException(Status.InternalServerError, f"failed to delete passwords: {inst}")
            raise inst
            
    def update_example_service_password(self, service_name: str, account_id: str, new_password: str):
        try:
            self._cur.execute("""insert or ignore into example_service_passwords 
                (service_name, account_id, password)
                values (?, ?, ?)""",
                (service_name, account_id, new_password))
            self._cur.execute("""update example_service_passwords set password=? where service_name=? and account_id=?""",
                (new_password, service_name, account_id))
        except HTTPException as inst:
            raise inst
        except Exception as inst:
            inst = HTTPException(Status.InternalServerError, f"failed to update example service password: {inst}")
            raise inst

    def get_example_service_password(self, service_name: str, account_id: str) -> str:
        try:
            self._cur.execute("select password from example_service_passwords where service_name=? and account_id=?",
                (service_name, account_id))
            rows = self._cur.fetchall()
            
            for row in rows:
                if len(row) != 1:
                    raise HTTPException(Status.InternalServerError, "returned amount of data from db did not match expected")
                return row[0]
            
            raise HTTPException(Status.NotFound, f"password for service_name:{service_name}, account_id:{account_id} does not exist")
        except HTTPException as inst:
            raise inst
        except Exception as inst:
            inst = HTTPException(Status.InternalServerError, f"failed to get example service password: {inst}")
            raise inst
    
        

