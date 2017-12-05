from bs4 import BeautifulSoup
import urllib.request
import re
import lxml

class Credits:
    
    url = None
    soup = None
    cleanr = None
    
    def __init__(self):
        self.cleanr = re.compile('<.*?>')
    
    def setUrl(self, url):
        self.url = url
        return self
        
    def load(self):
        self.soup = BeautifulSoup(urllib.request.urlopen(self.url), "lxml")
        return self

    def getCast(self):
        tables = self.soup.find_all('table', {'class': 'cast_list'})
        cast = []
        for row in tables[0].find_all('tr'):
            tds = row.find_all('td')
            if len(tds) == 4:
                actor = Cast()
                cast.append(actor.setTags(tds).parse().getJson())
        return cast
