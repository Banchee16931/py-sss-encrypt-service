from server.route import _Route
from server.router import _Router
from utils.http import Method


def test_main_path():
    """ Tests that the router can correctly send a route to the destination handler"""
    router = _Router()
    
    fake_handler = "fake handler"
    route_mock = _Route("path/path", fake_handler)
    route_mock.add_method(Method.GET)
    router.add_route(route_mock)
    
    router.get_handler(Method.GET, ["path", "path"])