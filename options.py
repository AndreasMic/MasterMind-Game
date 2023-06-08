from tkinter import *
from tkinter import messagebox


class Options(Toplevel):
    def __init__(self, options_button, func, settings):
        super().__init__()
        #Window Settings
        self.title("Game Settings")
        self.geometry("500x500")
        self.resizable(False, False)
        self.wm_iconbitmap("images/Letter_M_32.ico")
        self.config(padx=50, pady=10, bg="#040B6C")
        self.button = options_button
        self.settings = settings
        
        self.func = func #Function that returns the settings to the main window.
        
        
        #-------In Window Title--------
        self.title_text= Label(self, text="Game Settings", font=("Verdana", 30, "bold"), fg="yellow", bg="#040B6C")
        self.title_text.grid(row=0, column=0, columnspan=2, pady=50, sticky="EW")
        
        #------Color count-------#
        self.color_count = Label(self, text="1. Color Count:", font=("Verdana", 16), fg="yellow", bg="#040B6C")
        self.color_count.grid(row=1, column=0, pady=10, sticky="W")
        
        self.var1 = StringVar(self)
        self.var1.set(self.settings['color_count']) 
        self.spinbox_n = Spinbox(self, from_=5, to=10, width=4, textvariable=self.var1, command=self.spinbox_color)
        self.spinbox_n.grid(row=1, column=1, pady=10, sticky="EW")
        
        #------Combination Length------#
        self.comb_len = Label(self, text="2. Combination Length:", font=("Verdana", 16), fg="yellow", bg="#040B6C")
        self.comb_len.grid(row=2, column=0, pady=10, sticky="W")

        self.var2 = StringVar(self)
        self.var2.set(self.settings['comb_len'])
        
        self.comb_box = Spinbox(self, from_=3, to=5, width=4, textvariable=self.var2, command=self.spinbox_comb)
        self.comb_box.grid(row=2, column=1, pady=10, sticky="EW")

        #-----Same Color?------#
        self.same_color = Label(self, text="3. Same Color in the Combination?", font=(
            "Verdana", 16), fg="yellow", bg="#040B6C")
        self.same_color.grid(row=3, column=0, pady=10, sticky="W")
        
        self.check_state = IntVar()
        self.check_state.set(self.settings['same_color'])
        
        self.checkbutton = Checkbutton(self, variable=self.check_state)
        self.checkbutton.grid(row=3, column=1)
        
        #-----Number of tries-------#
        self.tries = Label(self, text="4. Number of Tries", font=(
            "Verdana", 16), fg="yellow", bg="#040b6c")
        self.tries.grid(row=4, column=0, pady=10, sticky="W")
        
        self.var3 = StringVar()
        self.var3.set(self.settings['tries'])
        self.spinbox_tries = Spinbox(self, from_=5, to=10, width=4, textvariable=self.var3, command=self.spinbox_tries_num)
        self.spinbox_tries.grid(row=4, column=1, pady=10, sticky="EW")
        
        ##----Apply settings-----##
        self.apply = Button(self, width=5, height=1, text="Apply Settings", font=("Arial", 14, "bold"), command=self.apply)
        self.apply.grid(row=5, column=0, columnspan=2, pady=10, sticky="NSEW")
        

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    #Widgets' functions    
    
    def checked_state(self):
        return self.check_state.get()
    
    def spinbox_comb(self):
        self.keep = self.comb_box.get()
        return self.keep
    
    def spinbox_color(self):
        return self.spinbox_n.get()
    
    def spinbox_tries_num(self):
        return self.spinbox_tries.get()
    
    #Function to apply the settings.
    #Pops a messagebox if any value is not permitted.
    def apply(self):
        try:
            color_count_val = int(self.spinbox_n.get())
            comb_len_val = int(self.comb_box.get())
            same_color_val = int(self.check_state.get())
            tries_val = int(self.spinbox_tries.get())
        except ValueError:
            messagebox.showerror("Wrong Entry", "Please insert a number")
        else:
            if color_count_val > 10 or color_count_val < 5:
                messagebox.showerror("Wrong Entry", "Please insert a number from 5 to 10")
            elif comb_len_val > 5 or comb_len_val < 3:
                messagebox.showerror("Wrong Entry", "Please insert combination length from 3 to 5")
            elif tries_val > 10 or tries_val < 5:
                messagebox.showerror("Wrong Entry", "Please insert number of tries from 5 to 10")
            else:
                self.on_close()
                settings = {
                    "color_count": color_count_val,
                    "comb_len": comb_len_val,
                    "same_color": same_color_val,
                    "tries": tries_val
                }
                
                self.func(settings)
        
    #Function to destroy window and change the pressed button back to normal state.
    def on_close(self):
        self.button.config(state='normal')
        self.destroy()


        
     