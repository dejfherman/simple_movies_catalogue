import hashlib
from unicodedata import normalize
from re import sub


def normalize_name(text: str) -> str:
    """
    Strip accents, lowercase, remove surrounding space and collapse repeated whitespace from the input string.
    """
    text = sub(r'[\u0300-\u036f]', '', normalize('NFKD', text))
    text = text.lower()
    text = text.strip()
    text = sub(r'\s+', ' ', text)
    return text


def hash_url(url: str) -> str:
    """
    Helper hashing method. Doesn't actually validate url format, we're using it with relative urls.
    """
    return hashlib.md5(url.encode('utf-8')).hexdigest()


def limit_search_query(query: str) -> str:
    """
    Limit the input string to a reasonable length. Doubles FE limitation in case of validation bypass.
    """
    return query.strip()[:100]
