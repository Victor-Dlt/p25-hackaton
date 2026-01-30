# C est la liste des clients 

from matplotlib import pyplot as plt
from matplotlib import animation as an

## création figure 

fig = plt.figure()

## clients
for client in C :
    x = client.coord_x
    y = client.coord_y
    plt.plot(x,y)

plt.show()
