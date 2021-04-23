import requests
from requests import HTTPError
from urllib.parse import urlparse
import json
import pysnowball.token as token


def fetch(url):
    HEADERS = {'Host': urlparse(url).netloc,
               'Accept': 'application/json',
               'Cookie': token.get_token(),
               'User-Agent': 'Xueqiu iPhone 11.8',
               'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
               'Accept-Encoding': 'br, gzip, deflate',
               'Connection': 'keep-alive'}

    response = requests.get(url, headers=HEADERS)

    # print(url)
    # print(HEADERS)
    # print(response.status_code)
    # print(response.content)

    if response.status_code == 400:
        res = json.loads(response.content)
        raise HTTPError(f"{res['error_code']}: {res['error_description']}")
    elif response.status_code != 200:
        raise HTTPError(response.content)

    res = json.loads(response.content)

    if res['error_code'] != 0:
        raise RuntimeError(f"Get stock population error {res['error_code']}: {res['error_description']}")

    return res['data']


def fetch_without_token(url):
    HEADERS = {'Host': urlparse(url).netloc,
               'Accept': 'application/json',
               'User-Agent': 'Xueqiu iPhone 11.8',
               'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
               'Accept-Encoding': 'br, gzip, deflate',
               'Connection': 'keep-alive'}

    response = requests.get(url, headers=HEADERS)

    # print(url)
    # print(HEADERS)
    # print(response.status_code)
    # print(response.content)
    if response.status_code == 400:
        res = json.loads(response.content)
        raise HTTPError(f"{res['error_code']}: {res['error_description']}")
    elif response.status_code != 200:
        raise HTTPError(response.content)

    res = json.loads(response.content)

    if res['error_code'] != 0:
        raise HTTPError(f"{res['error_code']}: {res['error_description']}")

    return res['data']