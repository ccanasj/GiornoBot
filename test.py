import matplotlib.pyplot as plt
import pandas as pd 
from math import pi
import random as rd
from io import BytesIO
from PIL import Image,ImageFont,ImageDraw

font = ImageFont.truetype('./Fuentes/SF Fedora.ttf', 45)
categorias = {0:'E',1:'D',2:'C',3:'B',4:'A',5:'S',}
#categories = ['Vel','Poder','Potencia',' Pre','Duracion','Rango']
N = 6
fondo1 = open('./Imagenes/BackGround1.jpg','rb')
fondo2 = open('./Imagenes/BackGround2.jpg','rb')
fondo3 = open('./Imagenes/BackGround3.jpg','rb')

fondos = [fondo1,fondo2,fondo3]

angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

def Fondo(nombre, nick, data, values):
    
    categories = [categorias[values[0]],categorias[values[1]],categorias[values[2]],categorias[values[3]],categorias[values[4]],categorias[values[5]]]

    values += values[:1]
    fig = plt.figure(figsize=(5,5),constrained_layout = True)
    ax = plt.subplot(polar = "True")
    
    plt.xticks(angles[:-1],categories)

    ax.tick_params(axis='x', colors='white', labelsize=33,grid_color = 'black')
    plt.yticks([0,1,2,3,4,5], size = 6)
    plt.ylim(0,5)

    plt.polar(angles,values,'red')
    plt.fill(angles,values,'r',alpha = 0.3)

    buf = BytesIO()
    plt.savefig(buf, bbox_inches='tight',transparent = True)
    buf.seek(0)
    Stats = Image.open(buf)
    a = rd.choice(fondos) 
    Back = Image.open(a)
    Back.paste(Stats,(5,200), mask=Stats)
    draw = ImageDraw.Draw(Back)
    draw.text((65,130),nick,(231,228,217),font = font)
    draw.text((700,610),nombre,(231,228,217),font = font)
    pfp = Image.open(data)
    try:
        Back.paste(pfp,(800,180),mask = pfp)
    except:
        Back.paste(pfp,(800,180))
    buf.close()
    return Back


