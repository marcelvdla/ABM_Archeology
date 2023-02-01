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
n_bins = 50
step=1

miners = []
total_miners = []

for index, row in df.iterrows():
    population.append(row[1])

    if row[0] == 744:

        # Plot Histogram of every Step
        plt.hist(population, range=(0,50), bins=n_bins)
        plt.title(f"Population Density Step {step}")
        plt.xlabel("Number of Agents")
        plt.ylabel("Number of Cells")
        plt.ylim((0,300))
        plt.tight_layout()
        plt.savefig(f'population_histograms/pop_density_step_{step}.png')
        plt.show()
        population = []
        step += 1
        
      





        
    
    

