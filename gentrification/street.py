from mesa import Agent

import person as p


class Street(Agent):
  """ a square of street for window shoppers """

  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.number_of_visitors = 0

  def count_visits(self):
    same_space = self.model.grid.get_cell_list_contents([self.pos])
    visitors = [obj for obj in same_space if isinstance(obj, p.Person)]
    self.number_of_visitors = len(visitors)

  def step(self):
    self.count_visits()
