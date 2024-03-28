# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 10:44:05 2023

@author: Dan

Scripts for CSA variation in 3d slicer
Every CSA calculation function must be executed while FrontalTransformOn = False (Drontal transform applied)
"""

import numpy as np
import math

"""
Glenoid Tilt angle measure
"""
# AxisNodeNames = ["Scapula - Axe transverse", "Glene - Up/Down Axis"]

# lineNodeNames = ["Scapula - Axe transverse centre Up/Down Axis", "Glene - Up/Down Axis"]


# Print angles between slice nodes
def ShowAngle(axis_1, axis_2, name_angle=""):
    """
    prints the angle between 2 axes
    and prints in front the name of the angle
    """

    AxisNodeNames = [axis_1, axis_2]
    lineDirectionVectors = []
    for lineNodeName in AxisNodeNames:
        lineNode = slicer.util.getFirstNodeByClassByName("vtkMRMLMarkupsLineNode", lineNodeName)
        lineStartPos = np.zeros(3)
        lineEndPos = np.zeros(3)
        lineNode.GetNthControlPointPositionWorld(0, lineStartPos)
        lineNode.GetNthControlPointPositionWorld(1, lineEndPos)
        lineDirectionVector = (lineEndPos - lineStartPos) / np.linalg.norm(lineEndPos - lineStartPos)
        lineDirectionVectors.append(lineDirectionVector)
    angleRad = vtk.vtkMath.AngleBetweenVectors(lineDirectionVectors[0], lineDirectionVectors[1])
    angleDeg = vtk.vtkMath.DegreesFromRadians(angleRad)
    # print("Angle between lines {0} and {1} = {2:0.3f}".format(lineNodeNames[0], lineNodeNames[1], angleDeg-90))
    # print(f"{name_angle} = {0:0.3f}".format(angleDeg - 90))
    print(name_angle + " = {0:0.3f}".format(angleDeg - 90))

    # Observe line node changes
    for lineNodeName in AxisNodeNames:
        lineNode = slicer.util.getFirstNodeByClassByName("vtkMRMLMarkupsLineNode", lineNodeName)
        lineNode.AddObserver(slicer.vtkMRMLMarkupsLineNode.PointModifiedEvent, ShowAngle)

# Print current angle
# ShowAngle()


"""
Created on Mon Apr 17 14:08:38 2023

@author: Dan
Function to project the CSA Angle measured in the 3D slicer model to a 2D angle as in a true-anteroposterior radiograph

"""

# Import CSA Markup


def CSA():

    import math

    #AngleNode = slicer.util.getFirstNodeByClassByName("vtkMRMLMarkupsAngleNode", "CSA")

    # Gets the 3 points coordinates necessary to calculate CSA
    ScapulaEnd = slicer.util.getNode("New Scapula End")
    # ScapulaEnd = slicer.util.getNode("Scapula End Copy")
    GleneDown = slicer.util.getNode("Glene Down")
    GleneUp = slicer.util.getNode("Glene Up")

    # Get frontal transform node
    TransformFrontal = slicer.util.getNode("Glene - Rotation plan frontal")

    P1 = np.zeros(3)
    ScapulaEnd.GetNthControlPointPositionWorld(0, P1)

    P2 = np.zeros(3)
    GleneDown.GetNthControlPointPositionWorld(0, P2)

    P3 = np.zeros(3)
    GleneUp.GetNthControlPointPositionWorld(0, P3)

    # Get inverse transform matrix to frontal plane
    TransformMatrixFrontal = vtk.vtkMatrix4x4()
    TransformFrontal.GetMatrixTransformFromWorld(TransformMatrixFrontal)

    TransformMatrixFrontal = slicer.util.arrayFromVTKMatrix(TransformMatrixFrontal)
    RotationMat = TransformMatrixFrontal[:3, :3]
    TranslationVect = TransformMatrixFrontal[:3, 3]

    # Transforms the points to the scapula local coordinate system before calculating CSA
    P1 = np.dot(RotationMat, np.atleast_2d(P1).T) + np.atleast_2d(TranslationVect).T
    P2 = np.dot(RotationMat, np.atleast_2d(P2).T) + np.atleast_2d(TranslationVect).T
    P3 = np.dot(RotationMat, np.atleast_2d(P3).T) + np.atleast_2d(TranslationVect).T

    P1[2], P2[2], P3[2] = 0, 0, 0

    # Vecteurs directeurs
    V1 = P1 - P2
    V2 = P3 - P2

    Angle = 0
    Angle = math.acos(np.dot(V1.T, V2) / (np.linalg.norm(V1) * np.linalg.norm(V2)))
    Angle = Angle / math.pi * 180

    print("CSA = {0}".format(Angle))

# To remoce the observer
# AngleNode.RemoveObserver(AngleNode)


"""
CSA variation script
Rotates the glenoid implant around an axis and calculates the matrix rotation required : Variation CSA - Matrice de rotation glene
Outputs the tilt angle and the CSA


