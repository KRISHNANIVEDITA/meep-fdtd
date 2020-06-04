
import numpy as np
import matplotlib.pyplot as plt
import math
import cmath
from matplotlib.colors import ListedColormap
import meep as mp
import numpy as np
import sys
import h5py 

if len(sys.argv)<2:
    print("usage: python3 simpleExample.py <freq [GHz]> <depth [m]> <densityGradient [0,1]>")
    exit()
##################################################################################

                                                   # A function to  define the varying permittivity in the region around south pole
def indexret(p):
	n=1.78-0.43*(np.exp(-p.y/71))
	return mp.Medium(index=n)                              


###################################################################################

freq=float(sys.argv[1])				#give values  to variables
depth=float(sys.argv[2])

##################################################################################

y=np.linspace(-25,25,500)
y=np.round(y,decimals=1)+25			#calculate elevation angle
diff= (depth-y)
theta = np.arctan(diff/10)

###################################################################################


cell = mp.Vector3(50,50,0)
resolution=10

geometry = [mp.Block(center=mp.Vector3(),
                     size=mp.Vector3(50,50,0),
                     material=indexret)]					#//main part of simulation

pml_layers = [mp.PML(1.0)]


sources = [mp.Source(mp.GaussianSource(1/3, fwidth=0.1*1/3), component=mp.Ez,
                         center=mp.Vector3(-24,-25+depth),
		         size=mp.Vector3(0,1) )]


sim = mp.Simulation(cell_size=cell,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution,
		    boundary_layers=pml_layers,
		    #force_complex_fields = True
		    )


sim.run(until=100)

###################################################################################

ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
plt.figure(1)
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')										#map Ez component and plot it

###################################################################################
