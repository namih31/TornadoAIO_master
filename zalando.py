import colorama
import requests
from bs4 import BeautifulSoup as bs
import random
from colorama import Fore
import time
from datetime import datetime
from Webhook import wbhk_cook_zalando,wbhk_zalando_cook_personal
import csv
import multiprocessing as mp
import json
import sys,os
import subprocess


def proxies_setup():
    global proxies
    proxies_txt = open('.\\config\\proxies.txt','r').readlines()
    proxies = []
    for line in proxies_txt:
        prx = line.split(":")

        if prx[3][-1:] == "\n":

            proxies.append({ "https": f"http://{prx[2]}:{prx[3][:-1]}@{prx[0]}:{prx[1]}",
                      "http": f"http://{prx[2]}:{prx[3][:-1]}@{prx[0]}:{prx[1]}"
                      })
        else:
            proxies.append({"https": f"http://{prx[2]}:{prx[3]}@{prx[0]}:{prx[1]}",
                     "http": f"http://{prx[2]}:{prx[3]}@{prx[0]}:{prx[1]}"
                     })



def now(tid):
    return (datetime.now().strftime("%H:%M:%S.%f")[:-3] + " [ZALANDO %4.0i] " % tid)

def login(email,pwd,bm_sz,_abck,tid,proxy):
    global s
    global frsx
    global zac
    global zsa
    global zsi
    global clientid
    global bm_sv
    global bm_sz1
    global ak_bmsc1

    s = requests.session()
    s.proxies = proxy

    headers = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    s.headers.update(headers)
    print(Fore.RESET + now(tid) + Fore.YELLOW + " Handling Cookies")
    response = s.get('https://www.zalando.it')
    time.sleep(random.uniform(0.5, 1))
    response = s.get("https://www.zalando.it/myaccount", allow_redirects=True)
    req_url = response.url
    time.sleep(random.uniform(0.5, 1))
    if response.status_code == 200:
        print(Fore.RESET + now(tid) + " Logging-in...")
    elif response.status_code != 200:
        print(Fore.RESET + now(tid) + Fore.RED + " Server Error")

    reqheaders = {
        'authority': 'accounts.zalando.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'it-IT,it;q=0.9',
    }
    response = s.get(req_url, headers=reqheaders)
    validator_url = 'https://accounts.zalando.com' + \
                    bs(response.text, 'lxml').find_all("script", {'type': 'text/javascript'})[1]['src']
    csrf = (response.headers['set-cookie'][11:47])
    xid = str(bs(response.text, 'lxml').find("div", {'id': 'sso'})).split("x-flow-id%22%3A%22")[1].split('%22%2C%22')[
        0].replace('%2B', '+')

    response = s.get('https://accounts.zalando.com/api/login/schema')

    time.sleep(random.uniform(0.5, 1))
    cookies = {
        'bm_sz': bm_sz,
        '_abck': _abck,
        'ak_bmsc': s.cookies.get("ak_bmsc", domain=".zalando.com"),
        'csrf-token': csrf,
        'bm_sv': s.cookies.get("bm_sv", domain=".zalando.com"),
    }
    if proxy == None:
        tlsproxy = ""
    else:
        tlsproxy = proxy["https"][7:]



    tls_headers = {
        'poptls-url': 'https://accounts.zalando.com/api/login',
        'authority': 'accounts.zalando.com',
        'accept': 'application/json',
        'accept-language': 'it-IT,it;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://accounts.zalando.com',
        'referer': req_url,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'x-csrf-token': csrf,
        'x-flow-id': xid,
    }

    json_data = {
        'email': email,
        'secret': pwd,
        'request': req_url[50:][:-68],
    }

    response = requests.post("http://127.0.0.1:8082/", headers=tls_headers,cookies=cookies, json=json_data)
    s.cookies.set("zsso-p",response.cookies.get("zsso-p",domain="127.0.0.1"),domain="accounts.zalando.com")

    if response.status_code == 201:
        print(Fore.RESET + now(tid) + Fore.LIGHTGREEN_EX + " Login Completed")
        response = s.get("https://zalando.it/myaccount")
        frsx = s.cookies['frsx']
        zac = s.cookies['zac']
        zsa = s.cookies['zsa']
        clientid = s.cookies['Zalando-Client-Id']
        zsi = s.cookies['zsi']


    elif response.status_code == 403:
        print(Fore.RESET + now(tid) + Fore.RED + " Akamai block, cookies not valid")
    return