In 3d slicer : Modify the IS rotation of the transform : Variation CSA - Rotation glene
"""
# This markups point list node specifies the center of rotation
# rotationAxisMarkupsNode = slicer.util.getNode("Variation CSA - Axe GH antéropostérieur")
# rotationAxisMarkupsNode = slicer.util.getNode("Variation CSA - Axe GHProth Antéropostérieur")

# Antero du corps
# rotationAxisMarkupsNode = slicer.util.getNode("Variation CSA - Axe Centre Glene Antéropostérieur")
rotationAxisMarkupsNode = slicer.util.getNode("Variation CSA - Axe Centre Glene Local")
# rotationAxisMarkupsNode = slicer.util.getNode("Variation CSA - Axe Centre Glene")
# rotationAxisMarkupsNode = slicer.util.getNode("Variation CSA - Axe centre Up/Down Axis")
# rotationAxisMarkupsNode = slicer.util.getNode("Variation CSA - Axe centre Up/Down Axis Copy")
# rotationAxisMarkupsNode = slicer.util.getNode("X Glene")

# Get frontal transform node
TransformFrontal = slicer.util.getNode("Glene - Rotation plan frontal")

# This transform can be edited in Transforms module (Edit / Rotation / IS slider)
rotationTransformNode = slicer.util.getNode("Variation CSA - Rotation glene")
# This transform has to be applied to the image, model, etc.


def CSAVariation(unusedArg1=None, unusedArg2=None, unusedArg3=None):

    finalTransformNode = slicer.util.getNode("Variation CSA - Matrice de rotation glene")

    # Get inverse transform matrix to frontal plane
    TransformMatrixFrontal = vtk.vtkMatrix4x4()
    TransformFrontal.GetMatrixTransformFromWorld(TransformMatrixFrontal)

    TransformMatrixFrontal = slicer.util.arrayFromVTKMatrix(TransformMatrixFrontal)
    RotationMat = TransformMatrixFrontal[:3, :3]
    TranslationVect = TransformMatrixFrontal[:3, 3]

    rotationAxisPoint1_World = np.zeros(3)
    rotationAxisMarkupsNode.GetNthControlPointPositionWorld(0, rotationAxisPoint1_World)
    rotationAxisPoint2_World = np.zeros(3)
    rotationAxisMarkupsNode.GetNthControlPointPositionWorld(1, rotationAxisPoint2_World)

    # Transform points from World coordinate to local scapula coordinate
    rotationAxisPoint1_World = np.dot(RotationMat, np.atleast_2d(rotationAxisPoint1_World).T) + np.atleast_2d(TranslationVect).T
    rotationAxisPoint2_World = np.dot(RotationMat, np.atleast_2d(rotationAxisPoint2_World).T) + np.atleast_2d(TranslationVect).T

    axisDirectionZ_World = rotationAxisPoint2_World - rotationAxisPoint1_World
    axisDirectionZ_World = axisDirectionZ_World / np.linalg.norm(axisDirectionZ_World)
    # Get transformation between world coordinate system and rotation axis aligned coordinate system
    worldToRotationAxisTransform = vtk.vtkMatrix4x4()
    p = vtk.vtkPlaneSource()
    p.SetNormal(axisDirectionZ_World)
    axisOrigin = np.array(p.GetOrigin())
    axisDirectionX_World = np.array(p.GetPoint1()) - axisOrigin
    axisDirectionY_World = np.array(p.GetPoint2()) - axisOrigin
    rotationAxisToWorldTransform = np.row_stack((np.column_stack((axisDirectionX_World, axisDirectionY_World, axisDirectionZ_World, rotationAxisPoint1_World)), (0, 0, 0, 1)))
    rotationAxisToWorldTransformMatrix = slicer.util.vtkMatrixFromArray(rotationAxisToWorldTransform)
    worldToRotationAxisTransformMatrix = slicer.util.vtkMatrixFromArray(np.linalg.inv(rotationAxisToWorldTransform))
    # Compute transformation chain
    rotationMatrix = vtk.vtkMatrix4x4()
    rotationTransformNode.GetMatrixTransformToParent(rotationMatrix)
    finalTransform = vtk.vtkTransform()
    finalTransform.Concatenate(rotationAxisToWorldTransformMatrix)
    finalTransform.Concatenate(rotationMatrix)
    finalTransform.Concatenate(worldToRotationAxisTransformMatrix)
    finalTransformNode.SetMatrixTransformToParent(finalTransform.GetMatrix())

    # shows the tilt
    ShowAngle("Scapula - Axe transverse", "Glene - Up/Down Axis", "Tilt")

    # Show version
    ShowAngle("Scapula - Axe transverse", "Glene - Left/Right Axis", "Version")

    # Shows CSA
    CSA()
    print("\n")


# Manual initial update
CSAVariation()

# Automatic update when point is moved or transform is modified
rotationTransformNodeObserver = rotationTransformNode.AddObserver(slicer.vtkMRMLTransformNode.TransformModifiedEvent, CSAVariation)
rotationAxisMarkupsNodeObserver = rotationAxisMarkupsNode.AddObserver(slicer.vtkMRMLMarkupsNode.PointModifiedEvent, CSAVariation)

# Execute these lines to stop automatic updates:
# rotationTransformNode.RemoveObserver(rotationTransformNodeObserver)
# rotationAxisMarkupsNode.RemoveObserver(rotationAxisMarkupsNodeObserver)

"""
Created on Tue May 23 09:12:43 2023

