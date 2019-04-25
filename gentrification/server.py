from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule

import commercial as c
import person as p
import residential as r
import street as s
import model as m

def agent_portrayal(agent):
  if agent is None:
    return

  portrayal = {"Shape": "circle",
               "Filled": "true",
               "r": 0.5}

  if type(agent) is p.Person:
    portrayal["Layer"] = 1
    portrayal["r"] = 0.4
    # if agent.yelped:
    #   portrayal["Color"] = "black"
    if agent.econ_status == 0:
      portrayal["Color"] = "#A9F5A9"
    elif agent.econ_status == 1:
      portrayal["Color"] = "#01DF01"
    elif agent.econ_status == 2:
      portrayal["Color"] = "#088A08"
    else:
      portrayal["Shape"] = "rect"
      portrayal["Color"] = "black"

  elif type(agent) is r.Residential:
    portrayal["Shape"] = "rect"
    portrayal["Layer"] = 0
    portrayal["w"] = 1
    portrayal["h"] = 1
    if agent.vacancy:
      portrayal["Color"] = "white"
    elif agent.property_value == 0:
      portrayal["Color"] = "#E3CEF6"
    elif agent.property_value == 1:
      portrayal["Color"] = "#BE81F7"
    elif agent.property_value == 2:
      portrayal["Color"] = "#7401DF"
    else:
      portrayal["Shape"] = "circle"
      portrayal["Color"] = "#7401DF"
      portrayal["r"] = 0.7

  elif type(agent) is c.Commercial:
    portrayal["Shape"] = "rect"
    portrayal["Layer"] = 0
    portrayal["w"] = 1
    portrayal["h"] = 1
    if agent.econ_status == 0:
      portrayal["Color"] = "#F6CECE"
    elif agent.econ_status == 1:
      portrayal["Color"] = "#F78181"
    elif agent.econ_status == 2:
      portrayal["Color"] = "#DF0101"
    else:
      portrayal["Shape"] = "circle"
      portrayal["Color"] = "#DF0101"
      portrayal["r"] = 0.7

  elif type(agent) is s.Street:
    portrayal["Color"] = "grey"
    portrayal["Shape"] = "rect"
    portrayal["Layer"] = 0
    portrayal["w"] = 1
    portrayal["h"] = 1

  return portrayal


if __name__ == '__main__':
  width = 20
  height = 20
  grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

  chart = ChartModule([
    {"Label": "Median Property Value", "Color": "Black"},
    {"Label": "Median Economic Status of Residents", "Color": "Red"},
    {"Label": "Median Economic Status of Visitors", "Color": "Blue"},
    {"Label": "Vacant homes with high property value", "Color": "Green"},
    {"Label": "Median popularity of businesses", "Color": "Purple"},
    {"Label": "Number of people sharing", "Color": "Pink"},
    {"Label": "Median number of visitors to businesses", "Color": "Orange"}
  ], data_collector_name='datacollector')

  server = ModularServer(
      m.GentrifiedNeighbourhood,
      [grid, chart],
      "Gentrified Neighbourhood",
      {
        "num_people": UserSettableParameter('slider', "Number of Initial Residents", 250, 100, 360, 10),
        "people_outside": UserSettableParameter('slider', "Number of People Outside the Neighbourhood", 100, 10, 700, 10),
        "num_res": UserSettableParameter('slider', "Number of Homes", 260, 100, 360, 10),
        "num_com": UserSettableParameter('slider', "Number of Businesses", 70, 20, 360, 10),
        "num_streets": 10,
        "width": width,
        "height": height
      })

  server.port = 8632
  server.launch()
