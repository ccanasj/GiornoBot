import matplotlib.pyplot as plt
import pandas as pd 
from math import pi
import random as rd
from io import BytesIO
from PIL import Image,ImageFont,ImageDraw

font = ImageFont.truetype('./Fuentes/SF Fedora.ttf', 35)
categories = ['Vel','Poder','Potencia',' Pre','Duracion','Rango']
N = len(categories)

angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

def Fondo(nombre, nick, data):
    values = [rd.randint(1,5) for i in range(6)]
    values += values[:1]

    fig = plt.figure(figsize=(5,5),constrained_layout = True)
    ax = plt.subplot(polar = "True")

    plt.xticks(angles[:-1],categories)
    ax.tick_params(axis='x', colors='white', labelsize=22,grid_color = 'black')
    plt.yticks([1,2,3,4,5], size = 5)
    plt.ylim(0,5)

    plt.polar(angles,values,'red')
    plt.fill(angles,values,'r',alpha = 0.3)

    buf = BytesIO()
    plt.savefig(buf, bbox_inches='tight',transparent = True)
    buf.seek(0)
    Stats = Image.open(buf)
    Back = Image.open('./Imagenes/2-1.jpg')
    Back.paste(Stats,(5,220), mask=Stats)
    draw = ImageDraw.Draw(Back)
    draw.text((50,130),nick,(231,228,217),font = font)
    draw.text((730,610),nombre,(231,228,217),font = font)
    pfp = Image.open(data)
    Back.paste(pfp,(750,115))
    Back.save('./Imagenes/XD.jpg')
    buf.close()


