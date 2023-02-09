# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 13:13:58 2023

@author: arong
"""

import imageio.v2 as imageio
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

"""
This file reads the data from the 20 iterations of the experiment as well as 
the control experiment and plots the avergae maximum number of agents as well
as the maximum number of miners in any cell at every step. 
"""


iterations = 20

all_max_pop_gold = []
all_max_miner_gold = []

all_max_pop_no_gold = [] 


for i in range(1, iterations +1):

    df_gold = pd.read_csv(f'./experiment/data_None_{i}.csv',delimiter=",")
    
    df_no_gold = pd.read_csv(f'./control_experiment/data_None_{i}.csv',delimiter=",")
    
    # index 0 is cell_number
    # index 1 is population
    # index 2 is number of miners
    # index 3 is probability
    # index 4 is list with gold statistics
    # index 5 is list with resource statistics
    # index 6 is economic opportunity
    # index 7 is resources
    # index 8 is number of trades
    
    population_gold = []
    miners_gold = []
    
    max_miner_gold = []
    max_pop_gold = []

    
    for index, row in df_gold.iterrows():
        population_gold.append(row[1])
        miners_gold.append(row[2])
    
        if row[0] == 744:
            
            max_pop_gold.append(np.max(population_gold))
            max_miner_gold.append(np.max(miners_gold))
            population_gold = []
            miners_gold = []
            
    population_no_gold = []
    miners_no_gold = []
    
    max_pop_no_gold = []
    
    for index, row in df_no_gold.iterrows():
        population_no_gold.append(row[1])
    
        if row[0] == 744:
            
            max_pop_no_gold.append(np.max(population_no_gold))

            population_no_gold = []
            miners_no_gold = []
    
    all_max_pop_gold.append(max_pop_gold)
    all_max_miner_gold.append(max_miner_gold)
    
    all_max_pop_no_gold.append(max_pop_no_gold)

# plot average and gini and miners for gold and no gold
avg_max_pop_gold = np.mean(all_max_pop_gold, axis = 0)
std_max_pop_gold = np.std(all_max_pop_gold, axis = 0)

avg_max_miner = np.mean(all_max_miner_gold, axis = 0)
std_max_miner = np.std(all_max_miner_gold, axis = 0)

avg_max_pop_no_gold = np.mean(all_max_pop_no_gold, axis = 0)
std_max_pop_no_gold = np.std(all_max_pop_no_gold, axis = 0)


steps = np.arange(100)

plt.plot(steps, avg_max_pop_gold, color='blue', label='Largest Cell - Experiment')
plt.fill_between(steps, avg_max_pop_gold + std_max_pop_gold, avg_max_pop_gold - std_max_pop_gold, color='blue', alpha = 0.5)

plt.plot(steps, avg_max_pop_no_gold, color='green', label='Largest Cell - Control Experiment')
plt.fill_between(steps, avg_max_pop_no_gold + std_max_pop_no_gold, avg_max_pop_no_gold - std_max_pop_no_gold, color='green', alpha = 0.5)

plt.plot(steps, avg_max_miner, color='red', label='Max Miners in one cell - Experiment')
plt.fill_between(steps, avg_max_miner + std_max_miner, avg_max_miner - std_max_miner, color='red', alpha = 0.5)

plt.legend()
plt.grid('both')
plt.xlabel("Step Number")
plt.ylabel("Number of Agents")
plt.tight_layout()
plt.savefig('largest_cell_dynamics.pdf', format="pdf")
plt.show()

