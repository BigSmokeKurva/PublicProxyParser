import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import subprocess
import os

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}
proxyList = []

def safety(fn):
    def wrapped():
        try: fn()
        except: pass
    return wrapped

@safety
def hidemy():

    startLen = len(proxyList)
    url = "https://hidemy.name/ru/proxy-list/#list"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    pagination = soup.find("div", class_="pagination")

    urlMax = int(pagination.find_all("li")[-2].find("a")["href"][22:-5])
    urls = ["https://hidemy.name/ru/proxy-list/#list"]
    for i in range(64, urlMax+64, 64):
        urls.append(f"https://hidemy.name/ru/proxy-list/?start={i}#list")

    for url in urls:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        proxies = soup.find('tbody')

        for i in proxies.find_all("tr"):
            proxyListTemp = i.find_all("td")

            if len(proxyListTemp[4].string.split(",")) == 1:
                proxyList.append(
                    [proxyListTemp[0].string,
                     proxyListTemp[1].string,
                     proxyListTemp[4].string])
            else:
                proxyListTemp[4] = proxyListTemp[4].string.split(",")
                proxyListTemp[4][1] = proxyListTemp[4][1].strip()
                proxyList.append(
                    [proxyListTemp[0].string,
                     proxyListTemp[1].string,
                     proxyListTemp[4][0]])
                proxyList.append(
                    [proxyListTemp[0].string,
                     proxyListTemp[1].string,
                     proxyListTemp[4][1]])

    #for i in proxyList:
    #    print(i)
    print(f"hidemy.name: получено {len(proxyList) - startLen} прокси.")

@safety
def freeproxylist():
    startLen = len(proxyList)
    url = "https://free-proxy-list.net/anonymous-proxy.html"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    proxies = soup.find("tbody")
    for i in proxies.find_all("tr"):
        proxyListTemp = i.find_all("td")
        proxyList.append(
            [proxyListTemp[0].string,
             proxyListTemp[1].string,
             "HTTP" if proxyListTemp[6].string == "no" else "HTTPS"])

    #for i in proxyList:
    #    print(i)
    print(f"free-proxy-list.net: получено {len(proxyList) - startLen} прокси.")

@safety
def proxydaily():
    startLen = len(proxyList)
    url = "https://proxy-daily.com/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    proxies = soup.find_all("div", class_="centeredProxyList freeProxyStyle")
    for i in proxies[0].string.split("\n"): #HTTP
        if len(i) < 1: continue
        i += ":HTTP"
        i = i.split(":")
        proxyList.append(i)
    for i in proxies[1].string.split("\n"): #SOCKS4
        if len(i) < 1: continue
        i += ":SOCKS4"
        i = i.split(":")
        proxyList.append(i)
    for i in proxies[2].string.split("\n"): #SOCKS5
        if len(i) < 1: continue
        i += ":SOCKS5"
        i = i.split(":")
        proxyList.append(i)

    #for i in proxyList:
    #    print(i)
    print(f"proxy-daily.com: получено {len(proxyList) - startLen} прокси.")

@safety
def socksproxy():
    startLen = len(proxyList)
    url = "https://www.socks-proxy.net/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    proxies = soup.find("tbody")
    for i in proxies.find_all("tr"):
        proxyListTemp = i.find_all("td")
        proxyList.append(
            [proxyListTemp[0].string,
             proxyListTemp[1].string,
             "SOCKS4" if proxyListTemp[4].string == "Socks4" else "SOCKS5"])

    #for i in proxyList:
    #    print(i)
    print(f"socks-proxy.net: получено {len(proxyList) - startLen} прокси.")

@safety
def proxyscape():
    startLen = len(proxyList)
    for i in requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", #HTTP
                          headers=headers).text.split("\n"):
        if len(i) < 1: continue
        i = i.strip() + ":HTTP"
        i = i.split(":")
        proxyList.append(i)

    for i in requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all", #SOCKS4
                          headers=headers).text.split("\n"):
        if len(i) < 1: continue
        i = i.strip() + ":SOCKS4"
        i = i.split(":")
        proxyList.append(i)

    for i in requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all", #SOCKS5
                          headers=headers).text.split("\n"):
        if len(i) < 1: continue
        i = i.strip() + ":SOCKS5"
        i = i.split(":")
        proxyList.append(i)

    #for i in proxyList:
    #    print(i)
    print(f"proxyscrape.com: получено {len(proxyList) - startLen} прокси.")

