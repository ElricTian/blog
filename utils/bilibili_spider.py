import codecs
import requests
import re
import random


def spider():
    """
    :return: bv
    """
    url = 'https://www.bilibili.com'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36'
    }
    response = requests.get(url, headers)
    html = response.content.decode()

    pattern = 'href="//www.bilibili.com/video/(.*?)"'
    results = re.findall(pattern, html, re.S)
    result = random.sample(results, 1)[0]
    return result


def bv2av(bvid):
    # 爬虫接口实现bv2av
    site = "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid
    lst = codecs.decode(requests.get(site).content, "utf-8").split("\"")
    print(lst)
    return int(lst[16][1:-1])


def bvid_to_aid(bvid):
    # 算法实现bv2av
    # Snippet source: https://www.zhihu.com/question/381784377/answer/1099438784

    table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608
    r = 0

    try:
        for i in range(6):
            r += tr[bvid[s[i]]] * 58 ** i
        return (r - add) ^ xor
    except:
        return '927580668'


def get_aid():

    bvid = spider()
    aid = bvid_to_aid(bvid)
    return aid

