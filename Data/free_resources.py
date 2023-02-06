# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 18:25:10 2023

@author: arong
"""

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



free_resources = []
sum_free_res = []
max_free_res = []
avg_free_res = []

n_bins = 100
step=1


for index, row in df.iterrows():

    free_resources.append(row[7])

    if row[0] == 744:
        
        sum_free_res.append(np.sum(free_resources)) 
        max_free_res.append(np.max(free_resources))
        avg_free_res.append(np.mean(free_resources))
        
        # Plot Histogram of every Step
        plt.hist(free_resources, range=(0,250), bins=n_bins)
        plt.title(f"Free Resources Step {step}")
        plt.xlabel("Resources")
        plt.ylabel("Number of Cells")
        # plt.ylim((0,150))
        plt.tight_layout()
        # plt.savefig(f'free_resources_histograms/free_res_step_{step}.png')
        # plt.show()
        free_resources = []
        step += 1

# steps = step
# filenames = [f'free_resources_histograms/free_res_step_{step}.png' for step in range(1, steps)]
# with imageio.get_writer('free_resources.gif', mode='I', duration=0.2) as writer:
#     for filename in filenames:
#         image = imageio.imread(filename)
#         writer.append_data(image)
# writer.close()

# Graph Global Dynamics
steps = np.arange(step-1)

plt.plot(steps, sum_free_res, label='sum of free resources')
plt.legend()
plt.title('Total Free Resources')
plt.xlabel("step")
plt.ylabel("Free Resources")
plt.grid('both')
plt.savefig("total_free_res_dyn")
plt.show()

# Graph Max and Mean Eco Opp
plt.plot(steps, max_free_res, label='max free resources') 
plt.plot(steps, avg_free_res, label='mean free resources')
plt.title('Free Resource Dynamics')
plt.legend()
plt.xlabel("step")
plt.ylabel("Free Resources")
plt.grid('both')
plt.savefig("max_avg_free_res_dyn")
plt.show()