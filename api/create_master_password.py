
from cryptography import encryption
from cryptography import hashing
from db.client import Client
from db.transaction import transaction
from models.create_master_password_request import CreateMasterPasswordRequest
from cryptography.generate import generate_password
from cryptography.sss import ShamirSecretSharing
from utils.http import HTTPException, Request, Response, Status
import json
from api.decorators import handler, log

@handler
@transaction
@log
def create_master_password(client: Client, req: Request) -> Response:
    try:
        js = json.loads(req.body)
        creation_req: CreateMasterPasswordRequest =  CreateMasterPasswordRequest(**js)
    except Exception as inst:
        raise HTTPException(Status.BadRequest, f'failed to decode request body as json: {inst}')
    
    if not "id" in req.params:
        raise HTTPException(Status.InternalServerError, "misconfigured handler: missing id in params")
    
    id = req.params["id"]
    
    creation_req.validate() 
    
    print("generating master password")
    master_password = generate_password()
    
    print("creating shares")
    shares = ShamirSecretSharing.create(
        creation_req.password_threshold, 
        len(creation_req.user_passwords),
        master_password
    )
    
    if len(shares) != len(creation_req.user_passwords):
        raise HTTPException(Status.InternalServerError, "failed to create shares equal to that of user passwords")
    
    print("storing data")
    for i, user_id in enumerate(creation_req.user_passwords):
        user_password = creation_req.user_passwords[user_id]
        
        hashed_password = hashing.create(user_password)
        encrypted_share = encryption.encrypt(user_password, shares[i])
        
        client.store_password(id, user_id, hashed_password, encrypted_share)
    
    resp = Response(Status.Created)
    
    return resp