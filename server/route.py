from typing import Self
from utils.http import Handler, Method

class _Route():
    routeRepr: str
    route: list[str]
    params: dict[int, str]
    handler: Handler
    __methods: list[Method]
    
    def __init__(self, route: str, handler: Handler):
        self.handler = handler
        self.route = route.split("/")
        while("" in self.route):
                self.route.remove("")
        self.routeRepr = route
        self.__methods = []
        self.params = {}
        for i in range(len(self.route)):
            if self.route[i].startswith("{") and self.route[i].endswith("}"):
                self.params[i] = str(self.route[i].replace("{", "").replace("}", ""))
                self.route[i] = "*"
        
    def methods(self) -> list[Method]:
        return self.__methods
    
    def add_method(self, *methods: Method) -> Self:
        for method in methods:
            self.__methods.append(method)
        return self
        
    def get_handler(self, route: list[str]) -> tuple[Handler, dict[str, str]]:
        if len(route) != len(self.route):
            raise Exception("input route was not the same size as stored route") 
        
        foundParams: dict[str, str] = {}
        
        for i in range(len(self.route)):
            if self.route[i] != "*":
                if self.route[i] != route[i]:
                    raise Exception("inputted route does not match stored route") 
            else:
                foundParams[self.params[i]] = route[i]
                
        return self.handler, foundParams
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return self.routeRepr