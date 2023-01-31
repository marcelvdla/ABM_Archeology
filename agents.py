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

        # initial agents to be created in this cell
        self.init_population = 3
        
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

    def save_step(self):

        data = (
            self.unique_id,
            self.population,
            self.number_of_miners,
            self.avg_probability,
            self.gold_stats,
            self.resource_stats,
            self.economic_opportunity,
            self.resources
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
        
    def initialize_population(self, agent_id):
        """
        create an intial population of agents within a cell (i.e. local environment)
        with a global agent ID to identify them as they move between cells.
        """
        for _ in range(self.init_population):
            self.agents[agent_id] = {
                "id": agent_id,
                "miner": False, # everyone is nonminer by default
                "destination": -1,
                "mining_ability": numpy.absolute(numpy.random.normal(5,2)),
                "gold": 0,
                "farming_ability": numpy.absolute(numpy.random.normal(5,2)),
                "resources": 10,
                "risk_factor": numpy.random.random()
            }
            agent_id += 1
        return agent_id

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
        Evaluate the max, mean and standrad deviation of both gold and resources
        of the agents within each cell.
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
            self.resource_stats = [numpy.max(resources), numpy.mean(resources), numpy.std(resources)]
            self.gold_stats = [numpy.max(resources), numpy.mean(resources), numpy.std(resources)]
            self.population = n
        else:
            self.resource_stats = [0,0,0]
            self.gold_stats = [0,0,0]
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
                probability = (resource_factor + distance_factor + gold_factor + agent["risk_factor"])/4
                # print(resource_factor)
                # print(distance_factor)
                # print(gold_factor)
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
        for id in self.agents:
            agent = self.agents[id]
            if agent["miner"]:
                if agent["resources"] < 2 and agent["gold"] > 0:
                    # trade gold with the echange rate
                    for agent2 in self.agents:
                        if agent2["id"] != agent["id"] and agent2["resources"] > 20:
                            agent["resources"] += self.exchange
                            agent["gold"] -= 1
                            agent2["resources"] -= self.exchange
                            agent2["gold"] += 1
                            break
                        else : # call move function or die ?
                            del agent

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