def clearcart(pid):
    deleteheaders = {
    'authority': 'www.zalando.it',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'accept': 'application/json',
    'x-xsrf-token': s.cookies.get("frsx",domain=".zalando.it"),
    'sec-ch-ua-mobile': '?0',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://www.zalando.it',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.zalando.it/cart/',
    'accept-language': 'it-IT,it;q=0.9',
    'cookie':'frsx=%s; ' % s.cookies.get("frsx",domain=".zalando.it") + 'Zalando-Client-Id=%s; ' % s.cookies.get("Zalando-Client-Id",domain=".zalando.it") + 'zsa=%s; ' % s.cookies.get("zsa",domain=".zalando.it") + 'zsi=%s; ' % s.cookies.get("zsi",domain=".zalando.it") ,
}

    carturl = 'https://www.zalando.it/api/cart-gateway/carts/%s' % cartid +'/items/%s' % (pid)
    response = s.delete(carturl, headers=deleteheaders)
    return

def clearallcart():
    deleteallheaders = {
    'authority': 'www.zalando.it',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'accept': 'application/json',
    'x-xsrf-token': s.cookies.get("frsx",domain=".zalando.it"),
    'sec-ch-ua-mobile': '?0',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://www.zalando.it',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.zalando.it/cart/',
    'accept-language': 'it-IT,it;q=0.9',
    'cookie':'frsx=%s; ' % s.cookies.get("frsx",domain=".zalando.it") + 'Zalando-Client-Id=%s; ' % s.cookies.get("Zalando-Client-Id",domain=".zalando.it") + 'zsa=%s; ' % s.cookies.get("zsa",domain=".zalando.it") + 'zsi=%s; ' % s.cookies.get("zsi",domain=".zalando.it") ,
}

    carturl = 'https://www.zalando.it/api/cart-gateway/carts/%s' % cartid +'/items'
    response = s.delete(carturl, headers=deleteallheaders)
    return

