import discord
from discord.ext import commands
import random as rd
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Catmi:EvhlQlj59QsRdEHx@botdata.olbzz.mongodb.net/test")

db = cluster["PlayerData"]
collections = db["StandInfo"]

dbg = cluster["GuildData"]
guilds = dbg["Guild"]

startInventory={'Flint':0,
                'Stick':0,
                'Feather':0,
                'Golden Flint':0,
                'Diamond Stick':0,
                'Golden Feather':0,
                'Arrow Stand':0,
                'Arrow Stand Requiem':0}

async def GuardarUsuario(user,atributos,stand,stats):
    myquery = { "_id": user.id }
    post = {"_id": user.id, "stand":stand,"atributo": atributos,"stats": stats,"inventario": startInventory}
    collections.insert_one(post)

async def Existe(user):
    myquery = { "_id": user.id }
    return collections.count_documents(myquery) != 0

async def GuardarStand(user,atributos,stand,stats,objeto):
    myquery = { "_id": user.id }
    collections.update_one(myquery, {"$set":{"stand":stand,"atributo": atributos,"stats": stats},"$inc":{f"inventario.{objeto}":-1}})

async def GuardarObjeto(user,objeto,cantidad):
    collections.update_one({ "_id": user.id }, {"$inc":{f"inventario.{objeto}":cantidad}})
    
async def GuardarInventario(user,inventario):
    collections.update_one({ "_id": user.id }, {"$set":{"inventario":inventario}})

async def GetObjetos(user):
    data = collections.find_one({ "_id": user.id})
    return data['inventario']

async def EnBatalla(retador,desafiado,EnBatalla):
    myquery = { "_id": retador.id,"_id": desafiado.id }
    collections.update_many({ "_id": retador.id,"_id": desafiado.id },{"$set":{"EnBatalla":EnBatalla}})

async def GetInfo(user):
    myquery = { "_id": user.id }
    if (collections.count_documents(myquery) != 0):
        result = collections.find_one(myquery)
        atributos = result['atributo']
        stand = result['stand']
        stats = result['stats']
        #EnBatalla = result['EnBatalla'] ,EnBatalla
        return [stand,atributos,stats]
    else:
        return None

async def GetInfoGuild(guild):
    myquery = { "_id": guild.id }
    result = guilds.find_one(myquery)
    prefix = result['prefix']
    channel = result['channel']
    #rol = result['rol']
    return [prefix,channel]

async def GuardarGuild(guild,prefix,channel):
    myquery = { "_id": guild.id }
    if (guilds.count_documents(myquery) == 0):
        post = {"_id": guild.id,"prefix": prefix, "channel": channel}
        guilds.insert_one(post)

async def SetPrefix(guild,prefix):
    guilds.update_one({"_id":guild.id}, {"$set":{"prefix": prefix}})

async def SetChannel(guild,channel):
    guilds.update_one({"_id":guild.id}, {"$set":{"channel": channel}})

'''async def SetRol(guild,rol):
    guilds.update_one({"_id":guild.id}, {"$set":{"rol": rol}})
'''
