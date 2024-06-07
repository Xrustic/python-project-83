from urllib.parse import urlparse
import validators


def validate(url):
    url_validator = validators.url(url)
    error = ''
    if not url:
        return 'URL обязателен для заполнения'
    if not url_validator:
        error = 'URL не правильный'
        return error
    if len(url) > 255:
        error = 'URL слишком длинный'
        return error


def normalize_url(url):
    parsed_url = urlparse(url)
    print(parsed_url)
    normalized_scheme = parsed_url.scheme.lower()
    print(normalized_scheme)
    normalized_host = parsed_url.hostname.lower()
    print(normalized_host)
    return f'{normalized_scheme}://{normalized_host}'
