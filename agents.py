import mesa_geo as mg
import random
import numpy
import sys

class VictoriaAgent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, atype=None):
        """
        Create Local Environment containing resources and agents.
        """
        super().__init__(unique_id, model, geometry, crs)
        # Gold location dictionary with elements unique_id:distance, path
        self.gold_loc = {}
        # initial agents to be created in this cell
        self.init_population = 10
        # amount of resources intially available to be collected
        self.resources = random.randint(20,50)
        # initial amount of gold available
        self.gold = 0
        # exchange rate i.e. how many resources one gold piece buys
        self.exchange = 5
        # func of gold and resources the people own and number of people
        self.economic_opportunity = 0 
        # list with agent dictionaries
        self.agents = []
        # number of agents, will be used to visualize population density
        self.population = len(self.agents)
        
        self.tell = 0
        self.atype = "Land"
       
        
################# Functions Alterring Cell Properties #########################


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
                
        
    def initialize_population(self):
        """
        create an intial population of agents within a cell (i.e. local environment)
        with a global agent ID to identify them as they move between cells.
        """
        for i in range(self.init_population):
            agent = {
                "id": agent_id,
                "miner": False,
                "destination": 0,
                "mining_ability": numpy.absolute(numpy.random.normal(5,2)),
                "gold": 0,
                "farming_ability": numpy.absolute(numpy.random.normal(5,2)),
                "resources": 10,
                "risk_factor": 0.5
            }
            self.agents.append(agent)
            # global agent_id += 1

    
    def calc_econ_opp(self):
        """
        function to calculate the economic opportunity in a cell as a function
        of the freely available resources, the resources owned by other agents
        and the number of agents in that cell.
        
        This value is used to determine where non miners move to.
        """
        total_wealth = 0
        
        for agent in self.agents:
            total_wealth += agent['resources'] + agent['gold']*self.exchange
            
        opp = (self.resources + total_wealth)/self.population
        self.economic_opportunity = opp
    
    
    def resource_regrowth(self):
        """
        Increase the resources of a cell by a randomly fluctuating amount
        """
        self.resoruces += random.randint(5,10)
    
    
    def information_spread(self):
        neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))

        if self.atype == "Gold" and self.tell:
            # Tell neighbors I have gold
            for n in neighbors:
                n.gold_loc[self.unique_id] = [1, self.gold, self.unique_id]
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


        
        
############### Functions Determining Actions of Indiviudals ##################


    def consume_resources(self):
        """
        Every agent within the cell consumes one of his resources and dies
        if there are no resources at his exposal
        """
        # keep count of agents that die to create new agents
        dead_agent_count = 0
        
        for agent in self.agents:
            
            if agent['resources'] > 0:
                agent['resources'] -= 1
            
            else:
                # delete agent
                dead_agent_count += 1
                
                
    def acquire_resources(self):
        """
        Individuals acquire resources based on their occupation (i.e. miners
        find gold and others farm free resources on land). These resources are
        extracted from the cell. Both Resources and Gold can't drop below 0'
        """
    
        for agent in self.agents:
            
            if agent['miner'] == False:
                resources_farmed = numpy.absolute(numpy.random.normal(agent["farming_ability"],1))
                if resources_farmed <= self.resources:
                    agent["resources"] += resources_farmed
                    self.resources -= resources_farmed
                
            elif agent['miner'] == True:
                gold_mined = numpy.absolute(numpy.random.normal(agent["mining_ability"],1))
                if gold_mined <= self.gold:
                    agent["gold"] += gold_mined
                    self.gold -= gold_mined
    
    def move(self):
        
        for agent in self.agents:
            
            if agent['miner'] == False:
                # check neighbouring cells for highest economic oppportunity 
                # move agent to that cell
            
            elif agent['miner'] == True:
                if agent['destination'] == #current cell:
                    #remain
                else:
                    # check next step towards gold mine
                    # move agent to that cell
        
            
            
####################### Functions Advancing the Model ########################

    def step(self):

        self.make_people() # should only be in the first step

        self.information_spread()
        
        # check if people become miners
        self.acquire_resources()
        self.resource_regrowth()
        self.calc_econ_opp()
        self.move() #very unfinished function
        # trade
        self.consume_resources() # unfinished function
        # replace dead agents randomly in new cells

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


############################## Old Functions #################################
    # def trade_and_move(self):
    #     for agent in self.agents:
    #         total_resources += agent["resource"]
    #         if agent["miner"]:
    #             if agent["resource"] < 2 and agent["gold"] > 0:
    #                 # trade 1 gold for 5 resources
    #                 for agent2 in self.agents:
    #                     if agent2["id"] != agent["id"] and agent2["resource"] > 20:
    #                         agent["resource"] += 5
    #                         agent["gold"] -= 1
    #                         agent2["resource"] -= 5
    #                         agent2["gold"] += 1
    #                         break
    #                     else : 
    #                         neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))
    #                         possible_steps = [move for move in neighbors if (move.resources > self.resources or move.trade_opp > self.trade_opp)]
    #                         if len(possible_steps) > 0:
    #                             move_to = random.choice(possible_steps)
    #                             move_to.agents.append(agent)
    #                             del agent

    #         # is trading factor dependent on total_resources?
    #         # maybe update trade opp ?

    #         if agent.miner == True and self.gold > 0:
    #             agent.gold += 1
    #             self.gold -=1
    #         elif agent.miner == False:
    #             agent.resources += 1
    #             self.resources -= 1


    # def random_move_miner(self):
    #     # Get neighbors
    #     neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))

    #     # Random movement of miners to agents
    #     if self.atype == "Miner":
    #         # If already next to goldmine don't move
    #         for n in neighbors:
    #             if n != self:
    #                 if n.atype == "Gold":
    #                     self.atype = "Settled"
    #                     return

    #         # Find possible movement
    #         possible_steps = [move for move in neighbors if move.atype == "Land"]
    #         # Move to a random neighboring land and change agent 
    #         if len(possible_steps) > 0:
    #             move_to = random.choice(possible_steps)
    #             move_to.atype = self.atype
    #             self.atype = "Land"

