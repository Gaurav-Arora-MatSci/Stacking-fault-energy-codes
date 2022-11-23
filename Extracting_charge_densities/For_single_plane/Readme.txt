Charge_densities_for_a_single_plane.py code can be used to extract the charge densities for a single plane in a given direction. The input needed for running the code are:'name of the file','direction', and the plane number. The name of the file should be input in the last line of the code along with the direction and plane number. This code outputs an excel file in which points along x direction, y direction and density is contained. This data file can late be used to plot charge density profile using contour plots.

Format of excel file:
To extarct X positions, Y positions and denisty, the returend array or the data in the excel has to be split horizontally equally as shown below.

|---------|
| X_array |     
|---------|
| Y_array |
|---------|
| Charge  |
| density |
-----------
