import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import proxy_changer as pc
import properties
import max_article
import pandas as pd

# initialisiere ein leere Liste für die Links zu den Produkten
# initialize list of links to store product-page links
links = []
proxiesF = []
product_nr = 0
breaker = False

n = 0
max_scrape_sites = 1
changefrequency = 0.25
start_time = time.ctime()
starttime_se = time.time()

total_nr_products = int(max_article.get_max_article("https://geizhals.at/?cat=tvlcd"))
print("Number of Products: {}".format(total_nr_products))
# TODO URL als konstante

print("Start at: '{}'".format(start_time))

product_links = open("Product_Links.csv", "w")
product_links.close()


#
def random_changer(x):
    if np.random.random() > (1 - x):
        return True
    else:
        return False


# Change Proxy (proxiesF)

def change_active_proxy():
    x = int((np.random.randint(len(proxies))))
    print("Change Proxyx X-Value : {} Length :{}".format(x, len(proxies)))
    proxiesF_tmp = proxies[x][2] + " : " + proxies[x][0] + ":" + proxies[x][1]
    print("Active proxy is: {} ".format(proxiesF_tmp))

    del x
    return proxiesF_tmp


# proxy_changer(PC):
# method to gather new proxy information if there are not enough working proxies in the List Proxy)
# x = Info (IP, Port, Protocol, Working )
# y = proxy
tmp_time_st = time.time()
proxies_ar = pc.gather_new_proxies()
print("Proxy-List lenght: {}.".format(len(proxies_ar[0])))
proxies = []
for i in range(len(proxies_ar[2])):
    proxies.append([proxies_ar[0][i],
                    proxies_ar[1][i],
                    proxies_ar[2][i],
                    proxies_ar[3][i]])
print("Proxy loading took {} Seconds (gatther_new_proxies".format(time.time() - starttime_se))
print(proxies)
print(len(proxies))
# TODO check out why gather_new_proxies isn't updating
# TODO call the function to gather new proxies and send it to requests
# TODO generate a random generator for proxychange Done
# TODO develop logic to manage broken proxies and gather new

# format proxy info for requests
proxiesF = proxies[0][2] + " : " + proxies[0][0] + ":" + proxies[0][1]

# print(soup.prettify())
while True:
    url = "https://geizhals.at/?cat=tvlcd&pg=" + str(n) + "#productlist"
    print("\n" + "-" * 10 + "Seite:", str(n + 1), "-" * 10)
    # Change Proxy by X% chance
    if random_changer(changefrequency):
        print("changing proxy")
        proxiesF = change_active_proxy()

    n += 1
    time.sleep(np.random.random() + 1)
    if n > max_scrape_sites:
        print("Test bei Seite {} abgebrochen".format(n))
        break

    try:
        response = requests.get(url, proxies=proxiesF)

        plain_text = response.text
        soup = BeautifulSoup(plain_text, "lxml")

        for product in soup.find_all("div", {"class": "productlist__item productlist__name"}):

            for link in product.find_all("a"):
                product_links = open("Product_Links.csv", "a")

                link_tmp = link.get("href")
                if "artikel" in str(link_tmp):
                    pass
                else:
                    product_nr += 1
                    print(product_nr, " ", end="")
                    links.append(link.get("href"))

                    product_links.write("https://geizhals.at/")
                    product_links.write(link_tmp)
                    product_links.write("\n")
                    if len(links) > total_nr_products:
                        print("plan hat gefunzt")
                        product_links.close()
                        breaker = True

                        break;
                product_links.close()
            if breaker:
                break
        if breaker:
            break


    except:
        print("Error")
        break

product_links.close()
product_info_list = []
links_produkte = open("Product_Links.csv", "r")
links_liste = (links_produkte.read()).split()

final = open("Final.csv", "w")

Infos = []
Preise = []
Anbieter = []
for productUrl in links_liste:
    tmp = properties.get_properties(productUrl, proxiesF)
    product_info_list.append(tmp)

    final.write(str(tmp) + "\n")
    Infos.append(tmp[0])
    Preise.append(tmp[1])
    Anbieter.append(tmp[2])



    if random_changer(changefrequency):
        proxiesF = change_active_proxy()
    print(len(product_info_list), " Produkte aufgenommen")
    time.sleep(np.random.random() + 0.1)

print("-"*10)

product_info_Df = pd.DataFrame(product_info_list[0])
print(product_info_Df.head())

links_produkte.close()
end_time = time.time()
final.close()
print("Duration :", (end_time - starttime_se))
# print("LinkTmpType: ", type(link_tmp))
