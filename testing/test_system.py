from http.client import HTTPException
import json
import os
import sqlite3
import tempfile
import types
from typing import Tuple
from unittest.mock import Mock
from db.client import DBClient
from db.database import Database
from db.decorators import with_dtclient
from server.server import Server
from testing.utils.api import attach_request_to_server, create_valid_server
from testing.utils.passwords import create_user_id, create_user_passwords
from utils.http import Status


def test_main_path():
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
    
    for x in range(10):
        # test data
        threshold, user_passwords = create_user_passwords()
        account_id = create_user_id()
        
        # creating master password
        print("creating master password")
        req_body = {"password_threshold":threshold, "user_passwords":user_passwords}
        server = attach_request_to_server(server, "/api/service/example/account/"+account_id, json.dumps(req_body))
        Server.do_POST(server)
        jsonResp = json.loads(server.wfile.write.call_args.args[0])
        print("response: ", jsonResp)
        resp = types.SimpleNamespace(**jsonResp)
        
        assert len(resp.password) > 0
        
    
    