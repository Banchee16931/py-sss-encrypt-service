from enum import Enum
from typing import List, Self, Sequence, Tuple
from typing_extensions import Protocol

Method = Enum('Method', ['GET', 'PUT', 'POST', 'DELETE'])

class Status(Enum):
    OK = 200
    Created = 201
    
    BadRequest = 400
    Unauthorized = 401
    Forbidden = 403
    NotFound = 404
    
    InternalServerError = 500
    NotImplemented = 501
    

class HTTPContentType(Enum):
    HTML = "text/html; charset=utf-8"
    JSON = "application/json; charset=utf-8"
    TEXT = "text/plain; charset=utf-8"

class HTTPException(Exception):
    status: Status
    message: str
    
    def __init__(self, status: Status, message: str):
        self.status = status
        self.message = message
        
    def status_code(self) -> int:
        return self.status.value

class Request:
    url: str
    params: dict[str, str]
    body: bytes
    content_type: str
    method: Method
    
    def __init__(self, method: Method, url: str, params: dict[str, str], content_type: str, body: bytes) -> None:
        self.method = method
        self.url = url
        self.params = params
        self.content_type = content_type
        self.body = body
        
class Response:
    status: Status
    body: bytes
    headers: dict[str, str]

    def __init__(self, status: Status) -> None:
        self.status = status
        self.body = bytes('', "utf-8")
        self.headers = {}
        
    def status_code(self) -> int:
        return self.status.value
        
    def set_header(self, key: str, value: str) -> Self:
        self.headers[key] = value
        return self
        
    def set_body(self, content_type: HTTPContentType, body: str) -> Self:       
        self.headers["Content-Type"] = content_type
        self.body = bytes(body, "utf-8")
        return self

class Handler(Protocol):
    def __call__(self, req: Request) -> Response:
        pass

def get_params(params: dict[str, str], *keys: str) -> Sequence[str]:
    values: List[str] = []
    for key in keys:
        if not key in params.keys():
            raise HTTPException(Status.InternalServerError, f"misconfigured handler or route: missing {key} in params")
        values.append(params[key])
    return tuple(values)