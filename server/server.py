from typing import override
from api.handler import Handler
from utils.http import HTTPException, Method, Request, Status
from db.decorators import with_dtclient
from http.server import BaseHTTPRequestHandler
from db.database import Database
from server.router import _Route, _Router
from http.server import HTTPServer
from socketserver import ThreadingMixIn

class Server(ThreadingMixIn, BaseHTTPRequestHandler, HTTPServer):
    _router: _Router = None
    
    def do_GET(self):
        self.handle_request(Method.GET)
        
    def do_POST(self):
        self.handle_request(Method.POST)
        
    def do_PUT(self):
        self.handle_request(Method.PUT)
        
    def do_DELETE(self):
        self.handle_request(Method.DELETE)
        
    @classmethod
    def pre_start(self):
        self.init_routes(self)
        print("Started Server")
    
    @override
    def handle_request(self, method: Method):
        try:             
            # getting handler
            split_route = self.path.split("/")
            while("" in split_route):
                split_route.remove("")
            handler, params = self._router.get_handler(method, split_route)
            
            # run handler
            req = Request(method, self.path, params, self.headers.get("Content-Type"), self.get_body())
            print("-", req.method.name.upper(), req.url)
            resp = handler(req)
            
            # basic headers
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
        
    def get_body(self) -> bytes:
        content_length = self.headers.get('Content-Length')
        if content_length == None:
            return bytes('', "utf-8")
        content_len = int(content_length)
        return self.rfile.read(content_len)
        
    def init_routes(self):      
        self._router = router = _Router()
        router.add_route(_Route("/api/service/{service_name}/account/{account_id}", 
            Handler.create_master_password
        ).add_method(Method.POST))
        router.add_route(_Route("/api/service/{service_name}/account/{account_id}/regen", 
            Handler.regenerate_master_password
        ).add_method(Method.POST))
        router.add_route(_Route("/api/service/{service_name}/account/{account_id}/login", 
            Handler.login
        ).add_method(Method.POST))
        
        print(router)