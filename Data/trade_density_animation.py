# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:20:17 2023

@author: arong
"""

#import imageio
import imageio.v2 as imageio
import os

steps = 200
filenames = [f'trade_histograms/trade_density_step_{step}.png' for step in range(1, steps)]
with imageio.get_writer('trade_desnity.gif', mode='I', duration=0.2) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
writer.close()