# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def PickedPoint2AnyMatrix(dataPath=str, MatrixName=str):
    
    import Mat2AnyMatrix
    import meshlab_pickedpoints
    import numpy as np
    
    data = meshlab_pickedpoints.load(dataPath)
    
    mat = np.zeros([len(data),3])
    names = []
    
    for i in range(len(data)):
        
        for j in range(3):
            mat[i,j]=data[i]['point'][j]
        
        names.append(data[i]['name'])
    
    Mat2AnyMatrix.Mat2AnyMatrix(MatrixName,mat,names)
    
# PickedPoint2AnyMatrix("humerus_generique_picked_points.pp","Points0")