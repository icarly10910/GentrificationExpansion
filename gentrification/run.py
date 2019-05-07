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
    'Mean Economic Status of Visitors',
    # 'Mean number of visitors to businesses',
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

  plt.legend(loc='upper center')


def run(variable_key, variable_value):
  fixed_parameters = {
    "people_inside": 200,
    "people_outside": 200,
    "outside_person_econ_dist_mean": 1.0,
    "share_threshold": 0.7,
    "property_value_dist_mean": 0.0,
    "num_residential": 250,
    "num_commercial": 50,
    "num_streets": 10,
    "width": 20,
    "height": 20
  }

  # Remove variable parameters from fixed parameters
  del fixed_parameters[variable_key]

  runner = BatchRunner(m.GentrifiedNeighbourhood,
    fixed_parameters=fixed_parameters,
    variable_parameters={variable_key: variable_value},
    iterations=10,
    max_steps=20,
    model_reporters=m.model_reporters)

  runner.run_all()
  return runner


if __name__ == '__main__':
  variable_parameters = {
    "outside_person_econ_dist_mean": np.linspace(0.0, 2.0, 10),
    "share_threshold": np.linspace(0.0, 1.0, 10),
    "people_outside": np.linspace(0, 500, 10),
    "num_residential": np.linspace(200, 320, 10),
    "num_commercial": np.linspace(20, 120, 10),
    "property_value_dist_mean": np.linspace(0.0, 2.0, 10),
  }
  num_rows = len(variable_parameters.items())

  for i, (variable_key, variable_value) in enumerate(variable_parameters.items()):
    runner = run(variable_key, variable_value)
    plot_dependence(runner.get_model_vars_dataframe(), runner.fixed_parameters, variable_key)

  plt.show()