def preload(preloadurl,preloadpid,tid,bm_sz,_abck):
    global cartid
    global etag
    global checkoutid
    global defurl
    global preloadcheckurl
    global nextstepheaders

    print(Fore.RESET + now(tid) + Fore.BLUE + " Initializing preload")

    cartheaders = {
        'authority': 'www.zalando.it',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'x-xsrf-token': s.cookies.get("frsx",domain=".zalando.it"),
        'x-zalando-feature': 'pdp',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'x-zalando-intent-context': 'navigationTargetGroup=MEN',
        'content-type': 'application/json',
        'x-zalando-request-uri': preloadurl[22:],
        'dpr': '0.9375',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'origin': 'https://www.zalando.it',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': preloadurl,
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'zac=%s' % s.cookies.get("zac",domain=".zalando.it"),
    }
    json_data = [
            {
                'id': 'e7f9dfd05f6b992d05ec8d79803ce6a6bcfb0a10972d4d9731c6b94f6ec75033',
                'variables': {
                    'addToCartInput': {
                        'productId': preloadpid,
                        'clientMutationId': 'addToCartMutation',
                    },
                },
            },
        ]
    add_to_cart_url = "https://www.zalando.it/api/graphql/add-to-cart/"
    time.sleep(random.uniform(0.5,1))
    response = s.post(add_to_cart_url, headers=cartheaders , json=json_data)
    if response.status_code != 200 :
        print(Fore.RESET + now(tid) + Fore.RED + " PRELOAD ERROR: error while adding to cart")

    addheaders = {
        'authority': 'www.zalando.it',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.zalando.it/cart',
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'zac=%s' % zac,
    }

    response = s.get("https://www.zalando.it/checkout/address",headers=addheaders)
    time.sleep(random.uniform(0.5,1))
    while 'defaultShippingAddress' not in response.text:
        time.sleep(random.uniform(1,2))
        response = s.get("https://www.zalando.it/checkout/address",headers=addheaders)


    soup = bs(response.text,'lxml')
    temp = str(soup.find_all("div",{'data-mobile-mode-options':'{"headerMode":"desktop","footerMode":"desktop","applicationType":"web","headers":{"x-zalando-header-mode":"desktop","x-zalando-footer-mode":"desktop","x-zalando-checkout-app":"web"},"isAppIos14":false}'}))
    index = temp.index('defaultShippingAddress')
    defaddress = temp[(index + 51):(index + 59)]
    defurl = 'https://www.zalando.it/api/checkout/address/%s/default' % defaddress
    if response.status_code != 200 :
        print(Fore.RESET + now(tid) + Fore.RED + " PRELOAD ERROR: error while selecting default address")

    addressheaders = {
        'authority': 'www.zalando.it',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'x-xsrf-token': frsx,
        'sec-ch-ua-mobile': '?0',
        'x-zalando-header-mode': 'desktop',
        'x-zalando-checkout-app': 'web',
        'content-type': 'application/json',
        'x-zalando-footer-mode': 'desktop',
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.zalando.it',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zalando.it/checkout/address',
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'Zalando-Client-Id=%s; ' % clientid +'zsa=%s; ' % zsa +'frsx=%s' % frsx,
    }

    response = s.post(defurl, headers=addressheaders ,json={"isDefaultShipping":'true'})
    time.sleep(random.uniform(0.5,1))

    print(Fore.RESET + now(tid) + Fore.BLUE + " Generating session id")

    nextstepheaders = {
    'authority': 'www.zalando.it',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.zalando.it/api/checkout/next-step',
    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'Zalando-Client-Id=%s; ' % s.cookies.get("Zalando-Client-Id",domain=".zalando.it") +'zsa=%s; ' % s.cookies.get("zsa",domain=".zalando.it") +'frsx=%s; ' % s.cookies.get("frsx",domain=".zalando.it") + 'zac=%s' % s.cookies.get("zac",domain=".zalando.it"),
    }

    response = s.get('https://www.zalando.it/api/checkout/next-step', headers=nextstepheaders)
    check = json.loads(str(response.text))
    preloadcheckurl = (check['url'])

    time.sleep(random.uniform(0.5,1))

    cartidheaders = {
        'authority': 'www.zalando.it',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.zalando.it/myaccount/',
        'accept-language': 'it-IT,it;q=0.9',
        'cookie': 'Zalando-Client-Id=%s; ' % s.cookies.get("Zalando-Client-Id",domain=".zalando.it") + 'zsi=%s; ' % s.cookies.get("zsi",domain=".zalando.it") + 'zsa=%s' % s.cookies.get("zsa",domain=".zalando.it"),
    }

    response = s.get('https://www.zalando.it/cart/', headers=cartidheaders)
    time.sleep(random.uniform(0.5, 1))
    soup = bs(response.text, 'lxml')
    temp = str(soup.find_all("div", {"id": "app"}))
    index = temp.index('data-data')
    cartid = temp[(index + 44):(index + 108)]
    session_cookies = {
        "bm_sz": bm_sz,
        "_abck": _abck,
        "ak_bmsc": s.cookies.get("ak_bmsc",domain=".zalando.com"),
        "bm_sv": s.cookies.get("bm_sv",domain=".zalando.com")
    }
    sessionheaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'it-IT,it;q=0.9',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    response = s.get(preloadcheckurl, headers=sessionheaders, cookies=session_cookies, allow_redirects=True)


    clearallcart()
    print(Fore.RESET + now(tid) + Fore.BLUE + " Preload compleated")
    return

