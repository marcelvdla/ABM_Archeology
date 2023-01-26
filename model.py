import mesa 
import mesa_geo as mg

from agents import VictoriaAgent

class GeoVictoria(mesa.Model):
    """ Model class for the Victoria Gold rush model """

    def __init__(self):
        self.schedule = mesa.time.RandomActivation(self)
        self.space = mg.GeoSpace(warn_crs_conversion=False)
        self.running = True

        self.minelist = []

        ac = mg.AgentCreator(VictoriaAgent, model=self)
        agents = ac.from_file("Shapefiles/victoria_hex.geojson")
        self.space.add_agents(agents)

        for agent in agents:
            self.schedule.add(agent)
    
    def step(self):
        self.schedule.step()
        # self.datacollector.collect(self) # need data ?

    # def run_model(self, step_count=20):
    #     '''
    #     Method that runs the model for a specific amount of steps.
    #     '''
    #     for i in range(step_count):
    #         self.schedule.step()