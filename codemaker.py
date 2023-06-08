from tkinter import *
from tkinter import messagebox
from AI_window import AI
from knuth_algor import AI_algor

#CodeMaker Class
class CodeMaker(Toplevel):
    def __init__(self, master,  button, settings, all_colors):
        super().__init__(master)
        #Window Settings
        self.title("CodeMaker")
        self.geometry("600x500")
        self.wm_iconbitmap("images/Letter_M_32.ico")
        self.config(padx=50, pady=20, bg="#040B6C")
        self.center_window()
        
        #Window parameters
        self.button = button #CodeMaker Button(Disable, enable)
        self.buttons=[] #List with all the created buttons so we can modify them.
        self.all_colors = all_colors #List with all the available colors
        self.settings = settings #Dictionary with game settings
        col_width = self.settings['comb_len'] #Variable to save the number of columns and buttons that will be created.
        self.button_colors = [None] * col_width #Initialize color button list.
        
        #-------In-Widnow Title----------
        self.title_text= Label(self, text="Mastermind", font=("Verdana", 30, "bold"), fg="yellow", bg="#040B6C")
        self.title_text.grid(row=0, column=0, columnspan=col_width, pady=50, sticky="EW")
        
        #-------Window Text-----------------
        self.color_text = Label(self, text="You are the Code Maker", font=(
            "Arial", 20, "italic"), fg="yellow", bg="#040B6C")
        self.color_text.grid(row=1, column=0, columnspan=col_width, pady=50, sticky='EW')
        
        #-------Configuration for all the columns------
        for i in range(col_width):
            self.columnconfigure(i, minsize=50, uniform="group", weight=1)
        self.create_buttons(col_width)
        
        #-------configure color line------
        self.rowconfigure(2, weight=1)
        
        #-------Apply Combination Button when player is ready-----
        self.apply_button = Button(self,  text="Apply Combination", command=self.apply)
        self.apply_button.grid(row=3, column=(col_width-2), columnspan=2, sticky='E')
        
        #--------Close Window Action-----
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    #-----Function that creates all the buttons----
    def create_buttons(self, col_width):
        for i in range(col_width):
            button = Button(self, width=10, bg='white', command=lambda idx = i: self.open_choice_window(idx))
            self.buttons.append(button)
            button.grid(row=2, column=i)
    
    #-----Function for the Color Selection Window---        
    def open_choice_window(self, idx):
        self.buttons[idx].config(state='disabled')
        self.choice_window = Choice(self.buttons[idx], self.change_button_color, self.button_colors, self.settings, self.all_colors)
        
    #-----Function that changes the color of the pressed button-----
    def change_button_color(self, button, color):
        idx = self.buttons.index(button)
        self.button_colors[idx] = color
        button.configure(bg=color)
    
    #-----Function to apply the combination and create the AI window where the computer solves the code.
    def apply(self):
        if None in self.button_colors:
            messagebox.showerror("You did not choose all the colors", "Please choose every available color!")
        else:
            self.button.config(state='normal')
            ai =AI_algor(self.settings, self.button_colors, self.all_colors)
            ai_window = AI(self.master, self.settings, ai.guess_list, ai.score_list, self.all_colors, self.button_colors)
            self.destroy()
    
    #------Function to change the pressed button state and the main window reappears
    def on_close(self):
        self.button.config(state='normal')
        self.master.state(newstate='normal')
        self.destroy()
    
    #----Function to center the window---   
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")


#Color Selection Window Class.
class Choice(Toplevel):
    def __init__(self, button, callback, button_colors, settings, all_colors):
        super().__init__()
        #Window Settings
        self.title("Color Selection")
        self.geometry("500x250")
        self.wm_iconbitmap("images/Letter_M_32.ico")
        
        #Window Parameters
        self.all_colors = all_colors 
        self.callback = callback 
        self.button = button 
        self.button_colors = button_colors 
        self.settings = settings 
        
        color_count = self.settings['color_count']
        
        #-------In Window Title------#
        self.title_text = Label(self, text="Please Choose a Color :)", font=("Verdana", 20, "bold"))
        self.title_text.grid(row=0, column=0, columnspan=color_count, pady=30, sticky="EW")
        
        for i in range(color_count):
            self.columnconfigure(i, minsize=50, uniform="group", weight=1)

        #---Creates the buttons--------#
        self.create_buttons(color_count)
        
        #---Close window action---------#
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    #----Function that creates the color buttons--------#
    def create_buttons(self, n):
        for i in range(n):
            button = Button(self, width=5, bg=self.all_colors[i], command=lambda c=self.all_colors[i]: self.choose_color(c))
            button.grid(row=1, column=i)
    
    #---Function that we pick the color--------#       
    def choose_color(self, color):
        if int(self.settings['same_color']) == 0 and (color in self.button_colors):
            messagebox.showerror("Error", "This Color Already Exists!")
        else:
            self.callback(self.button, color)
            self.button.config(state="normal")
            self.destroy()

    #---Function to change the pressed button state------#
    def on_close(self):
        self.button.config(state='normal')
        self.destroy()

        