from tkinter import *
from tkinter import messagebox
from results import Winner, Loser
import random

black = "⚫"
white = '⚪' 

#CodeBreaker class
class CodeBreaker(Toplevel):
    def __init__(self, master, button, settings, all_colors):
        super().__init__(master)
        #Window Settings
        self.title("CodeBreaker")
        self.geometry("600x700")
        self.wm_iconbitmap("images/Letter_M_32.ico")
        self.config(bg="#040B6C")
        self.center_window()
        
        #Window parameters
        self.button = button
        self.settings = settings
        self.all_colors = all_colors
        self.column_len = self.settings['comb_len']
        self.button_colors = [None] * self.column_len
        self.buttons = []
        self.combs = []
       
        self.row = 1
        self.column_len = self.settings['comb_len']
        self.color_list = self.all_colors[:self.settings['color_count']] #The available colors for selection from the user.
        self.random_colors = [] #List with computer random color choice.
        
        #We generate the computer given code.
        self.random_colors = self.generate_computer_code()


        #----------In Window Game Begins Title---------
        self.text = Label(self, text="The Game Begins. Choose a Combination!", fg="yellow", bg="#040B6C", font=("Verdana", 18, "bold"))
        self.text.grid(row = 0, column=0, columnspan=self.column_len+1, pady=30)
        
        #Παραμετροποίηση των στηλών
        for i in range(self.column_len):
            self.columnconfigure(i, minsize=50, uniform="group", weight=1)
        
        #----Δημιουργία των γραμμών----
        self.create_row()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    #----Συνάρτηση για την δημιουργία των γραμμών και του κουμπιού της καταχώρησης----
    def create_row(self):
        
        for i in range((self.column_len)):
            button = Button(self, width=10,  bg="white",
                            command=lambda idx=i: self.open_choice_window(idx))
            self.buttons.append(button)
            button.grid(row=self.row, column=i, pady=10)
        
        #---This label configures to show the black and white pegss
        comb = Label(self, text="", width=10, bg="white")
        self.combs.append(comb)
        comb.grid(row=self.row, column=(self.column_len))
        
        #---Apply button   
        self.apply_button = Button(self, text="Commit", width=10, command=self.apply)
        self.apply_button.grid(row=(self.row +1), column=(self.column_len))
    
    #-----Color Selection Window Function---
    def open_choice_window(self, idx):
        self.buttons[idx].config(state='disabled')
        self.choice_window = Choice(
            self.buttons[idx], self.change_button_color, self.button_colors, self.settings, self.all_colors)

    #-----Change the color of the pressed button-----
    def change_button_color(self, button, color):
        idx = self.buttons.index(button)
        self.button_colors[idx] = color
        button.configure(bg=color)
    
    #----Removing the current apply button so the row can be reconfigured
    def remove_button(self):
        self.apply_button.grid_remove()
    
    #---Apply function-----
    def apply(self):
        if None in self.button_colors:
            messagebox.showerror("You didn't choose all the colors", "Please select all the available colors")
        else:
            
            result = self.result() #The current feedback
            check = self.check() #Chekc if code is solved

            if check == 1: #The code is solved
                self.combs[self.row - 1].config(text=result)
                for button in self.buttons:
                    button.config(state='disabled')
                
                self.remove_button() #Removing the apply button
                self.row += 1
                
                self.replay_button() #Creating the Replay label and button
                
                winner = Winner() #Winning GIF
                winner.after(4000, lambda: winner.destroy()) #Stops after 4 seconds
            
            elif check == 0: #Code has not been cracked in the number of tries required to do so.
                self.combs[self.row - 1].config(text=result) #Configures the feedback to the label.
                for button in self.buttons: #Disables the previous buttons
                    button.config(state='disabled')
                
                self.remove_button()
                self.row += 1
                
                #Show user the correct combination.
                correct = Label(
                    self, text="The Correct Combination is: ", fg="yellow", bg="#040B6C", font=("Verdana", 18, "bold"))
                correct.grid(row=self.row, column=0, columnspan=(self.column_len+1))
                for i in range(self.column_len):
                    label = Label(self, width=10, bg=self.random_colors[i])
                    label.grid(row=self.row+1, column=i, pady=10)
                
                self.row += 1
                self.replay_button()  # Creating the Replay label and button
                
                
                loser = Loser() #Loser GIF.
                loser.after(4000, lambda: loser.destroy()) #Stops after 4 seconds.
            # In any other case it shows the previous feedback and creates new row of buttons for the user
            # to select new colors for his next combination.
            else: 
                self.combs[self.row - 1].config(text=result)
                self.button_colors = [None] * self.column_len
                for button in self.buttons:
                    button.config(state='disabled')
                self.row += 1
                self.buttons = []
                self.remove_button()
                
                self.create_row()
    
    
    # -------Generates the random code checking if same color combinations are allowed.---------
    def generate_computer_code(self):
        color_count = self.settings['comb_len']
        if self.settings['same_color'] == 0:
            return random.sample(self.color_list, color_count)
        else:
            return random.choices(self.color_list, k=color_count)
    
    
    
    # ------Function that calculates the black and white pegs between the secret code and the guess.
    def guesscode(self, code, guess):
        """Tuple για υπολογισμο του σκορ"""
        black_pegs = sum([1 for i in range(len(guess)) if code[i] == guess[i]])
        white_pegs = sum([min(code.count(color), guess.count(color))
                           for color in self.all_colors[:self.settings['color_count']]]) - black_pegs

        return black_pegs, white_pegs
    
    #-----Function that sums the black and white pegs as emojis for better visualazation.
    def result(self):
        score = self.guesscode(self.button_colors, self.random_colors)
        result = []
        result += [black for i in range(score[0])]
        result += [white for i in range(score[1])]
        return ''.join(result)

    #----Function that checks if the User wins or loses.
    def check(self):
        score = self.guesscode(self.button_colors, self.random_colors)
        if score[0] == self.column_len:
            return 1
        elif score[0] != self.column_len and self.settings['tries'] == self.row:
            return 0
    
    #---Function that creates a label and the replay button.
    def replay_button(self):
        replay = Label(self, text="Do You Want to Play Again?",
                       fg="yellow", bg="#040B6C", font=("Verdana", 18, "bold"))
        replay.grid(row=self.row+1, column=0, columnspan=(self.column_len+1))

        replay_button = Button(self, text="Replay",
                               width=10, command=self.replay)
        replay_button.grid(row=self.row+2, column=self.column_len)
    
    #---Function so it opens up a new Codebreaker Window
    def replay(self):
        self.destroy()
        window = CodeBreaker(self.master, self.button, self.settings, self.all_colors)
            
    #---Function to change the pressed button state and main window's state   
    def on_close(self):
        self.button.config(state='normal')
        self.master.state(newstate='normal')
        self.destroy()

    #---Function to center the window.
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
    
