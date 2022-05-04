import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

if __name__ == '__main__':

    # 1. POST DATA
    data = pd.read_csv('data/long.csv', sep=';')

    # Which scenario came first, for each couple?
    '''Why care? Because the first scenario is the only 'unbiased' one, 
    so, it may be interesting to see if the effects are perhaps different there.'''
    first = dict(enumerate([1,3,2,
             1,3,2,
             3,2,1,
             3,2,1,
             2,1,3,
             2,1,3],start=1))
    def is_first(row):
        if row['condition'] == first[row['couple']]:
            return True
        return False
    data['is_first'] = data.apply(is_first, axis=1)

    # Filter on data from first scenario (comment out if unwanted)
    data_first_only = data.loc[data.is_first == True]

    # Filter on data where someone was mimicking (comment out if unwanted)
    #data_first_only = data_first_only.loc[data_first_only.pp.isin([1,2,3,4,5,6,13,14,15,16,17,18])]

    # Plot difference in scores (0 = no chameleon, 1 = chameleon)
    fig, ax = plt.subplots(1,3, figsize=(10,4))
    for i, dep in enumerate(['positive_perception','copresence','bond']):
        sns.violinplot(data=data_first_only, x='chameleon', y=dep, ax=ax[i])
    plt.tight_layout()
    sns.despine(left=True)
    plt.show()

    # Independent samples t-test
    df = data_first_only
    ttest_ind(df.loc[df.chameleon == 1].positive_perception,
              df.loc[df.chameleon == 0].positive_perception)

    # OBJECTIVE DATA
    objective = pd.read_csv('data/karma_objective.csv', sep='\t')
    objective_scen1 = objective.loc[objective.scenario == 1]
    objective_scen1.columns = ['couple','scenario','_','mimicker','first_offer_from','first_offer',
                               'time_to_first_offer','total_duration','consensus','gender1','gender2']
    objective_scen1.consensus = pd.to_numeric(objective_scen1.consensus, downcast='integer')
    sns.stripplot(data=objective_scen1, x='mimicker',y='consensus')
    plt.show()