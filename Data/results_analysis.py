# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 15:51:14 2023

@author: arong
"""
import imageio.v2 as imageio
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

def gini(x):
    total = 0
    for i, xi in enumerate(x[:-1], 1):
        total += np.sum(np.abs(xi - x[i:]))
    return total / (len(x)**2 * np.mean(x))

iterations = 20

all_gini_gold = []
all_miner_fraction_gold = []

all_gini_no_gold = [] 
all_miner_fraction_no_gold = []

for i in range(1, iterations +1):

    df_gold = pd.read_csv(f'./runs_with_gold/data_None_{i}.csv',delimiter=",")
    
    df_no_gold = pd.read_csv(f'./runs_without_gold/data_None_{i}.csv',delimiter=",")
    
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
    miner_fraction_gold = []
    gini_gold = []

    
    for index, row in df_gold.iterrows():
        population_gold.append(row[1])
        miners_gold.append(row[2])
    
        if row[0] == 744:
            
            gini_gold.append(gini(np.array(population_gold)))
            miner_fraction_gold.append(np.sum(miners_gold)/np.sum(population_gold))
            population_gold = []
            miners_gold = []
            
    population_no_gold = []
    miners_no_gold = []
    miner_fraction_no_gold = []
    gini_no_gold = []
    
    for index, row in df_no_gold.iterrows():
        population_no_gold.append(row[1])
        miners_no_gold.append(row[2])
    
        if row[0] == 744:
            
            gini_no_gold.append(gini(np.array(population_no_gold)))
            miner_fraction_no_gold.append(np.sum(miners_no_gold)/np.sum(population_no_gold))
            population_no_gold = []
            miners_no_gold = []
    
    all_gini_gold.append(gini_gold)
    all_miner_fraction_gold.append(miner_fraction_gold)
    
    all_gini_no_gold.append(gini_no_gold)
    all_miner_fraction_no_gold.append(miner_fraction_no_gold)

# plot average and gini and miners for gold and no gold
avg_gini_gold = np.mean(all_gini_gold, axis = 0)
std_gini_gold = np.std(all_gini_gold, axis = 0)

avg_min_frac_gold = np.mean(all_miner_fraction_gold, axis = 0)
std_min_frac_gold = np.std(all_miner_fraction_gold, axis = 0)

avg_gini_no_gold = np.mean(all_gini_no_gold, axis = 0)
std_gini_no_gold = np.std(all_gini_no_gold, axis = 0)

avg_min_frac_no_gold = np.mean(all_miner_fraction_no_gold, axis = 0)
std_min_frac_no_gold = np.std(all_miner_fraction_no_gold, axis = 0)

steps = np.arange(100)

plt.plot(steps, avg_gini_gold, color='blue', label='Gini Coefficient')
plt.fill_between(steps, avg_gini_gold + std_gini_gold, avg_gini_gold - std_gini_gold, color='blue', alpha = 0.5)

plt.plot(steps, avg_gini_no_gold, color='green', label='Gini Coefficient Control')
plt.fill_between(steps, avg_gini_no_gold + std_gini_no_gold, avg_gini_no_gold - std_gini_no_gold, color='green', alpha = 0.5)

plt.plot(steps, avg_min_frac_gold, color='red', label='Miner Fraction')
plt.fill_between(steps, avg_min_frac_gold + std_min_frac_gold, avg_min_frac_gold - std_min_frac_gold, color='red', alpha = 0.5)

# plt.plot(steps, avg_min_frac_no_gold, color='orange', label='mean miner fraction control experiment')
# plt.fill_between(steps, avg_min_frac_no_gold + std_min_frac_no_gold, avg_min_frac_no_gold - std_min_frac_no_gold, color='orange', alpha = 0.5)

plt.legend()
plt.grid('both')
plt.xlabel("Step Number")
plt.ylabel("[-]")
plt.tight_layout()
plt.savefig('final_results.pdf', format="pdf")
plt.show()

# plot boxplot final gini values and do significance test

final_gini_gold = [gini_list[-1] for gini_list in all_gini_gold]
final_gini_no_gold = [gini_list[-1] for gini_list in all_gini_no_gold]

my_dict = {'Experiment': final_gini_gold, 'Control': final_gini_no_gold}

fig, ax = plt.subplots()
ax.boxplot(my_dict.values())
ax.set_xticklabels(my_dict.keys())
ax.grid(axis='both')
fig.savefig('boxplot.pdf', format="pdf")

# Perform significance tests 

statistic, p_value = ttest_ind(final_gini_gold, final_gini_no_gold, equal_var=False)
print(statistic)
print(p_value)