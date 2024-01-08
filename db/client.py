from sqlite3 import Cursor

from models.password import UserPassword
from utils.http import HTTPException, Status

class DBClient:
    """ Contains all the interactions that a handler can perform on the database. """
    _cur: Cursor
    
    def __init__(self, cur: Cursor):
        self._cur = cur
        
    def store_password(self, service_name: str, account_id: str, user_id: str, hashed_password: str, encrypted_share: str):
        """ Stores a given password in the passwords table. """
        try:
            self._cur.execute("insert into passwords (service_name, account_id, user_id, hashed_password, encrypted_share) values (?, ?, ?, ?, ?)",
                (service_name, account_id, user_id, hashed_password, encrypted_share)) # SQL execution
        except HTTPException as inst:
            raise inst
        except Exception as inst:
            inst = HTTPException(Status.InternalServerError, f"failed to store password: {inst}")
            raise inst
        
    def get_password(self, service_name: str, account_id: str, user_id: str) -> UserPassword:
        try:
            self._cur.execute("select hashed_password, encrypted_share from passwords where service_name=? and account_id=? and user_id=?",
                (service_name, account_id, user_id)) # SQL query
            rows = self._cur.fetchall() # Getting the rows from the query
            
            for row in rows:
                if len(row) != 2: # Checking the correct amount if columns has been returned
                    raise HTTPException(Status.InternalServerError, "returned amount of data from db did not match expected")
                return UserPassword(user_id, row[0], row[1]) # Returns the queried user password
            
            raise HTTPException(Status.NotFound, f"service_name:{service_name}, account_id:{account_id}, user_id:{user_id} does not exist")
        except HTTPException as inst:
            raise inst
        except Exception as inst:
            inst = HTTPException(Status.InternalServerError, f"failed to get password: {inst}")
            raise inst
        
    def delete_passwords(self, service_name: str, account_id: str):
        """ Deletes a subset of passwords that are under a speficic service's account. """
        try:
            self._cur.execute("delete from passwords where service_name=? and account_id=?",
                (service_name, account_id)) # SQL execute
        except HTTPException as inst:
            raise inst
        except Exception as inst:
            inst = HTTPException(Status.InternalServerError, f"failed to delete passwords: {inst}")
            raise inst
            
    def update_example_service_password(self, service_name: str, account_id: str, new_password: str):
        """ Replaces the old master password for a given service's account with the new one.
        
        PLEASE NOTE: This is a mock for the demo, yes it is saving raw passwords into the database. 
        No that isn't and issue because this is a mock and will never be in production.
        """
        
        try:
            self._cur.execute("""insert or ignore into example_service_passwords 
                (service_name, account_id, password)
                values (?, ?, ?)""",
                (service_name, account_id, new_password)) # SQL execute
            self._cur.execute("""update example_service_passwords set password=? where service_name=? and account_id=?""",
                (new_password, service_name, account_id)) # SQL execute
        except HTTPException as inst:
            raise inst
        except Exception as inst:
            inst = HTTPException(Status.InternalServerError, f"failed to update example service password: {inst}")
            raise inst

    def get_example_service_password(self, service_name: str, account_id: str) -> str:
        """ Gets the current master password associated with a service account. 
        
        PLEASE NOTE: This is a mock for the demo, yes it is saving raw passwords into the database. 
        No that isn't and issue because this is a mock and will never be in production.
        """
        
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
    
        

