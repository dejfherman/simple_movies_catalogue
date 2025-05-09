import random
import string

def mock_csfd_hash(length: int = 32):
    """
    Returns a random string resembling a calculated hash for a movie or an actor found on the CSFD site.
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def mock_csfd_hash_set(size: int):
    """
    Use when you want to be extra sure that your randomly generated hashes are unique.
    """
    hashes = set()
    while len(hashes) < size:
        hashes.add(mock_csfd_hash())
    return hashes