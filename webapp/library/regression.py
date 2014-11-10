__author__ = 'hendro'

import pandas as pd
import statsmodels.formula.api as sm
import math

def lm_independent_variable(tweets, variable_name, data, plotting=False):
    model = sm.ols(formula='{} ~ tweets'.format(variable_name), data=data).fit()

    return math.ceil(model.predict(pd.DataFrame({'tweets':[tweets]})))

def lm_dependent_variable(sessions, unique_pv, tweets, data, plotting=False, verbose=False):
    model = sm.ols(formula='total_pv ~ total_sessions + tweets', data=data).fit()

    if verbose:
        print "%s\n" % model.summary()

    return math.ceil(model.predict(pd.DataFrame({'total_sessions':[sessions], 'total_unq_pv':[unique_pv], 'tweets':[tweets]})))



