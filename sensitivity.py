# Imports

from SALib.sample import saltelli
from SALib.analyze import sobol

import sys
import time
import warnings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
from itertools import combinations

from mesa.batchrunner import BatchRunner
from model import GeoVictoria

# Functions for sensitivity analysis data logging

def get_data(problem, replicates, max_steps, distinct_samples):
    # Set the outputs
    model_reporters = {"Population": lambda m: [a.population for a in m.space.agents]}

    data = {}

    for i, var in enumerate(problem['names']):
        # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
        samples = np.linspace(*problem['bounds'][i], num=distinct_samples)
        
        # Keep in mind that wolf_gain_from_food should be integers. You will have to change
        # your code to acommodate for this or sample in such a way that you only get integers.
        
        batch = BatchRunner(GeoVictoria, 
                            max_steps=max_steps,
                            iterations=replicates,
                            variable_parameters={var: samples},
                            model_reporters=model_reporters,
                            display_progress=True)
        
        batch.run_all()
        
        data[var] = batch.get_model_vars_dataframe()
    
    return data

def get_data_sobol(problem, replicates, max_steps, distinct_samples):
    model_reporters = {"Population": lambda m: [a.population for a in m.space.agents]}
    
    # We get all our samples here
    param_values = saltelli.sample(problem, distinct_samples, calc_second_order=False)
    print(param_values)

    # READ NOTE BELOW CODE
    batch = BatchRunner(GeoVictoria, 
                        max_steps=max_steps,
                        variable_parameters={name:[] for name in problem['names']},
                        model_reporters=model_reporters)

    count = 0
    data = pd.DataFrame(index=range(replicates*len(param_values)), 
                                    columns=['stoch', 'alpha', 'beta', 'gamma'])
    data['Run'], data['Population'] = None, None

    for i in range(replicates):
        for vals in param_values: 
            # Change parameters that should be integers
            vals = list(vals)
            vals[2] = int(vals[2])
            # Transform to dict with parameter names and their values
            variable_parameters = {}
            for name, val in zip(problem['names'], vals):
                variable_parameters[name] = val

            batch.run_iteration(variable_parameters, tuple(vals), count)
            iteration_data = batch.get_model_vars_dataframe().iloc[count]
            iteration_data['Run'] = count # Don't know what causes this, but iteration number is not correctly filled
            data.iloc[count, 0:4] = vals
            data.iloc[count, 4:8] = iteration_data
            count += 1

            # clear_output()
            print(f'{count / (len(param_values) * (replicates)) * 100:.2f}% done')
    
    return data

def read_data(problem, convert=True):
    data = dict()
    for var in problem['names']:
        data[var] = pd.read_csv(f'Data/SA_data_{var}.csv', converters={'Population':ast.literal_eval})
        if convert:
            # print(data[var]['Population'].iloc[0])
            data[var]['gini'] = [gini(np.array(data[var]['Population'].iloc[i])) for i in range(len(data[var]['Population']))]

    return data

def gini(x):
    total = 0
    for i, xi in enumerate(x[:-1], 1):
        total += np.sum(np.abs(xi - x[i:]))
    return total / (len(x)**2 * np.mean(x))


# Functions for plotting the sensitivity analysis

def plot_param_var_conf(ax, df, var, param, i):
    """
    Helper function for plot_all_vars. Plots the individual parameter vs
    variables passed.

    Args:
        ax: the axis to plot to
        df: dataframe that holds the data to be plotted
        var: variables to be taken from the dataframe
        param: which output variable to plot
    """
    # print(df)
    x = df[var].groupby(var).mean().reset_index()[var]
    y = df[var].groupby(var).mean()[param]

    replicates = df[var].groupby(var)[param].count()
    err = (1.96 * df[var].groupby(var)[param].std()) / np.sqrt(replicates)

    ax.plot(x, y, c='k')
    ax.fill_between(x, y - err, y + err)

    ax.set_xlabel(var)
    ax.set_ylabel(param)

def plot_all_vars(df, param, problem):
    """
    Plots the parameters passed vs each of the output variables.

    Args:
        df: dataframe that holds all data
        param: the parameter to be plotted
    """

    f, axs = plt.subplots(4, figsize=(7, 15))
    
    for i, var in enumerate(problem['names']):
        # print(i, var, df[var])
        plot_param_var_conf(axs[i], df, var, param, i)

def plot_index(s, params, i, title=''):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        i (str): string that indicates what order the sensitivity is.
        title (str): title for the plot
    """

    if i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
    else:
        indices = s['S' + i]
        errors = s['S' + i + '_conf']
        plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=RuntimeWarning) 
    
    problem = {
        'num_vars': 4,
        'names': ['stoch', 'alpha', 'beta', 'gamma'],
        'bounds': [[0.5, 1.0], [1.0, 10.0], [0.05, 0.5], [0.0001, 0.001]]
    }
    
    sbl = int(sys.argv[1])
    replicates = int(sys.argv[2])
    max_steps = int(sys.argv[3])
    distinct_samples = int(sys.argv[4])

    start = time.time()

    if sbl:
        data = get_data_sobol(problem, replicates, max_steps, distinct_samples)
        data['gini'] = [gini(np.array(p)) for p in data['Population']]

        end = time.time()

        data.to_csv('Data/SA_sobol.csv')

        Si_pop = sobol.analyze(problem, data['gini'].values, print_to_console=True, calc_second_order=False)
        
        # First order
        plot_index(Si_pop, problem['names'], '1', 'First order sensitivity')
        plt.show()

        # Total order
        plot_index(Si_pop, problem['names'], 'T', 'Total order sensitivity')
        plt.show()  
    else:
        data = get_data(problem, replicates, max_steps, distinct_samples)

        end = time.time()

        for k in data:
            data[k]['gini'] = [gini(np.array(p)) for p in data[k]['Population']]
            data[k].to_csv(f'Data/SA_OFAT_{k}.csv')
        
        plot_all_vars(data, 'gini', problem)
        plt.show()

    print(f'Time taken to get data: {(end - start)/60} minutes')