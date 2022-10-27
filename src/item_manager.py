from random import choice, choices
from .stand_manager import generate_stand, generate_stand_requiem, get_skill, set_attributes, types
from .stand_string import skill_to_string, stand_to_string


items_recipes = {'Stand Arrow': ['Meteorite', 'Flint', 'String', 'Stick', 'Feather'],
                 'Stand Arrow Requiem': ['Meteorite', 'Ruby', 'Golden String', 'Diamond Stick', 'Golden Feather'],
                 'Skill Arrow': ['Meteorite', 'Stick', 'Feather'],
                 'Stone Pendant': ['Meteorite', 'Flint', 'Ruby', 'Golden String']}

trades = {'Ruby': 'Flint', 'Diamond Stick': 'Stick',
          'Golden Feather': 'Feather', 'Golden String': 'String'}

emojis = {"Flint": '<:Flint:1029565447240175616>',
          "Stick": '<:Stick:811814638983315497>',
          "Feather": '<:Feather:811814638630993920>',
          "String": '<:String:827029745333567568>',
          "Ruby": '<:Ruby:829034495118147604>',
          "Diamond Stick": '<:DiamondStick:811840519352221706>',
          "Golden Feather": '<:GoldenFeather:811840519113015297>',
          "Golden String": '<:GoldenString:827029761992687666>',
          "Meteorite": '<:Meteor:1029570265362997268>',
          "Stand Arrow": '<:StandArrow:811814640744529922>',
          "Stand Arrow Requiem": '<:StandArrowRequiem:814300958484856864>',
          "Skill Arrow": '<:SkillArrow:818650694033866752>',
          "Stone Pendant": '<:StonePendant:818653936448831563>',
          "Stone Mask": '<:StoneMask:814297491021103115>',
          "Red Stone Of Aja": '<:RedStoneOfAja:814298072473272322>',
          "Stone Mask With The Red Stone": '<:StoneMaskWithTheRedStone:814311812068802601>'}

items_values = ["Nothing",
                "Flint",
                "Stick",
                "Feather",
                "String",
                "Ruby",
                "Diamond Stick",
                "Golden Feather",
                "Golden String",
                "Meteorite"]

items_probability = [0.11, 0.13, 0.13, 0.13,
                     0.13, 0.03, 0.03, 0.03, 0.03, 0.25]

amounts = [1, 2, 3]
amounts_probability = [0.85, 0.10, 0.05]

places = ('un templo', 'una tumba', 'E L - S O T A N O', 'una piramide', 'la mansion Joestar', 'la guarida de DIO',
          'la casa de Kira', 'la iglesia', 'el Hipódromo', 'la casa blanca', 'unas ruinas', 'en algun lugar desconocido',
          '|| <:sadCat:783953550296088646> su corazón <:sadCat:783953550296088646> ||', 'en algun lugar')

stars = ['⭐', '⭐⭐', '⭐⭐⭐']


def generate_items():
    item = choices(population=items_values, weights=items_probability)[0]
    result = {'item': item, 'amount': 0}
    if item != "Nothing":
        result['amount'] = choices(
            population=amounts, weights=amounts_probability)[0]
        result['text'] = f'Exploraste {choice(places)} y Encontraste: **x{result["amount"]} {item}** {emojis[item]}'
        return result
    result['text'] = f'Exploraste {choice(places)} pero no encontraste nada <:weynooo:799854983100629022>'
    return result


def inventory_to_string(inventory):
    inventory_string = "\n".join(
        [f'**- {emojis[key]} *{key}* : {value}**' for key, value in inventory.items()])
    return inventory_string


def recipe_to_string(embed):
    for key, items in items_recipes.items():
        embed.add_field(
            name=f'『 {key} 』', value=f"**{' + '.join([emojis[item] for item in items])} = {emojis[key]}**", inline=False)
    for key, item in trades.items():
        embed.add_field(
            name=f'『 {key} 』', value=f"**x10 {emojis[item]} = {emojis[key]}**", inline=False)


def crafting(inventory, creation, amount):
    for item in items_recipes[creation]:
        if inventory[item] >= amount:
            inventory[item] -= amount
        else:
            return False
    inventory[creation] = inventory.get(creation, 0) + amount
    return True


def trading(inventory, material, amount):
    if inventory[trades[material]] >= 10 * amount:
        inventory[trades[material]] -= 10 * amount
        inventory[material] = inventory.get(material, 0) + amount
        return True
    else:
        return False


async def use(stand, item, embed):
    if item.startswith('Stand'):
        if item == 'Stand Arrow':
            stand = await generate_stand()
            image = 'https://media1.tenor.com/images/36d30efef07ecae295d330588618fc8b/tenor.gif?itemid=14490536'

        elif item == 'Stand Arrow Requiem':
            stand = await generate_stand_requiem()
            image = 'https://i.imgur.com/nt4GeCq.gif'

        stats, attributes = stand_to_string(stand)
        embed.description = f"{stars[stand['star'] - 1]} ***『 {stand['name']} 』***"
        embed.add_field(name="Atributos", value=attributes)
        embed.add_field(name="ㅤㅤ", value="ㅤㅤ")
        embed.add_field(name="Estadisticas", value=stats)
        embed.add_field(name=f"__{stand['skill']['name']}__",
                        value=skill_to_string(stand['skill']))
        embed.add_field(name="ㅤㅤ", value="ㅤㅤ")
        embed.add_field(name='Tipo Stand', value=f'***{types[stand["type"]]}***')
        embed.set_thumbnail(url=image)
    elif item == 'Skill Arrow':
        stand['skill'] = get_skill(stand['attributes'][2], stand['skill'])
        embed.add_field(name=f"¡Has obtenido la habilidad __{stand['skill']['name']}__!",
                        value=skill_to_string(stand['skill']))
    elif item == 'Stone Pendant':
        result = set_attributes(stand)
        if result:
            embed.add_field(name=f"¡Has mejora el atributo __{result['attribute_name']}__!",
                            value=f"**{result['old_attribute']} ---> {result['new_attribute']}**")
        else: 
            return 'Ya no puedes subir mas los atributos con **Stone Pendant**'
    return stand
