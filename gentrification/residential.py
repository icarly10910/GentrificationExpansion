import numpy as np
from mesa import Agent

import commercial as c


class Residential(Agent):
  """ A residence with property value and vacancy status"""

  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.property_value = np.random.choice([0, 1, 2], p=[0.8, 0.15,
                                                         0.05])  # JUST AN INITIALIZATION. WILL NEED TO FIX FOR INITIAL CONDITIONS
    self.vacancy = True
    # self.vacancies = np.array([0])

  def step(self):
    neighbours = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)
    neighbours = [n for n in neighbours if isinstance(n, Residential)]
    a = [obj.property_value for obj in neighbours]
    neighboursc = [n for n in neighbours if isinstance(n, c.Commercial)]
    b = [obj.property_value for obj in neighboursc]
    all_p_vals = np.hstack((np.asarray(a), np.asarray(b)))
    if len(all_p_vals) != 0:
      m = np.median(all_p_vals)
      choice = np.random.choice([0, 1])
      if choice == 0:
        if np.int(np.ceil(m)) > self.property_value:
          self.property_value = np.int(np.ceil(m))
    # if np.asarray(self.vacancies[:-20]).any() == np.zeros(len(self.vacancies[:-20])).any():
    #    if self.property_value > 0:
    #        self.property_value = self.property_value-1
    # print('property_value:',self.property_value,'vacant:', self.vacancy)
