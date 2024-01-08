

import random
import string
from cryptography.sss import _ShamirSecretSharing
from testing.utils.passwords import create_random_password


def test_fuzz_main_path():
    """ Tests that the SSS algorithm can create and then reassemble passwords """
    for x in range(100):
        master_password = create_random_password()
        share_count = random.randrange(2, 50)
        threshold = random.randrange(1, share_count)
        main_path_core(threshold, list(range(share_count)), master_password)
    
def main_path_core(threshold, user_passwords, master_password):    
    """ This is used to do the actual testing part of test_fuzz_main_path() """
    print(threshold, len(user_passwords), master_password)
    shares = _ShamirSecretSharing.create(
        threshold, 
        len(user_passwords),
        master_password
    )
    
    assert _ShamirSecretSharing.combine(shares) == master_password
    