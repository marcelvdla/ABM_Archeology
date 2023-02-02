import mesa_geo as mg
import numpy
import random

class VictoriaAgent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, atype=None):
        """
        Create Local Environment containing resources and agents.
        """
        super().__init__(unique_id, model, geometry, crs)
        self.model = model
        
        # Gold location dictionary with elements unique_id, distance, path
        self.gold_loc = {}
        
        # amount of resources intially available to be collected
        self.resources = random.randint(20,50)
        
        # initial amount of gold available
        self.gold = 0
        
        # exchange rate i.e. how many resources one gold piece buys
        self.exchange = 5
        
        # func of gold and resources the people own and number of people
        self.economic_opportunity = 0 
        
        # dictionary with agent dictionaries
        self.agents = {}
        
        # number of agents, will be used to visualize population density
        self.population = 3
        
        self.number_of_miners = 0
        
        self.avg_probability = 0
        
        self.tell = 0
        
        self.resource_stats = []
        
        self.gold_stats = []
        
        self.atype = "Land"

        self.moving_agent = dict()

        self.number_of_trades = 0

    def save_step(self):

        data = (
            self.unique_id,
            self.population,
            self.number_of_miners,
            self.avg_probability,
            self.gold_stats,
            self.resource_stats,
            self.economic_opportunity,
            self.resources,
            self.number_of_trades
        )
        self.model.writer.writerow(data)
       
        
################# Functions Alterring Cell Properties #########################


    def set_type(self, atype, gold_size = 0):
        self.atype = atype

        if atype == "Gold":
            self.atype = "Gold"
            self.gold_loc['unique_id'] = [0, gold_size, self.unique_id]
            self.tell += 1
    
    def get_neighbors(self, id=1):
        if id:
            return [n.unique_id for n in list(self.model.space.get_neighbors_within_distance(self, distance=2)) if n.unique_id != self.unique_id]
        else:
            return list(self.model.space.get_neighbors_within_distance(self, distance=2))
    

    def calc_econ_opp(self):
        """
        function to calculate the economic opportunity in a cell as a function
        of the freely available resources, the resources owned by other agents
        and the number of agents in that cell.
        
        This value is used to determine where non miners move to.
        """
        total_wealth = 0
        
        # iterate over agents
        for id in self.agents:
            agent = self.agents[id]
            total_wealth += agent['resources'] + agent['gold']*self.exchange
            
        ## ADD ONE SMOOTHING TO AVOID DIVISION BY ZERO
        opp = (self.resources + total_wealth)/(self.population +1)
        self.economic_opportunity = opp
        return opp
    
    
    def resource_regrowth(self):
        """
        Increase the resources of a cell by a randomly fluctuating amount
        """
        self.resources += random.randint(5,10)
    
    
    def information_spread_step(self, stoch=0.5):
        neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))

        nn_neighbors = [n for n in neighbors if self.unique_id not in list(n.gold_loc.keys())]

        if self.atype == "Gold" and self.tell == 1:
            # Tell neighbors I have gold
            for n in nn_neighbors:
                if n != self and random.random() < stoch:
                    n.gold_loc[self.unique_id] = [1, self.gold, self.unique_id]
                    n.tell += 1
            
            # Check if all neighbors know
            if len([n for n in neighbors if self.unique_id not in list(n.gold_loc.keys())]) == 0:
                self.tell = -1
        elif self.atype == "Land" and self.tell == 2:
            # Check if I can tell neighbors where gold is
            for n in nn_neighbors:
                if n.tell == 0 and random.random() < stoch:
                    n.tell += 1
                    for k in self.gold_loc.keys():
                        if k not in list(n.gold_loc.keys()):
                            distance = self.gold_loc[k][0] + 1
                            gold_size = self.gold_loc[k][1]
                            n.gold_loc[k] = [distance, gold_size, self.unique_id]

    def information_spread_advance(self):
        neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))

        if self.atype == "Land" and self.tell == 1:
            neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))
            knows = list(self.gold_loc.keys())
            for n in neighbors:
                n_knows = list(n.gold_loc.keys())
                if n.tell == 1 and not any(k in n_knows for k in knows):
                    n.tell += 1
            self.tell += 1
        elif self.atype == "Land" and self.tell == 2:
            ## Check for shorter route in neighbors
            for n in neighbors:
                for k in self.gold_loc.keys():
                    # If neighbor is goldmine
                    if n.unique_id == k:
                        self.gold_loc[k] = [1, self.gold_loc[k][1], n]
                    # else update shortest route via neighbor
                    elif k in n.gold_loc.keys() and n.gold_loc[k][0] < self.gold_loc[k][0] - 1:
                        self.gold_loc[k] = [n.gold_loc[k][0] + 1, self.gold_loc[k][1], n.unique_id]
            self.tell = 0
          
            
    def get_wealth_stats(self):
        """
        Gather data of individual agents within each cell
        """
        n = 0 
        resources = []
        gold = []
        if bool(self.agents):
            for id in self.agents:
                agent = self.agents[id]
                resources.append(agent["resources"])
                gold.append(["gold"])
                n += 1
            resources = numpy.array(resources)
            gold = numpy.array(gold)
            self.resource_stats = resources
            self.gold_stats = gold
            self.population = n
        else:
            self.resource_stats = []
            self.gold_stats = []
            self.population = 0
        
        
