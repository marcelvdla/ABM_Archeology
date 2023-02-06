import mesa_geo as mg
import numpy
import random

class VictoriaAgent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs):
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
        self.population = 0
        
        self.number_of_miners = 0
        
        self.avg_probability = 0
        
        self.tell = 0
        
        self.resource_stats = []
        
        self.gold_stats = []
        
        self.atype = "Land"

        self.moving_agent = dict()

        self.number_of_trades = 0

        self.time_step = 0

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
    
    
    def information_spread_step(self):
        neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))

        nn_neighbors = [n for n in neighbors if self.unique_id not in list(n.gold_loc.keys())]

        if self.atype == "Gold" and self.tell == 1:
            # Tell neighbors I have gold
            for n in nn_neighbors:
                if n != self and random.random() < self.model.stoch:
                    n.gold_loc[self.unique_id] = [1, self.gold, self.unique_id]
                    n.tell += 1
            
            # Check if all neighbors know
            if len([n for n in neighbors if self.unique_id not in list(n.gold_loc.keys())]) == 0:
                self.tell = -1
        elif self.atype == "Land" and self.tell == 2:
            # Check if I can tell neighbors where gold is
            for n in nn_neighbors:
                if n.tell == 0 and random.random() < self.model.stoch:
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
                        self.gold_loc[k] = [1, self.gold_loc[k][1], n.unique_id]
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
                gold.append(agent["gold"])
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
    
    def count_miners(self):
        num_miners = 0
        if bool(self.agents):
            for id in self.agents:
                if self.agents[id]["miner"] == True:
                    num_miners += 1
        
        self.number_of_miners = num_miners
        
        
        
