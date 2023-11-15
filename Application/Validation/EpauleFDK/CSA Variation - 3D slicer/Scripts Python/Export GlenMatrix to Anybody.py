# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 15:48:09 2023

@author: Dan
Export a 3D slicer 4x4 Transform matrix to Anybody code
"""



def ExportMat2Anybody(NodeName:str):
    import numpy as np
    
    MatrixNode = getNode(NodeName)
    Matrix = vtk.vtkMatrix4x4()
    MatrixNode.GetMatrixTransformToWorld(Matrix)
    
    Matrix = slicer.util.arrayFromVTKMatrix(Matrix)

    Matrix = np.around(Matrix, decimals=6)
    
    
    Rotation = f'AnyMat33 Rotation = {{\n{{{Matrix[0,0]} , {Matrix[0,1]} , {Matrix[0,2]}}},\n{{{Matrix[1,0]} , {Matrix[1,1]} , {Matrix[1,2]}}},\n{{{Matrix[2,0]} , {Matrix[2,1]} , {Matrix[2,2]}}}\n\n}};'
    Translation = f'AnyVec3 Position = 0.001*{{{Matrix[0,3]} , {Matrix[1,3]} , {Matrix[2,3]}}};'


    print(Translation)
    print(Rotation)