from typing import Dict
from typing_extensions import override

from connectors.ServiceConnector import ServiceConnector
from connectors.example_connector import _ExampleConnector
from utils.http import HTTPException, Status

class Connectors:
    def __new__(self):
        # forces this class to be a singleton, as we only want one database connection
        if not hasattr(self, 'instance'):
            self.instance = super(Connectors, self).__new__(self)
        
        return self.instance
    
    def __init__(self):
        self.service_to_handler: Dict[str, ServiceConnector] = {
            "example": _ExampleConnector("example")
        }
    
    @override
    def update_account_password(self, service_name: str, account_id: str, old_password: str, new_password: str):
        if not service_name in self.service_to_handler.keys():
            raise HTTPException(Status.BadRequest, "service with that name does not exists")
        
        return self.service_to_handler[service_name].update_account_password(
            account_id, old_password, new_password)
    
    @override
    def get_session_token(self, service_name: str, account_id: str, password: str) -> str:
        if not service_name in self.service_to_handler.keys():
            raise HTTPException(Status.BadRequest)
        
        return self.service_to_handler[service_name].get_session_token(account_id, password)