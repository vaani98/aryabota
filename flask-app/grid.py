""" the Singleton Grid, its attributes and state"""
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

    def __init__(self):
        """Virtually private constructor"""
        # TODO This class gets initialised twice, check why? On hot reload it happens only once, but on starting server
        # it happens twice
        if Grid.__instance is not None:
            raise Exception("This class is a singleton!")
        Grid.__instance = self

    def configure(self, rows, columns, coins = None, coins_per_position = None, obstacles = None, obstacles_per_position = None, type = None, answer = None):
        """Configure attributes"""
        self.rows = rows
        self.columns = columns
        if type is not None: 
            self.type = type
        if answer is not None: 
            self.answer = answer
        if coins is not None:
            self.coins = coins
        if coins_per_position is not None:
            self.coins_per_position = coins_per_position
        if obstacles is not None:
            self.obstacles = obstacles
        if obstacles_per_position is not None:
            self.obstacles_per_position = obstacles_per_position

    def get_number_of_coins(self, row, column):
        print(row, column)
        """Get number of coins at a given position in the grid, ie, (row, column)"""
        if self.coins_per_position is not None:
            if row < self.rows and column < self.columns:
                return self.coins_per_position[row - 1][column - 1]
            raise Exception("This position does not exist on the grid!")
        # TODO decide whether to just return 0 instead?
        raise Exception("No coins are present in this grid!")

    def check_answer(self, submitted_answer): 
        succeeded = None
        message = "not implemented yet!"
        if self.type == "value_match":
            succeeded = str(self.answer).lower() == str(submitted_answer).lower()
            if succeeded: 
                message = 'Correct answer!'
            else: 
                message = 'Wrong answer, please try again'
        return {
            "succeeded": succeeded,
            "message": message
        }

    def get_state(self):
        if self.__instance:
            return {
                "rows": self.rows,
                "columns": self.columns,
                "coins": self.coins,
                "coins_per_position": self.coins_per_position,
                "obstacles": self.obstacles,
                "obstacles_per_position": self.obstacles_per_position,
                "type": self.type,
            }
        return {}