from urllib.parse import urlparse
import validators


def validate(url):
    url_validator = validators.url(url)
    error = ''
    if not url:
        return 'URL обязателен для заполнения'
    if not url_validator:
        error = 'Некорректный URL'
        return error
    if len(url) > 255:
        error = 'URL слишком длинный'
        return error


def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_scheme = parsed_url.scheme.lower()
    normalized_host = parsed_url.hostname.lower()
    return f'{normalized_scheme}://{normalized_host}'