@author: userscale fator
Function that calculates the CSA based on the acromion Length offset in the x scapula coordinate in mm
"""


def AcromionOffset2CSA(AcromionOffset: float):

    """
    Acromion offset in millimeter
    """
    # Get frontal transform node
    TransformFrontal = slicer.util.getNode("Glene - Rotation plan frontal")

    GleneDown = slicer.util.getNode("Glene Down")
    GleneUp = slicer.util.getNode("Glene Up")
    ScapulaEnd = slicer.util.getNode("Scapula End")
    NewScapulaEnd = slicer.util.getNode("New Scapula End")

    P0 = np.zeros(3)
    ScapulaEnd.GetNthControlPointPositionWorld(0, P0)

    P2 = np.zeros(3)
    GleneDown.GetNthControlPointPositionWorld(0, P2)

    P3 = np.zeros(3)
    GleneUp.GetNthControlPointPositionWorld(0, P3)

    # Get inverse transform matrix to frontal plane
    TransformMatrixFrontal = vtk.vtkMatrix4x4()
    TransformFrontal.GetMatrixTransformFromWorld(TransformMatrixFrontal)

    TransformMatrixFrontal = slicer.util.arrayFromVTKMatrix(TransformMatrixFrontal)
    RotationMat = TransformMatrixFrontal[:3, :3]
    TranslationVect = TransformMatrixFrontal[:3, 3]

    # Transforms the points to the scapula local coordinate system before calculating CSA
    P0 = np.dot(RotationMat, np.atleast_2d(P0).T) + np.atleast_2d(TranslationVect).T
    P2 = np.dot(RotationMat, np.atleast_2d(P2).T) + np.atleast_2d(TranslationVect).T
    P3 = np.dot(RotationMat, np.atleast_2d(P3).T) + np.atleast_2d(TranslationVect).T

    # New Acromion End

    Offset = np.array([[AcromionOffset], [0], [0]])
    P1 = P0 + Offset

    # Set the new
    NewScapulaEnd.SetNthControlPointPosition(0, P1)

    # CSA calculation
    P1[2], P2[2], P3[2] = 0, 0, 0

    V1 = P1 - P2
    V2 = P3 - P2

    Angle = math.acos(np.dot(V1.T, V2) / (np.linalg.norm(V1) * np.linalg.norm(V2)))
    Angle = Angle / math.pi * 180

    print("CSA = {0}".format(Angle))


"""
Created on Tue Apr 18 12:38:30 2023

