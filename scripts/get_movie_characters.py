from bs4 import BeautifulSoup
import urllib.request
import re
import lxml

html_page = urllib.request.urlopen("http://www.imdb.com/title/tt0974015/fullcredits")
soup = BeautifulSoup(html_page, "lxml")
tables = soup.find_all('table', {'class': 'cast_list'})

cleanr = re.compile('<.*?>')

for row in tables[0].find_all('tr'):
    td_tags = row.find_all('td')
    if len(td_tags) == 4:
        a = td_tags[1].find_all('a')[0]
        imdbId = re.findall('\d+', a['href'])[0]
        name = re.sub(cleanr, '', td_tags[1].__str__().strip())
        name = " ".join(name.split())
        character = re.sub(cleanr, '', td_tags[3].__str__().strip())
        character = " ".join(character.split())
        pos = character.find('(')
        alternatives = []
        if pos > 0:
            extras = re.findall('\(.*?\)', character)
            character = character[0:pos]
            extras = list(map(lambda s: s[1:-1], extras))
            for extra in extras:
                if extra.startswith('as '):
                    alternatives.append(extra.replace('as ', ''))
                    extras.remove(extra)
        else:
            extras = []
        pos = character.find(' / ')
        if pos > 0:
            characters = character.split(' / ')
        else:
            characters = [character]
