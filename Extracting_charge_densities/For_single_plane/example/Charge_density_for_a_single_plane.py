#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Gaurav Arora, Ph.D. Email: gauravarora.1100@gmail.com 
"""
"""
This code can be used to extract charge denisty information in the form of grid for any given three perpendicular direction (a,b,c).
This code takes three inputs i.e, name of the CHGCAR file, the direction, and the plane number and returns charge density of a specified plane and the name of the CHGCAR file.
This code is modified version of the code which was downloaded from the internet.
This code appends the X_array, Y_array (representing dimensions in space) and the charge denisty vertically, which is stored in one array. 
The returned array is 3 dimensional. For example [224,480,60], where
224 are the total number of planes for which the density is calculates, and (480,60) is the dimension of charge density for a plane.To extarct X positions, Y positions and denisty, 
the returend array has to be split horizontally equally as shown below.

|---------|
| X_array |     
|---------|
| Y_array |
|---------|
| Charge  |
| density |
-----------

"""
def Charge_densities_from_CHGCAR_single_plane(str_id, direction,plane_number):
    print(f'##### Reading data from {str_id} file ######') 
    import sys
    import numpy as np
    from ase.calculators.vasp import VaspChargeDensity
    import pylab
    import pandas as pd
    import time
    
    init_time = time.time()
    
    counter = 0
    # Name of the CHGCAR file 
    inputstr = str(str_id)
    sys.stdout.flush()
    
    # Define the vasp charge density object
    # Read density and atoms
    vasp_charge = VaspChargeDensity(inputstr)
    density = vasp_charge.chg[-1]
    atoms = vasp_charge.atoms[-1]
    del vasp_charge
    
    # Read size of grid
    ngridpts = np.array(density.shape)
    #print (ngridpts)
    
    # Read total number of grid points
    totgridpts = ngridpts.prod()
    
    # Read scaling factor and unit cell
    unit_cell=atoms.get_cell()
    
    #Defining the plane for slicing, for SFE it's c plane
    inputstr = str(direction)
    normal=inputstr.strip().lower()[0]
    inormal = 'abc'.find(normal)
    if inormal==0:
       iplane1 = 1
       iplane2 = 2
    elif inormal==1:
       iplane1 = 0
       iplane2 = 2
    elif inormal==2:
       iplane1 = 0
       iplane2 = 1
    else:
       raise SyntaxError('Lattice vector must be either a, b, or c.')
    #    if inormal==-1:
    #        raise SyntaxError('Lattice vector must be either a, b, or c.')
    #    iplane1 = (inormal+1)%3
    #    iplane2 = (inormal+2)%3
    #print ("Plotting planes in %s direction" % normal)
    
    cell_lengths=np.sqrt(np.dot(unit_cell,unit_cell.transpose()).diagonal())
    
    #Getting all the possible z values for slicing the plane
    # Change here in order to get different number of planes, not all
    z_values = np.linspace(0,cell_lengths[inormal],num = ngridpts[inormal])
    
    # Define here the plane number by looking the z_values for which you want the charge density, in this case its 124th plane
    z_values = z_values[int(plane_number):int(plane_number)+1]
    
    #defining variable for storing all values of xarray,yarray,density2D
    charge_density_for_all_planes = []
    for value in z_values:
        inputstr = str(value)
        counter = counter + 1
        #print(i)
        #print(i)
        #inputstr=input("Enter the distance in Angstroms along this vector to make the cut.\n")
        try:
            distance=float(inputstr.strip())
        except:
            print ("Syntax error. Quiting program.")
            sys.exit(0)
    
        #Then find integer corresponding to closest plane on grid
        plane_index=int(round(ngridpts[inormal]*distance/cell_lengths[inormal]))%ngridpts[inormal]
        #Write out which distance we are actually using
        #print ("Using index %d which corresponds to a distance of %f Angstroms.\n" % (plane_index,float(plane_index)/float(ngridpts[inormal])*cell_lengths[inormal]))
        
        #Cut out plane from 3D real space density
        if inormal==0:
            density2D=density[plane_index,:,:]
        elif inormal==1:
            density2D=density[:,plane_index,:].T
            density2D=density[:,plane_index,:]
        else:
            density2D=density[:,:,plane_index]
    
        #Make arrays of x and y values
        #First vector will be plotted as the x-axis
        #Must be same dimensions as density2D
        #Find projection of second vector onto first
        yontox=np.dot(unit_cell[iplane1],unit_cell[iplane2].T)/cell_lengths[iplane1]
        #Find component of yvector perpendicular to xvector
        ynormal=np.cross(unit_cell[iplane1],unit_cell[iplane2].T)/cell_lengths[iplane1]
        ynormal=np.sqrt(np.dot(ynormal,ynormal.T))
        #Make arrays containing x and y values for each point
        xarray=np.zeros((ngridpts[iplane1],ngridpts[iplane2]),np.float64)
        yarray=np.zeros((ngridpts[iplane1],ngridpts[iplane2]),np.float64)
        for i in range(ngridpts[iplane1]):
            for j in range(ngridpts[iplane2]):
                xarray[i][j]=float(i)/float(ngridpts[iplane1])*cell_lengths[iplane1]+float(j)/float(ngridpts[iplane2])*yontox
                yarray[i][j]=float(j)/float(ngridpts[iplane2])*ynormal
        xarray_pd = pd.DataFrame(xarray)
        yarray_pd = pd.DataFrame(yarray)
        density2D_pd = pd.DataFrame(density2D)
        combined_pd = pd.concat([xarray_pd, yarray_pd, density2D_pd],axis = 0)
        charge_density_for_all_planes.append(combined_pd)
        #print(counter)
    final_time = time.time()
    total_time = final_time - init_time
    print("Total time in sec = {:.2f}".format(total_time))
    return(charge_density_for_all_planes, str_id)

charge_density, str_id = Charge_densities_from_CHGCAR_single_plane('CHGCAR-1', 'c', 124)
import numpy as np
np.savetxt('X_array-Y_array-density.txt',charge_density[0])

