"""the Singleton CoinSweeper robot, its attributes and state"""
from Grid import Grid

grid = Grid.get_instance()

class CoinSweeper:
    """CoinSweeper robot class
    Properties:
        row: current row (1-indexed)
        column: current column (1-indexed)
        dir: current direction the robot is facing (can be up, left, down, right)
    """
    __instance = None
    @staticmethod
    def get_instance():
        """Static access method"""
        if CoinSweeper.__instance is None:
            CoinSweeper()
        return CoinSweeper.__instance

    def __init__(self):
        """Virtually private constructor"""
        if CoinSweeper.__instance is not None:
            raise Exception("This class is a singleton!")
        CoinSweeper.__instance = self
        self.row = 1
        self.column = 1
        self.dir = "down"
        self.trail = []
        self.append_current_position_to_trail()

    def configure(self, row, column, dir):
        """Configure attributes"""
        self.row = row
        self.column = column
        self.dir = dir
        self.trail.clear()
        self.append_current_position_to_trail()

    # utility
    def get_dir(self):
        """Get current direction the CoinSweeper robot is facing"""
        return self.dir

    def get_state(self):
        """Get current state of the CoinSweeper robot's position wrapped in a dictionary"""
        return {
            "row": self.row,
            "column": self.column,
            "dir": self.dir,
            "trail": self.trail
        }

    def append_current_position_to_trail(self):
        self.trail.append({
            "row": self.row,
            "column": self.column
        })

    # ask
    def my_row(self):
        """Get current row of the CoinSweeper robot"""
        return self.row

    def my_column(self):
        """Get current column of the CoinSweeper robot"""
        return self.column

    # affect
    def move(self, steps):
        """Move the CoinSweeper robot in the direction in which it is facing
        steps: specified number of steps to move it by"""
        state = grid.get_state()
        #print(state)
        obstacle_message = "There's an obstacle, cannot move ahead"
        boundary_message = "This position does not exist on the grid!"
        if self.dir == "up":
            if(self.row - steps >= 1):
                for i in range(self.row,self.row-steps,-1):
                    self.row -= 1
                    if({'row': self.row, 'column': self.column} in state['obstacles']):
                        return [False, obstacle_message]
            else:
                return [False, boundary_message]
        elif self.dir == "down":
            if(self.row + steps <= grid.rows ):
                for i in range(self.row,self.row+steps):
                    self.row += 1
                    if({'row': self.row, 'column': self.column} in state['obstacles']):
                        return [False, obstacle_message]
            else:
                return [False, boundary_message]
        elif self.dir == "right":
            if(self.column + steps <= grid.columns ):
                for i in range(self.column,self.column+steps):
                    self.column += 1
                    if({'row': self.row, 'column': self.column} in state['obstacles']):
                        return [False, obstacle_message]
            else:
                message = "This position does not exist on the grid!"
                return [False, boundary_message]
        elif self.dir == "left":
            if(self.column - steps >= 1 ):
                for i in range(self.column,self.column-steps,-1):
                    self.column -= 1
                    if({'row': self.row, 'column': self.column} in state['obstacles']):
                       return [False, obstacle_message]
            else:
                return [False, boundary_message]
        self.append_current_position_to_trail()
        return [True, "moved!"]

    def turn_left(self):
        """Turn the CoinSweeper robot to its left"""
        if self.dir == "up":
            self.dir = "left"
        elif self.dir == "down":
            self.dir = "right"
        elif self.dir == "right":
            self.dir = "up"
        elif self.dir == "left":
            self.dir = "down"
            
    def turn_right(self):
        """Turn the CoinSweeper robot to its right"""
        if self.dir == "up":
            self.dir = "right"
        elif self.dir == "down":
            self.dir = "left"
        elif self.dir == "right":
            self.dir = "down"
        elif self.dir == "left":
            self.dir = "up"
