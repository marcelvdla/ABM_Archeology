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

population = []
max_population = []
total_population = []
mean_population = []
step=1

miners = []
total_miners = []

for index, row in df.iterrows():
    population.append(row[1])
    miners.append(row[2])
        
    if row[0] == 744:

        # Population Statistics
        max_population.append(max(population))
        total_population.append(sum(population))
        mean_population.append(np.mean(population))
        
        # Plot Histogram of every Step
        n_bins = 20
        plt.hist(population, range=(0,50), bins=n_bins)
        plt.title(f"Population Desnity Step {step}")
        plt.ylim((0,750))
        plt.show()
        population = []
        step += 1
        
        # number of miners
        total_miners.append(sum(miners))
        miners = []        


# Graph Total Population and Number of Miners
steps = np.arange(step-1)
plt.plot(steps, total_population, label='population size')
plt.plot(steps, total_miners, label='number of miners')
plt.title('Population Dynamics 1')
plt.legend()
plt.grid('both')
plt.show()

# Graph Max and Mean Population
plt.plot(steps, max_population, label='max population in a cell')
plt.plot(steps, mean_population, label='mean population in a cell')
plt.title('Population Dynamics 2')
plt.legend()
plt.grid('both')
plt.show()

        
    
    

