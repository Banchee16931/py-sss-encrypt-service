from server.route import _Route
from utils.http import HTTPException, Handler, Method, Status

class _Router():
    """ Matches up incoming requests with their relevant handler. """
    
    routes: dict[Method, list[_Route]]
        
    def __init__(self):
        self.routes = {}
    
    def get_handler(self, method: Method, path: list[str]) -> tuple[Handler, dict[str, str]]:     
        """ This returns the handler that is mapped to the given path. """ 
        if self.routes.get(method) == None:
            self.routes[method] = []
        
        # loops through each route to see if they are the one that has the correct handler.
        for route_option in self.routes[method]:
            try:
                return route_option.get_handler(path)
            except Exception:
                continue

        raise HTTPException(Status.NotFound, "no route exists for that path")
                
    def add_route(self, route: _Route) -> None:
        """ Adds a route to the self.routes Map """
        for method in route.methods():
            if self.routes.get(method) == None:
                self.routes[method] = []
            self.routes[method].append(route)
            
    def __repr__(self) -> str:
        return self.__str__()
                
    def __str__(self) -> str:
        routeList: list[str] = []
        for method, routes in self.routes.items():
            for route in routes: 
                routeList.append(" "+str(method.name) + " " + str(route))
        routeList.sort()
        routeList.insert(0, "initialised routes:")
        return '\n'.join(routeList)