@author: Dan
Frontal Transform On/OFF on 3d slicer
"""


def FrontalTransformOn(On=bool):

    # Nodes os et implants
    ScapulaNode = slicer.util.getNode("Scapula - Rotation repère")
    GleneNode = slicer.util.getNode("Variation CSA - Matrice de rotation glene")
    HumerusNode = slicer.util.getNode("Humerus - Rotation repère")
    HumerusImplantNode = slicer.util.getNode("HumerusImplant - Placement")

    # Axes
    AxeTransverse = slicer.util.getNode("Scapula - Axe transverse")
    AxeTransverse2 = slicer.util.getNode("Scapula - Axe transverse centre Up/Down Axis")
    CentreGlene = slicer.util.getNode("Centre Glene Implant")
    AxeCSA = slicer.util.getNode("Variation CSA - Axe Centre Glene Antéropostérieur")
    AxeCSA2 = slicer.util.getNode("Variation CSA - Axe GHProth Antéropostérieur")

    # repères
    xScapula = slicer.util.getNode("X Scapula")
    yScapula = slicer.util.getNode("Y Scapula")
    zScapula = slicer.util.getNode("Z Scapula")
    ScapulaEnd = slicer.util.getNode("Scapula End")
    NewScapulaEnd = slicer.util.getNode("New Scapula End")

    # Transform
    TransformScapula = slicer.util.getNode("Scapula - Rotation plan frontal")
    TransformGlene = slicer.util.getNode("Glene - Rotation plan frontal")

    TransformHumerus = slicer.util.getNode("Humerus - Rotation plan frontal")
    TransformHumerusImplant = slicer.util.getNode("HumerisImplant - Rotation plan frontal")

    # Transforme la glene et la scapula dans plan frontal
    if On:
        ScapulaNode.SetAndObserveTransformNodeID(TransformScapula.GetID())
        AxeTransverse.SetAndObserveTransformNodeID(TransformScapula.GetID())
        AxeTransverse2.SetAndObserveTransformNodeID(TransformScapula.GetID())
        AxeCSA.SetAndObserveTransformNodeID(TransformScapula.GetID())
        AxeCSA2.SetAndObserveTransformNodeID(TransformScapula.GetID())
        xScapula.SetAndObserveTransformNodeID(TransformScapula.GetID())
        yScapula.SetAndObserveTransformNodeID(TransformScapula.GetID())
        zScapula.SetAndObserveTransformNodeID(TransformScapula.GetID())
        ScapulaEnd.SetAndObserveTransformNodeID(TransformScapula.GetID())
        NewScapulaEnd.SetAndObserveTransformNodeID(TransformScapula.GetID())

        GleneNode.SetAndObserveTransformNodeID(TransformGlene.GetID())
        CentreGlene.SetAndObserveTransformNodeID(TransformGlene.GetID())

        HumerusNode.SetAndObserveTransformNodeID(TransformHumerus.GetID())
        HumerusImplantNode.SetAndObserveTransformNodeID(TransformHumerusImplant.GetID())

    # Désactive la transformation de la glene et de la scapula dans plan frontal
    if On is False:
        ScapulaNode.SetAndObserveTransformNodeID(None)
        AxeTransverse.SetAndObserveTransformNodeID(None)
        AxeTransverse2.SetAndObserveTransformNodeID(None)
        AxeCSA.SetAndObserveTransformNodeID(None)
        AxeCSA2.SetAndObserveTransformNodeID(None)

        xScapula.SetAndObserveTransformNodeID(None)
        yScapula.SetAndObserveTransformNodeID(None)
        zScapula.SetAndObserveTransformNodeID(None)
        ScapulaEnd.SetAndObserveTransformNodeID(None)
        NewScapulaEnd.SetAndObserveTransformNodeID(None)

        GleneNode.SetAndObserveTransformNodeID(None)
        CentreGlene.SetAndObserveTransformNodeID(None)

        HumerusNode.SetAndObserveTransformNodeID(None)
        HumerusImplantNode.SetAndObserveTransformNodeID(None)


"""
Created on Mon Apr 17 15:48:09 2023

