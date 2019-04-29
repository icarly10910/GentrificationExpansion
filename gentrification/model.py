import random

import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

import helpers
import commercial as c
import person as p
import residential as r
import street as s

import matplotlib.pyplot as plt

# TODO: Perhaps this should be defined in model as static member
model_reporters = {
  "Median popularity of businesses": helpers.med_pop,
  "Number of people sharing": helpers.yelpers,
  "Fraction of people sharing": helpers.fraction_yelpers,
  "Fraction of vacant homes with high property value": helpers.fraction_vacant_high,
  "People on the Street": helpers.people_on_street,
  "People in the Neighbourhood": helpers.people_in_neighbourhood,
  "Median Property Value": helpers.med_property_value,
  "Median Economic Status of Residents": helpers.med_econ_status_res,
  "Median Economic Status of Visitors": helpers.med_econ_status_visitors,
  "Median number of visitors to businesses": helpers.med_visits,
  "Mean Property Value":
    lambda model: np.mean([agent.property_value for agent in model.schedule.agents if
      isinstance(agent, r.Residential)]),
  "Mean Economic Status of Residents":
    lambda model: np.mean([agent.econ_status for agent in model.schedule.agents if
      isinstance(agent, p.Person) and agent.resident_status]),
  "Mean Economic Status of Visitors":
    lambda model: np.mean([agent.econ_status for agent in model.schedule.agents if
      isinstance(agent, p.Person) and not agent.resident_status and agent.in_neighbourhood]),
  "Mean number of visitors to businesses":
    lambda model: np.mean([bus.number_of_visitors for bus in model.schedule.agents if
      isinstance(bus, c.Commercial)]),
  "Fraction of people in the neighborhood":
    lambda model: float(len([agent for agent in model.schedule.agents if
      isinstance(agent, p.Person) and agent.in_neighbourhood])) / model.num_people
}


class GentrifiedNeighbourhood(Model):
  def from_dict(self, d):
    self.__dict__.update(d)

  def __init__(self, people_inside, people_outside, outside_person_econ_dist_mean, share_threshold,
      num_residential, num_commercial, num_streets, width, height):
    super().__init__()

    self.people_inside = int(people_inside)
    self.people_outside = int(people_outside)
    self.num_people = people_inside + people_outside
    self.outside_person_econ_dist_mean = outside_person_econ_dist_mean
    self.share_threshold = share_threshold
    self.num_residential = int(num_residential)
    self.num_commercial = int(num_commercial)
    self.num_streets = int(num_streets)

    self.schedule = RandomActivation(self)
    self.grid = MultiGrid(width, height, True)
    # Create agents
    available = []
    indices = []
    count = 0

    for i in range(height):
      for j in range(width - 1):
        available.append((i, j))
        indices.append(count)
        count += 1

    occupied = []
    res = []
    res_ind = []
    count = 0
    sched = 0
    for i in range(self.num_residential):  # place residences randomly
      a = r.Residential(sched, self)
      placed = False
      while not placed:
        position = np.random.choice(indices)
        indices.remove(position)
        position = available[position]
        # if (x,y) is valid and it doesn't already have a house on it, add a house
        if position not in occupied:
          self.grid.place_agent(a, position)
          self.schedule.add(a)
          occupied.append(position)
          res.append(position)
          res_ind.append(count)
          count += 1
          placed = True
          sched += 1

        else:
          print('something wrong 1')

    for i in range(self.num_commercial):  # place commercial randomly
      a = c.Commercial(sched, self)
      placed = False
      while not placed:
        position = np.random.choice(indices)
        indices.remove(position)
        position = available[position]
        # if (x,y) is valid and it doesn't already have a property on it, add a business
        if position not in occupied:
          self.grid.place_agent(a, position)
          self.schedule.add(a)
          occupied.append(position)
          placed = True
          sched += 1

    for i in range(self.num_streets):
      a = s.Street(sched, self)
      placed = False
      while not placed:
        position = np.random.choice(indices)
        indices.remove(position)
        position = available[position]
        # if (x,y) is valid and it doesn't already have a property on it, add a business
        if position not in occupied:
          self.grid.place_agent(a, position)
          self.schedule.add(a)
          occupied.append(position)
          placed = True
          sched += 1

    homes = []

    for i in range(self.people_inside):
      a = p.Person(sched, self, True)
      placed = False
      while not placed:
        position = np.random.choice(res_ind)
        res_ind.remove(position)
        position = res[position]
        if position not in homes:
          self.grid.place_agent(a, position)
          self.schedule.add(a)
          a.Home = position
          a.resident_status = True
          a.in_neighbourhood = True
          homes.append(position)
          a.home = position
          Res = self.grid.get_cell_list_contents(position)
          home = [obj for obj in Res if isinstance(obj, r.Residential)]
          home = home[0]
          home.vacancy = False
          a.econ_status = home.property_value
          placed = True
          sched += 1

    for i in range(self.people_outside):
      a = p.Person(sched, self, False)
      placed = False
      while not placed:
        y = random.randrange(self.grid.height)
        if y != self.grid.height:
          self.grid.place_agent(a, (y, self.grid.width - 1))
          self.schedule.add(a)
          a.resident_status = False
          a.in_neighbourhood = False
          placed = True
          sched += 1

    # DEBUG: Plot econ status distros
    # econ_inside = [person.econ_status for person in self.schedule.agents if
    #   isinstance(person, p.Person) and person.in_neighbourhood]
    # econ_outside = [person.econ_status for person in self.schedule.agents if
    #   isinstance(person, p.Person) and not person.in_neighbourhood]
    #
    # plt.hist(econ_inside)
    # plt.figure()
    # plt.hist(econ_outside)
    # plt.show()

    self.datacollector = DataCollector(model_reporters=model_reporters)

  def step(self):
    self.datacollector.collect(self)
    self.schedule.step()
