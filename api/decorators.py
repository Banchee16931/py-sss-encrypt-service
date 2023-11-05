from utils.http import Handler, Request, Response
from utils.http import HTTPException, HTTPContentType, Status
import json
from typing import Callable

def handler(func: Callable):
    def inner(*args, **kwargs) -> Response:
        try:
            found_req = False
            for arg in args:
                if type(arg) == Request:
                    found_req = True
                    if arg.content_type.replace(" ", "") != HTTPContentType.JSON.value.replace(" ", ""):
                        raise HTTPException(Status.BadRequest, 
                            f"invalid Content-Type ({arg.content_type}): must be {HTTPContentType.JSON.value}")
            if found_req == False:
                raise HTTPException(Status.InternalServerError, f"handler ({func.__name__}) is mis-configured: missing req param")
            
            return func(*args, **kwargs)
        except HTTPException as inst:
            resp = Response(inst.status)
            resp.set_body(HTTPContentType.JSON, json.dumps({
                "status_code":inst.status_code(), 
                "detail":inst.status.name, 
                "message":inst.message
            }))
            return resp
        except Exception as inst:
            resp = Response(Status.InternalServerError)
            resp.set_body(HTTPContentType.JSON, json.dumps({
                "status_code":Status.InternalServerError.value, 
                "detail":Status.InternalServerError.name, 
                "message":str(inst)
            }))
            return resp
    return inner

def log(func: Callable):
    def inner(*args, **kwargs) -> Response:
        try:
            req = None
            for arg in args:
                if type(arg) == Request:
                    req = True
                    req = arg
            if req == None:
                raise HTTPException(Status.InternalServerError, f"handler ({func.__name__}) is mis-configured: missing req param")
            
            print(" entered:", func.__name__)
            resp = func(*args, **kwargs)
            print(" exited:", func.__name__)
            return resp
        except Exception as inst:
            print(" RAISED EXCEPTION:", func.__name__ + ":", inst)
            print(" exited:", func.__name__)
            raise inst
    return inner