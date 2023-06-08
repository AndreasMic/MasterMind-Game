import itertools
from tkinter import messagebox

black = "⚫"
white = '⚪'

#AI class to solve the Mastermind code from the user.
class AI_algor:
    def __init__(self, settings, buttons_colors, all_colors):
        #Class settings.
        self.guess_list = [] #List to store the AI guesses
        self.score_list = [] #List to store the AI scores
        self.settings = settings
        self.all_colors = all_colors
        self.color_list = buttons_colors
        self.comb_len = self.settings["comb_len"]
        self.color_count = self.settings["color_count"]

        
        #Converting the color combination into a number combination so it is more efficient to work with knuth algorithm
        #and it's concept. It is also faster in difficult combinations and larger color counts.
        #Every color corresponds to its index from the all_colors list. 
        answer = [self.all_colors.index(color) for color in self.color_list]
        
        #Mastermind Function.
        self.Mastermind(self.color_count, self.comb_len, answer)
        

    #Function that returns the first guess the AI will use.
    def first_guess(self):
        if self.comb_len == 3:
            return (0, 0, 1)
        elif self.comb_len == 4:
            return (0, 0, 1, 1)
        else:
            return (0, 0, 1, 1, 1)


    #Mastermind Function 
    def Mastermind(self, colors_num, num, code):
        # List with every possible combination.
        total_codes = list(itertools.product(range(colors_num), repeat=num))
        #List with all the available combinations.
        knuth_codes = total_codes
        #List with all the remaining choices.
        possible_codes = total_codes
        #User's Combination.
        mastermind_code = code
        
        #First Guess
        guess = self.first_guess()
        #Variable that stores the feedback between the AI's guess and the User's code.
        feedback = self.guesscode(guess, mastermind_code)

        #Append the guess and feedback to the corresponding list.
        self.guess_list.append(guess)
        self.score_list.append(self.result(feedback))
        
        
        #While loop until AI cracks the code.
        while feedback != (num, 0):
            
            #Insert into the list every code that gives the same feedback as the result between the AI's current guess and the User's code.
            knuth_codes = [ code for code in knuth_codes if self.guesscode(code, guess) == feedback]
            
            
            if not knuth_codes:
                messagebox.showerror("Error", "Something went wrong")
                return 0
            #The AI's next code.
            code = self.get_code(knuth_codes, possible_codes)
            #The new feedback.
            feedback = self.guesscode(mastermind_code, code)
            #Append the guess and feedback to the corresponding list.
            self.guess_list.append(code)
            self.score_list.append(self.result(feedback))
            
            #The new guess
            guess = code
            
        
    #This function checks and returns the next code. 
    #If any of the codes of knuth_codes list exists in the guess_codes we pick the first we can find.
    #If not we pick the first code from the guess_codes list
    def get_guess_code_from_list(self, knuth_codes, guess_codes):
        for code in knuth_codes:
            if code in guess_codes:
                return code
            
        return guess_codes[0]

    ##This function returns the code from the previous function after it is processed from the min_max function
    #and removed from the possible_codes list. (so it can't be picked again)
    def get_code(self, knuth_codes, possible_codes): 
        guess_codes = self.min_max(knuth_codes, possible_codes)
        code = self.get_guess_code_from_list(knuth_codes, guess_codes)
        possible_codes.remove(code)
        return code

    #This function returns how many black and white pegs exists between  a code and a guess.
    def guesscode(self, code, guess):
        black_pegs = sum([1 for i in range(len(guess)) if code[i] == guess[i]])
        white_pegs = sum([min(code.count(i), guess.count(i))
                        for i in range(self.color_count)]) - black_pegs

        return black_pegs, white_pegs

    #This is the min_max function.
    def min_max(self, knuth_codes, possible_codes):
        #List with all the possible feedbacks from every code comparison.
        all_feedbacks = [score for score in itertools.product(
                    range(self.comb_len + 1), repeat=2) if (sum(score) <= self.comb_len)]
        
        #In this dictionary we insert every code's maximum value. 
        # key(code) : value(maximum value)
        scores = {}
        for code in possible_codes:
            times_found = { score : 0 for score in all_feedbacks} #Initialization of every feedback.
            scores[code] = 0 #Initialization of code's value.
            #In this for loop we check every possible combination with the remaining combinations
            #and for every feedback we add +1 to the corresponding dictionary value.
            for code_to_crack in knuth_codes:
                feedback = self.guesscode(code_to_crack, code)
                times_found[feedback] += 1
            #When the loop is over we find the maximum value from the times_found dictionary and put it in the scores dictionary
            #for every code.    
            scores[code] = max(times_found.values())
            
        #When both loops are over we keep the minimum value from scores dictionary.    
        minimum = min(scores.values())
        
        guess_codes = []#List with all the next possible AI's guesses.
        #In this list we append every code that has score equal to the minimum score.        
        for code in possible_codes:
            if scores[code] == minimum:
                guess_codes.append(code)
                
        return guess_codes
    #This function returns the black and white emojis so we can store them in the score_list and
    #finally use them in the AI_window for better visualazition of the result.
    def result(self, score):
        result = []
        result += [black for i in range(score[0])]
        result += [white for i in range(score[1])]
        return ''.join(result)