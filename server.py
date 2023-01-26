import mesa
import mesa_geo as mg

from model import GeoVictoria

import requests
import json

class Sched(mesa.visualization.TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Number of possible agents: " + str(model.schedule.get_agent_count())

# Define model parameters
model_params = {
}

def victoria_draw(agent):
    """
    Portrayal Method for canvas
    """
    portrayal = {
        "description":(f"Agent type: {agent.atype}", f"ID: {agent.unique_id}"),
        "weight":2
    }

    if agent.atype == "Land":
        portrayal["color"] = "Grey"
    elif agent.atype == "Gold":
        portrayal["color"] = "Yellow"

    if agent.gold_loc != {} and agent.atype != "Gold":
        portrayal["color"] = "Green"
    # elif agent.atype == "Miner":
    #     portrayal["color"] = "Red"
    # elif agent.atype == "Settled":
    #     portrayal["color"] = "Blue"
    return portrayal

map_element = mg.visualization.MapModule(
    victoria_draw, [-37,145], 7, 1000, 750)
server = mesa.visualization.ModularServer(
    GeoVictoria, [map_element], "Victoria", model_params
)
