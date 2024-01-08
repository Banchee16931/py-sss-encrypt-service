from typing import Any
from typing_extensions import Protocol, Callable
from db.client import DBClient
from utils.http import HTTPException, Handler, Request, Response, Status
from db.database import Database

def with_dtclient(db: Database) -> Callable[[Callable], Handler]:#
    """ This will add a new DBClient as the first parameter of whatever function it wraps. """
    def wrapper(func: Callable) -> Handler: # Used to create the wrapped function
        def inner(*args, **kwargs) -> Any: # Used to wrap the function
            conn, client = db.client()
            try:
                print("calling with", args)
                result = func(client, *args, **kwargs)
            except Exception as inst:
                client._cur.close()
                conn.close()
                raise inst
            else:
                client._cur.close()
                conn.close()
            return result
        return inner
    return wrapper