############### Functions Determining Actions of Indiviudals ##################

    def consume_resources(self):
        """
        Every agent within the cell consumes one of his resources and dies
        if there are no resources at his exposal
        """
        # keep count of agents that die to create new agents
        dead_agent_count = 0
        
        # iterate over agents
        for id in self.agents:
            agent = self.agents[id]
            if agent['resources'] > 0:
                agent['resources'] -= 1
                # self.resources -= 1
            else:
                del agent
                dead_agent_count += 1
                
                
    def acquire_resources(self):
        """
        Individuals acquire resources based on their occupation (i.e. miners
        find gold and others farm free resources on land). These resources are
        extracted from the cell. Both Resources and Gold can't drop below 0'
        """
        
        # iterate over agents
        for id in self.agents:
            agent = self.agents[id]
            # If agents are miners and in a cell with gold they mine
            if agent['miner'] == True and self.atype == "Gold":
                gold_mined = numpy.absolute(numpy.random.normal(agent["mining_ability"],1))
                if gold_mined <= self.gold:
                    agent["gold"] += gold_mined
                    agent["resources"] -= gold_mined
                    self.gold -= gold_mined
                    
            # Non-miners and miners that haven't reached their destination farm
            else:
                resources_farmed = numpy.absolute(numpy.random.normal(agent["farming_ability"],1))
                if resources_farmed <= self.resources:
                    agent["resources"] += resources_farmed
                    self.resources -= resources_farmed
    
    
    def turn_miner(self):
        """
        This function evaluates whether agents decide to become miners based
        on the knowledge they possess about the size of gold mines and the 
        distance to them as well as their personal risk level.
        """ 
        
        # find max resources owned by an agent in neighbouring and own cell
        max_resources = 0
        neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))
        for n in neighbors:
            for id in n.agents:
                agent = n.agents[id]
                if agent['resources'] > max_resources:
                    max_resources = agent['resources']
                
        prob_list = []
        # iterate over agents
        for id in self.agents:
            agent = self.agents[id]
            # iterate through all locations known in current cell
            for loc in self.gold_loc:
                distance = self.gold_loc[loc][0]
                gold_amount = self.gold_loc[loc][1]
                resource_factor = numpy.exp(-self.model.alpha*agent['resources']/max_resources)
                distance_factor = numpy.exp(-self.model.beta*distance)
                gold_factor = 2*((1/(1+numpy.exp(-self.model.gamma*gold_amount)))-0.5)
                # calculate probability of leaving to become a miner
                probability = (resource_factor*distance_factor*gold_factor*agent["risk_factor"])                   # print(resource_factor)
                # print(distance_factor)
                # print(gold_factor)
                # print(resource_factor)
                # print(agent["risk_factor"])
                # print(probability)
                # print("----------")
                prob_list.append(probability)
                if numpy.random.random() < probability:
                    agent['miner'] = True
                    agent['destination'] = -1 # cell ID extracted from loc
        self.avg_probability = numpy.mean(numpy.array(prob_list))
            
    def trade(self):
        """
        This function evaluates whether agents decide to trade based on 
        their individual resources and gold, and the resources of other agents.
        """
        if bool(self.agents):
            for id in list(self.agents):
                if self.agents[id]["miner"]:
                    if self.agents[id]["resources"] < 5 and self.agents[id]["gold"] > 0:
                        # trade gold with the echange rate
                        for id2 in list(self.agents):
                            if id != id2 and self.agents[id2]["resources"] > 10 and self.agents[id2]["miner"] == False:
                                self.agents[id]["resources"] += self.exchange
                                self.agents[id]["gold"] -= 1
                                self.agents[id2]["resources"] -= self.exchange
                                self.agents[id2]["gold"] += 1
                                self.resources += 1
                                self.number_of_trades += 1
                                break
                            elif id != id2 and self.agents[id2]["resources"] > 10 and self.agents[id2]["miner"] == True:
                                self.agents[id]["resources"] += 3
                                self.agents[id]["gold"] -= 1
                                self.agents[id2]["resources"] -= 3
                                self.agents[id2]["gold"] += 1
                                self.resources += 1
                                self.number_of_trades += 1
                                break
                    elif self.resources > 2*len(self.agents):
                        self.agents[id]["miner"] = False # make miner a non miner
                        if self.resources > 1 :
                            resources_farmed = numpy.absolute(numpy.random.normal(self.agents[id]["farming_ability"],1))
                            self.agents[id]["resources"] += resources_farmed
                            self.resources -= resources_farmed
                        else: del self.agents[id] # or die

    def move(self):
        
        # count number of miners
        num_miners = 0
        
        for agent in self.agents:
            if self.agents[agent]['miner'] == False:
                # look for neighbouring cells for highest economic oppportunity
                eco_opp = self.calc_econ_opp()
                neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))
                max_opp = max([n.calc_econ_opp() for n in neighbors])
                if max_opp > eco_opp and numpy.random.random() < self.agents[agent]["risk_factor"]:
                    possible_moves = [
                    n for n in neighbors if n.calc_econ_opp() == max_opp
                    ]
                    # move to cell with highest economic opp
                    move_to = random.choice(possible_moves)
                    # print("non-miner will move to", move_to.unique_id)
                    self.moving_agent[agent] = move_to.unique_id
                else: continue
            
            
            elif self.agents[agent]["miner"] == True:
                num_miners += 1
                
                if self.agents[agent]['destination'] == -1:
                    # Look if cell knows where gold is and add is to agent as destination
                    distance = 100
                    for k in self.gold_loc.keys():
                        if self.gold_loc[k][0] < distance:
                            distance = self.gold_loc[k][0]
                            self.agents[agent]["destination"] = k
                # Add agent agent to next location
                elif self.agents[agent]["destination"] != self.unique_id:
                    # print(self.agents, agent)
                    move_to = self.gold_loc[self.agents[agent]["destination"]][2]
                    # print("miner will move to", move_to)
                    self.moving_agent[agent] = move_to
                    
        self.number_of_miners = num_miners
                

