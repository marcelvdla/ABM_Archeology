import mesa

from agents import PeopleAgent, Sugar
from model import Sugarscape

def Agent_vis(agent):
    if agent is None:
        return
    if type(agent) is PeopleAgent:
        return {
            "Color": "red",
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "r": 0.4
        }
    
    elif type(agent) is Sugar:
        return {
            "Color": "yellow",
            "Shape": "circle",
            "Filled": "true",
            "Layer": 1,
            "r": 0.2
        }

grid = mesa.visualization.CanvasGrid(Agent_vis, 10, 10, 500, 500)
server = mesa.visualization.ModularServer(
    Sugarscape, [grid], "Sugarscape Model", {"N": 10, "width": 10, "height": 10}
)

server.launch()