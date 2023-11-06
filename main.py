from server.server import Server
from server.threaded_server import ThreadedHTTPServer

hostName = "localhost"
serverPort = 8080

def main():
    """ The start point of the system. """
    
    # Creating Server
    threadedServer = ThreadedHTTPServer(('localhost', 8080), Server)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Starting server
        threadedServer.serve_forever()
    except KeyboardInterrupt:
        pass

    # Properally closing server
    threadedServer.server_close()
    print("Server stopped.")
 
if __name__ == "__main__":   
    main()
    