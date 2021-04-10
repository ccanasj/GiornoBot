import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import asyncio
import urllib
import random as rd

translator = Translator()

async def get_info():
    abilitys = requests.get('https://powerlisting.fandom.com/wiki/Special:Random')
    soup1 = BeautifulSoup(abilitys.content, 'html.parser')
    abilityname = soup1.title.string.split('|')[0]
    ability = soup1.find_all('p')[1].text
    Limitaciones = soup1.get_text()
    if 'Limitations' in Limitaciones:
        limitation = Limitaciones.split('Limitations')[2].split('\n')[1]
        info_ability = translator.translate(f'{ability}_{abilityname}_{limitation}',src='en',dest = 'es').text.split('_')
        return [info_ability[1],info_ability[0],info_ability[2]]
    else:
        limitation = 'Sin limitaciones'
        info_ability = translator.translate(f'{ability}_{abilityname}',src='en',dest = 'es').text.split('_')
        return [info_ability[1],info_ability[0],limitation]

async def Animes(busqueda):
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
        Page (page: $page, perPage: $perPage) {
            media (id: $id, search: $search, type: ANIME) {
                id
                title {
                    romaji
                    english
                }
                description
                coverImage {
                        extraLarge
                }
                episodes
                duration
                status(version:2)
                averageScore
                isAdult
                format
                genres
                startDate{
                    year
                    month
                    day
                }
            }
        }
    }
    '''
    variables = {
        'search': busqueda,
        'page': 1,
        'perPage': 5
    }
    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json()

'''async def nombre():
    names = requests.get('http://www.tunevault.com/band-name-generator')
    soup = BeautifulSoup(names.content, 'html.parser')
    name = soup.findAll("span",limit = 5)
    return name[2].text'''

async def nombre():
    cadena = ''
    cantidad = rd.randint(1,4)
    names = requests.get(f'https://random-word-api.herokuapp.com/word?number={cantidad}&swear=1').json()
    for name in names:
        cadena += f'{name} '
    return cadena
    