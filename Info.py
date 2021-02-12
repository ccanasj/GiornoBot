import discord
from discord.ext import commands
import random as rd
import pymongo
from pymongo import MongoClient

cluster = MongoClient("MONGODB_URI")

db = cluster["PlayerData"]
collections = db["StandInfo"]

dbg = cluster["GuildData"]
guilds = dbg["Guild"]

async def Guardar(user,atributos,stand):
    myquery = { "_id": user.id }
    if (collections.count_documents(myquery) == 0):
        post = {"_id": user.id, "stand": stand, "stats": atributos}
        collections.insert_one(post)
    else:
        collections.update_one({"_id":user.id}, {"$set":{"stand":stand,"stats": atributos}})

async def GetInfo(user):
    myquery = { "_id": user.id }
    mydoc = collections.find(myquery)
    for result in mydoc:
        stand = result['stand']
        stats = result['stats']
    return [stand,stats]

async def GetInfoGuild(guild):
    myquery = { "_id": guild.id }
    mydoc = guilds.find(myquery)
    for result in mydoc:
        prefix = result['prefix']
        channel = result['channel']
        #rol = result['rol']
    return [prefix,channel]

async def GuardarGuild(guild,prefix,channel):
    myquery = { "_id": guild.id }
    if (guilds.count_documents(myquery) == 0):
        post = {"_id": guild.id,"prefix": prefix, "channel": channel}
        guilds.insert_one(post)
    else:
        guilds.update_one({"_id":guild.id}, {"$set":{"prefix": prefix, "channel": channel}})

async def SetPrefix(guild,prefix):
    guilds.update_one({"_id":guild.id}, {"$set":{"prefix": prefix}})

async def SetChannel(guild,channel):
    guilds.update_one({"_id":guild.id}, {"$set":{"channel": channel}})

'''async def SetRol(guild,rol):
    guilds.update_one({"_id":guild.id}, {"$set":{"rol": rol}})
'''
