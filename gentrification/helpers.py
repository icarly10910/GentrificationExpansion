import random

import numpy as np

import commercial as c
import person as p
import residential as r
import street as s


def decision(probability):
  return random.random() < probability


def pop(n):
  l = 0.2
  p = 1 - np.exp(-l * n)
  if p > 0.1:
    return p
  else:
    return 0.1


def e_stat(p):
  if p <= 0.3:
    return 0
  if 0.3 < p <= 0.6:
    return 1
  if p > 0.6:
    return 2


def people_on_street(model):
  street_visits = [agent.number_of_visitors for agent in model.schedule.agents if isinstance(agent, s.Street)]
  return sum(street_visits)


def people_in_neighbourhood(model):
  people = [agent for agent in model.schedule.agents if isinstance(agent, p.Person) and agent.in_neighbourhood]
  return len(people)


def med_property_value(model):
  prop_vals = [prop.property_value for prop in model.schedule.agents if isinstance(prop, r.Residential)]
  return np.median(prop_vals)


def med_econ_status_res(model):
  econ_stats = [agent.econ_status for agent in model.schedule.agents if
                isinstance(agent, p.Person) and agent.resident_status]
  return np.median(econ_stats)


def med_econ_status_visitors(model):
  econ_stats = [agent.econ_status for agent in model.schedule.agents if
                isinstance(agent, p.Person) and not agent.resident_status and agent.in_neighbourhood]
  return np.median(econ_stats)


def yelpers(model):
  yelpers = [agent for agent in model.schedule.agents if isinstance(agent, p.Person) and agent.yelped]
  for agent in yelpers:
    agent.yelped = False
  return len(yelpers)


def med_visits(model):
  bus_visits = [bus.number_of_visitors for bus in model.schedule.agents if isinstance(bus, c.Commercial)]
  return np.median(bus_visits)


def med_pop(model):
  bus_pop = [bus.popularity for bus in model.schedule.agents if isinstance(bus, c.Commercial)]
  return np.median(bus_pop)


def fraction_vacant_high(model):
  total = high_vacant = 0
  for prop in model.schedule.agents:
    if isinstance(prop, r.Residential):
      total += 1
      if prop.vacancy and prop.property_value == 2:
        high_vacant += 1
  return float(high_vacant) / total
