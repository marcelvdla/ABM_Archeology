# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 16:19:45 2023

@author: arong
"""

#import imageio
import imageio.v2 as imageio
import os
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

gold_amounts = []
max_gold = []
avg_gold = []
n_bins = 50
step= 1

for index, row in df.iterrows():

    current_row = row[4][1:-1]
    current_row = current_row.split(" ")
    
    for gold in current_row:
        if gold != "":
            gold_amounts.append(float(gold))
            

    if row[0] == 744:
        max_gold.append(np.max(gold_amounts))
        avg_gold.append(np.mean(gold_amounts))
            
        # Plot Histogram of every Step
        plt.hist(gold_amounts , range=(0,50), bins=n_bins)
        plt.title(f"Gold Possession {step}")
        plt.xlabel("Amount of Gold")
        plt.ylabel("Number of Agents")
        plt.ylim((0,300))
        plt.tight_layout()
        # plt.savefig(f'gold_histograms/gold_possessions_step_{step}.png')
        plt.show()
        gold_amounts = []
        step += 1

# steps = step
# filenames = [f'gold_histograms/gold_possessions_step_{step}.png' for step in range(1, steps)]
# with imageio.get_writer('gold_possession.gif', mode='I', duration=0.2) as writer:
#     for filename in filenames:
#         image = imageio.imread(filename)
#         writer.append_data(image)
# writer.close()

plt.plot(np.arange(step-1), max_gold, label='max gold')
plt.plot(np.arange(step-1), avg_gold, label='avergae gold')
plt.title('Agent Gold Ownership')
plt.legend()
plt.xlabel("step")
plt.ylabel("amount of gold")
plt.grid('both')
# plt.savefig("agent_gold_dyn")
plt.show()