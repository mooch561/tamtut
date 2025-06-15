import os
import glob
import random
from PIL import ImageTk, Image
import tkinter as tk

# DEPRECATED: This file is no longer maintained and may be removed in future releases.

# Get the directory where this script is located, for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class TamLetter:
    type = 'c'
    pos = 1
    img = ""

    def __init__(self, t, p):
        self.type = t
        self.pos = p
        filename = os.path.join(BASE_DIR, "images", f"{self.type}{self.pos}.JPG")
        self.img = ImageTk.PhotoImage(Image.open(filename).resize((200, 200)))

class FlashCard:
    lrange = 0
    hrange = 0
    current = 0
    is_seq_or_rnd = 0

    def __init__(self, l, r):
        self.lrange = l
        self.hrange = r
        self.current = self.lrange

        print("flash card range of " + str(l) + " <-> " + str(r))

    def next_seq(self):
        current = self.current
        print(str(current), " is the current value. is_seq_or_rnd is ", str(self.is_seq_or_rnd) )
        if self.current >= self.hrange:
            self.current = self.lrange
        else:
            self.current = self.current + 1
        return(current)

    def next_rnd(self):
        self.current = random.randint(self.lrange, self.hrange)
        return(self.current)

    def next(self):
        if self.is_seq_or_rnd == 0:
            return(self.next_seq())
        else:
            return(self.next_rnd())

def get_letters(type):
    prefix = os.path.join(BASE_DIR, "images", f"{type}*.JPG")
    files = [x for x in glob.glob(prefix)]
    
    letter_objs = []
    for f in files:
        p = os.path.basename(f).replace(".JPG", "").replace(type, "")
        # print("adding " + str(p) + " of type " + type)
        letter_objs.append(TamLetter(type, p))
    
    return letter_objs

def butCallBack():
    global vLetters, cLetters, flashCard, is_v_or_c
    global canvas, currimg

    canvas.delete(currimg)

    letters = cLetters
    if is_v_or_c == 0:
        letters = vLetters

    pos = flashCard.next() 
    letter = letters[0]
    for x in letters:
        if int(x.pos) == int(pos):
            letter = x
            break

    print("position: " + str(pos) + " letter here is type: " + str(letter.type) +  " pos: " + str(letter.pos) )
    currimg = canvas.create_image(100, 100, anchor=tk.NW, image=letter.img)
    return 1

def radioSelCallBack():
    global is_v_or_c, is_seq_or_rand, flashCard, vLetters, cLetters, radio_var1, radio_var2

    if radio_var1.get() == 0:
        flashCard.hrange = len(vLetters)
        is_v_or_c = 0
    else:
        flashCard.hrange = len(cLetters)
        is_v_or_c = 1

    flashCard.is_seq_or_rnd = radio_var2.get()
    is_seq_or_rand = radio_var2.get()
    return 1

### main ###
currdir = os.getcwd()
print("current directory is", currdir)

top = tk.Tk()

canvas = tk.Canvas(top, width=400, height=300)
canvas.pack()
header_path = os.path.join(BASE_DIR, 'images', 'header.JPG')
img = ImageTk.PhotoImage(Image.open(header_path))
currimg = canvas.create_image(50, 50, anchor=tk.NW, image=img)

b = tk.Button(top, text = "Next Alphabet", command = butCallBack)
b.pack()

is_v_or_c = 1
is_seq_or_rand = 0
vLetters = get_letters('v')
cLetters = get_letters('c')
flashCard = FlashCard(1, len(cLetters))

radio_var1 = tk.IntVar()
radio_var2 = tk.IntVar()

r1 = tk.Radiobutton(top, text = "Vowels", variable = radio_var1, value = 0, command = radioSelCallBack)
r1.pack()
r1.deselect()
r2 = tk.Radiobutton(top, text = "Consonants", variable = radio_var1, value = 1, command = radioSelCallBack)
r2.pack()
r2.select()
r3 = tk.Radiobutton(top, text = "Sequence", variable = radio_var2, value = 0, command = radioSelCallBack)
r3.pack()
r3.select()
r4 = tk.Radiobutton(top, text = "Random", variable = radio_var2, value = 1, command = radioSelCallBack)
r4.pack()
r4.deselect()

top.mainloop()
