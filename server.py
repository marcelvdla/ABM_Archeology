import mesa
import mesa_geo as mg
import matplotlib

from model import GeoVictoria

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
            f"resources: {round(agent.resources)}",
            f"gold_resource: {agent.gold}",
            f"init_population: {agent.init_population}",
            f"agents: {agent.agents}",
            f"population: {agent.population}",
            f"economic_opportunity: {agent.economic_opportunity}"
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

    if agent.gold_loc != {} and agent.atype != "Gold":
        portrayal["color"] = "Green"

    for a in agent.agents:
        if agent.agents[a]["miner"] and agent.atype != "Gold":
            portrayal["color"] = "Red"

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
            f"resources: {round(agent.resources)}",
            f"gold_resource: {agent.gold}"
            ],
        "weight":2
    }

    if agent.gold_loc != {}:
        t = portrayal["description"]
        t.append(f"path to gold: {list(agent.gold_loc.values())}")
        portrayal["description"] = t
    
    population = agent.population
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
