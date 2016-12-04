import requests, bs4
''' This part takes the productlist site and returns the maximum number of articles.
    The selector and subsequent editing of the value may be used for ALL other article groups on GH'''

def get_max_article(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    art_list = soup.select('.btn3')
    max_art = (art_list[0].getText()).split()
    return str(max_art[0]).strip()
