from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import bs4
import numpy as np
import pandas as pd


# Proxy changer is a snipped module to gather Infos about Proxies
# It is party of the "ADAGA" project



##########################################################
# get the text from every EVEN row of the table          #
# 1.step get the IP out of JS String                     #
# 2. get the "port" and the "protocol" out of the columns#
# 3. the information in "proxy_info" (list of lists)     #
##########################################################
def gather_new_proxies():
    # Set Firefox binary to actual Firefoxbinary


    binary = FirefoxBinary(r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe")
    driver = webdriver.Firefox(firefox_binary=binary)

    # Go to Freeproxy.net, wait til loaded and collect incl. JavaScript Info
    # Pars it to bs4

    proxy_URL = "http://freeproxylists.net/"
    driver.get(proxy_URL)
    time.sleep(1)
    res_proxy = driver.page_source
    soup_proxy = bs4.BeautifulSoup(res_proxy, "lxml")

    # TODO check out why gatehr _new proxies isn't updating
    # 1.Step (IPS)
    proxy_IP = []  # temporary List to store IPS
    proxy_info = [[], [], [], []]  # output List
    print("start")

    IP = soup_proxy.select(".Even a")
    for proxyIP in IP:
        proxy_IP.append((proxyIP.getText()))

    for IPs in proxy_IP:
        proxy_info[0].append(IPs)

    # 2.Step (Port und Protocol)
    Reihen = soup_proxy.select(".Even td")
    x = 0
    for x in range(0, (len(Reihen) - 10), 10):
        if ((str(Reihen[x + 2].getText()) == "HTTP") or (str(Reihen[x + 2].getText()) == "HTTPS")):
            proxy_info[1].append(Reihen[x + 1].getText())
            proxy_info[2].append(Reihen[x + 2].getText())
            # TODO make 4.column work (should only contain "True"
            proxy_info[3].append(1)

    proxy_info_np = np.array(proxy_info)
    driver.close()
    print("done")
    return proxy_info_np
