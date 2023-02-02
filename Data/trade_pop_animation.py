import imageio.v2 as imageio
import os

steps = 200
filenames = [f'trade_scatter/trade_population_step_{step}.png' for step in range(1, steps)]
with imageio.get_writer('trade_population.gif', mode='I', duration=0.2) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
writer.close()