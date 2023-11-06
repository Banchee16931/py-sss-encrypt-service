from typing import Self
from utils.http import Handler, Method

class _Route():
    
    path: str
    split_path: list[str]
    params: dict[int, str]
    handler: Handler
    __methods: list[Method]
    
    def __init__(self, route: str, handler: Handler):
        self.handler = handler
        self.split_path = route.split("/")
        while("" in self.split_path):
                self.split_path.remove("")
        self.path = route
        self.__methods = []
        self.params = {}
        for i in range(len(self.split_path)):
            if self.split_path[i].startswith("{") and self.split_path[i].endswith("}"):
                self.params[i] = str(self.split_path[i].replace("{", "").replace("}", ""))
                self.split_path[i] = "*"
        
    def get_handler(self, path: list[str]) -> tuple[Handler, dict[str, str]]:
        """ This takes in a given path and checks if it matches the one the Route has store. 
        
        If it does it returns self.handler. Otherwise, it raises and exception. """
        if len(path) != len(self.split_path):
            raise Exception("input route was not the same size as stored route") 
        
        foundParams: dict[str, str] = {}
        
        for i in range(len(self.split_path)):
            if self.split_path[i] != "*":
                if self.split_path[i] != path[i]:
                    raise Exception("inputted route does not match stored route") 
            else:
                foundParams[self.params[i]] = path[i]
                
        return self.handler, foundParams
    
    def methods(self) -> list[Method]:
        """ Returns the stored method list. """
        return self.__methods
    
    def add_method(self, *methods: Method) -> Self:
        """ Adds a method to the stored method list """
        for method in methods:
            self.__methods.append(method)
        return self
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return self.path