####################### Functions Advancing the Model ########################

    def step(self):

        self.get_wealth_stats()

        self.information_spread_step()
        
        # check if people become miners
        self.turn_miner() # unfinished function

        # agents acquire resources from cells
        self.acquire_resources()

        # agents consume resources or die if not in possession of any
        self.consume_resources() # unfinished function
        
        # resources in cells regrow
        self.resource_regrowth()

        # trade between agents
        self.trade()
        
        # calculate and update economic opporunity in cells
        self.calc_econ_opp()
        
        # move agents to cells with highest economic opportunity
        self.move() # very unfinished function
        
        # replace dead agents randomly in new cells

    # advance function
    def advance(self):
        self.population = len(self.agents) # update population

        # TO DO: CHANGE UPDATE RESOURCES 
        # self.resources -= (self.miners + self.nonminers)
        if self.resources < 0 : self.resources = 0
        # self.resources += numpy.random.normal(loc=1, scale=0.2) * self.nonminers
        # self.resources += numpy.random.normal(loc=1, scale=0.2) * self.nonminers + numpy.random.normal(loc=1.1, scale=0.2) * self.miners 
        
        self.information_spread_advance()

        ## Add moving agents to other node
        for moving_id in self.moving_agent:
            for a in self.model.space.agents:
            
                if a.unique_id == self.moving_agent[moving_id]:
                    a.agents[moving_id] = self.agents[moving_id]
    
            # Remove agent from dictionary of agents
            self.agents.pop(moving_id)

        # Clear moving agent dict after advance
        self.moving_agent = dict()

        # Save data to file
        self.save_step()



