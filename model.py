import mesa 
import mesa_geo as mg

class VictoriaAgent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, agent_type=None):
        """Create new agent
        Args:
            id: Unique identifier for the agent.
            agent_type: Indicator for the agent's type (miner/farmer/trader)
        """

        super().__init__(unique_id, model, geometry, crs)
        self.atype = agent_type

    def step(self):
        ## Implement step method
        pass

class GeoVictoria(mesa.Model):
    """ Model class for the Victoria Gold rush model """

    def __init__(self):

        self.schedule = mesa.time.RandomActivation(self)
        self.space = mg.GeoSpace(warn_crs_conversion=False)
        self.running = True

        ac = mg.AgentCreator(VictoriaAgent, model=self)
        agents = ac.from_file("Shapefiles/victoria_hex.geojson")
        self.space.add_agents(agents)
    
    def step(self):
        ## Implement step
        pass