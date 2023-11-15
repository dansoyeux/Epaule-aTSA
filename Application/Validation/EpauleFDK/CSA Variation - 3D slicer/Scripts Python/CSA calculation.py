# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 14:08:38 2023

@author: Dan
Function to project the CSA Angle measured in the 3D slicer model to a 2D angle as in a true-anteroposterior radiograph

"""

#Import CSA Markup

def CSA():
    import numpy as np
    import math
        
    #AngleNode = slicer.util.getFirstNodeByClassByName("vtkMRMLMarkupsAngleNode", "CSA")
    
    #Gets the 3 points coordinates necessary to calculate CSA
    ScapulaEnd = getNode("Scapula End")
    # ScapulaEnd = getNode("Scapula End Copy")
    GleneDown = getNode("Glene Down")
    GleneUp = getNode("Glene Up")
    
    
    #Get frontal transform node 
    TransformFrontal = getNode("Glene - Rotation plan frontal")
    
    P1 = np.zeros(3)
    ScapulaEnd.GetNthControlPointPositionWorld(0, P1)
    
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
    P1 = np.dot(RotationMat,np.atleast_2d(P1).T) + np.atleast_2d(TranslationVect).T
    P2 = np.dot(RotationMat,np.atleast_2d(P2).T) + np.atleast_2d(TranslationVect).T
    P3 = np.dot(RotationMat,np.atleast_2d(P3).T) + np.atleast_2d(TranslationVect).T
    
        
    P1[2],P2[2],P3[2] = 0,0,0
    
    #Vecteurs directeurs
    V1 = P1 - P2
    V2 = P3 - P2
    
    Angle = 0
    Angle = math.acos(np.dot(V1.T,V2) / (np.linalg.norm(V1) * np.linalg.norm(V2)))
    Angle = Angle/math.pi*180
    
    
    print("CSA = {0}".format(Angle))
    
#Print current angle
# CSA()

#AngleNode = slicer.util.getFirstNodeByClassByName("vtkMRMLMarkupsAngleNode", "CSA")
#AngleNode.AddObserver(slicer.vtkMRMLMarkupsLineNode.PointModifiedEvent, CSA)


#Remove observer
#AngleNode.RemoveObserver(AngleNode)