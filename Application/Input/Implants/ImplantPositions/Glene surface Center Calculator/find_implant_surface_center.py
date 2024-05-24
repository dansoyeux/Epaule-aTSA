# -*- coding: utf-8 -*-
"""
Script from the website
https://programming-surgeon.com/en/sphere-fit-python/
"""

import numpy as np
import sphere_fitting

# import numpy-stl

from stl import mesh
# use numpy-stl to manipulate surfaces

#Nom du fichier STL à importer
# STL_file_name = 'GleneCeraver_T3_Surface'
STL_file_name = 'TeteCeraver_51_Surface'


sphere_stl = mesh.Mesh.from_file(f"{STL_file_name}.stl")

# read stl file
sphere_points = sphere_stl.points.reshape([-1, 3])


# calculate by sphere_fit function in fitting.py
radius, center = sphere_fitting.sphere_fit(sphere_points)

print(f"The position of the center of the implant '{STL_file_name}' is (in mm):\n x = {center[0]}\n y = {center[1]} \n z = {center[2]}")

# Saves the sphere in a .asc file to be opened in meshlab
sphere_fitting.draw_sphere(radius, center, f"sphere_{STL_file_name}")
