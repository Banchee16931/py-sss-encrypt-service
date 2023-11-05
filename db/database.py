import sqlite3
from typing import Tuple

from db.client import Client
from db.transaction import transaction
from utils.http import HTTPException, Status

class Database:
    def __new__(self):
        # forces this class to be a singleton, as we only want one database connection
        if not hasattr(self, 'instance'):
            self.instance = super(Database, self).__new__(self)
            
        print("setting up schema")
        conn, client = self.client(self)
        try:
            self._setup(client)    
        except Exception as inst:
            client._cur.close()
            conn.close()
            raise inst
        else:
            client._cur.close()
            conn.close()
        
        return self.instance
        
    def client(self) -> Tuple[sqlite3.Connection, Client]:
        try:
            conn = sqlite3.connect("./db.sqlite")
            conn.isolation_level = None
            cur = conn.cursor()
            return conn, Client(cur)
        except Exception as inst:
            raise HTTPException(Status.InternalServerError, f"failed to create db connection: {inst}")
        
        
    @transaction
    def _setup(client: Client):
        try:
            print("ensuring passwords table")
            client._cur.execute("""
            create table if not exists passwords (
                service_name text,
                account_id text,
                user_id text,
                hashed_password text,
                encrypted_share text,
                primary key (service_name, account_id, user_id)
            );""")
            client._cur.execute("""
            create table if not exists example_service_passwords (
                service_name text,
                account_id text,
                password text,
                primary key (service_name, account_id)
            );""")
        except Exception as inst:
            raise HTTPException(Status.InternalServerError, f"failed to create database: {str(inst)}")
        
        
    
