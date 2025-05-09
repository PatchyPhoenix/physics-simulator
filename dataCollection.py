import pickle


class StoreList:
    def __init__(self):
        self.data = []

    def appendList(self, element):
        self.data.append(element)
    
    def updateList(self, element, position):
        self.data[position] = element

    def popList(self, position):
        self.data.pop(position)

    def removeList(self, element):
        self.data.remove(element)

    def dump(self, name):
        with open(f'data/{name}.dat', 'wb') as f:
            pickle.dump(self.data, f)


class StoreDict:
    def __init__(self):
        self.data = {}

    def addEntry(self, key, value):
        self.data[key] = value

    def removeEntry(self, key):
        self.data.pop(key)

    def updateEntry(self, key, value):
        self.data[key] = value

    def dump(self, name):

        with open(f'data/{name}.dat', 'wb') as f:
            pickle.dump(self.data, f)