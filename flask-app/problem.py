from re import sub
from typing import Dict, List
from grid import Grid
from coin_sweeper import CoinSweeper

class DictCompareWrapper:
    def __init__(self, json):
        self.json = json
    def __eq__(self, other):
        comp = True
        obj = self.json
        other_obj = other.json
        for key in obj.keys():
            if comp:
                if key not in other_obj.keys():
                    return False
                print(key)
                comp = comp and obj[key] == other_obj[key]
            else:
                return False
        return comp

class ListCompareWrapper:
    def __init__(self, array, compare_type):
        self.array = array
        self.compare_type = compare_type
    def __eq__(self, other):
        if self.compare_type == "lenient":
            comp = True
            for item in self.array:
                if comp:
                    comp = comp and item in other.array
                else:
                    return False
            return comp
        else:
            return self.array == other.array

def wrap(obj, compare_type):
    if isinstance(obj, dict):
        for key in obj.keys():
            obj[key] = wrap(obj[key], compare_type)
        obj = DictCompareWrapper(obj)
    elif isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = wrap(obj[i], compare_type)
        obj = ListCompareWrapper(obj, compare_type)
    return obj

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
        compare_type = self.answer["type"]
        reqd_ans = wrap(reqd_state, compare_type)
        ans = wrap(submitted_answer, compare_type)
        return reqd_ans == ans

    def check_answer(self, submitted_answer):
        succeeded = None
        message = "Not implemented yet!"
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
