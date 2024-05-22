from urllib.parse import urlparse, urlunparse
import validators


def validate(url):
    error = ''
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    result_url = urlunparse([scheme, netloc, '', '', '', ''])
    if not validators.url(result_url):
        error = 'URL не правильный'
        return error, url

    if len(result_url) > 255:
        error = 'URL слишком длинный'
    return error, result_url
