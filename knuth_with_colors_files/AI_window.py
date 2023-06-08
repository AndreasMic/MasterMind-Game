
from tkinter import *
from results import Winner, Loser


class AI(Toplevel):
    def __init__(self, master, settings, guesses, scores, all_colors, button_colors):
        super().__init__(master)
        #Window Settings
        self.title("Computer Solver")
        self.geometry("660x700")
        self.wm_iconbitmap("images/Letter_M_32.ico")
        self.config(bg="#040B6C")
        self.center_window()
        
        #Window Parameters.
        self.settings = settings
        self.correct_answer = button_colors #User's Code.
        self.all_colors = all_colors #List with all colors(Not necessary. Storing this list so we don't have to change the main.py)
        self.col_length = self.settings['comb_len'] #Combination length.
        self.row=1 #The current row(for grid system purposes)
        self.guess_list = guesses # List with all combinations the AI used to solve the code
        self.score_list = scores # List with all the scores(feedbacks).

        
        #---------------Computer play Label----------------#
        self.text_label = Label(self, text="The Computer plays", font=("Verdana", 30, "bold"), fg="yellow", bg="#040B6C")
        self.text_label.grid(row=0, column=0, columnspan=self.col_length+1, pady=30)
        
        #--------------Column Configuration-------#
        for i in range(self.col_length):
            self.columnconfigure(i, minsize=50, uniform="group", weight=1)

        # Variable to store the result (if the computer solved the code in the required tries).
        status = self.win_or_lose()
        
        # Limit variable gets the number of rows that will be created in the window.
        if status == 1:
            limit = len(self.guess_list)
        else:
            limit = self.settings['tries']
        
        #Creates every row after 1 second for better visualization of the steps.
        self.after(1000, lambda: self.create_rows(
            self.guess_list, self.score_list, 0, limit, status))
    
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        
    #---Function to check if the AI solved the code in the required tries--    
    def win_or_lose(self):
        if len(self.guess_list) > self.settings['tries']:
            return 0
        else:
            return 1
       
    
    #------Function to visualize in the window the results---     
    def create_rows(self, guess, res, counter, limit, status):
        if counter < limit:
            guess = self.guess_list[counter]
            res = self.score_list[counter]
            for i in range(self.col_length):
                label = Label(self, width=10, bg=guess[i]) #Creates the Label with the corresponding color.
                label.grid(row=self.row, column=i, pady=10)
            
            label_score = Label(self, width=10, text=res)
            label_score.grid(row=self.row, column=self.col_length)   
            self.row += 1
        elif counter == limit: #When we reach the limit we present the desired result.
            
            
            winning_label = Label(self, text=f"The Computer Wins!" if status == 1 else "The Computer loses!",
                                    fg="yellow", bg="#040B6C", font=("Verdana", 18, "bold"))
            winning_label.grid(row=self.row, column=0, columnspan=(self.col_length+1))
            self.row += 1
            
            correct = Label(
                self, text="The correct combination is: ", fg="yellow", bg="#040B6C", font=("Verdana", 18, "bold"))
            correct.grid(row=self.row, column=0,
                         columnspan=(self.col_length+1))
            for i in range(self.col_length):
                label = Label(self, width=10, bg=self.correct_answer[i])
                label.grid(row=self.row+1, column=i, pady=10)

            if status == 1:                
                winner = Winner()
                winner.after(4000, lambda: winner.destroy())
            else:
                loser = Loser()
                loser.after(4000, lambda: loser.destroy())
            
        counter += 1
        self.after(1000, lambda: self.create_rows(
            guess, self.score_list, counter, limit, status))
        
    #---Function to change the pressed button's state---
    def on_close(self):
        self.master.state(newstate='normal')
        self.destroy()

    #---Function to center the window
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.update()
