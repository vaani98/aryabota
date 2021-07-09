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

    def configure(self, rows, columns, coins = None, coins_per_position = None):
        """Configure attributes"""
        self.rows = rows
        self.columns = columns
        if coins is not None:
            self.coins = coins
        if coins_per_position is not None:
            self.coins_per_position = coins_per_position

    def initialize_grid(self):
        """Initialise the grid with a random number of coins at each location"""
        self.coins_per_position = [[random.randint(0,10) for i in range(self.columns)] for j in range(self.rows)]

    def get_number_of_coins(self, row, column):
        print(row, column)
        """Get number of coins at a given position in the grid, ie, (row, column)"""
        if self.coins_per_position is not None:
            if row < self.rows and column < self.columns:
                return self.coins_per_position[row - 1][column - 1]
            raise Exception("This position does not exist on the grid!")
        # TODO decide whether to just return 0 instead?
        raise Exception("No coins are present in this grid!")
    
    def get_state(self):
        if self.__instance:
            return {
                "rows": self.rows,
                "columns": self.columns,
                "coins": self.coins,
                "coins_per_position": self.coins_per_position
            }
        return {}
