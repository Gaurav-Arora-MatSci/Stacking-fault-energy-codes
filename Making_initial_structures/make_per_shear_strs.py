#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Gaurav Arora, Ph.D. email:gauravarora.1100@gmail.com
This code take CONTCAR as input and outputs two files used for calculating stacking fault energy. 
It works for 1,2,3,4 different atom types.This code only works for 108 atoms with 9 layers in 111 direction.
Please note that the name of the file should be CONTCAR and should be placed in the same folder with the code.
"""

def make_per_sheared_str():
    print('Warning: This code only works for 108 atom system with 9 layers in 111 direction')
    import pandas as pd
    import numpy as np
    import subprocess

    """
    # This command is based on linux, it reads the CONTCAR file and keeps the part that is needed further
    #It deletes the lines which are not needed like the zeroes at the end of the file
    #The only care which is to be taken is number, now it is 116: it is calculated by adding total
    #number of atoms + 8. For example, 108 + 8 = 116 is used here.
    """

    command = subprocess.getoutput("""head -n 116 CONTCAR > CONTCAR-1""")
    command = subprocess.getoutput("""mv CONTCAR-1 CONTCAR""")
    command = subprocess.getoutput("""rm CONTCAR-1""")

    #Reading the obtained CONTCAR

    f = open('CONTCAR')

    _ = f.readline()
    _ = f.readline()

    x_dim = f.readline().split()
    y_dim = f.readline().split()
    z_dim = f.readline().split()
    xx, xy, xz = float(x_dim[0]), float(x_dim[1]), float(x_dim[2])
    yx, yy, yz = float(y_dim[0]), float(y_dim[1]), float(y_dim[2])
    zx, zy, zz = float(z_dim[0]), float(z_dim[1]), float(z_dim[2])

    types = f.readline().split()
    types_of_atoms = len(types)

    natoms_ = f.readline().split()
    natoms_ = list(map(int, natoms_))
    natoms = sum(natoms_)

    dir_cart = f.readline()#type of coordinates

    info = f.readlines()
    x_coor, y_coor, z_coor = [], [], []
    for line in info:
        q = line.strip().split()
        x_coor.append(float(q[0]))
        y_coor.append(float(q[1]))
        z_coor.append(float(q[2]))
    f.close()


    #Converting Direct coordinated to cartesian coordinates
    # This methodolgy of converting Direct to caretsian is tested using the info from the OUTCAR file

    ## Calculating the length of the box
    x_len = np.sqrt(xx*xx + xy*xy + xz*xz)
    y_len = np.sqrt(yx*yx + yy*yy + yz*yz)
    z_len = np.sqrt(zx*zx + zy*zy + zz*zz)

    ## Converting direct coordinates to cartesian coordinates
    x_coor_cart = pd.DataFrame(np.array(x_coor) * x_len)
    y_coor_cart = pd.DataFrame(np.array(y_coor) * y_len)
    z_coor_cart = pd.DataFrame(np.array(z_coor) * z_len)


    coordinates_cart = np.array(pd.concat([x_coor_cart, y_coor_cart, z_coor_cart], axis =1))

    """Moving the z atoms back to boundaries before making a vacuumm so that all the atoms are in a same plane
    It is moved by the length of the cell in z-direction and in here the tolernace is set to be +-1 angstrom
    This can be changed as needed."""
    for k in range (0,natoms):
        if coordinates_cart[k,2] > -1 and coordinates_cart[k,2] < 1:
            coordinates_cart[k,2] = coordinates_cart[k,2] + z_len
        else:
            coordinates_cart[k,2] = coordinates_cart[k,2]

    vacuum = 6 #Defining the vacuum for the system

    ##Making perfect system POSCAR file
    f = open('POSCAR_per_vac', 'w')
    f.write('Perfect vacuum\n')
    f.write('1.00000\n')
    f.write(str(xx) + ' ' + str(xy) + ' ' + str(xz) + '\n')
    f.write(str(yx) + ' ' + str(yy) + ' ' + str(yz) + '\n')
    f.write(str(zx) + ' ' + str(zy) + ' ' + str(zz + vacuum) + '\n')


    if types_of_atoms == 1:
        f.write(str(types[0]) + '\n')
        f.write(str(natoms_[0]) + '\n')
    if types_of_atoms == 2:
        f.write(str(types[0]) + ' ' + str(types[1]) + '\n')
        f.write(str(natoms_[0]) + ' ' + str(natoms_[1]) + '\n')
    if types_of_atoms == 3:
        f.write(str(types[0]) + ' ' + str(types[1]) + ' ' + str(types[2]) + '\n')
        f.write(str(natoms_[0]) + ' ' + str(natoms_[1]) + ' ' + str(natoms_[2]) + '\n')
    if types_of_atoms == 4:
        f.write(str(types[0]) + ' ' + str(types[1]) + ' ' + str(types[2]) + ' ' + str(types[3]) + '\n')
        f.write(str(natoms_[0]) + ' ' + str(natoms_[1]) + ' ' + str(natoms_[2]) + ' ' + str(natoms_[3]) + '\n')

    f.write('Cartesian \n')
    coordinates = pd.DataFrame(coordinates_cart)
    coordinates = coordinates.to_string(index = False, header = False)
    f.write(coordinates)
    f.close()


    #shifting the plane based on z_values or making a Stacking fault
    cut_off_z_value = ((z_len / 9)*4) + 1 #In here define the Z-value above which all the atoms needs to be shifted.
    z_cut = cut_off_z_value

    #Shifting the atoms. This formaula is derived using reverse engineering from excel sheet.
    for k in range (0,natoms):
        if coordinates_cart[k,2] > z_cut:
            coordinates_cart[k,0] = coordinates_cart[k,0] + (x_len/12)
            coordinates_cart[k,1] = coordinates_cart[k,1] + (y_len/4)
        else:
            coordinates_cart[k,0] = coordinates_cart[k,0]
            coordinates_cart[k,1] = coordinates_cart[k,1]
     
    #shifting the atoms in x and y dir based on PBC     
    for k in range (0,natoms):
        if coordinates_cart[k,0] > x_len :
            coordinates_cart[k,0] = coordinates_cart[k,0] - x_len
        if coordinates_cart[k,1] > y_len :
            coordinates_cart[k,1] = coordinates_cart[k,1] - y_len
        else:
            coordinates_cart[k,0] = coordinates_cart[k,0]
            coordinates_cart[k,1] = coordinates_cart[k,1]
                

    #Wrting the shifted plane file with vacuum
    f = open('POSCAR_shif_vac' , 'w')
    f.write('Shifted vacuum\n')
    f.write('1.00000\n')
    f.write(str(xx) + ' ' + str(xy) + ' ' + str(xz) + '\n')
    f.write(str(yx) + ' ' + str(yy) + ' ' + str(yz) + '\n')
    f.write(str(zx) + ' ' + str(zy) + ' ' + str(zz + vacuum) + '\n')

    if types_of_atoms == 1:
        f.write(str(types[0]) + '\n')
        f.write(str(natoms_[0]) + '\n')
    if types_of_atoms == 2:
        f.write(str(types[0]) + ' ' + str(types[1]) + '\n')
        f.write(str(natoms_[0]) + ' ' + str(natoms_[1]) + '\n')
    if types_of_atoms == 3:
        f.write(str(types[0]) + ' ' + str(types[1]) + ' ' + str(types[2]) + '\n')
        f.write(str(natoms_[0]) + ' ' + str(natoms_[1]) + ' ' + str(natoms_[2]) + '\n')
    if types_of_atoms == 4:
        f.write(str(types[0]) + ' ' + str(types[1]) + ' ' + str(types[2]) + ' ' + str(types[3]) + '\n')
        f.write(str(natoms_[0]) + ' ' + str(natoms_[1]) + ' ' + str(natoms_[2]) + ' ' + str(natoms_[3]) + '\n')

    f.write('Cartesian \n')
    coordinates = pd.DataFrame(coordinates_cart)
    coordinates = coordinates.to_string(index = False, header = False)
    f.write(coordinates)
    f.close()
    return()
    


make_per_sheared_str()