@safety
def proxylist():
    startLen = len(proxyList)
    for i in requests.get("https://www.proxy-list.download/api/v0/get?l=en&t=http", #HTTP
                          headers=headers,
                          ).json()[0]["LISTA"]:
        proxyList.append([i["IP"], i["PORT"], "HTTP"])

    for i in requests.get("https://www.proxy-list.download/api/v0/get?l=en&t=socks4", #SOCKS4
                          headers=headers,
                          ).json()[0]["LISTA"]:
        proxyList.append([i["IP"], i["PORT"], "SOCKS4"])

    for i in requests.get("https://www.proxy-list.download/api/v0/get?l=en&t=socks5", #SOCKS5
                          headers=headers,
                          ).json()[0]["LISTA"]:
        proxyList.append([i["IP"], i["PORT"], "SOCKS5"])

    #for i in proxyList:
    #    print(i)
    print(f"proxy-list.download: получено {len(proxyList) - startLen} прокси.")

@safety
def scrapingant():
    startLen = len(proxyList)
    url = "https://scrapingant.com/free-proxies/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    proxies = soup.find("table", class_="proxies-table")
    for i in proxies.find_all("tr"):
        proxyListTemp = i.find_all("td")
        if len(proxyListTemp) < 1: continue
        proxyList.append(
            [proxyListTemp[0].string,
             proxyListTemp[1].string,
             proxyListTemp[2].string])

    #for i in proxyList:
    #    print(i)
    print(f"scrapingant.com: получено {len(proxyList) - startLen} прокси.")

@safety
def usproxy():
    startLen = len(proxyList)
    url = "https://www.us-proxy.org/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    proxies = soup.find("tbody")
    for i in proxies.find_all("tr"):
        proxyListTemp = i.find_all("td")
        proxyList.append(
            [proxyListTemp[0].string,
             proxyListTemp[1].string,
             "HTTP" if proxyListTemp[6].string == "no" else "HTTPS"])

    #for i in proxyList:
    #    print(i)
    print(f"us-proxy.org: получено {len(proxyList) - startLen} прокси.")

@safety
def premproxy():
    startLen = len(proxyList)
    session = HTMLSession()
    for https in [False, True]:
        if https:
            stype = "list"
            pn1 = ":HTTPS"
            pn2 = ":HTTP"
        else:
            stype = "socks-list"
            pn1 = ":SOCKS4"
            pn2 = ":SOCKS5"

        url = f"https://premproxy.com/{stype}/"
        response = session.get(url, headers=headers)
        response.html.render()
        urls = []
        for i in range(1, int(str(response.html.find("#proxylist > div:nth-child(1) > div:nth-child(6) > ul:nth-child(1)")[0].text).split("\n")[-2])+1):
            urls.append(f"https://premproxy.com/{stype}/ip-port/{i}.htm")

        for url in urls:
            response = session.get(url, headers=headers)
            response.html.render()
            for i in str(response.html.find("#ipportlist")[0].text).split("\n"):
                p1 = str(i + pn1).split(":")
                p2 = str(i + pn2).split(":")
                proxyList.append(
                    [p1[0],
                     p1[1],
                     p1[2]])
                proxyList.append(
                    [p2[0],
                     p2[1],
                     p2[2]])
    #for i in proxyList:
    #    print(i)
    print(f"premproxy.com: получено {len(proxyList) - startLen} прокси.")

@safety
def proxylistorg():
    startLen = len(proxyList)
    session = HTMLSession()

    url = "http://proxy-list.org/russian/index.php?p=1"
    response = session.get(url, headers=headers)
    response.html.render()
    urls = []
    for i in range(1, int(str(response.html.find(".table-menu")[0].text).split(" ")[-2])+1):
        urls.append(f"http://proxy-list.org/russian/index.php?p={i}")
    for url in urls:
        response = session.get(url, headers=headers)
        response.html.render()

        for i in response.html.find(".table")[0].find("ul"):
            i = str(i.text).split("\n")
            proxy = str(i[0][i[0].index(")")+1:] + ":" + i[1]).split(":")
            proxyList.append(
                [proxy[0],
                 proxy[1],
                 proxy[2]])

    #for i in proxyList:
    #    print(i)
    print(f"proxy-list.org: получено {len(proxyList) - startLen} прокси.")

@safety
def coolproxynet():
    startLen = len(proxyList)
    for i in requests.get("http://www.cool-proxy.net/proxies.json",
                          headers=headers,
                          ).json():
        proxyList.append([i["ip"], i["port"], "HTTP"])
        proxyList.append([i["ip"], i["port"], "HTTPS"])

    #for i in proxyList:
    #    print(i)
    print(f"cool-proxy.net: получено {len(proxyList) - startLen} прокси.")

