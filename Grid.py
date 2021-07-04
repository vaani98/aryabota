#Create grid singleton class
#Take no of rows and columns as input( have default values )
#Then initialize that to random values
import random

class Grid:
    __instance = None
    @staticmethod
    def getInstance():
        # Static access method
        if Grid.__instance == None:
            Grid()
        return Grid.__instance

    def __init__(self, rows=10, columns=10):
        # Virtually private constructor
        if Grid.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Grid.__instance = self
        #self.total_value = 0
        self.rows = rows
        self.columns = columns

    def initialize_grid(self):
        self.grid = [[random.randint(0,10) for i in range(self.columns)] for j in range(self.rows)]
        print(self.grid)

    def getNumberOfCoins(self, x, y):
        if(x < self.rows and y < self.columns):
            '''print("Grid.py",self.grid[x][y])
            self.value = self.grid[x][y]
            print("Grid.py value",self.value)
            self.total_value = self.total_value + self.value
            print("Grid.py total value",self.total_value)'''
            return self.grid[x][y]
        else:
            raise Exception("Input values out of range")

    def getTotalValue(self):
        return self.total_value