from http.server import HTTPServer
from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate green threads."""
    
    def server_activate(self) -> None:
        self.RequestHandlerClass.pre_start()
        HTTPServer.server_activate(self)
        