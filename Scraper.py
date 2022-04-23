import json
from bs4 import BeautifulSoup as bs
import requests
from Webhook import wbhk_zalando

def sizes_in_stock(produrl):
    global s
    s = requests.session()
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
    response = s.get(produrl)
    soup = bs(response.text,"lxml")
    temp = soup.body.find("script",{"class":"re-1-12","data-re-asset":"","type":"application/json"}).text.strip()
    all_sizes = (json.loads(temp)["graphqlCache"]["{\"id\":\"a587302d2dadcb918cd0e7b1561792ca3b3b1c83e98a65e0a749906ce134b73b\",\"variables\":{\"id\":\"ern:product:uri:"f"{produrl[23:-5]}""\",\"enableGiftWrappingOption\":false}}"]["data"]["product"]["simplesWithStock"])
    instock = []
    for data in all_sizes:
        instock.append(data['sku'])
    return instock

def get_allskus(produrl):
    global s
    s = requests.session()
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
#    global produrl
    response = s.get(produrl)
    soup = bs(response.text,"lxml")
    temp = soup.body.find("script",{"class":"re-1-12","data-re-asset":"","type":"application/json"}).text.strip()
    total_stock = (json.loads(temp)["graphqlCache"]["{\"id\":\"3cbcb551386476489f3ea05d361fc0c6a15c13fb7678d667fc79952db14f23fa\",\"variables\":{\"id\":\"ern:product:uri:"f"{produrl[23:-5]}""\"}}"]["data"]["product"]["simples"])
    size = []
    sku = []
    for data in total_stock:
        size.append(data['size'])
        sku.append(data['sku'])

    stock = {'size':size,'sku':sku}
    return stock['sku']

def zalando_scraper(produrl):
    global name
    global description
    s = requests.session()
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
    response = s.get(produrl)
    soup = bs(response.text,"lxml")
    prov = soup.find("meta",{"name":"description"})
    temp = soup.body.find("script",{"class":"re-1-12","data-re-asset":"","type":"application/json"}).text.strip()
    scrapedatasku = (json.loads(temp)["graphqlCache"]["{\"id\":\"3cbcb551386476489f3ea05d361fc0c6a15c13fb7678d667fc79952db14f23fa\",\"variables\":{\"id\":\"ern:product:uri:"f"{produrl[23:-5]}""\"}}"]["data"]["product"]["simples"])
    prov = prov['content']
    infos = prov.split(' - ')
    name = (infos[0][1:])
    img = (json.loads(temp)["graphqlCache"]["{\"id\":\"3cbcb551386476489f3ea05d361fc0c6a15c13fb7678d667fc79952db14f23fa\",\"variables\":{\"id\":\"ern:product:uri:"f"{produrl[23:-5]}""\"}}"]["data"]["product"]['media'][0]['uri'])
    skus = "```"
    size = "```"
    stock = "```"
    for scrape in scrapedatasku:
        skus = skus + ('%s\n' % ( scrape['sku']))
        size = size + ('%s\n' % scrape['size'])
        stock = stock + ('%s\n' % scrape['offer']['stock']['quantity'])
    skus = skus + "```"
    size = size + "```"
    stock = stock + "```"
    allsizes = ''
    for sku in get_allskus(produrl):
        allsizes =  allsizes  + str(sku) + ','
    allsizes = "```" + allsizes[:-1] + "```"
    wbhk_zalando(name,produrl,skus,size,stock,img,allsizes)
    return

