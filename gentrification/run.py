import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner

import model as m


def plot_everything(run_data):
  plt.figure()
  plt.xlabel('Iteration #')

  for reporter in m.model_reporters.keys():
    plt.plot(run_data.Run, run_data[reporter], '-o')

  plt.legend()


def plot_key_measures(run_data):
  plt.figure()
  plt.xlabel('Iteration #')

  for reporter in ['Median Property Value', 'Median Economic Status of Residents', 'Median Economic Status of Visitors']:
    plt.plot(run_data.Run, run_data[reporter], '-o')

  plt.legend()


def plot_dependence(run_data, var):
  plt.figure()
  plt.xlabel(var)

  mean_values = run_data.groupby(var).mean()

  for reporter in [
    'Median Property Value',
    'Median Economic Status of Residents',
    'Median Economic Status of Visitors',
    'Fraction of vacant homes with high property value',
  ]:
    print(run_data.set_index([var, reporter]))
    plt.plot(mean_values[reporter], '-o')

  plt.legend()


def run():
  batch_runner = BatchRunner(m.GentrifiedNeighbourhood,
    fixed_parameters={
      "num_people": 250,
      "num_res": 260,
      "num_com": 70,
      "num_streets": 2,
      "width": 20,
      "height": 20
    },
    variable_parameters={
      "people_outside": range(0, 700, 100)
    },
    iterations=1,
    max_steps=50,
    model_reporters=m.model_reporters)

  batch_runner.run_all()
  return batch_runner.get_model_vars_dataframe()


if __name__ == '__main__':
  run_data = run()

  # plot_everything(run_data)
  # plot_key_measures(run_data)
  plot_dependence(run_data, 'people_outside')

  plt.show()
