from bs4 import BeautifulSoup
import requests


def extract_page_data(url):
    result = False
    try:
        response = requests.get(url)
        print(response, '-----resp')
        if response.status_code == 200:
            print(response.status_code, '---resp, st code')
            soup = BeautifulSoup(response.text, "html.parser")
            h1_tag = soup.find('h1')
            title_tag = soup.find('title')
            meta_description_tag = soup.find(
                'meta', attrs={'name': 'description'})
            return {
                    'h1': h1_tag.text[:255] if h1_tag else '',
                    'title': title_tag.text[:255] if title_tag else '',
                    'status_code': response.status_code,
                    'description': (
                        meta_description_tag.get('content', '')[:255]
                        if meta_description_tag else '')
                }
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.InvalidSchema):
        pass
    return result
