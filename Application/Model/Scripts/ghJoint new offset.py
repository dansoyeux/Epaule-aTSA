# -*- coding: utf-8 -*-
"""
Created on Fri May 26 12:57:10 2023

@author: user
"""

import numpy as np


# No rotation
# ghProth = np.array([0.02881235, -0.04817918, -0.03530596])

# middle rotation
ghProth = 0.001*np.array([29.241353 , -44.094887 , -35.305958])



gh = np.array([0.02339799, -0.05086301, -0.03438096])

RotMat = np.matrix([[-0.193467, 0.121863, 0.973509],
[-0.226877, 0.959804, -0.165235],
[-0.954514, -0.252834, -0.158043]])

gh_Rot = np.dot(gh,RotMat)

ghProth_Rot = np.dot(ghProth,RotMat)

Offset = ghProth_Rot - gh_Rot

print(Offset) 