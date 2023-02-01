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
max_trades = []
average_trades = []
total_trades = []
step=1


for index, row in df.iterrows():
    trades.append(row[8])
        
    if row[0] == 744:

        # Population Statistics
        max_trades.append(max(trades))
        total_trades.append(sum(trades))
        average_trades.append(np.mean(trades))

        trades = []
        step += 1
         
# Graph Total Population and Number of Miners
steps = np.arange(step-1)
plt.plot(steps, total_trades)
plt.title('Global Trade Dynamics')
plt.xlabel("step")
plt.ylabel("number of trades")
plt.grid('both')
plt.savefig("global_trade_dyn")
plt.show()

# Graph Max and Mean Population
plt.plot(steps, max_trades, label='max trades in a cell')
plt.plot(steps, average_trades, label='average trades in a cell')
plt.title('Cell Trade Dynamics')
plt.legend()
plt.xlabel("step")
plt.ylabel("number of trades")
plt.grid('both')
plt.savefig("cell_trade_dyn") 
plt.show()

        
    
    

