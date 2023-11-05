import secrets
import string

__PASSWORD_LEN = 128

def generate_password() -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(__PASSWORD_LEN))