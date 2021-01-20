import requests
from bs4 import BeautifulSoup
#from googletrans import Translator
#translator = Translator()

def get_info():
    abilitys = requests.get('http://powerlisting.wikia.com/wiki/Special:Random')
    names = requests.get('https://www.coolgenerator.com/album-name-generator')
    soup1 = BeautifulSoup(abilitys.content, 'html.parser')
    soup2 = BeautifulSoup(names.content, 'html.parser')

    Standname = soup2.find('b').text
    abilityname = soup1.title.string.split('|')[0]
    ability = soup1.find_all('p')[1].text

    #ability = translator.translate(ability,src='en',dest = 'es')

    return [Standname,abilityname,ability]


