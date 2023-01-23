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
    if agent.atype is None:
        portrayal["color"] = "Grey"
    else:
        portrayal["color"] = "Blue"
    return portrayal

map_element = mg.visualization.MapModule(
    victoria_draw, [52, 12], 4)
server = mesa.visualization.ModularServer(
    GeoVictoria, [map_element], "Victoria", model_params
)
