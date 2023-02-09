# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 13:35:11 2023

@author: arong
"""

import imageio.v2 as imageio
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

"""

"""

iterations = 20

population = []
all_trades = []


for i in range(1, iterations +1):

    df_gold = pd.read_csv(f'./experiment/data_None_{i}.csv',delimiter=",")
    
    # index 0 is cell_number
    # index 1 is population
    # index 2 is number of miners
    # index 3 is probability
    # index 4 is list with gold statistics
    # index 5 is list with resource statistics
    # index 6 is economic opportunity
    # index 7 is resources
    # index 8 is number of trades
    
    for index, row in df_gold.iterrows():
        pop = row[1]
        trades = row[8]
    
        if trades != 0:
            population.append(pop)
            all_trades.append(trades)
            
plt.scatter(population, all_trades, marker='.')
plt.xlabel("Population")
plt.ylabel("Trades")
plt.grid('both')
plt.tight_layout()
plt.savefig('population_trade_scatter.pdf', format="pdf")
plt.show()