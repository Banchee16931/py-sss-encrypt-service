import json
import sqlite3
import tempfile
import types
from typing import Tuple
from connectors import Connectors
from cryptography import Crypt
from cryptography.sss import _ShamirSecretSharing

from db.client import DBClient
from db.database import Database
from db.decorators import with_dtclient
from server.server import Server
from testing.utils.api import attach_request_to_server, create_valid_server
from testing.utils.passwords import create_user_id, create_user_passwords
from utils.http import HTTPException, Status

def test_master_password_generation():
     # database setup
    database = types.SimpleNamespace()
    database_file = tempfile.NamedTemporaryFile(delete=False)
    database_file.close()
    database_file = database_file.name
    def client() -> Tuple[sqlite3.Connection, DBClient]:
        try:
            conn = sqlite3.connect(database_file)
            conn.isolation_level = None
            cur = conn.cursor()
            return conn, DBClient(cur)
        except Exception as inst:
            raise HTTPException(Status.InternalServerError, f"failed to create db connection: {inst}")
        
    database.client = client
    with_dtclient(database)(Database.setup)()
    
    # server setup    
    server = create_valid_server("", "")
    server.database = database
    Server._init_routes(server)
    server = create_valid_server(server.router, "")
    
    # test data
    threshold, user_passwords = create_user_passwords()
    account_id = create_user_id()
    
    # setting up for creating master password
    print("creating master password")
    req_body = {"password_threshold":2, "user_passwords":user_passwords}
    # requirement: 2.1 
    server = attach_request_to_server(server, "/api/service/example/account/"+account_id, json.dumps(req_body))
    # act
    server.do_POST()
    # assert
    server.wfile.write.was_called()
    jsonResp = json.loads(server.wfile.write.call_args.args[0])
    resp = types.SimpleNamespace(**jsonResp)
    # requirement: 2.2
    @with_dtclient(database)
    def check_database(client: DBClient):
        shares = []
        for user, password in user_passwords.items():
            user_pass = client.get_password("example", account_id, user)
            assert Crypt.check_hash(password, user_pass.hashed_password) # check has is of user password
            share = Crypt.decrypt(password, user_pass.encrypted_share)
            shares.append(share)
            
        output_password = Crypt.combine(shares[:2])
        assert _ShamirSecretSharing.combine(shares) == resp.password
    check_database()