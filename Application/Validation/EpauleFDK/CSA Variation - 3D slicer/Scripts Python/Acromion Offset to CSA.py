# -*- coding: utf-8 -*-
"""
Created on Tue May 23 09:12:43 2023

@author: userscale fator
Function that calculates the CSA based on the acromion Length offset in the x scapula coordinate in mm
"""




def AcromionScale2CSA(AcromionOffset:float):

    
    import numpy as np
    import math

    #Get frontal transform node 
    TransformFrontal = getNode("Glene - Rotation plan frontal")

    GleneDown = getNode("Glene Down")
    GleneUp = getNode("Glene Up")
    ScapulaEnd = getNode("Scapula End")
    NewScapulaEnd = getNode("New Scapula End")

    P0 = np.zeros(3)
    ScapulaEnd.GetNthControlPointPositionWorld(0, P0)
    
    P2 = np.zeros(3)
    GleneDown.GetNthControlPointPositionWorld(0, P2)

    P3 = np.zeros(3)
    GleneUp.GetNthControlPointPositionWorld(0, P3)

    #Get inverse transform matrix to frontal plane
    TransformMatrixFrontal = vtk.vtkMatrix4x4()
    TransformFrontal.GetMatrixTransformFromWorld(TransformMatrixFrontal)

    TransformMatrixFrontal = slicer.util.arrayFromVTKMatrix(TransformMatrixFrontal)
    RotationMat = TransformMatrixFrontal[:3,:3]
    TranslationVect = TransformMatrixFrontal[:3,3]


    #Transforms the points to the scapula local coordinate system before calculating CSA
    P0 = np.dot(RotationMat,np.atleast_2d(P0).T) + np.atleast_2d(TranslationVect).T
    P2 = np.dot(RotationMat,np.atleast_2d(P2).T) + np.atleast_2d(TranslationVect).T
    P3 = np.dot(RotationMat,np.atleast_2d(P3).T) + np.atleast_2d(TranslationVect).T
    
    
    # New Acromion End
    
    Offset = np.array([[AcromionOffset],[0],[0]])
    P1 = P0 + Offset
    
    # Set the new 
    NewScapulaEnd.SetNthControlPointPosition(0,P1)
     
    
    # CSA calculation
    P1[2],P2[2],P3[2]=0,0,0


    V1 = P1 - P2
    V2 = P3 - P2

    Angle = math.acos(np.dot(V1.T,V2) / (np.linalg.norm(V1) * np.linalg.norm(V2)))
    Angle = Angle/math.pi*180

    print("CSA = {0}".format(Angle))