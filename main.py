from cryptography import hashing
from server.server import Server
from server.threaded_server import ThreadedHTTPServer

hostName = "localhost"
serverPort = 8080

def main():
    hash = hashing.create("1")
    print("here we go: ", hashing.same("1", hash))
    
    threadedServer = ThreadedHTTPServer(('localhost', 8080), Server)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        threadedServer.serve_forever()
    except KeyboardInterrupt:
        pass

    threadedServer.server_close()
    print("Server stopped.")
 
if __name__ == "__main__":   
    main()
    