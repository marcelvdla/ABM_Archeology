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
n_bins = 20
step=1

for index, row in df.iterrows():
    if row[0] < 744:
        population.append(row[1])
    else:
        print(max(population))
        print(sum(population))
        plt.hist(population, range=(0,50), bins=n_bins)
        plt.title(f"Population Desnity Step {step}")
        plt.ylim((0,750))
        plt.show()
        population = []
        step += 1
        
    
    

