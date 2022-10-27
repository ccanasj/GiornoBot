from pymongo import MongoClient
from TOKEN import MONGO

cluster = MongoClient(MONGO)

collections = cluster["GiornoBot"]["Players"]

start_inventory = {'Flint': 1000,
                   'Stick': 1000,
                   'Feather': 1000,
                   'String': 1000,
                   'Ruby': 1000,
                   'Diamond Stick': 1000,
                   'Golden Feather': 1000,
                   'Golden String': 1000,
                   'Meteorite': 1000,
                   'Stand Arrow': 1000,
                   'Stand Arrow Requiem': 1000,
                   'Skill Arrow': 1000,
                   'Stone Pendant': 1000
                   }


async def save_player(user, stand):
    post = {"_id": user, "stand": stand, "inventory": start_inventory, "part": 1}
    collections.insert_one(post)


async def exists(user):
    return collections.count_documents({"_id": user}) != 0


async def save_stand(user, stand, item):
    collections.update_one({"_id": user}, {"$set": {"stand": stand},
                                           "$inc": {f"inventory.{item}": -1}})


async def save_item(user, item, amount):
    collections.update_one({"_id": user}, {"$inc": {f"inventory.{item}": amount}})


async def save_inventory(user, inventory):
    collections.update_one({"_id": user}, {"$set": {"inventory": inventory}})


async def save_level(user, level):
    collections.update_one({"_id": user}, level)


async def get_inventory(user):
    result = collections.find_one({"_id": user}, {"_id": 0, "inventory": 1})
    return result['inventory'] if result else None


async def get_user(user):
    result = collections.find_one({"_id": user})
    return result

async def get_level(user):
    result = collections.find_one({"_id": user}, {"_id": 0, "stand": {"name": 1, "level": 1}})
    return result['stand'] if result else None

async def get_stand(user):
    result = collections.find_one({"_id": user}, {"_id": 0, "stand": 1})
    return result['stand'] if result else None


async def get_stats(user):
    result = collections.find_one({"_id": user}, {"_id": 0, "stand": {"name": 1, "attributes": 1}})
    return result['stand'] if result else None
