#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:31:13 2022

@author: garora
"""

def ploting_charge_density(data, str_id, max_intensity):

    #Importing the modules 
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
    #Reading the data from the previous saved excel file containing
    #information about X_array, Y_array, and density for a given plane
    
    data = pd.read_excel(str(data))
    
    #getting the length of the data to divide it equally in 3 parts
    total_len = len(data)
    chunk_size = int(total_len/3)
    
    #Extracting the density from the data
    density = data.iloc[2 * chunk_size : 3 * chunk_size,:]
    
    #Setting the maximum intensity for the density data 
    density_array = np.array(density)
    density_array[np.where(density_array > max_intensity)] = max_intensity
    
    #Extracting X and Y array information
    x_value = data.iloc[0: 1 * chunk_size,:]
    y_value = data.iloc[1 * chunk_size : 2 * chunk_size,:]
    
    #Plotting the image
    fig,ax = plt.subplots(1,1,figsize = (10,3.75))
    style  = 'gist_rainbow' #style can be chnaged here for contour plot
    
    figure_ = ax.contourf(x_value, y_value, density_array, 200, cmap = style)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('Charge_density_image_str_id-' + str(str_id) + '.png', format = "png")
    plt.close()
    del figure_
    return()

ploting_charge_density('density.xlsx', 1, 0.65)
    