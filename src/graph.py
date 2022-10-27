import matplotlib.pyplot as plt
from math import pi
from io import BytesIO
from .stand_manager import categories

angles = [n / float(6) * 2 * pi for n in range(6)]
angles += angles[:1]
x_angles = angles[:-1]


def graph(values, color):

    labels = [categories[values[0]], categories[values[1]], categories[values[2]],
              categories[values[3]], categories[values[4]], categories[values[5]]]

    values += values[:1]

    plt.figure(figsize=(3, 3))

    ax = plt.subplot(polar="True")
    ax.set_yticklabels([])
    ax.set_theta_offset(0.5)

    plt.ylim(0,5)

    plt.xticks(x_angles, labels)
   
    plt.polar(angles, values, color)
    plt.fill(angles, values, color, alpha=0.6)

    buf = BytesIO()
    plt.savefig(buf)
    plt.close()
    buf.seek(0)
    return buf
