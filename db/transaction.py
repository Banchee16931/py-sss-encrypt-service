from typing import Any, Callable
from db.client import DBClient
from utils.http import HTTPException, Status

def transaction(func: Callable) -> Any:
    """ 
    When wrapped round a function with a valid DBClient, it will
    start and handle a transaction that lasts the lifetime of the wrapped function. 
    """
    def inner(*args, **kwargs) -> Any:
        # Get paramter of type Client
        client = None
        for arg in args:
            if type(arg) == DBClient:
                client = arg
                
        if client == None: # Error if not wrapping a DBClient based class
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