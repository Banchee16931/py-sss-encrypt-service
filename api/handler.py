from api.create_master_password import CreateMasterPasswordRequest, create_master_password
from api.login import LoginRequest, get_master_password
from api.regenerate_master_password import RegenerateMasterPasswordRequest, regenerate_master_password
from connectors import Connectors
from db.client import DBClient
from db.database import Database
from db.decorators import with_dtclient
from db.transaction import transaction
from utils.http import HTTPContentType, HTTPException, Request, Response, Status, get_params
import json
from api.decorators import JSONHandler, log

class CreateMasterPasswordHandler:
    """ Handles create master password requests. """
    @JSONHandler
    @transaction
    @log
    def __call__(client: DBClient, req: Request) -> Response:
        print("decoding parameters")
        service_name, account_id = get_params(req.params, "service_name", "account_id")
        try:
            print("decoding request body")
            js = json.loads(req.body)
            creation_req: CreateMasterPasswordRequest =  CreateMasterPasswordRequest(**js)
        except Exception as inst:
            raise HTTPException(Status.BadRequest, f'failed to decode request body as json: {inst}')
        
        creation_req.validate()
        
        master_password, passwords = create_master_password(creation_req)
        
        print("storing passwords")
        for password in passwords:
            client.store_password(service_name, account_id,password.user_id, password.hashed_password, 
                password.encrypted_share)
        
        print("returned newly generated password")
        resp = Response(Status.Created).set_body(HTTPContentType.JSON, json.dumps({"password":master_password}))
        
        return resp

class LoginHandler:
    """ Handles login requests. """
    @JSONHandler
    @log
    def __call__(client: DBClient, req: Request) -> Response:
        print("decoding parameters")
        service_name, account_id = get_params(req.params, "service_name", "account_id")
        try:
            print("decoding request body")
            js = json.loads(req.body)
            login_req: LoginRequest =  LoginRequest(**js)
        except Exception as inst:
            raise HTTPException(Status.BadRequest, f'failed to decode request body as json: {inst}')
        
        login_req.validate() 

        try:
            master_password = get_master_password(client, service_name, account_id, login_req)
        except HTTPException as inst:
            if (inst.status == Status.NotFound):
                raise HTTPException(Status.Unauthorized, inst.message)
            raise inst
        except Exception as inst:
            raise inst
        
        session_key = Connectors().get_session_token(service_name, account_id, master_password)
        
        resp = Response(Status.OK).set_header("Authorization", f"Bearer {session_key}")
        
        return resp

class RegenerateMasterPasswordHandler:
    """ Handles regenerate master password requests. """
    @JSONHandler
    @log
    def __call__(client: DBClient, req: Request) -> Response:
        print("decoding parameters")
        service_name, account_id = get_params(req.params, "service_name", "account_id")
        try:
            print("decoding request body")
            js = json.loads(req.body)
            regen_req: RegenerateMasterPasswordRequest =  RegenerateMasterPasswordRequest(**js)
        except Exception as inst:
            raise HTTPException(Status.BadRequest, f'failed to decode request body as json: {inst}')
        
        regen_req.validate()
        
        regenerate_master_password(client, service_name, account_id, regen_req)
        
        resp = Response(Status.Created)
        
        return resp