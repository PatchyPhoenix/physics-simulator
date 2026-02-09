import pickle
import matplotlib.pyplot as plt
import numpy as np

x = None
y = None

name = input("enter name: ")

with open(f'data/{name}.dat', 'rb') as f:
    data = pickle.load(f)
    l1 = []
    l2 = []
    for x, y in data.items():
        l1.append(x)   
        l2.append(y)
    y = np.array(l2)
    x = np.array(l1)
    plt.plot(x, y)

    if name.startswith('t'):
        plt.xlabel("Time (s)")
    else:
        plt.xlabel("Position (X)")

    if name.endswith("g"):
       plt.ylabel("g")

    elif name.endswith("v"):
       plt.ylabel("Velocity")

    elif name.endswith("a"):
       plt.ylabel("Acceleration")

    elif name.endswith("ee"):
        plt.ylabel("Relative Error (Energy)")

    elif name.endswith("e"):
       plt.ylabel("Energy")

    elif name.endswith("sp"):
        plt.ylabel("Softening Parameter")

    #plt.ylim(-1, 1)

    plt.show()

"""with open('data/1g.dat', 'rb') as f:
    data = pickle.load(f)
    l1 = []
    l2 = []
    for x in data:
      l1.append(x)   
      l2.append(data[x])
    x = np.array(l1)
    y = np.array(l2)
    plt.plot(x, y)
    plt.show()

with open('data/1a.dat', 'rb') as f:
    data = pickle.load(f)
    l1 = []
    l2 = []
    for x in data:
      l1.append(x)   
      l2.append(data[x][0])
    x = np.array(l1)
    y = np.array(l2)
    plt.plot(x, y)
    plt.show()"""