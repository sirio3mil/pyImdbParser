from bs4 import BeautifulSoup
import urllib.request
import re
import lxml

html_page = urllib.request.urlopen("http://www.imdb.com/title/tt0974015/fullcredits")
soup = BeautifulSoup(html_page, "lxml")
tables = soup.find_all('table', {'class': 'cast_list'})

cleanr = re.compile('<.*?>')

for row in tables[0].find_all('tr'):
    actor = {}
    td_tags = row.find_all('td')
    if len(td_tags) == 4:
        a = td_tags[1].find_all('a')[0]
        actor['imdb'] = re.findall('\d+', a['href'])[0]
        actor['name'] = re.sub(cleanr, '', td_tags[1].__str__().strip())
        actor['name'] = " ".join(actor['name'].split())
        character = re.sub(cleanr, '', td_tags[3].__str__().strip())
        character = " ".join(character.split())
        pos = character.find('(')
        alternatives = []
        if pos > 0:
            actor['extras'] = re.findall('\(.*?\)', character)
            character = character[0:pos]
            actor['extras'] = list(map(lambda s: s[1:-1], actor['extras']))
            for extra in actor['extras']:
                if extra.startswith('as '):
                    if 'alternatives' not in actor.keys():
                        actor['alternatives'] = []
                    actor['alternatives'].append(extra.replace('as ', ''))
                    actor['extras'].remove(extra)
                    if len(actor['extras']) == 0:
                        del actor['extras']
        pos = character.find(' / ')
        if pos > 0:
            actor['characters'] = character.split(' / ')
        else:
            actor['characters'] = [character]
        if len(actor['characters']) == 0:
            del actor['characters']
        else:
            actor['characters'] = list(map(lambda s: s.strip(), actor['characters']))
