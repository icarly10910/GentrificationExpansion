from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule

import commercial as c
import person as p
import residential as r
import street as s
import model as m


status_strings = {0: 'L', 1: 'M', 2: 'H'}


def agent_portrayal(agent):
  if agent is None:
    return

  portrayal = {"Shape": "circle",
               "Filled": "true",
               "r": 0.5}

  # portrayal["text_color"] = "black"

  if type(agent) is p.Person:
    # portrayal["text"] = "%s" % status_strings[agent.econ_status]
    portrayal["Layer"] = 1

    portrayal["r"] = 0.4
    # if agent.yelped:
    #   portrayal["Color"] = "black"
    if agent.econ_status == 0:
      portrayal["Color"] = "#A9F5A9"
    elif agent.econ_status == 1:
      portrayal["Color"] = "#01DF01"
    else:
      portrayal["Color"] = "#088A08"
    # else:
    #   portrayal["Shape"] = "rect"
    #   portrayal["Color"] = "black"

  elif type(agent) is r.Residential:
    # portrayal["text"] = "%s %s" % ('V' if agent.vacancy else 'R', status_strings[agent.property_value])
    portrayal["Shape"] = "rect"
    portrayal["Layer"] = 0
    portrayal["w"] = 1
    portrayal["h"] = 1
    if agent.vacancy:
      if agent.property_value == 0:
        portrayal["Color"] = "#B3CDE0"
      elif agent.property_value == 1:
        portrayal["Color"] = "#6497B1"
      else:
        portrayal["Color"] = "#005B96"
    else:
      if agent.property_value == 0:
        portrayal["Color"] = "#E3CEF6"
      elif agent.property_value == 1:
        portrayal["Color"] = "#BE81F7"
      else:
        portrayal["Color"] = "#7401DF"
    # else:
    #   portrayal["Shape"] = "circle"
    #   portrayal["Color"] = "#7401DF"
    #   portrayal["r"] = 0.7

  elif type(agent) is c.Commercial:
    # portrayal["text"] = "C %s" % status_strings[agent.econ_status]
    portrayal["Shape"] = "rect"
    portrayal["Layer"] = 0
    portrayal["w"] = 1
    portrayal["h"] = 1
    if agent.econ_status == 0:
      portrayal["Color"] = "#F6CECE"
    elif agent.econ_status == 1:
      portrayal["Color"] = "#F78181"
    else:
      portrayal["Color"] = "#DF0101"
    # else:
    #   portrayal["Shape"] = "circle"
    #   portrayal["Color"] = "#DF0101"
    #   portrayal["r"] = 0.7

  elif type(agent) is s.Street:
    portrayal["text"] = "S"
    portrayal["Color"] = "grey"
    portrayal["Shape"] = "rect"
    portrayal["Layer"] = 0
    portrayal["w"] = 1
    portrayal["h"] = 1

  return portrayal


if __name__ == '__main__':
  chart = ChartModule([
    {"Label": "Mean Property Value", "Color": "Black"},
    {"Label": "Mean Economic Status of Residents", "Color": "Red"},
    {"Label": "Mean Economic Status of Visitors", "Color": "Blue"},
    {"Label": "Fraction of vacant homes with high property value", "Color": "Green"},
    {"Label": "Median popularity of businesses", "Color": "Purple"},
    {"Label": "Number of people sharing", "Color": "Pink"},
    {"Label": "Fraction of people sharing", "Color": "Black"},
    {"Label": "Median number of visitors to businesses", "Color": "Orange"}
  ], data_collector_name='datacollector')

  # width = 5
  # height = 5
  width = 20
  height = 20
  grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

  server = ModularServer(
      m.GentrifiedNeighbourhood,
      [grid, chart],
      "Gentrified Neighbourhood",
      {
        "people_inside": UserSettableParameter('slider', "Number of Initial Residents", 250, 100, 360, 10),
        "people_outside": UserSettableParameter('slider',
          "Number of People Outside the Neighbourhood", 100, 10, 700, 10),
        "outside_person_econ_dist_mean": UserSettableParameter('slider',
          "Mean of Economic Distribution for People Outside", 1, 0, 2, 0.1),
        "share_threshold": UserSettableParameter('slider',
          "Store popularity threshold for Yelping", 0.7, 0, 1, 0.1),
        "property_value_dist_mean": UserSettableParameter('slider',
          "Mean of Property Value Distribution for Homes", 0, 0, 2, 0.1),
        "num_residential": UserSettableParameter('slider', "Number of Homes", 260, 100, 360, 10),
        "num_commercial": UserSettableParameter('slider', "Number of Businesses", 70, 20, 360, 10),
        "num_streets": 10,
        "width": width,
        "height": height
        # "num_people": 5,
        # "people_outside": UserSettableParameter('slider', "Number of People Outside the Neighbourhood", 2, 2, 8, 1), #range(2, 8, 1),
        # "inside_person_econ_dist_mean": 2,
        # "outside_person_econ_dist_mean": 1,
        # "num_res": 3,
        # "num_com": 4,
        # "num_streets": 2,
        # "width": width,
        # "height": height
      })

  server.port = 8632
  server.launch()
