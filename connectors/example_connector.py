from typing import override
from connectors import ServiceConnector
from db.client import Client
from db.database import Database
from db.decorators import with_dtclient
from utils.http import HTTPException, Status

class _ExampleConnector(ServiceConnector):
    def __init__(self, service_name: str):
        self.service_name = service_name
    
    @override
    @with_dtclient(Database())
    def update_account_password(client: Client, self, account_id: str, old_password: str, new_password: str) -> str:     
        stored_old_password = client.get_example_service_password(self.service_name, account_id)
        if stored_old_password != old_password:
            raise HTTPException(Status.Unauthorized, f"invalid password for service {self.service_name} and account {account_id}")
        
        client.update_example_service_password(self.service_name, account_id, new_password)
    
    @override
    @with_dtclient(Database())
    def get_session_token(client: Client, self, account_id: str, password: str) -> str:        
        try:
            stored_password = client.get_example_service_password(self.service_name, account_id)
            if stored_password != password:
                raise HTTPException(Status.Unauthorized, f"invalid password for service {self.service_name} and account {account_id}")
        except:
            # If there isn't a password yet, for the examples sake, we just create it
            client.update_example_service_password(self.service_name, account_id, password)
        
        return f"demo-token-{self.service_name.replace(" ", "_")}-{account_id.replace(" ", "_")}"