import bcrypt

def create(password: str):
    return bcrypt.hashpw(password.encode("latin-1"), bcrypt.gensalt()).decode("latin-1")
    
def same(password: str, hash: str):
    return bcrypt.checkpw(password.encode("latin-1"), hash.encode("latin-1"))