import mesa_geo as mg
import random
import numpy
import sys

class VictoriaAgent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, atype=None):
        """Create new agent
        Args:
            id: Unique identifier for the agent.
            agent_type: Indicator for the agent's type (miner/farmer/trader)
        """
        super().__init__(unique_id, model, geometry, crs)
        # Gold location dictionary with elements unique_id:distance, path
        self.gold_loc = {}
        self.miners = 0
        self.resources = random.randint(20,200)
        self.gold_resource = 10
        self.nonminers = 80
        
        self.tell = 0
        self.atype = "Land"
        
    def set_type(self, atype):
        # Randomly create goldmines
        # n = random.random() 
        self.atype = atype

        if atype == "Gold":
            self.atype = "Gold"
            self.gold_loc['unique_id'] = 0
            self.miners = 20
            self.tell += 1
        # else:
        #     self.atype = "Miner"
                

    def step(self):
        # total population
        population = self.miners + self.nonminers

        # people move if the resources are less
        if self.resources < population:
            neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))

            possible_steps = [move for move in neighbors if (move.resources - (move.miners + move.nonminers)) > self.resources]

            if len(possible_steps) > 0:
                # moving people
                diff = population - self.resources
                people_moving = int(numpy.random.normal(loc=diff, scale=1))

                # every excess miner/nonminer moves to a random neighbor
                for _ in range(people_moving):
                    move_to = random.choice(possible_steps)
                    # miners are the first to move
                    if self.miners > 0:
                        self.miners -= 1
                    else: self.nonminers -= 1
                    move_to.nonminers += 1

        # Get neighbors
        neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))

        # Random movement of miners to agents
        if self.atype == "Miner":
            # If already next to goldmine don't move
            for n in neighbors:
                if n != self:
                    if n.atype == "Gold":
                        self.atype = "Settled"
                        return

            # Find possible movement
            possible_steps = [move for move in neighbors if move.atype == "Land"]
            # Move to a random neighboring land and change agent 
            if len(possible_steps) > 0:
                move_to = random.choice(possible_steps)
                move_to.atype = self.atype
                self.atype = "Land"
        elif self.atype == "Gold" and self.tell:
            # Tell neighbors I have gold
            for n in neighbors:
                n.gold_loc[self.unique_id] = 1
                n.tell += 1
                self.tell = 0
        elif self.atype == "Land":
            # Check if I can tell neighbors where gold is
            if self.tell == 2:
                for n in neighbors:
                    if n.tell == 0:
                        for k in self.gold_loc.keys():
                            n.gold_loc[k] = self.gold_loc[k] + 1
                            n.tell += 1
            elif self.tell == 1:
                self.tell += 1

    # advance function
    def advance(self):
        self.resources -= (self.miners + self.nonminers)
        if self.resources < 0 : self.resources = 0
        # self.resources += numpy.random.normal(loc=1, scale=0.2) * self.nonminers
        self.resources += numpy.random.normal(loc=1, scale=0.2) * self.nonminers + numpy.random.normal(loc=1.1, scale=0.2) * self.miners 


## Suggestion for moving agents as separate class:
class MovingAgent(VictoriaAgent):
    def __init__(self, agentproperties):
        ## To Do give agent a goal node, make it move every x steps
        pass
