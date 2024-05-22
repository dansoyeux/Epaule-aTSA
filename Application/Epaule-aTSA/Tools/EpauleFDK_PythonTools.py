# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:38:18 2023

@author: Dan
"""
# %% needed libraries

import numpy as np

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

# %% Tools to link 3d slicer with Anybody


"""
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