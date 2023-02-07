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


def gini(x):
    total = 0
    for i, xi in enumerate(x[:-1], 1):
        total += np.sum(np.abs(xi - x[i:]))
    return total / (len(x)**2 * np.mean(x))

iterations = 20

all_gini_gold = []
all_miner_fraction_gold = []

all_gini_no_gold = [] 

for i in range(1, iterations +1):

    df_gold = pd.read_csv(f'./runs_with_gold/data_None_{i}.csv',delimiter=",")
    
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
    
    all_gini_gold.append(gini_gold)
    all_miner_fraction_gold.append(miner_fraction_gold)


# plot average and gini and miners for gold and no gold

# plot boxplot final gini values and do significance test
