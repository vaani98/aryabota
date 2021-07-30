from re import sub
from grid import Grid
from coin_sweeper import CoinSweeper
import copy

""" the Singleton Problem, its attributes and state"""
class Problem:
    __instance = None
    @staticmethod
    def get_instance():
        """Static access method"""
        if Problem.__instance is None:
            Problem()
        return Problem.__instance

    def __init__(self):
        """Virtually private constructor"""
        # TODO This class gets initialised twice, check why? On hot reload it happens only once, but on starting server
        # it happens twice
        if Problem.__instance is not None:
            raise Exception("This class is a singleton!")
        Problem.__instance = self

    def get_type(self):
        return self.type

    def configure(self, type, statement, answer):
        """Configure attributes"""
        self.type = type
        self.statement = statement
        self.answer = answer

    def compare_states(self, submitted_answer):
        reqd_state = self.answer["state"]
        print("comparing states!!")
        print(submitted_answer)
        print(reqd_state)
        try:
            for key in reqd_state["coin_sweeper"]:
                if reqd_state["coin_sweeper"][key] != submitted_answer["coin_sweeper"][key]:
                    return False
        except KeyError as e:
            print(e)
            return False
        return True

    def check_answer(self, submitted_answer):
        succeeded = None
        message = "Not implemented yet!"
        print('! in check answer', self, submitted_answer)
        if self.type == "value_match":
            succeeded = str(self.answer["value"]).lower() == str(submitted_answer["text_answer"]).lower()
        elif self.type == "state_match":
            succeeded = self.compare_states(submitted_answer)
        if succeeded: 
            message = 'Correct answer!'
        else: 
            message = 'Wrong answer, please try again'
        return {
            "succeeded": succeeded,
            "message": message
        }

    def get_initial_state(self):
        grid = Grid.get_instance()
        bot = CoinSweeper.get_instance()
        grid_state = grid.get_state()
        coin_sweeper_state = bot.get_state()
        grid_state.update(coin_sweeper_state)
        grid_state["type"] = self.type
        if self.type == "state_match":
            if "coin_sweeper" in self.answer["state"]:
                grid_state["home"] = self.answer["state"]["coin_sweeper"]
        return grid_state
