import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import asyncio
translator = Translator()

async def get_info():
    abilitys = requests.get('https://powerlisting.fandom.com/wiki/Special:Random')
    names = requests.get('https://www.coolgenerator.com/album-name-generator')
    soup1 = BeautifulSoup(abilitys.content, 'html.parser')
    soup2 = BeautifulSoup(names.content, 'html.parser')
    Standname = soup2.find('b').text
    abilityname = soup1.title.string.split('|')[0]
    ability = soup1.find_all('p')[1].text
    Limitaciones = soup1.get_text()
    if 'Limitations' in Limitaciones:
        limitation = Limitaciones.split('Limitations')[2].split('\n')[1]
        info_ability = translator.translate(f'{ability}_{abilityname}_{limitation}',src='en',dest = 'es').text.split('_')
        return [Standname,info_ability[1],info_ability[0],info_ability[2]]
    else:
        limitation = 'Sin limitaciones'
        info_ability = translator.translate(f'{ability}_{abilityname}',src='en',dest = 'es').text.split('_')
        return [Standname,info_ability[1],info_ability[0],limitation]

def Animes(busqueda):
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (id: $id, search: $search, type: ANIME) {
                id
                title {
                    romaji
                    english
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

def Anime2(busqueda):
    url = f"https://api.jikan.moe/v3/search/anime?q={busqueda}&limit=3"

    response = requests.get(url)
    print(response.json())
    return response.json()

