# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 18:39:21 2023

@author: arong
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('./data_None.csv',delimiter=",")

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
n_bins = 50
step=1


for index, row in df.iterrows():
    trades.append(row[8])

    if row[0] == 744:

        # Plot Histogram of every Step
        plt.hist(trades, range=(0,50), bins=n_bins)
        plt.title(f"Trade Desnity Step {step}")
        plt.xlabel("Number of Agents")
        plt.ylabel("Number of Cells")
        plt.ylim((0,300))
        plt.tight_layout()
        plt.savefig(f'trade_histograms/trade_density_step_{step}.png')
        plt.show()
        trades = []
        step += 1
        
      





        
    
    

