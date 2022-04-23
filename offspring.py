import time
import requests
from bs4 import BeautifulSoup as bs
"""
size_chart = "EU"
s = requests.session()
productid = 'zuOoXH2BvT'
productheaders = {
    'authority': 'www.offspring.co.uk',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'it-IT,it;q=0.9',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
}

response = s.get(f'https://www.offspring.co.uk/view/product/offspring_catalog/1,22/{productid}', headers=productheaders)
start = time.time()
soup = bs(response.text,'lxml')

if size_chart == "UK":
    sizes_uk = soup.find("ul", {"class": "product__sizes-select js-size-select-list", "data-locale": "UK"}).find_all(
        "li", {"class": "product__sizes-option"})
    for _ in range(len(sizes_uk)):
        sizes_uk[_] = sizes_uk[_]['data-name']
        sizecontainer = sizes_uk

elif size_chart == "EU":
    sizes_eu = soup.find("ul", {"class": "product__sizes-select js-size-select-list", "data-locale": "EU"}).find_all(
        "li", {"class": "product__sizes-option"})
    for _ in range(len(sizes_eu)):
        sizes_eu[_] = sizes_eu[_]['data-name']
        sizecontainer = sizes_eu
elif size_chart == "US":
    sizes_us = soup.find("ul", {"class": "product__sizes-select js-size-select-list", "data-locale": "US"}).find_all(
        "li", {"class": "product__sizes-option"})
    for _ in range(len(sizes_us)):
        sizes_us[_] = sizes_us[_]['data-name']
        sizecontainer = sizes_us

"""




