from bs4 import BeautifulSoup
import requests


def check_url(url):
    result = {'result': False}
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            h1 = soup.h1.string if soup.h1 else None
            title = soup.title.string if soup.title else None
            description = soup.find(
                "meta", {"name": "description"}).get("content")
            result = {
                'result': True,
                'status_code': response.status_code,
                'h1': h1,
                'title': title,
                'description': description,
            }
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.InvalidSchema):
        pass
    return result
