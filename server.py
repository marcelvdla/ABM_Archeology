import mesa
import mesa_geo as mg

from model import GeoVictoria

import requests
import json

# Define model parameters
model_params = {
}

def victoria_draw(agent):
    """
    Portrayal Method for canvas
    """
    portrayal = dict()
    if agent.atype == "Land":
        portrayal["color"] = "Grey"
    elif agent.atype == "Gold":
        portrayal["color"] = "Yellow"
    elif agent.atype == "Miner":
        portrayal["color"] = "Red"
    return portrayal

map_element = mg.visualization.MapModule(
    victoria_draw, [-37,145], 7, 1000, 750)
server = mesa.visualization.ModularServer(
    GeoVictoria, [map_element], "Victoria", model_params
)
