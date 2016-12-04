import bs4
import requests
import re
import pprint

Produkt = {}  # Dictionary, in which all pairs(name, properties, etc...) of individual product is saved
gh_url = 'https://geizhals.at/samsung-ue49ku6170-a1447439.html'


def get_properties(url):
    resp = requests.get(url)
    descSoup = bs4.BeautifulSoup(resp.text, 'html.parser')
    descriptions = descSoup.select('#gh_proddesc')  # Gets descriptions of products main site off GH

    # RE to get product name
    REprodName = re.compile(r'((\w|\d)*)*-((\w|\d)*)*-a')
    # prodName = str(REprodName.search(url).group(0))
    Produkt['Produktname'] = str(REprodName.search(url).group(0)[:-2])

    # FOR LATER USE eanRe = re.compile(r'\d*')        Regex für EANs
    #               realEan = eanRe.search(ean)

    # This part gets EAN No. and 'Listed since' from GH and adds it to dictionary "Produkt"
    # takes p elements in  descriptions and returns a list, which first element is the EAN number; :-5 to slice '<\p>' off
    ean = ((str(descSoup.select('#gh_proddesc p')).split()[1])[:-5])
    gelSeit = ((str(descSoup.select('#gh_proddesc p')).split()[4])[:-1])
    Produkt['EAN'] = ean
    Produkt['Gelistet_seit'] = gelSeit

    cleanDesc = str(descriptions)[str(descriptions).find(r'Diagonale:'):str(descriptions).find('<p>EAN')]
    descList = cleanDesc.split('\x95')

    # For loop, which splits the list of descriptions into 2 parts (name and value of property)
    # and replaces problematic slashes

    for prop in descList:
        propName, propValue = str(prop).split(': ')
        if r'/\u200b' in str(propValue):
            prop.replace('\/\\u200b', r'/')
            print('found and replaced')
        Produkt[propName] = propValue
    print('Properties: ', Produkt)
    # use find No to slice string of descs
    # find start of descs = after proddesc



    # loops over classes getting the prices and appends it as a list to "Produkte" dictionary
    Preise = []
    gh_prices = descSoup.select('.gh_price')
    REprices = re.compile(r'(\d)+')
    for k in range(len(gh_prices)):
        simplePrice = str((REprices.search(gh_prices[k].getText())).group())
        Preise.append(simplePrice)
    print('Preise: ', Preise)

    # Gets Distributors of individual products and creates
    Anbieter = []
    ghAnbieter = descSoup.select('.notrans')

    for distributor in range((len(ghAnbieter))):
        Anbieter.append((ghAnbieter[distributor].getText()).strip())
    print('Anbieter: ', Anbieter)

    # TODO:
    all_infos = []
    all_infos.append(Produkt)
    all_infos.append(Preise)
    all_infos.append(Anbieter)

    sortedKeys = sorted(Produkt.keys())
    print('Sorted Keys: ', sortedKeys)


#   print(all_infos)
#    fileName = str(Produkt['Produktname']) + ".csv"
#    infoFile = open(fileName, 'a')
#    infoFile.write()
get_properties(gh_url)
