import requests


def check_url(url):
    result = {'result': False}
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print('text =', r.text)
            h1 = 'h1'
            title = 'title'
            description = 'descr'
            result.update({'result': True,
                           'status_code': r.status_code,
                           'h1': h1,
                           'title': title,
                           'description': description,
                           })
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.InvalidSchema):
        print('Request error', url)

    return result
