import datetime

import requests


def get_json():

    headers = {
        'referer': 'https://www.csdn.net/nav/python',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    url = 'https://www.csdn.net/api/articles?type=more&category=python&shown_offset=0'
    response = requests.get(url, headers)
    content = response.json()
    articles = content['articles']
    all_data = []

    for article in articles:
        author = article['nickname']
        title = article['title']
        url = article['url']
        release_time = datetime.datetime.now()
        data = {'author': author, 'title': title, 'url': url, 'like': 0, 'release_time': release_time}
        all_data.append(data)

    return all_data


if __name__ == '__main__':
    get_json()
