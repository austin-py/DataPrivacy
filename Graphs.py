from matplotlib import pyplot

import Stats


pyplot.plot(Stats.results['PR(>F)'], 'bo')
pyplot.legend()
pyplot.show()