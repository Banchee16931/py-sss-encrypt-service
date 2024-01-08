import types
from server.server import Server
from unittest.mock import Mock
from testing.utils.api import create_valid_server

from utils.http import HTTPContentType, HTTPException, Method, Response, Status

def test_main_path():
    """ Tests that the server correctly handles GET, POST, PUT and DELET requests"""    
    # mock handler setup
    mocked_handler = Mock()
    mocked_handler.return_value = Response(Status.OK)
    
    # mock router setup
    mocked_router = Mock()
    mocked_router.get_handler = Mock()
    mocked_router.get_handler.return_value =  [mocked_handler ,{"value":"test_value", "value_2":"test_value_2"}]
    
    # setting up server
    server_mock = create_valid_server(mocked_router, "path/path")
    
    # act
    server_mock.do_GET()
    mocked_router.get_handler.assert_called_with(Method.GET, ["path", "path"])
    server_mock.do_PUT()
    mocked_router.get_handler.assert_called_with(Method.PUT, ["path", "path"])
    server_mock.do_DELETE()
    mocked_router.get_handler.assert_called_with(Method.DELETE, ["path", "path"])
    server_mock.do_POST()
    mocked_router.get_handler.assert_called_with(Method.POST, ["path", "path"])
    
def test_call_failed():
    """ Tests that the server will correctly report errors """
    # test data
    test_status: Status = Status.BadRequest
    test_message = "test message"
    
    # router that fails
    router_mock = types.SimpleNamespace()
    def raise_exception(a, b):
        raise HTTPException(test_status, test_message)
    router_mock.get_handler = raise_exception
    
    # basic server setup
    server_mock = create_valid_server(router_mock, "path/path")
    server_mock.send_error = Mock()
    
    # act
    server_mock.do_GET()
    
    # assert
    server_mock.send_error.assert_called_once_with(400, explain="test message")