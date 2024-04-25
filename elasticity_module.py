from cfe.estimation import drop_columns_wo_covariance
import pandas as pd
import numpy as np
import cfe
from cfe import Regression

def output_as_pickle(expenditure_data, household_data, path):
    x = pd.read_csv(expenditure_data)
    d = pd.read_csv(household_data)
    x.columns.name = 'j'
    d.columns.name = 'k'
    x = x.groupby('j',axis=1).sum()
    x = x.replace(0,np.nan)
    y = np.log(x.set_index(['i','t','m']))
    d.set_index(['i','t','m'],inplace=True)
    y = drop_columns_wo_covariance(y,min_obs=30)
    use = y.index.intersection(d.index)
    y = y.loc[use,:]
    d = d.loc[use,:]
    y = y.stack()
    d = d.stack()
    assert y.index.names == ['i','t','m','j']
    assert d.index.names == ['i','t','m','k']
    result = Regression(y=y,d=d)
    result.predicted_expenditures()
    result.to_pickle(path)