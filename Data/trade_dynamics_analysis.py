# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 13:58:04 2023

@author: arong
"""

import imageio.v2 as imageio
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

"""
This file reads the data from the 20 iterations of the experiment and plots
the average sum of trades over the number of steps.
"""


iterations = 20

all_trade_sums = []

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
    
    trades = []
    trade_sums = []

    for index, row in df_gold.iterrows():
        trades.append(row[8])

    
        if row[0] == 744:
            
            trade_sums.append(np.sum(trades))
            trades = []
    
    all_trade_sums.append(trade_sums)

# plot average and gini and miners for gold and no gold
avg_sum_trades = np.mean(all_trade_sums, axis = 0)
std_sum_trades = np.std(all_trade_sums, axis = 0)


steps = np.arange(100)

plt.plot(steps, avg_sum_trades, color='b')
plt.fill_between(steps, avg_sum_trades + std_sum_trades, avg_sum_trades - std_sum_trades, color='b', alpha = 0.5)

plt.grid('both')
plt.xlabel("Step Number")
plt.ylabel("Sum of Trades")
plt.tight_layout()
plt.savefig('trade_dynamics.pdf', format="pdf")
plt.show()