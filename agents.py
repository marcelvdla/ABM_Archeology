import mesa_geo as mg
import random
import sys

class VictoriaAgent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, agent_type=None):
        """Create new agent
        Args:
            id: Unique identifier for the agent.
            agent_type: Indicator for the agent's type (miner/farmer/trader)
        """
        super().__init__(unique_id, model, geometry, crs)

        n = random.random() 
        if n < 0.8:
            self.atype = "Land"
        elif n < 0.85:
            self.atype = "Gold"
        else:
            self.atype = "Miner" 
            
    def step(self):
        neighbors = self.model.space.get_neighbors(self)
        if self.atype == "Miner":
            # If already next to goldmine don't move
            for n in neighbors:
                if n.atype == "Gold":
                    self.model.schedule.remove(self)
                    return None

            # Get neighborhood within vision, only finds land
            possible_steps = [move for move in neighbors if move.atype == "Land"]
            # Move to a random neighboring land and change agent 
            if len(possible_steps) > 0:
                move_to = random.choice(possible_steps)
                move_to.atype = self.atype
                # self.model.schedule.add(move_to)
                self.atype = "Land"
            # self.model.schedule.remove(self)

class Gold(VictoriaAgent):
    pass

class Miner(VictoriaAgent):
    pass
