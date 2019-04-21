import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner

import model as m

if __name__ == '__main__':
  batch_runner = BatchRunner(m.GentrifiedNeighbourhood,
    fixed_parameters={
      "num_people": 250,
      "people_outside": 100,
      "num_res": 260,
      "num_com": 70,
      "num_streets": 10,
      "width": 20,
      "height": 20
    },
    iterations=10,
    max_steps=10,
    model_reporters=m.model_reporters)
  batch_runner.run_all()

  run_data = batch_runner.get_model_vars_dataframe()
  # print(run_data.head())

  for reporter in m.model_reporters.keys():
    plt.scatter(run_data.Run, run_data[reporter], label=reporter)

  plt.xlabel('Iteration #')
  plt.legend()
  plt.show()
