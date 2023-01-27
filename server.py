import mesa
import mesa_geo as mg
import matplotlib

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
        "description":[
            f"Agent type: {agent.atype}", 
            f"ID: {agent.unique_id}",
            f"miners: {agent.miners}",
            f"non-miners: {agent.nonminers}",
            f"resources: {round(agent.resources)}",
            f"gold_resource: {agent.gold}"
        ],
        "weight":2
    }

    if agent.gold_loc != {}:
        t = portrayal["description"]
        t.append(f"path to gold: {list(agent.gold_loc.values())}")
        portrayal["description"] = t

    if agent.atype == "Land":
        portrayal["color"] = "Grey"
    elif agent.atype == "Gold":
        portrayal["color"] = "Yellow"
    elif agent.atype == "Road":
        portrayal["color"] = "Red"

    if agent.gold_loc != {} and agent.atype != "Gold":
        portrayal["color"] = "Green"
    # elif agent.atype == "Miner":
    #     portrayal["color"] = "Red"
    # elif agent.atype == "Settled":
    #     portrayal["color"] = "Blue"
    return portrayal

def victoria_pop(agent):
    color_dict = {
        5: "#030303",
        4: "#333333",
        3: "#666666",
        2: "#B3B3B3",
        1: "#E5E5E5"
    }

    portrayal = {
        "description":[
            f"Agent type: {agent.atype}", 
            f"ID: {agent.unique_id}", 
            f"tell: {agent.tell}",
            f"miners: {agent.miners}",
            f"non-miners: {agent.nonminers}",
            f"resources: {round(agent.resources)}",
            f"gold_resource: {agent.gold}"
            ],
        "weight":2
    }

    if agent.gold_loc != {}:
        t = portrayal["description"]
        t.append(f"path to gold: {list(agent.gold_loc.values())}")
        portrayal["description"] = t
    
    population = agent.miners + agent.nonminers
    if int(population/30) > 5 : col = 5 
    elif int(population/30) < 1: col = 1
    else: col = int(population/30)
    portrayal["color"] = color_dict[col]

    return portrayal


map_element = mg.visualization.MapModule(
    victoria_draw, [-37,145], 7, 1000, 750)
server = mesa.visualization.ModularServer(
    GeoVictoria, [map_element], "Victoria", model_params
)
