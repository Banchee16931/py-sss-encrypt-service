from server.route import _Route


def test_main_path():
    """ Tests that a _Route can correctly receive a path and check if it matches itself """
    # assign
    test_handler = "fake handler"
    test_value = "this is a value"
    
    route = _Route("this/is/a/path/{value}", test_handler)
    
    # act
    actual_handler, actual_params = route.get_handler(["this", "is", "a", "path", test_value])
    
    # assert
    assert actual_handler == test_handler
    assert actual_params == {"value": test_value}