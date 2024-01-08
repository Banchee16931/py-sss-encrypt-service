from unittest.mock import Mock
from server.route import _Route
from server.router import _Router
from server.server import Server
from testing.utils.api import create_valid_server
from utils.http import HTTPContentType, Method, Request, Response, Status


def test_server_handle_request():
    """ Checks that a request can be correctly routed from the server """
    # test data
    test_value = "I am a test value"
    input_path = "path/other/"+test_value
    expected_request = Request(Method.GET, input_path, {"value":test_value}, HTTPContentType.JSON, "{}")
    
    # handler setup
    handler = Mock()
    handler.return_value = Response(Status.OK)
    
    # router setup
    router = _Router()
    target_route = _Route("path/other/{value}", handler)
    target_route.add_method(Method.GET)
    router.add_route(target_route)
    
    # server setup
    server_mock = create_valid_server(router, "path/other/"+test_value)
    server_mock.send_response = Mock()
    server_mock.send_header = Mock()
    
    # act
    Server.do_GET(server_mock)
    
    # assert
    handler.assert_called_once_with(expected_request)
    server_mock.send_response.assert_called_once_with(Status.OK.value)