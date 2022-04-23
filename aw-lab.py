import random

import requests
from bs4 import BeautifulSoup as bs
import json
import re
from magic_number import DatadomeMagicNumber
from twocaptcha import TwoCaptcha
import time
from datetime import datetime
from colorama import Fore
from harvester import Harvester
import logging
import threading



tid = 1

solver = TwoCaptcha('caf383053c3663ab305eac57699cb4b8')
s = requests.session()

"""
prx = '93.93.18.129:44444:14aff46be6374:66bdad3110'
proxy = {
    'https' : f'http://{prx}',
    'http' : f'http://{prx}'

}
s.proxies = proxy
"""

datadome_awlab = 'https://www.aw-lab.com/on/demandware.store/Sites-awlab-it-Site/it_IT/DDUser-Challenge'

def now(tid):
    return (datetime.now().strftime("%H:%M:%S.%f")[:-3] + " [AW-LAB %4.0i] " % tid)

def initialize():
    global datadome

    cartheaders = {
        'authority': 'www.aw-lab.com',
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
    response = s.get('https://www.aw-lab.com/carrello', headers=cartheaders)
    time.sleep(random.uniform(1, 2))

    if datadome_awlab in response.url:
        datadomesolver(response)

def addtocart():
    time.sleep(random.uniform(1, 2))

    cookies = {
        '__cq_uuid': s.cookies['cqcid'],
        'dwsid': s.cookies['dwsid'],
        'datadome': s.cookies['datadome'],
    }

    headers = {
        'authority': 'www.aw-lab.com',
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'it-IT,it;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.aw-lab.com',
        'referer': 'https://www.aw-lab.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',

    }

    params = {
        'format': 'ajax',
    }

    data = {
        'Quantity': '1',
        'sizeTable': '',
        'cartAction': 'add',
        'pid': 'AW_22121RGB_5010294_09',
        'productSetID': 'AW_22121RGB_5010294_09',
        'redirect': 'true',
    }
    response = s.post('https://www.aw-lab.com/on/demandware.store/Sites-awlab-it-Site/it_IT/Cart-AddProduct', headers=headers, params=params, cookies=cookies, data=data)
    if datadome_awlab in response.url:

        datadomesolver(response)
        time.sleep(random.uniform(1,2))
        response = s.post('https://www.aw-lab.com/on/demandware.store/Sites-awlab-it-Site/it_IT/Cart-AddProduct',
                          headers=headers, params=params, cookies=cookies, data=data)
    print(response.text)
    time.sleep(random.uniform(1, 2))
    if response.status_code == 200 and datadome_awlab not in response.url:
        print(Fore.RESET + now(tid) + Fore.GREEN + ' Added to cart')
    elif response.status_code == 429:
        print(Fore.RESET + now(tid) + Fore.LIGHTRED_EX + ' CLOUDFLARE block')
    else:
        print(Fore.RESET + now(tid) + Fore.RED + ' Failed adding to cart')

def start_captcha_server():
    global tokens
    logging.getLogger('harvester').setLevel(logging.CRITICAL)
    harvester = Harvester()
    tokens = harvester.intercept_recaptcha_v2(
        domain='geo.captcha-delivery.com',
        sitekey='6LcSzk8bAAAAAOTkPCjprgWDMPzo_kgGC3E5Vn-T'
    )

    server_thread = threading.Thread(target=harvester.serve, daemon=True)
    server_thread.start()
    harvester.launch_browser()

def datadomesolver(response):
    print(Fore.RESET + now(tid) + Fore.YELLOW + ' Solving Datadome')
    soup = bs(response.text,'lxml')
    dd = json.loads((soup.find("script").text)[7:].replace("'",'"'))
    initialCid = dd['cid']
    hsh = dd['hsh']
    t = dd['t']
    host = dd['host']
    cid = s.cookies['datadome']
    post_url = 'https://'+host.replace('&#x2d;','-')+'/captcha/?initialCid={}&hash={}&cid={}&t={}'.format(initialCid, hsh, cid,t)
    time.sleep(random.uniform(1,2))
    first_post = s.get(post_url)
    if 'sitekey' in first_post.text:
        sitekey = first_post.text.split("'sitekey' : '")[1].split("'")[0]
        challenge_link = first_post.url
        solver_response = solver.recaptcha(sitekey=sitekey,url=challenge_link)['code']
        useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
        magicnum = DatadomeMagicNumber(cid,10,useragent).Generate()
        time.sleep(random.uniform(1,2))
        response = s.get(f'https://geo.captcha-delivery.com/captcha/check?cid={cid}&icid={initialCid.replace("&#x2d;","-")}&ccid=&g-recaptcha-response={solver_response}&hash={hsh}&ua={useragent}&referer=https%3A%2F%2Fwww.aw-lab.com%2Fon%2Fdemandware.store%2FSites-awlab-it-Site%2Fit_IT%2FCart-Show&parent_url=https%3A%2F%2Fwww.aw-lab.com%2F&x-forwarded-for=&captchaChallenge={magicnum}&s=32468')
        s.cookies.set('datadome',str((json.loads(response.text))['cookie'].split('; ')[0][9:]) , domain='.aw-lab.com', path='/')
        if response.status_code == 200:
            print(Fore.RESET + now(tid) + Fore.LIGHTBLUE_EX + ' Datadome solved')
    else:
        print(Fore.RESET + now(tid) + Fore.LIGHTRED_EX + ' Proxy ban')



def checkout():
    cookies = {
        'dwsid': s.cookies['dwsid'],
        'datadome': s.cookies['datadome'],
    }

    headers = {
        'authority': 'www.aw-lab.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'it-IT,it;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://www.aw-lab.com/spedizione',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    }

    response = s.get('https://www.aw-lab.com/fatturazione', headers=headers, cookies=cookies)
    csrf = bs(response.text, 'lxml').find("input", {"class": "js-input js-input_field", "type": "hidden"})['value']

    cookies = {
        'dwsid': s.cookies['dwsid'],
        '__dfduuid': s.cookies['__dfduuid'],
        'datadome': s.cookies['datadome'],
    }

    headers = {
        'authority': 'www.aw-lab.com',
        'accept': '*/*',
        'accept-language': 'it-IT,it;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.aw-lab.com',
        'referer': 'https://www.aw-lab.com/fatturazione',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'dwfrm_billing_save': 'true',
        'dwfrm_billing_billingAddress_addressId': 'guest-shipping',
        'dwfrm_billing_billingAddress_addressFields_isValidated': 'true',
        'dwfrm_billing_billingAddress_addressFields_firstName': 'Francesco',
        'dwfrm_billing_billingAddress_addressFields_lastName': 'Sicari',
        'dwfrm_billing_billingAddress_addressFields_address1': 'Via Guerriero Guerra 19',
        'dwfrm_billing_billingAddress_addressFields_postal': '06127',
        'dwfrm_billing_billingAddress_addressFields_city': 'Perugia',
        'dwfrm_billing_billingAddress_addressFields_states_state': 'PG',
        'dwfrm_billing_billingAddress_addressFields_country': 'IT',
        'dwfrm_billing_billingAddress_invoice_accountType': 'private',
        'dwfrm_billing_billingAddress_invoice_companyName': '',
        'dwfrm_billing_billingAddress_invoice_taxNumber': '',
        'dwfrm_billing_billingAddress_invoice_vatNumber': '',
        'dwfrm_billing_billingAddress_invoice_sdlCode': '',
        'dwfrm_billing_billingAddress_invoice_pec': '',
        'dwfrm_billing_couponCode': '',
        'translationsAdyen': '{"sk_SK":{"creditCard.label":"PLATBA KARTOU","creditCard.holderName":"DR\u017DITEL KARTY","creditCard.holderName.placeholder":"J. Smith","creditCard.holderName.invalid":"Zadajte platn\xFA hodnotu","creditCard.numberField.title":"\u010C\xEDslo karty","creditCard.numberField.placeholder":"1234 5678 9012 3456","creditCard.numberField.invalid":"Zadajte platn\xFA hodnotu","creditCard.expiryDateField.title":"PLATNOS\u0164 DO","creditCard.expiryDateField.placeholder":"MM/RR","creditCard.expiryDateField.invalid":"Zadajte platn\xFA hodnotu","creditCard.expiryDateField.month":"Mese","creditCard.expiryDateField.month.placeholder":"MM","creditCard.expiryDateField.year.placeholder":"RR","creditCard.expiryDateField.year":"Anno","creditCard.cvcField.title":"CVC k\xF3d","creditCard.cvcField.placeholder":"123","creditCard.oneClickVerification.invalidInput.title":"Zadajte aspo\u0148 3 znaky.","creditCard.cvcField.placeholder.4digits":"4 cifre","creditCard.cvcField.placeholder.3digits":"3 cifre","cost.free":"Zdarma"},"it_IT":{"creditCard.label":"CARTA DI CREDITO","cost.free":"Gratuito"},"pl_PL":{"creditCard.label":"P\u0141ATNO\u015A\u0106 ONLINE KART\u0104 P\u0141ATNICZ\u0104","cost.free":"Bezp\u0142atnie"},"cs_CZ":{"creditCard.label":"PLATBA KARTOU","cost.free":"Zdarma"},"es_ES":{"creditCard.label":"PAY BY CARD","cost.free":"Gratis"},"en_GB":{"creditCard.label":"PAY BY CARD","cost.free":"Free"},"en_IT":{"creditCard.label":"Credit card","cost.free":"Free"}}',
        'dwfrm_adyPaydata_adyenStateData': '',
        'dwfrm_adyPaydata_paymentFromComponentStateData': '',
        'dwfrm_adyPaydata_merchantReference': '',
        'dwfrm_adyPaydata_orderToken': '',
        'dwfrm_billing_paymentMethods_creditCard_number': '',
        'dwfrm_billing_paymentMethods_creditCard_type': '',
        'adyenPaymentMethod': '',
        'adyenIssuerName': '',
        'dwfrm_adyPaydata_adyenFingerprint': 'DpqwU4zEdN0050000000000000KZbIQj6kzs0032254872cVB94iKzBG608Dq53IZDBix7RX3az8002vkTBbDITTR00000qZkTE00000J4SreNhVjkw1CEN4breT:40',
        'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'PayPal',
        'dwfrm_billing_billingAddress_personalData': 'true',
        'dwfrm_billing_billingAddress_tersmsOfSale': 'true',
        'csrf_token': 'oZixDkCXlsNIhzFussQso9JwQhXvGRdCTyp5H58xvGoczbnK0J18k93EbAUjpF1jc4Q7kvLteLuGC9E-kfdJ6JIHps6SNa48_nQ3GURzrkAmxeS90Bc1HmoAmsTIQkM3h3lYp7m20oouKJkz-o5RcnL8J5cELM2fi3yKpXUtxfWq0lySXXc=',
        'dwfrm_adyPaydata_adyenPaymentMethod': '',
    }

    response = s.post('https://www.aw-lab.com/on/demandware.store/Sites-awlab-it-Site/it_IT/COBilling-Billing', headers=headers, cookies=cookies, data=data)


initialize()
addtocart()



"""
cookies = {
    'dwsid': s.cookies['dwsid'],
    'datadome': s.cookies['datadome'],
}

headers = {
    'authority': 'www.aw-lab.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'it-IT,it;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://www.aw-lab.com/spedizione',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
}

response = s.get('https://www.aw-lab.com/fatturazione', headers=headers)
print(response.text)
csrf = bs(response.text, 'lxml').find("input", {"class": "js-input js-input_field", "type": "hidden"})['value']
print(s.cookies)
"""
