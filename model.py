import mesa 
import mesa_geo as mg
import pandas as pd
import csv
import numpy as np

from agents import VictoriaAgent

class GeoVictoria(mesa.Model):
    """ Model class for the Victoria Gold rush model """  

    def __init__(self, file=None):
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.space = mg.GeoSpace(warn_crs_conversion=False)
        self.running = True
        self.agent_id = 1
        self.minelist = []
        self.alpha = 2
        self.beta = 0.2
        self.gamma = 0.001
        self.writer = csv.writer(open(f'Data/data_{file}.csv', 'w'))
        self.writer.writerow((
                            "unique_id",
                            "population",
                            "number_of_miners",
                            "avg_probability",
                            "gold_stats",
                            "resource_stats",
                            "economic_opportunity",
                            "resources"))

        start_state = pd.read_csv("Modelstates/test.csv")

        ac = mg.AgentCreator(VictoriaAgent, model=self)
        agents = ac.from_file("Shapefiles/victoria_hex.geojson")
        self.space.add_agents(agents)

        for agent in agents:
            if agent.unique_id in list(start_state["unique_id"]):
                index = start_state.index[start_state["unique_id"] == agent.unique_id][0]
                agent.set_type(start_state["type"][index])
                # Hardcode 1000 initial gold
                agent.gold = 1000

            # initial population
            self.initialize_population(agent)
            self.schedule.add(agent)

    def initialize_population(self, agent):
        """
        create an intial population of agents within a cell (i.e. local environment)
        with a global agent ID to identify them as they move between cells.
        """
        for _ in range(10):
            agent.agents[self.agent_id] = {
                "id": self.agent_id,
                "miner": False, # everyone is nonminer by default
                "destination": -1,
                "mining_ability": np.random.uniform(2,4),
                "gold": 0,
                "farming_ability": np.random.uniform(2,4),
                "resources": 10,
                "risk_factor": np.random.random()*0.3
            }
            self.agent_id += 1

    def step(self):
        self.schedule.step()