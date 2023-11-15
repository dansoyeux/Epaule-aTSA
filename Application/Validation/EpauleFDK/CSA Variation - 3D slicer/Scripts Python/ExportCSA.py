# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:32:37 2023

@author: dan
Exports the Glene position and rotation matrix and ghProth Position (center of the sphere fitted to the glenoid implant surface)
"""


def ExportCSA():
    import numpy as np
    
    FrontalTransformOnOff(True)
    
    MatrixNode = getNode("GleneImplant - RotMat 4x4")
    ghNode = getNode("ghProth")
    
    Matrix = vtk.vtkMatrix4x4()
    MatrixNode.GetMatrixTransformToWorld(Matrix)
    
    Matrix = slicer.util.arrayFromVTKMatrix(Matrix)
    
    Matrix = np.around(Matrix, decimals=6)
    
    ghPosition = np.zeros(3)
    ghNode.GetNthControlPointPositionWorld(0, ghPosition)
    
    
    
    #Get frontal transform node 
    TransformFrontal = getNode("Glene - Rotation plan frontal")
    
    #Get inverse transform matrix to frontal plane
    TransformMatrixFrontal = vtk.vtkMatrix4x4()
    TransformFrontal.GetMatrixTransformFromWorld(TransformMatrixFrontal)
    
    TransformMatrixFrontal = slicer.util.arrayFromVTKMatrix(TransformMatrixFrontal)
    RotationMat = TransformMatrixFrontal[:3,:3]
    TranslationVect = TransformMatrixFrontal[:3,3]
    
    
    #Transforms the points to the scapula local coordinate system before calculating CSA
    ghPosition = np.dot(RotationMat,np.atleast_2d(ghPosition).T) + np.atleast_2d(TranslationVect).T
    
    ghPosition = np.round(ghPosition,6)
    
    
    
    Rotation = f'AnyMat33 Rotation = {{\n{{{Matrix[0,0]} , {Matrix[0,1]} , {Matrix[0,2]}}},\n{{{Matrix[1,0]} , {Matrix[1,1]} , {Matrix[1,2]}}},\n{{{Matrix[2,0]} , {Matrix[2,1]} , {Matrix[2,2]}}}\n\n}};'
    Translation = f'AnyVec3 Position = 0.001*{{{Matrix[0,3]} , {Matrix[1,3]} , {Matrix[2,3]}}};'
    ghProthLocal = f'\nAnyVec3 Center_Absolute = 0.001*{{{ghPosition[0][0]} , {ghPosition[1][0]} , {ghPosition[2][0]}}};'
    
    print(Translation)
    print(Rotation)
    print(ghProthLocal)