from typing import Any, Callable
from db.client import Client
from utils.http import HTTPException, Status

def transaction(func: Callable) -> Any:
    def inner(*args, **kwargs) -> Any:
        client = None
        for arg in args:
            if type(arg) == Client:
                client = arg
                
        if client == None:
            raise HTTPException(int(Status.InternalServerError.value), f"handler ({func.__name__}) is mis-configured: missing db client param")
        
        client._cur.execute("begin;")
        print(" started transaction")
        try:
            ret = func(*args, **kwargs)
            client._cur.execute("commit;")
            print(" commited transaction")
            return ret
        except Exception as inst:
            client._cur.execute("rollback;")
            print(" rolled back transaction")
            raise inst
    return inner