@safety
def echolinkorg():
    startLen = len(proxyList)
    url = "http://www.echolink.org/proxylist.jsp"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    for i in soup.find_all("tr", class_="normal-row"):
        i = i.find_all("td")
        proxyList.append(
            [i[1].string.strip(),
             i[2].string.strip(),
             "HTTP"])
        proxyList.append(
            [i[1].string.strip(),
             i[2].string.strip(),
             "HTTPS"])

    #for i in proxyList:
    #    print(i)
    print(f"echolink.org: получено {len(proxyList) - startLen} прокси.")

@safety
def xroxycom():
    startLen = len(proxyList)
    url = "https://www.xroxy.com/proxylist.php?port=&type=&ssl=&country=&latency=&reliability=&sort=reliability&desc=true&pnum=0#table"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    urls = []
    for i in range(0, int(int(soup.select("b:nth-child(1)")[-1].text)//10)+1):
        urls.append(f"https://www.xroxy.com/proxylist.php?port=&type=&ssl=&country=&latency=&reliability=&sort=reliability&desc=true&pnum={i}#table")

    for url in urls:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        for row in [soup.find_all("tr", class_="row0"), soup.find_all("tr", class_="row1")]:
            for i in row:
                i = i.find_all("td")
                ptype = i[2].text.upper()
                if not ptype in ["SOCKS4", "SOCKS5", "HTTPS", "HTTP"]: continue
                proxyList.append(
                    [i[0].text.strip(),
                     i[1].text,
                     ptype])

    #for i in proxyList:
    #    print(i)
    print(f"xroxy.com: получено {len(proxyList) - startLen} прокси.")

@safety
def ipadresscom():
    startLen = len(proxyList)
    url = "https://www.ip-adress.com/proxy-list"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    for i in soup.select(".htable > tbody:nth-child(2)")[0].find_all("tr"):
        i = i.find_all("td")
        proxy = i[0].text.split(":")
        proxyList.append(
            [proxy[0],
             proxy[1],
             "HTTP"])
        proxyList.append(
            [proxy[0],
             proxy[1],
             "HTTPS"])

    #for i in proxyList:
    #    print(i)
    print(f"ip-adress.com: получено {len(proxyList) - startLen} прокси.")

@safety
def nntimecom():
    startLen = len(proxyList)
    session = HTMLSession()
    url = "http://nntime.com/proxy-list-01.htm"
    response = session.get(url, headers=headers)
    response.html.render()
    urls = []
    for i in range(1, int(response.html.find("#navigation")[0].find("a")[-2].text)+1):
        urls.append(f"http://nntime.com/proxy-list-0{i}.htm")

    for url in urls:
        response = session.get(url, headers=headers)
        response.html.render()
        for i in response.html.find("#proxylist > tbody:nth-child(2)")[0].find("tr"):
            i = i.find("td")[1].text
            i = str(i[:i.index("document")] + i[i.index("):")+1:]).split(":")
            proxyList.append(
                [i[0],
                 i[1],
                 "HTTPS"])
            proxyList.append(
                [i[0],
                 i[1],
                 "HTTP"])
    #for i in proxyList:
    #    print(i)
    print(f"nntime.com: получено {len(proxyList) - startLen} прокси.")

@safety
def proxynovacom():
    startLen = len(proxyList)
    session = HTMLSession()
    url = "https://www.proxynova.com/proxy-server-list/"
    response = session.get(url, headers=headers)
    response.html.render()
    for i in response.html.find("#tbl_proxy_list > tbody:nth-child(2)")[0].find("tr"):
        i = i.find("td")
        if len(i) < 2: continue
        i = [i[0].text[i[0].text.index(";")+1:], i[1].text]
        proxyList.append(
            [i[0],
             i[1],
             "HTTPS"])
        proxyList.append(
            [i[0],
             i[1],
             "HTTP"])
    #for i in proxyList:
    #    print(i)
    print(f"proxynova.com: получено {len(proxyList) - startLen} прокси.")

@safety
def proxylistende():
    startLen = len(proxyList)
    url = "https://www.proxy-listen.de/Proxy/Proxyliste.html"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    value = soup.select("#right_row > input:nth-child(4)")[0]["value"]
    for ptype in ["http", "https", "socks4", "socks5", "httphttps"]:
        data = {
        "filter_port": "",
        "filter_http_gateway": "",
        "filter_http_anon": "",
        "filter_response_time_http": "",
        "fefefsfesf4tzrhtzuh": value,
        "filter_country": "",
        "filter_timeouts1": "",
        "liststyle": "info",
        "proxies": "50",
        "type": ptype,
        "submit": "Show"
    }
        response = requests.post(url, headers=headers, data=data)
        soup = BeautifulSoup(response.text, 'lxml')
        for i in [soup.find_all("tr", class_="proxyListOdd"), soup.find_all("tr", class_="proxyListEven")]:
            for proxy in i:
                proxy = proxy.find_all("td")

                if not ptype == "httphttps":
                    proxyList.append(
                        [proxy[0].text,
                         proxy[1].text,
                         ptype.upper()])
                else:
                    proxyList.append(
                        [proxy[0].text,
                         proxy[1].text,
                         "HTTP"])
                    proxyList.append(
                        [proxy[0].text,
                         proxy[1].text,
                         "HTTPS"])
    #for i in proxyList:
    #    print(i)
    print(f"proxy-listen.de: получено {len(proxyList) - startLen} прокси.")

@safety
def myproxycom():
    startLen = len(proxyList)
    urls = [
        "https://www.my-proxy.com/free-socks-4-proxy.html",
        "https://www.my-proxy.com/free-socks-5-proxy.html",
        "https://www.my-proxy.com/free-proxy-list.html",
        "https://www.my-proxy.com/free-proxy-list-2.html",
        "https://www.my-proxy.com/free-proxy-list-3.html",
        "https://www.my-proxy.com/free-proxy-list-4.html",
        "https://www.my-proxy.com/free-proxy-list-5.html",
        "https://www.my-proxy.com/free-proxy-list-6.html",
        "https://www.my-proxy.com/free-proxy-list-7.html",
        "https://www.my-proxy.com/free-proxy-list-8.html",
        "https://www.my-proxy.com/free-proxy-list-9.html",
        "https://www.my-proxy.com/free-proxy-list-10.html",
    ]

    for url in urls:
        if "socks-4" in url: ptype = "SOCKS4"
        elif "socks-5" in url: ptype = "SOCKS5"
        else: ptype = "HTTPHTTPS"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        proxies = soup.select(".list")[0].text.split("#")[:-1]
        for i in range(len(proxies)):
            if not i == 0:
                proxies[i] = proxies[i][2:]
            i = proxies[i].split(":")
            if not ptype == "HTTPHTTPS":
                proxyList.append(
                    [i[0],
                     i[1],
                     ptype])
            else:
                proxyList.append(
                    [i[0],
                     i[1],
                     "HTTP"])
                proxyList.append(
                    [i[0],
                     i[1],
                     "HTTPS"])
    #for i in proxyList:
    #    print(i)
    print(f"my-proxy.com: получено {len(proxyList) - startLen} прокси.")

"""@safety
def proxy_py():
    startLen = len(proxyList)
    url = "http://127.0.0.1:55555/api/v1/"
    json_data = {
        "model": "proxy",
        "method": "count",
    }
    count = requests.post(url, json=json_data).json()["count"]
    json_data = {
        "model": "proxy",
        "method": "get",
        "limit": 1024,
        "offset": 0,
        "fields": "address,protocol,port"
    }
    offset = 0
    for i in range(count//1024):
        response = requests.post(url, json=json_data).json()
        #print(response)
        for proxy in response["data"]:
            proxy["address"] = proxy["address"][proxy["address"].index("//")+2:]
            proxy["address"] = proxy["address"][:proxy["address"].index(":")]

            proxyList.append([proxy["address"], proxy["port"], proxy["protocol"].upper()])
        json_data["offset"] += 1024
    #for i in proxyList:
    #    print(i)
    print(f"proxy_py: получено {len(proxyList) - startLen} прокси.")"""

#proxy_py()

def writeFile():
    with open("checker/temp.txt", "w", encoding="utf-8") as f:
        for i in proxyList:
            f.write(str(f"{i[0]},{i[1]},{i[2]}".strip()+"\n"))

def main():
    hidemy()
    freeproxylist()
    proxydaily()
    socksproxy()
    proxyscape()
    proxylist()
    scrapingant()
    usproxy()
    premproxy()
    proxylistorg()
    coolproxynet()
    echolinkorg()
    xroxycom()
    ipadresscom()
    nntimecom()
    proxynovacom()
    proxylistende()
    myproxycom()

    writeFile()
    print(f"Всего прокси - {len(proxyList)}")
    a = input("Введите количество потоков (200 среднячок): ")
    subprocess.Popen(fr'"{os.path.abspath(os.curdir)}/checker/ProxyCheck.exe" {a} "{os.path.abspath(os.curdir)}/"', shell=True)

if __name__ == '__main__':
    main()

