""" the Singleton Grid, its attributes and state"""
import random

class Grid:
    """Properties:
        rows: number of rows, default 10
        columns: number of columns, default 10"""
    __instance = None
    @staticmethod
    def get_instance():
        """Static access method"""
        if Grid.__instance is None:
            Grid()
        return Grid.__instance

    def __init__(self, rows = 10, columns = 10):
        """Virtually private constructor"""
        # TODO This class gets initialised twice, check why? On hot reload it happens only once, but on starting server
        # it happens twice
        if Grid.__instance is not None:
            raise Exception("This class is a singleton!")
        Grid.__instance = self
        self.rows = rows
        self.columns = columns
        self.initialize_grid()

    def configure(self, rows, columns, coins_allocated = None):
        """Configure attributes"""
        self.rows = rows
        self.columns = columns
        if coins_allocated is not None:
            self.coins_allocated = coins_allocated

    def initialize_grid(self):
        """Initialise the grid with a random number of coins at each location"""
        self.coins_allocated = [[random.randint(0,10) for i in range(self.columns)] for j in range(self.rows)]
        # print(self.coins_allocated)

    def get_number_of_coins(self, row, column):
        print(row, column)
        """Get number of coins at a given position in the grid, ie, (row, column)"""
        if self.coins_allocated is not None:
            if row < self.rows and column < self.columns:
                return self.coins_allocated[row - 1][column - 1]
            raise Exception("This position does not exist on the grid!")
        # TODO decide whether to just return 0 instead?
        raise Exception("No coins are present in this grid!")
    # def get_total_value(self):
    #     """Get the total number of coins in the grid"""
    #     return self.total_value
