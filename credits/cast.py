import re
import .person
   
class Cast(Person):
    
    imdb = None
    name = None
    character = None
    extras = None
    alternatives = None
    characters = None
    
    def __init__(self):
        self.extras = []
        self.alternatives = []
        self.characters = []
    
    def parse(self):
        self.setImdbId()
        self.setCleanName()
        self.setCharacter()
        self.setExtras()
        self.setCharacters()
        return self
    
    def getJson(self):
        json = {}
        json['imdb'] = self.imdb
        json['name'] = self.name
        if len(self.extras) > 0:
            json['extras'] = self.extras
        if len(self.characters) > 0:
            json['characters'] = self.characters
        if len(self.alternatives) > 0:
            json['alternatives'] = self.alternatives
        return json
    
    def setImdbId(self):
        self.imdb = re.findall('\d+', self.tags[1].find_all('a')[0]['href'])[0]
        return self
    
    def setCleanName(self):
        self.name = " ".join(re.sub(cleanr, '', self.tags[1].__str__().strip()).split())
        return self
    
    def setCharacter(self):
        self.character = " ".join(re.sub(cleanr, '', self.tags[3].__str__().strip()).split())
        return self
    
    def setExtras(self):
        pos = self.character.find('(')
        if pos > 0:
            self.extras = re.findall('\(.*?\)', self.character)
            self.character = self.character[0:pos]
            self.extras = list(map(lambda s: s[1:-1], self.extras))
            for extra in self.extras:
                if extra.startswith('as '):
                    self.alternatives.append(extra.replace('as ', ''))
                    self.extras.remove(extra)
        return self
                                   
    def setCharacters(self):
        pos = self.character.find(' / ')
        if pos > 0:
            self.characters = self.character.split(' / ')
        else:
            self.characters = [self.character]
        if len(self.characters) > 0:
            self.characters = list(map(lambda s: s.strip(), self.characters))
        return self
