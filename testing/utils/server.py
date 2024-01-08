import socket
import types

from server.router import _Router
from server.server import Server
from utils.http import HTTPContentType


def create_valid_server(router: _Router, path: str):
    server_mock = types.SimpleNamespace()
    server_mock.headers = type("object", (), {"get": lambda value: HTTPContentType.JSON })
    server_mock.path = path
    server_mock.handle_request = Server.handle_request
    server_mock._get_body = lambda: "{}"
    server_mock.send_response = lambda code, status=None:None
    server_mock.send_header = lambda key, header:None
    server_mock.end_headers = lambda:None
    server_mock._router = router
    
    # ensure test fails during error
    def error_occurred(code: int,
        message: str | None = None,
        explain: str | None = None):
        print("code: ", code)
        if message:
            print("message: ", message)
        if explain:
            print("explain: ", explain)
        assert False
        
    server_mock.send_error = error_occurred
    
    return server_mock