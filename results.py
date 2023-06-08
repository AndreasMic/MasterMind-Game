from tkinter import *
from PIL import Image, ImageTk
from itertools import count, cycle

#Winning GIF Class
class Winner(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("You win!")
        self.geometry("640x480")
        self.wm_iconbitmap("images/Letter_M_32.ico")
        self.gif= ImageLabel(self)
        self.gif.pack()
        self.gif.load('images/winner.gif')

#Losing GIF Class.
class Loser(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("You Lost!")
        self.geometry("384x290")
        self.wm_iconbitmap("images/Letter_M_32.ico")
        self.gif= ImageLabel(self)
        self.gif.pack()
        self.gif.load('images/loser.gif')


#Gif inside a label Class
class ImageLabel(Label):
    #Load GIF Image    
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy())) 
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames) 

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None
    
    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)
