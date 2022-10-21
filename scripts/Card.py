class Card:
    def __init__(self):
        self.name = "" #string
        self.path = "" #string
        self.rarity = "" #string
        self.tags = [] #list of strings
        self.dropweight = 0 #float
        self.levelupweight = 0 #float
        self.maxlevel = 0 #int
        
        self.modifiers = [] #list of dictionaries (3 values: stat, type, value)
        self.namelocalization = {} #dictionary of strings to strings (language to name)
    
    def print_info(self):
        print(self.name)
        print(self.path)
        print(self.rarity)
        print(self.tags)
        print(self.dropweight)
        print(self.levelupweight)
        print(self.maxlevel)
        print(self.modifiers)
        print(self.namelocalization)