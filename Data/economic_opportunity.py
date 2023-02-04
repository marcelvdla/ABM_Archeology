# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 18:06:20 2023

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

economic_opp = []
sum_eco_opp = []
max_eco_opp = []
avg_eco_opp = []

n_bins = 100
step=1

for index, row in df.iterrows():
    economic_opp.append(row[6])

    if row[0] == 744:
        
        sum_eco_opp.append(np.sum(economic_opp))
        max_eco_opp.append(np.max(economic_opp))
        avg_eco_opp.append(np.mean(economic_opp))
        # Plot Histogram of every Step
        plt.hist(economic_opp, range=(0,250), bins=n_bins)
        plt.title(f"Economic Opportunity Distribution Step {step}")
        plt.xlabel("Economic Opportunity")
        plt.ylabel("Number of Cells")
        # plt.ylim((0,150))
        plt.tight_layout()
        # plt.savefig(f'economic_opp_histograms/eco_opp_step_{step}.png')
        plt.show()
        economic_opp = []
        step += 1

# steps = step
# filenames = [f'economic_opp_histograms/eco_opp_step_{step}.png' for step in range(1, steps)]
# with imageio.get_writer('eco_opp.gif', mode='I', duration=0.2) as writer:
#     for filename in filenames:
#         image = imageio.imread(filename)
#         writer.append_data(image)
# writer.close()

# Graph Global Dynamics
steps = np.arange(step-1)

plt.plot(steps, sum_eco_opp, label='sum of economic opportunity')
plt.legend()
plt.title('Total Economic Opportunity')
plt.xlabel("step")
plt.ylabel("Economic Opportunity")
plt.grid('both')
# plt.savefig("total_eco_opp_dyn")
plt.show()

# Graph Max and Mean Eco Opp
plt.plot(steps, max_eco_opp, label='max economic opportunity') 
plt.plot(steps, avg_eco_opp, label='mean economic opportunity')
plt.title('Economic Opportunity Dynamics')
plt.legend()
plt.xlabel("step")
plt.ylabel("Economic Opportunity")
plt.grid('both')
# plt.savefig("max_avg_eco_opp_dyn")
plt.show()