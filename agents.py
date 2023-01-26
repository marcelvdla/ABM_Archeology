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
        # Gold location dictionary with elements unique_id:distance, path
        self.gold_loc = {}
        self.miners = 0.1
        self.resources = 100
        self.gold_resource = 10
        
        # Randomly create goldmines
        n = random.random() 
        if n < 0.99:
            self.atype = "Land"
        else: #if n < 0.85:
            self.atype = "Gold"
            self.gold_loc['unique_id'] = 0
        # else:
        #     self.atype = "Miner"

    def step(self):
        # Get neighbors
        neighbors = list(self.model.space.get_neighbors_within_distance(self, distance=2))

        if self.atype == "Miner":
            # If already next to goldmine don't move
            for n in neighbors:
                if n != self:
                    if n.atype == "Gold":
                        self.atype = "Settled"
                        return

            # Find possible movement
            possible_steps = [move for move in neighbors if move.atype == "Land"]
            # Move to a random neighboring land and change agent 
            if len(possible_steps) > 0:
                move_to = random.choice(possible_steps)
                move_to.atype = self.atype
                self.atype = "Land"
        elif self.atype == "Gold":
            # Tell neighbors I have gold
            for n in neighbors:
                n.gold_loc[self.unique_id] = 1
        elif self.atype == "Land":
            # Check if neighbors know where gold is
            for n in neighbors:
                for k in n.gold_loc.keys():
                    self.gold_loc[k] = n.gold_loc[k] + 1

    # dummy advance function
    def advance(self):
        return super().advance()


## Suggestion for moving agents as separate class:
class MovingAgent(VictoriaAgent):
    def __init__(self, agentproperties):
        ## To Do give agent a goal node, make it move every x steps
        pass
