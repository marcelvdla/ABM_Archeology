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
# n_bins = 744
step=1

miners = []
total_miners = []
trades = []

for index, row in df.iterrows():
    # if row[1] != 0:
    #     population.append(row[2])
    # else: population.append(0)
    population.append(row[1])
    trades.append(row[8])

    if row[0] == 744:
        plt.clf()
        plt.scatter(population, trades, marker='.')
        plt.title(f"Population Density vs Trade")
        plt.xlabel("Population")
        plt.ylabel("Trades")
        plt.ylim((0,100))
        plt.xlim((0,100))
        plt.tight_layout()
        # plt.show()
        plt.savefig(f'trade_scatter/trade_population_step_{step}.png')
        population = []
        trades = []
        step += 1








        
    
    