def atc(produrl,productpids,tid,target):


    if len(target) != 0 and datetime.strptime(target, '%Y-%m-%d %H:%M:%S')>datetime.now():
        print(Fore.RESET + now(tid) + Fore.YELLOW + " Waiting for droptime")
        ytime = datetime.now()
        xtime = datetime.strptime(target, '%Y-%m-%d %H:%M:%S')
        time.sleep(((max(xtime, ytime) - min(xtime, ytime)).seconds) - 4)

    cartheaders = {
        'authority': 'www.zalando.it',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'x-xsrf-token': s.cookies.get("frsx",domain=".zalando.it"),
        'x-zalando-feature': 'pdp',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'x-zalando-intent-context': 'navigationTargetGroup=MEN',
        'content-type': 'application/json',
        'x-zalando-request-uri': produrl[22:],
        'dpr': '0.9375',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'origin': 'https://www.zalando.it',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': produrl,
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'zac=%s' % s.cookies.get("zac",domain=".zalando.it"),
    }
    json_data = []
    for pid in productpids:
        json_data.append({
            'id': 'e7f9dfd05f6b992d05ec8d79803ce6a6bcfb0a10972d4d9731c6b94f6ec75033',
            'variables': {
                'addToCartInput': {
                    'productId': pid,
                    'clientMutationId': 'addToCartMutation',
                },
            },
        }, )

    add_to_cart_url = "https://www.zalando.it/api/graphql/add-to-cart/"
    response = s.post(add_to_cart_url, headers=cartheaders , json=json_data)
    if 'errors' in response.text:
        print(Fore.RESET + now(tid) + Fore.RED + " Item not live, retrying")
        while 'errors' in response.text:
            time.sleep(random.uniform(0.300,0.320))
            response = s.post(add_to_cart_url, headers=cartheaders, json=json_data)
            print(Fore.RESET + now(tid) + Fore.RED + " Item not live, retrying")
    else:
        print(Fore.RESET + now(tid) + Fore.LIGHTGREEN_EX + " Added to cart")

def checkout(tid,_abck,_abck1,webhook_personal):
    global asw

    confirmheaders = {
        'authority': 'www.zalando.it',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.zalando.it/',
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'frsx=%s; ' % frsx + 'Zalando-Client-Id=%s; ' % clientid + 'mpulseinject=false; ' + 'bm_sz=%s; ' % s.cookies.get("bm_sz",domain=".zalando.it") + 'ak_bmsc=%s; ' % (
                      s.cookies.get('ak_bmsc', domain='.zalando.it')) + 'zac=%s; ' % zac + '_abck=%s' % _abck1
    }
    response = s.get("https://www.zalando.it/checkout/confirm", headers=confirmheaders)
    while 'eTag' not in response.text:
        time.sleep(random.uniform(0.2, 0.6))
        response = s.get("https://www.zalando.it/checkout/confirm", headers=confirmheaders)

    soup = bs(response.text, 'lxml')
    temp = str(soup.find("div", {'data-feature-toggles': '{"header-variant":false,"split-shipment-layout-enabled":false,"default-delivery-destination-pup":false,"eligible-membership-trial-enabled":false,"hide-express-phone-number-form":false,"hide-free-delivery-partner-text":true,"enable_co2_offsetting":true,"show-pup-specific-message":true,"campaign-flag":false,"test-config":true,"show-express-pup-fee":false,"show-pup-selection-new-layout":false,"show-delivery-option-type-prefix":false}'})['data-props'])
    props = (json.loads(temp))['model']
    checkoutid = props['checkoutId']
    etag = props['eTag'].replace('"', '')
    etag = "\"%s\"" % etag


    checkoutheaders = {
        'authority': 'www.zalando.it',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'x-xsrf-token': s.cookies.get("frsx",domain=".zalando.it"),
        'sec-ch-ua-mobile': '?0',
        'x-zalando-header-mode': 'desktop',
        'x-zalando-checkout-app': 'web',
        'content-type': 'application/json',
        'x-zalando-footer-mode': 'desktop',
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.zalando.it',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zalando.it/checkout/confirm',
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'frsx=%s; ' % s.cookies.get("frsx",domain=".zalando.it") + 'Zalando-Client-Id=%s; ' % s.cookies.get("Zalando-Client-Id",domain=".zalando.it") + 'bm_sz=%s; ' % s.cookies.get("bm_sz",domain=".zalando.it") + 'ak_bmsc=%s; ' % (s.cookies.get('ak_bmsc', domain='.zalando.it')) + 'zsa=%s; ' % s.cookies.get("zsa",domain=".zalando.it") + '_abck=%s' % _abck1,

    }

    json_data = {
        'checkoutId': checkoutid,
        'eTag': etag,
    }
    response = s.post('https://www.zalando.it/api/checkout/buy-now', headers=checkoutheaders, json=json_data)


    if 'paypal' in response.text:
        paypalurl = str(response.text)[8:]
        paypalurl = paypalurl[:-2]
        print(Fore.RESET + now(tid) + Fore.LIGHTGREEN_EX + " Successfull checkout")
        brand = props['groups'][0]['articles'][0]['brandName']
        model = props['groups'][0]['articles'][0]['name']
        size = props['groups'][0]['articles'][0]['size']
        photo = props['groups'][0]['articles'][0]['imageUrl']
        wbhk_cook_zalando(brand,model,size,photo,paypalurl,tid)
        asw = 1
        if webhook_personal != "":
            wbhk_zalando_cook_personal(brand,model,size,photo,paypalurl,tid,webhook_personal)


    else:
        print(Fore.RESET + now(tid) + Fore.LIGHTRED_EX + " OOS at checkout, checking for restocks")
        asw = 0

