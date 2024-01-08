import types
from unittest.mock import Mock

from server.router import _Router
from server.server import Server
from testing.utils.prebuilt import prebuild
from utils.http import HTTPContentType


def create_valid_server(router: _Router, path: str):
    server_mock = types.SimpleNamespace()
    server_mock.headers = type("object", (), {"get": lambda value: HTTPContentType.JSON.value })
    server_mock.path = path
    server_mock.handle_request = prebuild(server_mock, Server.handle_request)
    server_mock._get_body = lambda: "{}"
    server_mock.send_response = lambda code, status=None:None
    server_mock.send_header = Mock()
    server_mock.end_headers = lambda:None
    server_mock.router = router
    server_mock.wfile = types.SimpleNamespace()
    server_mock.wfile.write = Mock()
    server_mock.do_GET = prebuild(server_mock, Server.do_GET)
    server_mock.do_DELETE = prebuild(server_mock, Server.do_DELETE)
    server_mock.do_POST = prebuild(server_mock, Server.do_POST)
    server_mock.do_PUT = prebuild(server_mock, Server.do_PUT)
    
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

def attach_request_to_server(server: Server, path: str, body: str) -> Server:
    server.path = path
    server._get_body = lambda: body.encode("utf-8")
    return server