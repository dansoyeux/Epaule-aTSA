# -*- coding: utf-8 -*-
"""
Created on Fri May 26 11:02:16 2023
https://programming-surgeon.com/en/sphere-fit-python/

@author: user
"""

import numpy as np
import sphere_fitting

# import numpy-stl

from stl import mesh
# use numpy-stl to manipulate surfaces

#Nom du fichier STL à importer
sphere_stl = mesh.Mesh.from_file('GleneCeraver_T3_Surface.stl')
# sphere_stl = mesh.Mesh.from_file('TeteCeraver_51_Surface.stl')



# read stl file
sphere_points = sphere_stl.points.reshape([-1, 3])
# read point clouds of the stl
# print(sphere_points)

# [[ 154.80566  -124.725586  192.21085 ]
# [ 153.9873   -124.725586  192.33838 ]
# [ 153.9873   -124.098175  193.5     ]
# ...
# [ 157.29794  -124.725586  235.5     ]
# [ 157.26074  -124.711945  235.5     ]
# [ 157.26074  -124.725586  235.52    ]]
# point vectors of the point clouds

radius, center = sphere_fitting.sphere_fit(sphere_points)
# calculate by sphere_fit function in fitting.py
print(radius*2)
# 23.087794980492543
print(center)
# [ 154.15674832 -133.40106545  213.64071843]

# sphere_fitting.draw_sphere(radius, center)