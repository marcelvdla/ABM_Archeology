import warnings
warnings.filterwarnings("ignore")
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa import Model
import random

from agents import PeopleAgent, Sugar

class Sugarscape(Model):
    def __init__(self, width, height, N):
        self.no_agents = N
        self.width = width
        self.height = height
        self.gold_patches = 5
        self.grid = MultiGrid(width=width, height=height, torus=True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            {"PeopleAgent": lambda m: m.schedule.get_agent_count(),
            "Sugar": lambda m: m.schedule.get_agent_count()}
        )
        agent_id = 0

        # create gold patches
        for i in range(self.gold_patches):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            # random gold value
            gold_val = random.randint(1, 10)
            gold = Sugar(agent_id, (x,y), self, gold_val)
            agent_id += 1
            self.grid.place_agent(gold, (x,y))
            self.schedule.add(gold)
        
        # create people agent
        for i in range(self.no_agents):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            init_gold = random.randint(1,4)
            vision = 1 # random.randrange(1,4)
            people = PeopleAgent(agent_id, (x,y), self, False, init_gold, vision)
            agent_id += 1
            self.grid.place_agent(people, (x,y))
            self.schedule.add(people)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self) # need data ?

    def run_model(self, step_count=20):
        '''
        Method that runs the model for a specific amount of steps.
        '''
        for i in range(step_count):
            self.step()

    # ------------------------------------------------------------
