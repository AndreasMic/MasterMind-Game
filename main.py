from tkinter import *
from PIL import Image
from codemaker import CodeMaker
from codebreaker import CodeBreaker
from options import Options


class Master(Tk):
    def __init__(self):
        super().__init__()
        #Main window settings
        self.geometry("540x763")
        self.title("Mastermind")
        self.wm_iconbitmap("images/Letter_M_32.ico")
        self.resizable(False, False) 
        self.center_window() #Function so the window is always center no matter the user's screen.
        #Default settings
        self.defaul_settings = {
            "color_count": 6,
            "comb_len": 4,
            "same_color": 0,
            "tries": 10
            }
        self.all_colors = ["blue", "red", "green", "yellow", "orange",
                           "brown", "purple", "lightblue", "limegreen", "black"] #All the available colors.
        self.settings = {} #Dictionary with the user's settings        


        #-----------Create gif ------------
        gifImage = "./images/giphy2.gif"
        
        self.canvas = Canvas(width=540, height=763, bg='lightgreen', highlightthickness=0)
        self.openImage = Image.open(gifImage)
        self.frames = self.openImage.n_frames
        self.imageObject = [PhotoImage(
            file=gifImage, format=f"gif -index {i}") for i in range(self.frames)]
        self.count = 0
        showAnimation = None
        self.img = self.canvas.create_image(270, 380, image="")
        self.canvas.grid(rowspan=3, columnspan=2)
        self.animation(self.count)

        #--------Game Title------------------
        self.mastermind = self.canvas.create_text(
            270, 45, text="Mastermind", fill="#FFEA20", font=("Verdana", 35, "italic bold"))
        
        #--------Welcome Label----------
        self.welcome_text = self.canvas.create_text(
            270, 250, text="Welcome to the Mastermind game!", fill='yellow', font=('Verdana', 20, 'bold'))
        
        #--------Choose Character Label--------
        self.choose_text = self.canvas.create_text(
            270, 500, text="Choose a characer!", fill='#D36B00', font=('Arial', 18, 'italic'))
        
        #--------Create Options Button-----  
        self.options_image = PhotoImage(file="images/option2.png")
        self.options_button = Button(self, image=self.options_image, command=self.options_com)
        self.options_button.grid(row=0, column=1, sticky="NE") 

        #-------Create CodeMaker Button---------
        self.maker_button = Button(self, width=20, height=2, text="C o d e M a k e r", bg="lightgreen", font=("Arial", 14, "italic"), command=self.codem)
        self.maker_button.grid(row=2, column=0, sticky='EW')
        
        #-------Create CodeBreaker Button-------
        self.breaker_button = Button(self, width=20, height=2, text="C o d e B r e a k e r", bg='red', font=("Arial", 14, "italic"), command=self.codeb)
        self.breaker_button.grid(row=2, column=1, sticky="EW")

    
    #--------Function for maker_button-----    
    def codem(self):
        self.state(newstate="iconic")
        self.maker_button.config(state='disabled')
        if self.settings:
            self.codemaker_window = CodeMaker(self, self.maker_button, self.settings, self.all_colors)
        else:
            self.codemaker_window = CodeMaker(self, self.maker_button, self.defaul_settings, self.all_colors)
    
    
    #-------Function for breaker_button-----
    def codeb(self):
        self.state(newstate="iconic")
        self.breaker_button.config(state='disabled')
        if self.settings:
            self.codebreaker_window = CodeBreaker(self, self.breaker_button, self.settings, self.all_colors)
        else:
            self.codebreaker_window = CodeBreaker(self, self.breaker_button, self.defaul_settings, self.all_colors)
    
    #--------Function to update the user's settings-----
    def update(self, settings):
            self.settings = settings

    #--------Function for options button--------
    def options_com(self):
        self.options_button.config(state='disabled')
        if self.settings:
            self.options_window = Options(self.options_button, self.update, self.settings)
        else:
            self.options_window = Options(self.options_button, self.update, self.defaul_settings)
        
    #-------Function to animate the gif image-----  
    def animation(self, count):
        global showAnimation
        newImage = self.imageObject[count]
        self.canvas.itemconfig(self.img, image=newImage)
        count += 1
        if count == self.frames:
            count = 0
        showAnimation = self.after(
            50, lambda: self.animation(count))
    
    #-------Function to center the window at every screen------#
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.geometry(f"{width}x{height}+{x}+{y}")
    
       
#------Main Programm-----       
if __name__ == "__main__":
    main_program = Master()
    main_program.mainloop()