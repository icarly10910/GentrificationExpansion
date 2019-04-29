import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner

import model as m

import numpy as np

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


def format_decimal(value):
  return "{0}".format(str(round(value, 1) if value % 1 else int(value)))


def plot_dependence(run_data, fixed_parameters, var):
  plt.figure()
  plt.xlabel(var)

  mean_values = run_data.groupby(var).mean()

  for reporter in [
    # 'Median Property Value',
    'Mean Property Value',
    # 'Median Economic Status of Residents',
    'Mean Economic Status of Residents',
    # 'Median Economic Status of Visitors',
    'Mean number of visitors to businesses',
    'Fraction of people in the neighborhood',
    'Fraction of vacant homes with high property value',
  ]:
    print(run_data.set_index([var, reporter]))
    plt.plot(mean_values[reporter], '-o')

  # place a text box in upper left in axes coords, containing fixed parameter values
  params_string = '\n'.join(['%s: %s' % (name, format_decimal(value)) for
    name, value in sorted(fixed_parameters.items()) if name not in ['height', 'width']])
  plt.text(0.05, 0.95, params_string, transform=plt.axes().transAxes, #fontsize=12,
    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

  plt.legend()


def run():
  runner = BatchRunner(m.GentrifiedNeighbourhood,
    fixed_parameters={
      "num_people": 250,
      "people_outside": 100,
      "outside_person_econ_dist_mean": 1.0,
      # "share_threshold": 0.7,
      "num_residential": 260,
      "num_commercial": 70,
      "num_streets": 10,
      "width": 20,
      "height": 20
    },
    variable_parameters={
      # "outside_person_econ_dist_mean": np.arange(0.0, 2.0, 1.0)
      "share_threshold": np.linspace(0.0, 1.0, num=5)
    },
    iterations=1,
    max_steps=20,
    model_reporters=m.model_reporters)

  runner.run_all()
  return runner


if __name__ == '__main__':
  runner = run()

  # plot_everything(run_data)
  # plot_key_measures(run_data)

  # plot_dependence(runner.get_model_vars_dataframe(),
  #   runner.fixed_parameters, 'outside_person_econ_dist_mean')
  plot_dependence(runner.get_model_vars_dataframe(),
    runner.fixed_parameters, 'share_threshold')
  plt.show()
