import numpy as np
from mesa import Agent

import helpers
import person as p
import residential as r


class Commercial(Agent):
  """ An agent with fixed initial wealth."""

  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.econ_status = np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])
    if self.econ_status == 0:
      self.popularity = 0.2
      self.number_of_visitors = 1
    if self.econ_status == 1:
      self.popularity = 0.5
      self.number_of_visitors = 4
    if self.econ_status == 2:
      self.popularity = 0.8
      self.number_of_visitors = 8
    self.avgs = [self.number_of_visitors]
    self.av_ppl = np.average(np.asarray(self.avgs))

  def count_visits(self):
    same_space = self.model.grid.get_cell_list_contents([self.pos])
    visitors = [obj for obj in same_space if isinstance(obj, p.Person)]
    self.number_of_visitors = len(visitors)
    self.avgs = np.hstack((np.asarray(self.avgs), np.asarray(self.number_of_visitors)))
    if len(self.avgs) > 50:
      self.avgs = self.avgs[:-50]
    self.av_ppl = np.average(np.asarray(self.avgs))
    self.popularity = helpers.pop(self.av_ppl)
    self.econ_status = helpers.e_stat(self.popularity)

    neighbours = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=1)
    neighbours = [n for n in neighbours if isinstance(n, Commercial)]
    neighbourh = [n for n in neighbours if isinstance(n, r.Residential)]
    a = [obj.econ_status for obj in neighbours]
    b = [obj.property_value for obj in neighbourh]
    all_p_vals = np.hstack((np.asarray(a), np.asarray(b)))
    if len(all_p_vals) != 0:
      m = np.median(all_p_vals)
      choice = np.random.choice([0, 1])
      if choice == 0:
        if np.int(np.ceil(m)) > self.econ_status:
          self.econ_status = np.int(np.ceil(m))

  def step(self):
    # print('here in bus')
    self.count_visits()
