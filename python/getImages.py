import re
import requests
from bs4 import BeautifulSoup


site = 'https://brawlify.com/maps/'
site = "https://brawlify.com/gamemodes/detail/Duels"
response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')

urls = [img['src'] for img in img_tags]


for url in urls:
    filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
    if not filename:
         print("Regex didn't match with the url: {}".format(url))
         continue
    print(url)
    pictureName=filename.group(1)
    pictureName=pictureName.replace("-"," ").upper()
    pictureName=pictureName.replace(" 2","")
    pictureName=pictureName.replace("'","")
    pictureName=pictureName.replace(".PNG",".JPG")
    print(pictureName)

    with open("../web/static/img/maps/"+pictureName, 'wb') as f:
        if 'http' not in url:
            # sometimes an image source can be relative 
            # if it is provide the base url which also happens 
            # to be the site variable atm. 
            url = '{}{}'.format(site, url)
        response = requests.get(url)
        f.write(response.content)