@author: Dan
Export a 3D slicer 4x4 Transform matrix to Anybody code
"""


def ExportMat2Anybody(NodeName: str):

    MatrixNode = slicer.util.getNode(NodeName)
    Matrix = vtk.vtkMatrix4x4()
    MatrixNode.GetMatrixTransformToWorld(Matrix)

    Matrix = slicer.util.arrayFromVTKMatrix(Matrix)

    Matrix = np.around(Matrix, decimals=6)

    Rotation = f'AnyMat33 Rotation = {{\n{{{Matrix[0,0]} , {Matrix[0,1]} , {Matrix[0,2]}}},\n{{{Matrix[1,0]} , {Matrix[1,1]} , {Matrix[1,2]}}},\n{{{Matrix[2,0]} , {Matrix[2,1]} , {Matrix[2,2]}}}\n\n}};'
    Translation = f'AnyVec3 Position = 0.001*{{{Matrix[0,3]} , {Matrix[1,3]} , {Matrix[2,3]}}};'

    print(Translation)
    print(Rotation)


"""
Created on Mon May 22 14:32:37 2023

@author: dan
Exports the Glene position and rotation matrix and ghProth Position (center of the sphere fitted to the glenoid implant surface)
"""


def ExportCSA():

    FrontalTransformOn(True)

    MatrixNode = slicer.util.getNode("GleneImplant - RotMat 4x4")
    ghNode = slicer.util.getNode("ghProth")

    Matrix = vtk.vtkMatrix4x4()
    MatrixNode.GetMatrixTransformToWorld(Matrix)

    Matrix = slicer.util.arrayFromVTKMatrix(Matrix)

    Matrix = np.around(Matrix, decimals=6)

    ghPosition = np.zeros(3)
    ghNode.GetNthControlPointPositionWorld(0, ghPosition)

    # Get frontal transform node
    TransformFrontal = slicer.util.getNode("Glene - Rotation plan frontal")

    # Get inverse transform matrix to frontal plane
    TransformMatrixFrontal = vtk.vtkMatrix4x4()
    TransformFrontal.GetMatrixTransformFromWorld(TransformMatrixFrontal)

    TransformMatrixFrontal = slicer.util.arrayFromVTKMatrix(TransformMatrixFrontal)
    RotationMat = TransformMatrixFrontal[:3, :3]
    TranslationVect = TransformMatrixFrontal[:3, 3]

    # Transforms the points to the scapula local coordinate system before calculating CSA
    ghPosition = np.dot(RotationMat, np.atleast_2d(ghPosition).T) + np.atleast_2d(TranslationVect).T

    ghPosition = np.round(ghPosition, 6)

    Rotation = f'AnyMat33 Rotation = {{\n{{{Matrix[0,0]} , {Matrix[0,1]} , {Matrix[0,2]}}},\n{{{Matrix[1,0]} , {Matrix[1,1]} , {Matrix[1,2]}}},\n{{{Matrix[2,0]} , {Matrix[2,1]} , {Matrix[2,2]}}}\n\n}};'
    Translation = f'AnyVec3 Position = 0.001*{{{Matrix[0,3]} , {Matrix[1,3]} , {Matrix[2,3]}}};'
    ghProthLocal = f'\nAnyVec3 Center_Absolute = 0.001*{{{ghPosition[0][0]} , {ghPosition[1][0]} , {ghPosition[2][0]}}};'

    print(Translation)
    print(Rotation)
    print(ghProthLocal)


# def ExportHumerus():

#     FrontalTransformOn(True)

#     # HumerusImplantPlacement
#     HumerusImplantPlacement = MatrixNode = slicer.util.getNode("HumerusImplant - Placement")

#     Matrix = vtk.vtkMatrix4x4()
#     HumerusImplantPlacement.GetMatrixTransformToWorld(Matrix)

#     Matrix = slicer.util.arrayFromVTKMatrix(Matrix)
#     Matrix = np.around(Matrix, decimals=6)

#     # Get frontal transform node
#     TransformFrontal = slicer.util.getNode("HumerusImplant - Rotation plan frontal")

#     # Get inverse transform matrix to frontal plane
#     TransformMatrixFrontal = vtk.vtkMatrix4x4()
#     TransformFrontal.GetMatrixTransformFromWorld(TransformMatrixFrontal)

#     TransformMatrixFrontal = slicer.util.arrayFromVTKMatrix(TransformMatrixFrontal)


# %% Tools for converting Anybody to python
""""
Converts a string containing the anybody definition of a matrix and converts it to an numpy.array
"""


def AnyMatrix2Array(string):
    string = string.replace(" ", "")
    matrix = []
    if string[0:2] == "{{":
        Type = "Matrix"
        rows = string.split("},{")
        rows[0] = rows[0].replace("{{", "")
        rows[-1] = rows[-1].replace("}}", "")
    else:

        rows = string.split("},{")
        rows[0] = rows[0].replace("{", "")
        rows[-1] = rows[-1].replace("}", "")

        if len(rows[0].split(",")) == 1:
            Type = "Value"
        else:
            Type = "Vector"

    if Type == "Value":
        matrix = eval(rows[0])
    elif Type == "Vector":
        rows = rows[0].split(",")
        rows = [eval(i) for i in rows]
        matrix.append(rows)
        matrix = np.array(matrix)
    else:
        for row in rows:
            elements = row.split(",")
            elements = [eval(i) for i in elements]
            matrix.append(elements)
        matrix = np.array(matrix)

    return matrix

# %% Tools for 3d slicer


"""
Input : rotation matrix and translation vector to a 4x4 matrix for a 3d slicer transform
"""


def TransformMatrix(RotMat=None, Vect=None):

    if RotMat is None:
        RotMat = np.eye(3)
    if Vect is None:
        Vect = np.zeros(3)

    Mat = np.eye(4)

    Mat[0:3, 0:3] = RotMat
    Mat[0:3, 3] = Vect
    return Mat


"""
Function to set the 4x4 transform matrix to a transform in 3d slicer from a rotation matrix and translation vector numpy arrays
"""


def SetTransformMatrix(TransformName, RotMat=None, Vect=None):

    TransformMat = TransformMatrix(RotMat, Vect)

    Transform = getNode(TransformName)
    Transform.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(TransformMat))
