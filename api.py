from random import randint
from aiohttp import ClientSession

session = ClientSession()


async def get_name():
    args = {'number': randint(1, 3)}
    async with session.get(f'https://random-word-api.herokuapp.com/word', params=args)as data:
        return ' '.join(await data.json())

async def get_cat_fact():
    async with session.get("https://some-random-api.ml/facts/cat") as data:
        return await data.json()

async def get_pokemon(id):
    async with session.get(f'https://pokeapi.co/api/v2/pokemon/{id}') as data:
        return await data.json()