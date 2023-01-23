import warnings
warnings.filterwarnings("ignore")
from mesa import Agent
import random


class Sugar(Agent):
    def __init__(self, unique_id, model, pos, amount = 0):
        super().__init__(unique_id, model)
        self.pos = pos
        self.amount = amount


class PeopleAgent(Agent):
    def __init__(self, unique_id, pos, model, moore=False, sugar=0, vision=0):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.sugar = sugar
        self.vision = vision
    
    def amo_sugar(self, pos):
        cells = self.model.grid.get_cell_list_contents([pos])
        for agent in cells:
            print("agent-----", type(agent))
            if type(agent) is Sugar:
                print("------", type(agent), "--", agent.amount, "-------")
                return agent.amount
            else: return 0

    def move(self):
        # Get neighborhood within vision
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center = False, radius=self.vision)

        # look for max sugar
        max_sugar = max( self.amo_sugar(pos) for pos in possible_steps)
        possible_moves = [
            pos for pos in possible_steps if self.amo_sugar(pos) == max_sugar
        ]
        self.model.grid.move_agent(self, random.choice(possible_moves))

    def take(self):
        gold_patch = self.amo_sugar(self.pos)
        self.sugar += gold_patch.amount
        gold_patch.amount = 0
        self.model.grid.remove_agent(gold_patch)

    def step(self):
        self.move()
        self.take()

    # When do you remove agent - people ?????

