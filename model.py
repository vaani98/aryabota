"""
CoinSweeper robot class
"""
class CoinSweeper:
    __instance = None
    @staticmethod
    def getInstance():
        # Static access method
        if CoinSweeper.__instance == None:
            CoinSweeper()
        return CoinSweeper.__instance

    def __init__(self):
        # Virtually private constructor
        if CoinSweeper.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CoinSweeper.__instance = self
        self.x = 1
        self.y = 1
        self.dir = "down"
    
    # utility
    def getDir(self):
        return self.dir

    def getDetails(self):
        return {
            "x": self.myX(),
            "y": self.myY(),
            "dir": self.getDir()
        }
    
    # ask
    def myX(self):
        return self.x
    
    def myY(self):
        return self.y
    
    # affect
    def move(self, steps):
        if self.dir == "up":
            self.y -= steps
        elif self.dir == "down":
            self.y += steps
        elif self.dir == "right":
            self.x += steps
        else:
            self.x -= steps
            
    def turnLeft(self):
        if self.dir == "up":
            self.dir = "left"
        elif self.dir == "down":
            self.dir = "right"
        elif self.dir == "right":
            self.dir = "up"
        else:
            self.dir = "down"
