# MasterMind-Game
This is the classic MasterMind game. This game was part of my final University project for Python Programming language.
You can either be the CodeMaker which means that you create the combination and the Computer tries to solve the code using Knuth's algorithm with the min_max function
or you can be the CodeBreaker which means the computer creates the code and you try to solve it.


#--------------------------------------------------------------------------------------------------------------------------------------#
If you want to use pyinstaller to create a .exe file you need to use the lines of code below to the beginning of every file.

def resource(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
also change the "file path" e.g images, GIFs,  to the line below.
resource("file_path")
