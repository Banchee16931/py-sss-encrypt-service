from abc import abstractmethod

class ServiceConnector:
    @abstractmethod
    def update_account_password(self, account_id: str, password: str):
        pass
    
    @abstractmethod
    def get_session_token(self, account_id: str, password: str) -> str:
        pass