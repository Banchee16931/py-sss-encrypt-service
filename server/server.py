from typing import override
from api.handler import CreateMasterPasswordHandler, LoginHandler, RegenerateMasterPasswordHandler
from utils.http import HTTPException, Method, Request, Status
from http.server import BaseHTTPRequestHandler
from server.router import _Route, _Router
from http.server import HTTPServer
from socketserver import ThreadingMixIn

class Server(ThreadingMixIn, BaseHTTPRequestHandler, HTTPServer):
    """This received HTTP requests and routes them to the correct method on the router."""

    _router: _Router = None 
    
    def do_GET(self):
        """ The function that is called during a GET HTTP request. """
        self.handle_request(Method.GET)
        
    def do_POST(self):
        """ The function that is called during a POST HTTP request. """
        self.handle_request(Method.POST)
        
    def do_PUT(self):
        """ The function that is called during a PUT HTTP request. """
        self.handle_request(Method.PUT)
        
    def do_DELETE(self):
        """ The function that is called during a DELETE HTTP request. """
        self.handle_request(Method.DELETE)
        
    @classmethod
    def pre_start(self):
        """ This is ran before any requests are received """
        self._init_routes(self) # sets up the routes on the router so that requests go to their correct handlers
        print("Started Server")
    
    @override
    def handle_request(self, method: Method):
        """ 
        This is the actual method that handles requests. 
        It uses the router to get the relevant handler and calls it. 
        """
        try:             
            # getting handler
            split_route = self.path.split("/")
            while("" in split_route):
                split_route.remove("")
            handler, params = self._router.get_handler(method, split_route)
            
            # run handler
            req = Request(method, self.path, params, self.headers.get("Content-Type"), self._get_body())
            print("-", req.method.name.upper(), req.url)
            resp = handler(req)
            
            # attach basic headers
            self.send_response(resp.status_code())
            self.protocol_version = 'HTTP/1.0'
                
            # adding extra headers
            for key, header in resp.headers.items():
                self.send_header(key, header)
        
            self.end_headers()
            
            # adding body
            if len(resp.body) > 0:
                self.wfile.write(resp.body)    
                        
        except HTTPException as inst:
            # default handle exceptions via HTML
            self.send_error(inst.status_code(), explain = inst.message)
        except Exception as inst:
            # default handle exceptions via HTML
            self.send_error(int(Status.InternalServerError.value), str(inst))
        
    def _get_body(self) -> bytes:
        """ This returns the body of the request currently being handled. """
        content_length = self.headers.get('Content-Length')
        if content_length == None:
            return bytes('', "utf-8")
        content_len = int(content_length)
        return self.rfile.read(content_len)
        
    def _init_routes(self):      
        """ Adds the routes to the router. """
        self._router = router = _Router()
        router.add_route(_Route("/api/service/{service_name}/account/{account_id}", 
            CreateMasterPasswordHandler()
        ).add_method(Method.POST))
        router.add_route(_Route("/api/service/{service_name}/account/{account_id}/regenerate", 
            RegenerateMasterPasswordHandler()
        ).add_method(Method.POST))
        router.add_route(_Route("/api/service/{service_name}/account/{account_id}/login", 
            LoginHandler()
        ).add_method(Method.POST))
        
        print(router)