############### Functions Determining Actions of Indiviudals ##################

    
    def agent_step(self):
        threshold = 5
        
        for agent_id in self.agents: 
            agent = self.agents[agent_id]
            agent["resources"] -= 1
            
            if agent["miner"] == True and agent["destination"] != self.unique_id and agent["resources"] > threshold:
                # move miner to next cell
                self.move_miner(agent_id)
                 
            
            elif agent["miner"] == True and agent["destination"] != self.unique_id and agent["resources"] < threshold:
                # Stops being a miner
                agent["miner"] = False
                # Check if miner can farm
                succesful_farm = self.farm(agent_id)
                # If succesfull in farming farm else move
                if succesful_farm:
                    continue
                else:
                    self.move_non_miner(agent_id)

            
            elif agent["miner"] == True and agent["destination"] == self.unique_id and agent["resources"] > threshold:
                # try mining
                succesful_mine = self.mine(agent_id)
                if succesful_mine:
                    continue
                else:
                    agent["miner"] = False
                    
            
            elif agent["miner"] == True and agent["destination"] == self.unique_id and agent["resources"] < threshold:
                succesful_trade = self.trade(agent_id)
                if succesful_trade:
                    continue
                else:
                    # otherwise move to next best cell
                    # should they try farm first?
                    agent["miner"] = False
                    self.move_non_miner(agent_id)

                
            elif agent["miner"] == False and agent["resources"] > threshold:
                turn_miner = self.turn_miner(agent_id)
                if turn_miner:
                    agent["miner"] = True
                else:
                    move = self.move_non_miner(agent_id)
                    if move:
                        continue
                    else:
                        succesful_farm = self.farm(agent_id)
                    
            elif agent["miner"] == False and agent["resources"] < threshold:
                succesful_farm = self.farm(agent_id)
                

    def move_miner(self, agent_id):
        """
        Move Miner to next step to reach destination
        """
        move_to = self.gold_loc[self.agents[agent_id]["destination"]][2]
        self.moving_agent[agent_id] = move_to
    
    
    def move_non_miner(self, agent_id):
        """
        move a non miner to a cell with highest economic opportunity based
        on their personal risk factor
        """
        eco_opp = self.economic_opportunity
        neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))
        max_opp = max([n.economic_opportunity for n in neighbors])
        if max_opp > eco_opp and numpy.random.random() < self.agents[agent_id]["risk_factor"]:
            possible_moves = list([n for n in neighbors if n.economic_opportunity == max_opp])
            # move to cell with highest economic opp
            move_to = random.choice(possible_moves)
            self.moving_agent[agent_id] = move_to.unique_id
            return True
        else:
            return False
    
    
    def farm(self, agent_id):
        """
        Check if agent is able to farm given the free resources in the cell.
        
        If possible farm and return True, else return False.
        """
        
        if self.resources >= self.agents[agent_id]["farming_ability"]:
            self.resources -= self.agents[agent_id]["farming_ability"]
            self.agents[agent_id]["resources"] += self.agents[agent_id]["farming_ability"]
            return True
        
        elif self.resources > 0:
            self.agents[agent_id]["resources"] += self.resources
            self.resources = 0
            return True
        
        else:
            return False
    
    
    def mine(self, agent_id):
        """
        Check if agent is able to mine given the free resources in the cell.
        
        If possible mine and return True, else return False.
        """
        if self.gold >= self.agents[agent_id]["mining_ability"]:
            self.gold -= self.agents[agent_id]["mining_ability"]
            self.agents[agent_id]["gold"] += self.agents[agent_id]["mining_ability"]
            return True
        
        elif self.gold > 0:
            self.agents[agent_id]["gold"] += self.gold
            self.gold = 0
            return True
        
        else:
            return False
        
            
    def trade(self, agent_id):
        """
        check if trade is possible, trade and return True
        
        if not possible return False
        """
        success = False
        if bool(self.agents):
            for id in self.agents:
                if agent_id != id and self.agents[id]["resources"] > 10 and self.agents[id]["miner"] == False:
                    self.agents[agent_id]["resources"] += self.exchange
                    self.agents[agent_id]["gold"] -= 1
                    self.agents[id]["resources"] -= self.exchange
                    self.agents[id]["gold"] += 1
                    self.resources += 1
                    self.number_of_trades += 1
                    success = True
                    break
                
                elif agent_id != id and self.agents[id]["resources"] > 10 and self.agents[id]["miner"] == True:
                    self.agents[agent_id]["resources"] += 3
                    self.agents[agent_id]["gold"] -= 1
                    self.agents[id]["resources"] -= 3
                    self.agents[id]["gold"] += 1
                    self.resources += 1
                    self.number_of_trades += 1
                    success = True
                    break
        
        return success

    
    def turn_miner(self, agent_id):
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
                if n.agents[id]['resources'] > max_resources:
                    max_resources = n.agents[id]['resources']
        
        for loc in self.gold_loc:
            distance = self.gold_loc[loc][0]
            gold_amount = self.gold_loc[loc][1]
            resource_factor = numpy.exp(-self.model.alpha*self.agents[agent_id]['resources']/max_resources)
            distance_factor = numpy.exp(-self.model.beta*distance)
            gold_factor = 2*((1/(1+numpy.exp(-self.model.gamma*gold_amount)))-0.5)
            # calculate probability of leaving to become a miner
            probability = (resource_factor*distance_factor*gold_factor*self.agents[agent_id]["risk_factor"])
            if numpy.random.random() < probability:
                self.agents[agent_id]["destination"] = loc
                return True
            else:
                return False
                
    def gold_mine(self):
        if self.time_step == 4 and self.unique_id == 685:
            self.atype = "Gold"
            self.gold = 1000

        if self.time_step == 6 and self.unique_id == 635:
            self.atype = "Gold"
            self.gold = 1000

        if self.time_step == 9 and self.unique_id == 693:
            self.atype = "Gold"
            self.gold = 1000
        
        if self.time_step == 12 and self.unique_id == 315:
            self.atype = "Gold"
            self.gold = 1000

        if self.time_step == 15 and self.unique_id == 121:
            self.atype = "Gold"
            self.gold = 1000
        
        if self.time_step == 19 and self.unique_id == 638:
            self.atype = "Gold"
            self.gold = 1000
        
        if self.time_step == 21 and self.unique_id == 368:
            self.atype = "Gold"
            self.gold = 1000
        
# 643,"Gold",None
# 346,"Gold",None
# 718,"Gold",None
# 263,"Gold",None
# 725,"Gold",None


####################### Functions Advancing the Model ########################

    def step(self):

        self.information_spread_step()
        
        self.agent_step()

        self.gold_mine()
        

    # advance function
    def advance(self):

        # TO DO: CHANGE UPDATE RESOURCES 
        if self.resources < 0 : self.resources = 0
        
        # resources in cells regrow
        self.resource_regrowth()
        
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
        
        self.population = len(self.agents) # update population
        
        self.count_miners()
        
        self.get_wealth_stats()
        
        # calculate and update economic opporunity in cells
        self.calc_econ_opp()
        
        # Save data to file
        self.save_step()

        self.time_step += 1



