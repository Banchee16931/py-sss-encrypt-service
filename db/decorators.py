from typing import Any
from typing_extensions import Protocol, Callable
from db.client import Client
from utils.http import HTTPException, Handler, Request, Response, Status
from db.database import Database

def with_dtclient(db: Database) -> Callable[[Callable], Handler]:
    def wrapper(func: Callable) -> Handler:
        def inner(*args, **kwargs) -> Any:
            conn, client = db.client()
            try:
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