def dropmain(email, pwd, produrl, productpids, preloadurl, preloadpid, bm_sz, _abck, _abck1, tid,target,restockmodeactive,proxy,webhook_personal):
    login(email, pwd, bm_sz, _abck, tid, proxy)
    preload(preloadurl,preloadpid,tid,bm_sz,_abck)
    atc(produrl, productpids,tid,target)
    checkout(tid,_abck,_abck1,webhook_personal)
    if asw == 0 and restockmodeactive == 'Y':
        print(Fore.RESET + now(tid) + Fore.YELLOW + " Waiting for restock")
        restock(tid,_abck, _abck1,webhook_personal)
    return

def restock(tid,_abck, _abck1,webhook_personal):
    response = s.get('https://www.zalando.it/api/checkout/next-step', headers=nextstepheaders)
    while 'cart' in response.text:
        time.sleep(random.uniform(0.5,0.9))
        response = s.get('https://www.zalando.it/api/checkout/next-step', headers=nextstepheaders)

    if 'confirm' in response.text:
        checkout(tid,_abck, _abck1,webhook_personal)

    return

def dropstart():
    subprocess.Popen(".\\Req\\tornadoaio_tls_client.exe")
    proxies_setup()
    f = open('.\\config\\settings.json', 'r')
    settings = json.load(f)
    webhook_personal = settings["webhook"]
    file = open(".\\config\\zalando_drop_tasks.csv", 'r')
    csvreader = csv.reader(file)
    next(csvreader)
    data = []
    for line in csvreader:
        data.append(line)
    processes = []

    bm_sz_ = ["2E8253B20692949D1D3C9DAA746734DD~YAAQChTfrXdKY1CAAQAAV6u3Ug80PirnQv2ckanYXCWJaBHCVinbjr1LZTUYgxF5EMEUDFaqrG06FflJSaYSnA9Sru7iHHlPOoLZzsZEWMDsYgO0LvFtSKQGF8cEcuIwkjNkjOwzfbLfN9XUp5FmlljPNmunNxht1nLZXhwlFrP8MpXIOwTXvoNE9eJJXM+n61bR0w/JOgKmfmPd7c87IxTYCWvwWCWAcHD4K/yFl53g2gsNBJAxdHuSVd2B8OylGbiq8mtVY3qmRSBQPMXF2KDNf8OgA7B3R6m/1QuasdKvdHn/QpIIAKV3o1V2Qy9nMA/+oco/IqizeJXvNsHuiWKTR5CEokh0GiTgzT82t3ZYWwax/KnFu8+KXN5r7AAvywTxRHnO7mjAbeiMco064JQ=~4338480~4600385"]
    _abck_ = ["1FC5850D320B979D229E021E3140249C~0~YAAQChTfrdNLY1CAAQAAY8a3UgdpT+sv7PA7UvJD+N4Um9z4X5lmICGkheF4Qhtnc6WmaXUCJjiosa6CcPArjKDbhxknInDv+rBaVqgYnNmRbs7iQCzj+TFCmnfEZxizdDG0BX4evLtEl3zQxAaRqFTilDYCwA3DXlmRKSctdIaMnM42ndV/rAN+evlubdkJshvWYReUMAFzfRXgntUMDILhyWBowdifvhCmvWXo/ZHkIwz8TBzmjuWqQRxnP08G7awBQme9DtmsyR7dh1ANSFxLJ9SBw6a9RRKPDdd1U/jcuZALDjLgdkO0uJXFzjOBzQg8R09ml33cgZHokcuDfhBsU//LvBHQbK817+Znv+wvD1dQ0w2A5NQsmnNZugvTDtGxhwdSrLBX3S3OwbkrBdJBx3g0VWPphOUabzbZmRMDoZFJOxnjFaQY2ldR4Edz2+D3nqIcbYxkqsdlESnxcPor4Hk0VhcNbTwsNjMtpgSs~-1~-1~1650658753"]
    _abck1_ = ["57A52DB5DFB3B0F93046AFBB86B4B5C3~-1~YAAQChTfrYjNZFCAAQAAbSjPUgeBkWEAiSbNAvnCs+4vR//LdUQyJelhXc6TRdW0nVR50tmAh3A/ItO1LASiXKtjT7vFWAAwp5CTohelTlxX1PQ8ZNeVK8h3nY57Q8VfjdFYmeiexiGHxUR89VLdvVSOhuLUNHJTPgdTtzV5/C8coGU5TKQN6mboyTdReJCcCX+ADAZyAiBjPOQKMY4cXVtQcwQWjAPupmvXosTEwWgkoCWvsVsYw5Mw8BNGTvqjsIfoQxnXzcyJPu0DkfyH2ou8XTyvDXtfQ8zXUJ2KetUi+NrYFY0dHBX/beTnHx4au8yfTy76+MwVu4Qg3LOglVrj2XSWl0n7RexMQT1heJXz4q+1fUSbrEVurAJ5v+djOeMXansFHgXddDLqB9ctq5No7AOb7Mmo8QVG0ZkcZkRFgqVPAnG5sKD2KhSAZ/bUtJb0nszrtWUCHnW1m4c8Bju51Cy4udC1D3kJBrKLJiwtcMpN6NbfNTofcgfqZeUBHWfAYTc72kmlcGI=~-1~-1~-1"]

    for _ in range(len(data)):
        email = data[_][0]
        pwd = data[_][1]
        produrl = data[_][2]
        productpids = data[_][3].split(',')
        preloadurl = data[_][4]
        preloadpid = data[_][5]
        restockmodeactive = data[_][7]

        bm_sz = bm_sz_[_]
        _abck = _abck_[_]
        _abck1 = _abck1_[_]
        tid = (_ + 1)
        target = data[_][6]
        if _ in range(len(proxies)):
            proxy = proxies[_]
        else:
            proxy = None

        p = mp.Process(target=dropmain,
                       args=(email, pwd, produrl, productpids, preloadurl, preloadpid, bm_sz, _abck, _abck1, tid,target,restockmodeactive,proxy,webhook_personal))
        processes.append(p)

    for p in processes:
        p.start()


if __name__ == '__main__':
    dropstart()
