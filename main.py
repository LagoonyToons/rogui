#a gui program for creating cards for rogue genesia's mod easy cards
from pstats import Stats
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import os
import sys

#add scripts folder to path, try to keep the directory clean
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/scripts")

import Card #Card object
import Card_Visualization as cv #Creates graphics and level up stats of a given card
from constants import * #constants such as stat names, rarities, etc


class CardMaker:
    def __init__(self, master):
        #gui setup
        self.master = master
        master.title("Card Maker")
        master.geometry("800x900")
        master.resizable(True, True)

        #data
        self.cards = [] #potentially load an entire folder of cards and move between them with a dropdown menu, but for now just one card
        self.modifier_row_start = 6
        self.modifier_row_end = self.modifier_row_start + ALLOCATED_MODIFIER_SLOTS
        self.modifier_row_next = self.modifier_row_start
        self.modifiers = []

        self.localization_row_start = self.modifier_row_end + 2
        self.localization_row_end = self.localization_row_start + ALLOCATED_LOCALIZATION_SLOTS
        self.localization_row_next = self.localization_row_start
        self.localizations = []

        #add save and load drop down menu
        self.menubar = tkinter.Menu(master)
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load", command=self.load)
        self.filemenu.add_command(label="Save", command=self.save)
        self.filemenu.add_command(label="Save as", command=self.save_as)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=master.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        master.config(menu=self.menubar)

        #widget for getting card name
        self.name_label = tkinter.Label(master, text="Card Name")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tkinter.Entry(master)
        self.name_entry.grid(row=0, column=1)

        #widget for getting card image path and button to open file dialog
        self.path_label = tkinter.Label(master, text="Image Path")
        self.path_label.grid(row=1, column=0)
        self.path_entry = tkinter.Entry(master)
        self.path_entry.grid(row=1, column=1)
        self.path_button = tkinter.Button(master, text="Browse", command=self.browse_image)
        self.path_button.grid(row=1, column=2)

        #widget for getting card rarity, dropdown menu using RARITIES list
        self.rarity_label = tkinter.Label(master, text="Rarity")
        self.rarity_label.grid(row=2, column=0)
        self.rarity_var = tkinter.StringVar(master)
        self.rarity_var.set(RARITIES[0])
        self.rarity_menu = tkinter.OptionMenu(master, self.rarity_var, *RARITIES)
        self.rarity_menu.grid(row=2, column=1)

        #widgets for getting card tags, multiple checkboxes using TAGS list
        self.tag_label = tkinter.Label(master, text="Tags")
        self.tag_label.grid(row=3, column=0)
        self.tag_var = []
        self.tag_check = []
        for i in range(len(TAGS)):
            self.tag_var.append(tkinter.IntVar())
            self.tag_check.append(tkinter.Checkbutton(master, text=TAGS[i], variable=self.tag_var[i]))
            self.tag_check[i].grid(row=3, column=i+1)

        #Widget for getting drop weight and levelupweight
        self.weight_label = tkinter.Label(master, text="Drop Weight")
        self.weight_label.grid(row=4, column=0)
        self.weight_entry = tkinter.Entry(master)
        self.weight_entry.grid(row=4, column=1)
        self.levelupweight_label = tkinter.Label(master, text="Level Up Weight")
        self.levelupweight_label.grid(row=4, column=2)
        self.levelupweight_entry = tkinter.Entry(master)
        self.levelupweight_entry.grid(row=4, column=3)

        #widget for getting maxlevel
        self.maxlevel_label = tkinter.Label(master, text="Max Level")
        self.maxlevel_label.grid(row=5, column=0)
        self.maxlevel_entry = tkinter.Entry(master)
        self.maxlevel_entry.grid(row=5, column=1)

        #widget for getting modifiers
        self.modifiers = []
        self.create_modifier()

        #widget button for creating a new modifier or removing the last one
        self.modifier_button = tkinter.Button(master, text="Add Modifier", command=self.create_modifier)
        self.modifier_button.grid(row=self.modifier_row_end+1, column=0)
        self.modifier_remove_button = tkinter.Button(master, text="Remove Modifier", command=self.remove_modifier)
        self.modifier_remove_button.grid(row=self.modifier_row_end+1, column=1)

        #widget for card localization
        self.localizations = []
        self.create_localization()

        #widget button for creating a new localization or removing the last one
        self.localization_button = tkinter.Button(master, text="Add Localization", command=self.create_localization)
        self.localization_button.grid(row=self.localization_row_end+1, column=0)
        self.localization_remove_button = tkinter.Button(master, text="Remove Localization", command=self.remove_localization)
        self.localization_remove_button.grid(row=self.localization_row_end+1, column=1)

        #widget canvas for displaying the card
        self.card_canvas = cv.Card_Visualization(self.make_card(), master)
        self.card_canvas.draw(False) #call this whenever the card is updated

        #create scrollbar of text on the righthand side which will be set later when the card preview is created
        self.scrollbar = tkinter.Scrollbar(master, orient=tkinter.VERTICAL)
        self.scrollbar.grid(row=999, column=2, columnspan=1, sticky=tkinter.N+tkinter.S)
        self.text = tkinter.Text(master, yscrollcommand=self.scrollbar.set)
        self.text.grid(row=999, column=2, columnspan=5, sticky=tkinter.N+tkinter.S)
        #reduce size of text widget
        self.text.config(width=50, height=20)
        self.scrollbar.config(command=self.text.yview)

        #make a button that calls self.card_canvas.draw() to update the card
        self.update_button = tkinter.Button(master, text="Update Card", command=self.draw_card)
        self.update_button.grid(row=self.localization_row_end+2, column=0)

    def draw_card(self):
        self.card_canvas.get_stats() #reset the card stats
        self.card_canvas.set_card(self.make_card())
        #modifier_text is a list of list of strings based on total levels and modifiers        
        modifier_text = self.card_canvas.get_modifier_text()
        self.text.delete(1.0, tkinter.END)
        for i in range(len(modifier_text)):
            if i >= self.card_canvas.card.maxlevel: #overlevel +1, +2
                self.text.insert(tkinter.END, "Level " + str(self.card_canvas.card.maxlevel) + "+" + str(i - self.card_canvas.card.maxlevel+1) + ":\n")
            else:
                self.text.insert(tkinter.END, "Level " + str(i+1) + ":\n")
            for j in range(len(modifier_text[i])):
                self.text.insert(tkinter.END, modifier_text[i][j] + "\n")
            self.text.insert(tkinter.END, "\n")
        self.card_canvas.draw(True)

    def create_modifier(self):
        #widget for getting modifier value, type(MODIFERTYPE), and stat(STATS)
        self.modifiers.append([])
        self.modifiers[-1].append(tkinter.Entry(self.master))
        self.modifiers[-1][0].grid(row=self.modifier_row_next, column=0)
        self.modifiers[-1].append(tkinter.StringVar(self.master))
        self.modifiers[-1][1].set(MODIFIERTYPE[0])
        self.modifiers[-1].append(tkinter.OptionMenu(self.master, self.modifiers[-1][1], *MODIFIERTYPE))
        self.modifiers[-1][2].grid(row=self.modifier_row_next, column=1)
        self.modifiers[-1].append(tkinter.StringVar(self.master))
        self.modifiers[-1][3].set(STATS[0])
        self.modifiers[-1].append(tkinter.OptionMenu(self.master, self.modifiers[-1][3], *STATS))
        self.modifiers[-1][4].grid(row=self.modifier_row_next, column=2)
        self.modifier_row_next += 1

    def remove_modifier(self):
        if len(self.modifiers) > 0:
            #remove the last modifier
            #remove value
            self.modifiers[-1][0].grid_forget()
            #remove type
            self.modifiers[-1][2].grid_forget()
            #remove stat
            self.modifiers[-1][4].grid_forget()

            #remove the modifier from the list
            self.modifiers.pop()
        
    def create_localization(self):
        #widget for getting localization name(NAMELOCALIZATION) and description
        self.localizations.append([])
        self.localizations[-1].append(tkinter.StringVar(self.master))
        self.localizations[-1][0].set(NAMELOCALIZATION[0])
        self.localizations[-1].append(tkinter.OptionMenu(self.master, self.localizations[-1][0], *NAMELOCALIZATION))
        self.localizations[-1][1].grid(row=self.localization_row_next, column=0)
        self.localizations[-1].append(tkinter.Entry(self.master))
        self.localizations[-1][2].grid(row=self.localization_row_next, column=1)

        self.localization_row_next += 1

    def remove_localization(self):
        if len(self.localizations) > 0:
            #remove the last localization
            #remove name
            self.localizations[-1][1].grid_forget()
            #remove description
            self.localizations[-1][2].grid_forget()

            #remove the localization from the list
            self.localizations.pop()
    
    def make_card(self):
        #get card name
        name = self.name_entry.get()

        #get card image path
        if self.path_entry.get() == "":
            image_path = "placeholder.png"
        else:
            image_path = self.path_entry.get()

        #get card rarity
        rarity = self.rarity_var.get()

        #get card tags
        tags = []
        for i in range(len(TAGS)):
            if self.tag_var[i].get() == 1:
                tags.append(TAGS[i])

        #get card drop weight
        if self.weight_entry.get() == "":
            weight = 0
        else:
            weight = float(self.weight_entry.get())

        #get card level up weight
        if self.levelupweight_entry.get() == "":
            levelupweight = 0
        else:
            levelupweight = float(self.levelupweight_entry.get())

        #get card max level
        if self.maxlevel_entry.get() == "":
            maxlevel = 0
        else:
            maxlevel = int(self.maxlevel_entry.get())

        #get card modifiers
        #"ModifierValue": "ModifierType": "Stat":
        modifiers = []
        for i in range(len(self.modifiers)):
            if self.modifiers[i][0].get() != "":
                modifiers.append({"ModifierValue": float(self.modifiers[i][0].get()), "ModifierType": self.modifiers[i][1].get(), "Stat": self.modifiers[i][3].get()})
            else:
                modifiers.append({"ModifierValue": 0, "ModifierType": self.modifiers[i][1].get(), "Stat": self.modifiers[i][3].get()})

        #get card localizations
        #language, name
        localizations = {}
        for i in range(len(self.localizations)):
            localizations[self.localizations[i][0].get()] = self.localizations[i][2].get()

        card = Card.Card()
        card.name = name
        card.path = image_path
        card.rarity = rarity
        card.tags = tags
        card.dropweight = weight
        card.levelupweight = levelupweight
        card.maxlevel = maxlevel
        card.modifiers = modifiers
        card.namelocalization = localizations

        return card
    
    def save(self):
        save_card(self.make_card())

    def load(self): #fill in the widgets with the card data
        #open file dialog
        filename = filedialog.askopenfilename(initialdir = "./data/",title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
        if filename != "":
            self.card = load_card(filename)
        #get card name
        self.name_entry.delete(0, tkinter.END)
        self.name_entry.insert(0, self.card.name)

        #get card image path
        self.path_entry.delete(0, tkinter.END)
        self.path_entry.insert(0, self.card.path)

        #get card rarity
        self.rarity_var.set(self.card.rarity)

        #get card tags
        for i in range(len(TAGS)):
            self.tag_var[i].set(0)
        for i in range(len(self.card.tags)):
            self.tag_var[TAGS.index(self.card.tags[i])].set(1)

        #get card drop weight
        self.weight_entry.delete(0, tkinter.END)
        self.weight_entry.insert(0, self.card.dropweight)

        #get card level up weight
        self.levelupweight_entry.delete(0, tkinter.END)
        self.levelupweight_entry.insert(0, self.card.levelupweight)

        #get card max level
        self.maxlevel_entry.delete(0, tkinter.END)
        self.maxlevel_entry.insert(0, self.card.maxlevel)

        #get card modifiers
        #"ModifierValue": "ModifierType": "Stat":
        for i in range(len(self.modifiers)):
            self.remove_modifier()
        for i in range(len(self.card.modifiers)):
            self.create_modifier()
            self.modifiers[-1][0].delete(0, tkinter.END)
            self.modifiers[-1][0].insert(0, self.card.modifiers[i]["ModifierValue"])
            self.modifiers[-1][1].set(self.card.modifiers[i]["ModifierType"])
            self.modifiers[-1][3].set(self.card.modifiers[i]["Stat"])

        #get card localizations
        #language, name
        for i in range(len(self.localizations)):
            try:
                self.remove_localization()
            except:
                pass
        if len(self.card.namelocalization) > 0:
            for i in range(len(self.card.namelocalization)):
                self.create_localization()
                self.localizations[-1][0].set(list(self.card.namelocalization.keys())[i])
                self.localizations[-1][2].delete(0, tkinter.END)
                self.localizations[-1][2].insert(0, list(self.card.namelocalization.values())[i])

    def save_as(self):
        #open file dialog
        filename = filedialog.asksaveasfilename(initialdir = "./data/",title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
        if filename != "":
            #remove everything before the last / including the /
            filename = filename[filename.rfind("/")+1:]
            #add .json if it's not there
            if filename[-5:] != ".json":
                filename += ".json"
            save_card(self.make_card(), filename)

    def browse_image(self):
        #open file dialog and get image
        filename = filedialog.askopenfilename(initialdir = "./assets/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
        if filename != "":
            #remove "assets/" from the path and everything before it
            filename = filename[filename.find("assets/"):]
            self.image_path = filename[7:]
            print(self.image_path)
            #fill in the image path
            self.path_entry.delete(0, tkinter.END)
            self.path_entry.insert(0, self.image_path)
        
def load_card(filename): #loads a SINGLE card from a json file
    card = Card.Card()
    f = open(filename, "r")
    f = json.load(f)

    data = f["Stats"][0] #remove top level of json

    card.name = data["Name"]
    card.path = data["TexturePath"]
    card.rarity = data["Rarity"]
    card.tags = data["Tags"]
    card.dropweight = data["DropWeight"]
    card.levelupweight = data["LevelUpWeight"]
    card.maxlevel = data["MaxLevel"]
    card.modifiers = data["Modifiers"]
    card.namelocalization = data["NameLocalization"]

    return card

def save_card(card, output_file=""): #Saves a SINGLE card into a json file
    save_path = "data/"
    if output_file == "":
        output_file = card.name + ".json"

    if card.path == "":
        card.path = "placeholder.png"
    
    data = {}
    data["Stats"] = []
    data["Stats"].append({
        "Name": card.name,
        "TexturePath": card.path,
        "Rarity": card.rarity,
        "Tags": card.tags,
        "DropWeight": card.dropweight,
        "LevelUpWeight": card.levelupweight,
        "MaxLevel": card.maxlevel,
        "Modifiers": card.modifiers,
        "NameLocalization": card.namelocalization
    })
    # print(card.namelocalization)

    with open(save_path + output_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    
if __name__ == '__main__':
    print("Starting Card Editor")
    root = tkinter.Tk()
    my_gui = CardMaker(root)
    root.mainloop()
        