import mesa 
import mesa_geo as mg
import pandas as pd

from agents import VictoriaAgent

class GeoVictoria(mesa.Model):
    """ Model class for the Victoria Gold rush model """

    def __init__(self):
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.space = mg.GeoSpace(warn_crs_conversion=False)
        self.running = True

        self.minelist = []

        start_state = pd.read_csv("Modelstates/test.csv")


        ac = mg.AgentCreator(VictoriaAgent, model=self)
        agents = ac.from_file("Shapefiles/victoria_hex.geojson")
        self.space.add_agents(agents)

        for agent in agents:
            if agent.unique_id in list(start_state["unique_id"]):
                index = start_state.index[start_state["unique_id"] == agent.unique_id][0]
                agent.set_type(start_state["type"][index])
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()
        # self.schedule.advance()
        # self.datacollector.collect(self) # need data ?

    # def run_model(self, step_count=20):
    #     '''
    #     Method that runs the model for a specific amount of steps.
    #     '''
    #     for i in range(step_count):
    #         self.schedule.step()