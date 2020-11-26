import pandas as pd
import numpy as np
import seaborn as sea
from matplotlib import pyplot as plt

results = pd.read_csv('/Users/koendereus/Desktop/session3/results_lexical_decision.csv')
results.rename(columns = {'Unnamed: 0': 'trial_number'}, inplace = True)

# Create a list of conditions
conditions = [
    results['trial'].str.startswith('NW'),
    results['trial'].str.startswith('LF'),
    results['trial'].str.startswith('HF')
]

# Create a list of values we want to assign to each condition
values = ['NW', 'LF', 'HF']

# Create a new column and assign values to the conditions
results['condition'] = np.select(conditions, values)
print(results)

# Make dataset of summary stats
summary = results.groupby(by = 'condition').aggregate(
    mean_RT = pd.NamedAgg('reaction_time', np.mean),
    std_RT = pd.NamedAgg('reaction_time', np.std),
)
summary.reset_index(inplace = True)
print(summary)

# Produce plots to visualise data
sea.boxplot(x = 'condition', y = 'reaction_time', data = results).set(xlabel = '', ylabel = 'Reaction time (s)')
plt.savefig('boxplots.png')

histogram = sea.catplot(data = results, kind = 'bar', x = 'condition', y = 'reaction_time', ci = 'sd')
histogram.set_axis_labels('', 'Reaction time (s)')
plt.savefig('histograms.png')