import mesa 
import mesa_geo as mg
import pandas as pd
import csv
import numpy as np

from agents import VictoriaAgent

class GeoVictoria(mesa.Model):
    """ Model class for the Victoria Gold rush model """  

    def __init__(self, stoch=0.5, alpha=2, beta=0.1, gamma=0.001, file=None):
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.space = mg.GeoSpace(warn_crs_conversion=False)
        self.running = True
        self.agent_id = 1
        self.minelist = []
        self.stoch = stoch
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.writer = csv.writer(open(f'Data/data_{file}.csv', 'w'))
        self.writer.writerow((
                            "unique_id",
                            "population",
                            "number_of_miners",
                            "avg_probability",
                            "gold_stats",
                            "resource_stats",
                            "economic_opportunity",
                            "resources",
                            "trades"))
        self.datacollector = mesa.DataCollector({"gini": "gini"})

        start_state = pd.read_csv("Modelstates/test.csv")

        ac = mg.AgentCreator(VictoriaAgent, model=self)
        agents = ac.from_file("Shapefiles/victoria_hex.geojson")
        self.space.add_agents(agents)

        pop_list = []

        for agent in agents:
            if agent.unique_id in list(start_state["unique_id"]):
                index = start_state.index[start_state["unique_id"] == agent.unique_id][0]
                agent.set_type(start_state["type"][index])
                # Hardcode 1000 initial gold
                agent.gold = 1000

            # initial population
            self.initialize_population(agent)
            self.schedule.add(agent)
            pop_list.append(agent.population)
        
        self.gini = self.gini_coef(np.array(pop_list))

    def initialize_population(self, agent):
        """
        create an intial population of agents within a cell (i.e. local environment)
        with a global agent ID to identify them as they move between cells.
        """
        # number_of_agents = np.random.randint(low=5,high=15)
        # for _ in range(number_of_agents):
        for i in range(3):
            agent.agents[self.agent_id] = {
                "id": self.agent_id,
                "miner": False, # everyone is nonminer by default
                "destination": -1,
                "mining_ability": np.random.uniform(2,4),
                "gold": 0,
                "farming_ability": np.random.uniform(2,4),
                "resources": 10,
                "risk_factor": np.random.random() # *0.5
            }
            self.agent_id += 1

    def gini_coef(self, x):
        """ Compute gini coefficient for population x
        """
        total = 0
        for i, xi in enumerate(x[:-1], 1):
            total += np.sum(np.abs(xi - x[i:]))
        return total / (len(x)**2 * np.mean(x))


    def step(self):
        self.schedule.step()
        self.gini = self.gini_coef(np.array([a.population for a in self.schedule.agents]))
        self.datacollector.collect(self)