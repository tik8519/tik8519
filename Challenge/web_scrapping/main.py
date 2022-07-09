from typing import List
import requests
import re


def h3_parser(url: str) -> List:
    """Находит на указанном сайте все заголовки h3 в html разметке"""
    site_info = requests.get(url)
    tags_h3: List = re.findall(r'<h3.+</h3', site_info.text)
    result = list()
    for i_tags in tags_h3:
        tag: list = re.findall(r'>.+<', i_tags)
        result.append(tag[0][1:-1])
    return result


if __name__ == '__main__':
    print(h3_parser('http://www.columbia.edu/~fdc/sample.html'))
