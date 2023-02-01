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
            # f"init_population: {agent.init_population}",
            f"agents: {agent.agents}",
            f"population: {agent.population}",
            f"economic_opportunity: {agent.economic_opportunity}",
            f"trades: {agent.number_of_trades}"
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

    flag = False
    if agent.atype != "Gold":
        for a in agent.agents:
            # print(a, type(a))
            if agent.agents[a]["miner"]:
                flag = True
                portrayal["color"] = "Red"
    if agent.atype != "Gold" and flag == False:
        portrayal["color"] = "Blue"
            
    # elif agent.atype == "Miner":
    #     portrayal["color"] = "Red"
    # elif agent.atype == "Settled":
    #     portrayal["color"] = "Blue"

    if bool(agent.agents) == False and agent.atype == "Gold":
        portrayal["color"] = "Yellow"
    elif bool(agent.agents) == False and agent.atype == "Land":
        portrayal["color"] = "White"
    
    if agent.number_of_trades > 0:
        portrayal["color"] = "Purple"
    
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
            f"resources: {round(agent.resources)}",
            f"gold_resource: {agent.gold}",
            f"agents: {agent.agents}",
            f"population: {agent.population}",
            f"economic_opportunity: {agent.economic_opportunity}",
            f"trades: {agent.number_of_trades}"
            ],
        "weight":2
    }

    if agent.gold_loc != {}:
        t = portrayal["description"]
        t.append(f"path to gold: {list(agent.gold_loc.values())}")
        portrayal["description"] = t
    
    population = len(agent.agents)
    if int(population/3) > 5 : col = 5 
    elif int(population/3) < 1: col = 1
    else: col = int(population/3)
    portrayal["color"] = color_dict[col]

    if agent.atype == "Gold":
        portrayal["color"] = "Yellow"

    return portrayal

map_element = mg.visualization.MapModule(
    victoria_draw, [-37,145], 7, 1000, 750)
server = mesa.visualization.ModularServer(
    GeoVictoria, [map_element], "Victoria", model_params
)
