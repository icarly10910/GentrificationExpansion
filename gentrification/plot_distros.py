import helpers

import matplotlib.pyplot as plt

plt.subplot(2, 3, 5)

for i, mean in enumerate([0, 0.5, 1, 1.5, 2]):
  a = [helpers.econ_status_choice(mean) for n in range(0, 500)]
  plt.subplot(2, 3, i + 1)
  plt.title('mean: %.1f  stddev: 1' % mean)
  plt.xticks([0, 1, 2])
  plt.hist(a)

plt.show()
