import sys
from Scraper import *
import validators
from zalando import *
import json
from colorama import Fore
import platform
import subprocess
import urllib.request
from colorama import init
import requests
import os

__version__ = "0.0.1"



def TornadoCLIintro():
    print("""\
    
     /$$$$$$$$                                            /$$            /$$$$$$  /$$       /$$$$$$
    |__  $$__/                                           | $$           /$$__  $$| $$      |_  $$_/
       | $$  /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$ | $$  \__/| $$        | $$  
       | $$ /$$__  $$ /$$__  $$| $$__  $$ |____  $$ /$$__  $$ /$$__  $$| $$      | $$        | $$  
       | $$| $$  \ $$| $$  \__/| $$  \ $$  /$$$$$$$| $$  | $$| $$  \ $$| $$      | $$        | $$  
       | $$| $$  | $$| $$      | $$  | $$ /$$__  $$| $$  | $$| $$  | $$| $$    $$| $$        | $$  
       | $$|  $$$$$$/| $$      | $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$/|  $$$$$$/| $$$$$$$$ /$$$$$$
       |__/ \______/ |__/      |__/  |__/ \_______/ \_______/ \______/  \______/ |________/|______/
                                                                                                  """)

def select_choice(selections):
    while True:
        user_choice = input("Enter a choice > ")
        for item in selections:
            for selection_tag in selections[item]:
                if user_choice.lower().strip() == selection_tag:
                    return item

def zalando():
    print(("\n    Zalando    \n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"))
    print("0: Main Menu\n1: Scraper\n2: Run Tasks\n")

    selections = {
        0: ["0", "Main Menu"],
        1: ["1", "Scraper"],
        2: ["2", "Run Tasks"],
    }
    selections = select_choice(selections)

    if selections == 0:
        mainmenu()
    elif selections == 1:
        zalando_scrape_menu()
    elif selections == 2:
        dropstart()

def zalando_scrape_menu():
    product = (input("Enter the product url to scrape or press 0 to return to main menu > "))
    if product == '0':
        mainmenu()

    while validators.url(product) != True:
        product = input('Invalid url, retry or press 0 to return to main menu > ')
        if product == '0':
            mainmenu()

    product = str(product)
    zalando_scraper(product)
    print("\n0: Main Menu\n1: Continue to Scrape \n")

    selections = {
        0: ["0", "Main Menu"],
        1: ["1", "Continue to Scrape"],
    }
    selections = select_choice(selections)
    if selections == 0:
        mainmenu()
    elif selections == 1:
        zalando_scrape_menu()

def authentication(license_key,hardware_id,ip,name,system):
    authresp = requests.post("http://18.192.56.76/version",headers={'tornadoaio-license':license_key,'accept':'application/json'},json={'hwid': hardware_id, 'ip': ip, 'name': name, 'system': system})
    return authresp.status_code,json.loads(str(authresp.text))

def mainmenu():

    print(("\n   Main Menu   \n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"))
    print("1: Zalando\n2: Quit\n")

    selections = {
        1: ["1", "Zalando"],
        2: ["2", "Quit"]

    }
    selections = select_choice(selections)

    if selections == 1:
        zalando()
    if selections == 2:
        sys.exit()
def clirun():
    TornadoCLIintro()
    mainmenu()

if __name__ == '__main__':
    os.system('cls')
    f = open('.\\config\\settings.json', 'r')
    settings = json.load(f)
    license_key = settings['key']
    uname = platform.uname()
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    system = uname.system
    name = uname.node
    hardware_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
    ip = external_ip
    status = authentication(license_key, hardware_id, ip, name, system)[0]

    if status == 200 or status == 201:
        if (__version__) == (authentication(license_key, hardware_id, ip, name, system)[1])["version"]:
            clirun()
        else:
            print(Fore.BLUE + f'Update avalaible (v.{(authentication(license_key, hardware_id, ip, name, system)[1])["version"]})')

    elif  status == 403:
        print(Fore.RED + 'License not found!')
        time.sleep(3)
        sys.exit()
    elif status == 405:
        print(Fore.LIGHTRED_EX + 'License is already in use on another machine!\n Reset your key and retry.')
        time.sleep(5)
        sys.exit()
    else:
        print(Fore.LIGHTRED_EX + 'SERVER ERROR')
