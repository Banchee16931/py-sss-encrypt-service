from abc import abstractmethod

class ServiceConnector:
    """ Acts as an interface for how auth conntectors to external services should be implemented. """
    @abstractmethod
    def update_account_password(self, account_id: str, old_password: str, new_password: str):
        """ Makes it so that if the old password is correct the new password replaces it for this service. """
        pass
    
    @abstractmethod
    def get_session_token(self, account_id: str, password: str) -> str:
        """ Gets a session token from the service that has an expiry date. """
        pass