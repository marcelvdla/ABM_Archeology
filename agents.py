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
        self.init_population = 10
        # self.miners = 0
        self.resources = random.randint(20,200)
        self.gold = 10
        self.trade_opp = 0 # func of gold and resources the people own

        # self.nonminers = 80

        global agent_id 
        agent_id = 0

        self.agents = []
        self.population = len(self.agents)
        
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
                
    def make_people(self):
        for i in range(self.init_population):
            agent = {
                "id": agent_id,
                "miner": False,
                "gold": 0,
                "resources": 10,
                "risk_factor": 0.5
            }
            self.agents.append(agent)
            # global agent_id += 1

    def trade_and_move(self):
        for agent in self.agents:
            total_resources += agent["resource"]
            if agent["miner"]:
                if agent["resource"] < 2 and agent["gold"] > 0:
                    # trade 1 gold for 5 resources
                    for agent2 in self.agents:
                        if agent2["id"] != agent["id"] and agent2["resource"] > 20:
                            agent["resource"] += 5
                            agent["gold"] -= 1
                            agent2["resource"] -= 5
                            agent2["gold"] += 1
                            break
                        else : 
                            neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))
                            possible_steps = [move for move in neighbors if (move.resources > self.resources or move.trade_opp > self.trade_opp)]
                            if len(possible_steps) > 0:
                                move_to = random.choice(possible_steps)
                                move_to.agents.append(agent)
                                del agent

            # is trading factor dependent on total_resources?
            # maybe update trade opp ?

            if agent.miner == True and self.gold > 0:
                agent.gold += 1
                self.gold -=1
            elif agent.miner == False:
                agent.resources += 1
                self.resources -= 1

    def information_spread(self):
        neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))

        if self.atype == "Gold" and self.tell:
            # Tell neighbors I have gold
            for n in neighbors:
                n.gold_loc[self.unique_id] = [1, self.gold_resource, self.unique_id]
                n.tell += 1
                self.tell = -1
        elif self.atype == "Land":
            # Check if I can tell neighbors where gold is
            if self.tell == 2:
                for n in neighbors:
                    if n.tell == 0:
                        n.tell += 1
                        for k in self.gold_loc.keys():
                            n.gold_loc[k] = [self.gold_loc[k][0] + 1, self.gold_loc[k][1], self.unique_id]

    def random_move_miner(self):
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

    def step(self):

        self.make_people(self) # should only be in the first step

        self.trade_and_move(self)

        self.information_spread()

    # advance function
    def advance(self):
        self.population = len(self.agents) # update population

        self.resources -= (self.miners + self.nonminers)
        if self.resources < 0 : self.resources = 0
        # self.resources += numpy.random.normal(loc=1, scale=0.2) * self.nonminers
        self.resources += numpy.random.normal(loc=1, scale=0.2) * self.nonminers + numpy.random.normal(loc=1.1, scale=0.2) * self.miners 

        if self.atype == "Land" and self.tell == 1:
            neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))
            for n in neighbors:
                if n.tell == 1:
                    n.tell += 1
                    


## Suggestion for moving agents as separate class:
class MovingAgent(VictoriaAgent):
    def __init__(self, agentproperties):
        ## To Do give agent a goal node, make it move every x steps
        pass
