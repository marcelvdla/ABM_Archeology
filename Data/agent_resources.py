# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 17:35:59 2023

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

agent_resources = []
max_resources = []
avg_resources = []
n_bins = 100
step= 1

for index, row in df.iterrows():

    current_row = row[5][1:-1]
    current_row = current_row.split(" ")
    
    for resources in current_row:
        if resources != "":
            agent_resources.append(float(resources))
            

    if row[0] == 744:
        max_resources.append(np.max(agent_resources))
        avg_resources.append(np.mean(agent_resources))
        
        # Plot Histogram of every Step
        plt.hist(agent_resources , range=(0,300), bins=n_bins)
        plt.title(f"Resource Possession {step}")
        plt.xlabel("Amount of Resources")
        plt.ylabel("Number of Agents")
        plt.ylim((0,500))
        plt.tight_layout()
        # plt.savefig(f'agent_resource_histograms/agent_resources_step_{step}.png')
        plt.show()
        agent_resources = []
        step += 1

# steps = step
# filenames = [f'agent_resource_histograms/agent_resources_step_{step}.png' for step in range(1, steps)]
# with imageio.get_writer('agent_resources.gif', mode='I', duration=0.2) as writer:
#     for filename in filenames:
#         image = imageio.imread(filename)
#         writer.append_data(image)
# writer.close()

plt.plot(np.arange(step-1), max_resources, label='max resources')
plt.plot(np.arange(step-1), avg_resources, label='avergae resources')
plt.title('Agent Resource Ownership')
plt.legend()
plt.xlabel("step")
plt.ylabel("number of resources")
plt.grid('both')
# plt.savefig("agent_resource_dyn")
plt.show()