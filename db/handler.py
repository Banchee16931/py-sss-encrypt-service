from typing_extensions import Protocol, Callable
from db.client import Client
from utils.http import Handler, Request, Response
from db.database import Database

class Handler_With_DBClient(Protocol):
    def __call__(self, db: Client, req: Request) -> Response:
        pass

def handler_with_dbclient(db: Database) -> Callable[[Handler_With_DBClient], Handler]:
    def wrapper(handler: Handler_With_DBClient) -> Handler:
        def cursor_decorator(req: Request) -> Response:
            conn, client = db.client()
            try:
                result = handler(client, req)    
            except Exception as inst:
                client._cur.close()
                conn.close()
                raise inst
            else:
                client._cur.close()
                conn.close()
            return result
        return cursor_decorator
    return wrapper