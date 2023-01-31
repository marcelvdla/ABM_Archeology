import mesa 
import mesa_geo as mg
import pandas as pd
import csv

from agents import VictoriaAgent

class GeoVictoria(mesa.Model):
    """ Model class for the Victoria Gold rush model """  

    def __init__(self, file=None):
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.space = mg.GeoSpace(warn_crs_conversion=False)
        self.running = True
        self.agent_id = 1
        self.minelist = []
        self.alpha = 5
        self.beta = 0.5
        self.gamma = 0.1
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
            self.agent_id = agent.initialize_population(self.agent_id)
            self.agent_id += 1
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()