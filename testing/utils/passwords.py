import random
import string
from typing import Dict, Tuple


def create_random_password():
    possible_chars = string.ascii_letters+string.digits
    return "".join(random.choices([*possible_chars], k=random.randrange(1, 30)))

def create_user_passwords() -> Tuple[int, Dict[str, str]]:
    user_passwords = {}
    for x in range(random.randrange(2, 50)):
        user_passwords[create_user_id()] = create_random_password()
    
    return random.randrange(1,len(user_passwords)), user_passwords
    
def create_user_id():
    possible_chars = string.ascii_letters+string.digits
    return "".join(random.choices([*possible_chars], k=random.randrange(1, 10)))