#Color Selection Class
class Choice(Toplevel):
    def __init__(self, button, callback, button_colors, settings, all_colors):
        super().__init__()
        #Window settings
        self.title("Color Selection")
        self.geometry("500x250")
        self.wm_iconbitmap("images/Letter_M_32.ico")
        
        #Window parameters.
        self.all_colors = all_colors
        self.callback = callback
        self.button = button
        self.button_colors = button_colors
        self.settings = settings
        
        color_count = self.settings['color_count']
        
        self.title_text = Label(self, text="Please Choose a Color :)", font=("Verdana", 20, "bold"))
        self.title_text.grid(row=0, column=0, columnspan=color_count, pady=30, sticky="EW")
        
        for i in range(color_count):
            self.columnconfigure(i, minsize=50, uniform="group", weight=1)

        self.create_buttons(color_count)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    #---Function that creates the color buttons.   
    def create_buttons(self, n):
        for i in range(n):
            button = Button(self, width=5, bg=self.all_colors[i], command=lambda c=self.all_colors[i]: self.choose_color(c))
            button.grid(row=1, column=i)
    
    #---Function that return the color to the pressed button.       
    def choose_color(self, color):
        if self.settings['same_color'] == 0 and (color in self.button_colors):
            messagebox.showerror("Error", "This Color Already Exists!")
        else:
            self.callback(self.button, color)
            self.button.config(state="normal")
            self.destroy()

    #---Function to change the pressed button state.
    def on_close(self):
        self.button.config(state='normal')
        self.destroy()
    
    
