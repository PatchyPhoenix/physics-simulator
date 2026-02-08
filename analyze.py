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
    for x in data:
        l1.append(x)   
        if name.endswith("g"):
            l2.append(data[x])
        else:
            l2.append(data[x][0])
    with open("have fun da.txt", "w") as d:
        d.write(str(l2))
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