######################################################
import re
from multiping import multi_ping
import requests
from bs4 import BeautifulSoup
import colorama
from art import *
######################################################

proxy_all = 229500
proxy_list = []

def parser():
    page = 1
    enum = 1
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    proxies = {'http': 'http://172.67.181.16:80'}
    valid = colorama.Fore.GREEN + "прокси валидный"
    non_valid = colorama.Fore.RED + "прокси не валидный"
    for _ in range(10):
        url = f"https://ru.proxytools.online/proxy-list/?page={page}"
        response = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find("table", class_="table")
        tbody = table.find("tbody")
        trs = tbody.find_all("tr")
        for tr in trs:
            ip = tr.find("a", href=re.compile("/proxy-list/")).get("href")
            link = f"https://ru.proxytools.online{ip}"
            req = requests.get(link, proxies=proxies, headers=headers)
            ip_link = BeautifulSoup(req.text, 'lxml')

            ip_addr = ip_link.find("title")
            p = ip_link.find("p", string=re.compile('^Прокси')).text
            proxy = f"{ip_addr.text.partition(' ')[2]}:{p.partition(':')[2].replace(',', ' ').split()[0]}"

            proxy_list.append(proxy + "\n")
            print(f"{enum}: {ip_addr.text.partition(' ')[2]}:{p.partition(':')[2].replace(',', ' ').split()[0]}")




            enum += 1
        page += 1
    file = open('proxy_list.txt', 'w')
    try:
        file.writelines(proxy_list)
    finally:
        file.close()
def check_status_ip(timeout=3):
    j = 0
    with open("proxy_list.txt") as file:
        proxy_base = ''.join(file.readlines()).strip().split('\n')

    for proxy in proxy_base:
        multi_ping(proxy_base[j].partition(":")[0], timeout=2, retry=3)
        j += 1


def commands():
    q = str(input(colorama.Fore.CYAN + ">>>"))
    print(colorama.Fore.RESET)
    if q == "help":
        print(q)
        commands()
    elif q == "update_list":
        parser()
        commands()
    elif q == "check_status":
        check_status_ip()
        commands()
    elif q == "exit":
        exit()
    else:
        print("нет такой команды!!!")
        commands()

if __name__ == "__main__":
    print(colorama.Fore.RED + text2art("S.P.C"))
    commands()

