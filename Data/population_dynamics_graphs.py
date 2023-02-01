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

population = []
max_population = []
total_population = []

step=1

miners = []
total_miners = []
max_miners = []

for index, row in df.iterrows():
    population.append(row[1])
    miners.append(row[2])
        
    if row[0] == 744:

        # Population Statistics
        max_population.append(max(population))
        total_population.append(sum(population))

        population = []
        step += 1
        
        # number of miners
        total_miners.append(sum(miners))
        max_miners.append(max(miners))
        miners = []        


# Graph Total Population and Number of Miners
steps = np.arange(step-1)
plt.plot(steps, total_population, label='population size')
plt.plot(steps, total_miners, label='number of miners')
plt.title('Global Population Dynamics')
plt.legend()
plt.xlabel("step")
plt.ylabel("number of agents")
plt.grid('both')
# plt.savefig("global_pop_dyn") # change name
plt.show()

# Graph Max and Mean Population
plt.plot(steps, max_population, label='max population in a cell')
plt.plot(steps, max_miners, label='max miners in a cell')
plt.title('Cell Population Dynamics')
plt.legend()
plt.xlabel("step")
plt.ylabel("number of agents")
plt.grid('both')
# plt.savefig("cell_pop_dyn") # change name
plt.show()

        
    
    

