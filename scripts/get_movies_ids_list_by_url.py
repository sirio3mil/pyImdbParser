from bs4 import BeautifulSoup
import urllib.request
import re
import lxml

html_page = urllib.request.urlopen("http://www.imdb.com/")
soup = BeautifulSoup(html_page, "lxml")
anchors = soup.find_all('a', {'href': re.compile('/title/tt.*')})

for anchor in anchors:
    print (re.findall('\d+', anchor['href'])[0])
