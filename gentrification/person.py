import random

import numpy as np
from mesa import Agent

import commercial as c
import helpers
import residential as r
import street as s

def decision(probability):
  return random.random() < probability


def econ_status_choice(dist_mean):
  return min(2, max(0, int(round(np.random.normal(dist_mean, scale=1)))))


class Person(Agent):
  """ An agent with fixed initial wealth."""

  def __init__(self, unique_id, model, inside_neighborhood=True):
    super().__init__(unique_id, model)
    self.yelped = False
    # if inside_neighborhood:
      # self.econ_status = np.random.choice([0, 1, 2],
      #                                     p=[0.6, 0.3, 0.1])  # RANDOM INITIALIZATION OF ECONOMIC STATUS. CAN CHANGE.
      # # Choose value from normal distribution with mean i, stddev 1, round to int, limit to range [0, 2]
      # self.econ_status = 2 #econ_status_choice(model.inside_person_econ_dist_mean)
    # else:
      # self.econ_status = np.random.choice([0, 1, 2],
      #                                     p=[0.2, 0.3, 0.5])  # RANDOM INITIALIZATION OF ECONOMIC STATUS. CAN CHANGE.
    if not inside_neighborhood:
      self.econ_status = econ_status_choice(model.outside_person_econ_dist_mean)

    self.prob_enter = np.random.normal(0.3, 0.15)

  def buy_or_sell(self):
    if self.in_neighbourhood:
      if self.resident_status:
        residence = self.model.grid.get_cell_list_contents([self.Home])
        home = [obj for obj in residence if isinstance(obj, r.Residential)]
        home = home[0]
        med_all = helpers.med_property_value(self.model)
        good_offer = np.random.choice([0, 1], p=[0.1, 0.9])
        if self.econ_status < home.property_value:
          y = random.randrange(self.model.grid.height)
          if y != self.model.grid.height:
            self.model.grid.move_agent(self, (y, self.model.grid.width - 1))
          else:
            self.model.grid.move_agent(self, (y - 1, self.model.grid.width - 1))
          self.prob_enter = self.prob_enter * 0.5
          self.resident_status = False
          self.in_neighbourhood = False
          home.vacancy = True
        elif good_offer == 0 and self.econ_status < med_all:
          y = random.randrange(self.model.grid.height)
          if y != self.model.grid.height:
            self.model.grid.move_agent(self, (y, self.model.grid.width - 1))
          else:
            self.model.grid.move_agent(self, (y - 1, self.model.grid.width - 1))
          self.prob_enter = self.prob_enter * 0.5
          self.resident_status = False
          self.in_neighbourhood = False
          home.vacancy = True
        # aa = home.vacancies
        # if home.vacancy:
        #    home.vacancies = np.hstack((aa, np.asarray(0)))
        # else:
        #    home.vacancies = np.hstack((aa, np.asarray(1)))

      if not self.resident_status:
        residences = [res for res in self.model.schedule.agents if isinstance(res, r.Residential)]
        houses_for_sale = [obj for obj in residences if obj.vacancy]
        affordable_homes = [obj for obj in houses_for_sale if (obj.property_value <= self.econ_status)]
        if len(affordable_homes) != 0:
          new_house = np.random.choice(affordable_homes)  # pick a random affordable home to buy
          self.model.grid.move_agent(self, new_house.pos)  # move in!
          self.Home = new_house.pos  # update the location of your home.
          self.resident_status = True  # update your resident status
          new_house.vacancy = False
          self.in_neighbourhood = True
          # print('me:', self.econ_status, 'newhouse before:', new_house.property_value)
          new_house.property_value = self.econ_status  # possibly increase property value of your home!
          # print('newhouse after:', new_house.property_value)
        else:
          self.prob_enter = self.prob_enter * 0.8

  def enter_or_leave(self):
    if self.in_neighbourhood and not self.resident_status:  # if in neighbourhood but not resident
      d = decision(self.prob_enter)  # Will return False with probability 1-prob_enter
      if d == False:
        y = random.randrange(self.model.grid.height)
        if y != self.model.grid.height:
          self.model.grid.move_agent(self, (y, self.model.grid.width - 1))
        else:
          self.model.grid.move_agent(self, (y - 1, self.model.grid.width - 1))

    if not self.in_neighbourhood:
      self.in_neighbourhood = decision(self.prob_enter)
      if self.in_neighbourhood:
        streets = [street for street in self.model.schedule.agents if isinstance(street, s.Street)]
        st = np.random.choice(streets)
        self.model.grid.move_agent(self, st.pos)

  def shop(self):
    if self.in_neighbourhood:
      businesses = [business for business in self.model.schedule.agents if isinstance(business, c.Commercial)]
      popularity = [obj.popularity for obj in businesses]
      sums = sum(popularity)
      popularity = np.asarray(popularity) / sums
      store = np.random.choice(businesses, p=popularity)
      if store.econ_status <= self.econ_status:
        self.model.grid.move_agent(self, store.pos)
        self.prob_enter = self.prob_enter * 1.2  # increase probability of entering
        if store.popularity > self.model.share_threshold:
          sh = np.random.choice([0, 1], p=[0.8, 0.2])
          if sh == 0:
            self.share(store)
            self.yelped = True
      else:
        self.prob_enter = self.prob_enter * 0.8  # decrease probability of entering

  def go_home(self):
    if self.resident_status:
      self.model.grid.move_agent(self, self.Home)

  def share(self, store):
    yelp = 1.3 * store.popularity
    store.popularity = yelp
    store.yelped = True
    non_residents = [b for b in self.model.schedule.agents if isinstance(b, Person) and not b.in_neighbourhood]
    for b in non_residents:
      pyelp = 1.3 * b.prob_enter
      b.prob_enter = pyelp

  def step(self):
    # self.yelped = False
    action = np.random.choice([0, 1, 2, 3], p=[0.15, 0.3, 0.4, 0.15])
    if action == 0:
      self.buy_or_sell()
    if action == 1:
      self.enter_or_leave()
    if action == 2:
      self.shop()
    if action == 3:
      self.go_home()
