# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 15:32:30 2023
Script that reads picked points files and prints the anybody script needed to input these points : Points coordinates, Point names 
Can also add an offset on a dimension
@author: Dan
"""


# Prints an array to a AnyMatrix, and adds a comment at the end of each line
def Mat2AnyMatrix(MatrixName=str, mat=list, Names=None, Offset=None):
    """
    Can add an offset variable to any x,y,z directopm
    Offset.OffsetValue : Offset vector (x,y or z)

    OffsetPoints : Point names to Offset
    OffsetName : name of the offset variable in the Anybody script
    """

    if Names:
        CommentString = 1

    else:
        CommentString = 0
        Names = [""] * len(mat)

    if Offset:
        # Constructs a list with a 0 if no offset and a 1 if there is an offset
        OffsetOn = [0 if pos == 0 else 1 for pos in Offset["OffsetFactor"]]

    string = "AnyMatrix " + MatrixName + " = {\n"
    for i in range(len(mat)):
        string += "  {"

        for j in range(len(mat[0])):

            if Offset:
                # Adds the offset name and the multiply factor if there is one
                if Names[i] in Offset["OffsetPoints"]:
                    if j == 0:
                        string += str(mat[i, j]) + (" + " + Offset["OffsetName"] + " * " + str(Offset["OffsetFactor"][j])) * OffsetOn[j] + ", "
                    elif j == 1:
                        string += str(mat[i, j]) + (" + " + Offset["OffsetName"] + " * " + str(Offset["OffsetFactor"][j])) * OffsetOn[j] + ", "
                    elif j == 2:
                        string += str(mat[i, j]) + (" + " + Offset["OffsetName"] + " * " + str(Offset["OffsetFactor"][j])) * OffsetOn[j] + "}"
                else:
                    if j != len(mat[0]) - 1:
                        string += str(mat[i, j]) + ", "
                    else:
                        string += str(mat[i, j]) + "}"

            else:
                if j != len(mat[0]) - 1:
                    string += str(mat[i, j]) + ", "
                else:
                    string += str(mat[i, j]) + "}"

        # dernière ligne
        if i == len(mat) - 1:
            string += ("  // " + Names[i]) * CommentString + "\n};"
        # fin de ligne
        else:
            string += "," + ("  // " + Names[i]) * CommentString + "\n"

    return string


# Prints an array of string to a AnyStringArray for anybody
def Names2AnyStringArray(ArrayName=str, Array=str):

    string = "AnyStringArray " + ArrayName + " = {\n"

    for i in range(len(Array)):
        if i == len(Array) - 1:
            string += " \"" + Array[i] + "\"\n};"
        else:
            string += " \"" + Array[i] + "\",\n"

    return string


"""
Reads a picked point file (.pp)
outputs the points coordinates and the points names

"""


def ReadPickedPoints(dataPath):

    # Module that can read .pp files can be found here : https://pypi.org/project/meshlab-pickedpoints/
    import meshlab_pickedpoints
    import numpy as np

    data = meshlab_pickedpoints.load(dataPath)

    mat = np.zeros([len(data), 3])
    Names = []

    for i in range(len(data)):

        for j in range(3):
            mat[i, j] = data[i]['point'][j]

        Names.append(data[i]['name'])

    return mat, Names




def PickedPoint2AnyMatrix(dataPath=str, MatrixName=str, ArrayName=str, NamesOn=bool, Offset=None, AddPoint=None):
    """
    Prints the picked points matrix from a .pp file to a AnyScript matrix format

    NamesOn : activates or not output of the name of the points (useful for an RBF transform for example)
    OffsetValue : Offset vector
    OffsetPoints : Array with the points names to Offset
    """

    import numpy as np

    mat, Names = ReadPickedPoints(dataPath)

    if AddPoint is not None:
        mat = np.append(AddPoint["Coordinates"], mat, axis=0)
        Names = AddPoint["PointNames"] + Names

    # without an offset
    if Offset is None:
        string = Mat2AnyMatrix(MatrixName, mat, Names)
    else:
        string = Mat2AnyMatrix(MatrixName, mat, Names, Offset)

    if NamesOn:
        string = string + "\n \n" + Names2AnyStringArray(ArrayName, Names)

    return string


def build_grid(minx=float, maxx=float, miny=float, maxy=float, minz=float, maxz=float, nx=int, ny=int, nz=int):
    """
    Creates an array containing points in a 3d grid of points
    """

    import numpy as np

    x = np.linspace(minx, maxx, nx)
    y = np.linspace(miny, maxy, ny)
    z = np.linspace(minz, maxz, nz)

    xx, yy, zz = np.meshgrid(x, y, z)

    Mat = np.array([[0, 0, 0]])

    for i in range(len(x)):
        for j in range(len(y)):
            for k in range(len(z)):
                Mat = np.append(Mat, [[xx[i, j, k], yy[i, j, k], zz[i, j, k]]], axis=0)

    Mat = np.delete(Mat, 0, axis=0)
    
    return Mat


def PointGridAnybody(minx=float, maxx=float, miny=float, maxy=float, minz=float, maxz=float, nx=int, ny=int, nz=int):
    """
    From an array of points, defines an object grid in 3D in the anybody script language
    """

    Mat = build_grid(minx, maxx, miny, maxy, minz, maxz, nx, ny, nz)
    string = Mat2AnyMatrix("Grid", Mat)

    return string




def PickedPoints2AnyPoints(dataPath=str, Offset=None, AddPoint=None):
    """
    Creates morphing points from a .pp files in the anybody format (Source and Target points)
    One for AffineMorphing and one for RBF morphing (with names)
    """

    PickedPointsSource = PickedPoint2AnyMatrix(dataPath, "PointsAffine0", "PointsName0", False, None, AddPoint=AddPoint)
    PickedPointsSource += "\n \n" + PickedPoint2AnyMatrix(dataPath, "PointsRBF0", "PointsName0", True, None, AddPoint=AddPoint)

    PickedPointsTarget = PickedPoint2AnyMatrix(dataPath, "PointsAffine1", "PointsName1", False, Offset=Offset, AddPoint=AddPoint)
    PickedPointsTarget += "\n\n" + PickedPoint2AnyMatrix(dataPath, "PointsRBF1", "PointsName1", False, Offset=Offset, AddPoint=AddPoint)

    return PickedPointsSource, PickedPointsTarget


# Old clavicula scaling function when acj moved with acromion scaling (worked ish, not exact precision but worked)
# 15/06/2023
def ClaviculaScaleFactor(Scapula_Offset):

    import numpy as np

    Scapula_RotMat = np.matrix([[0.436403, -0.05781788, -0.8978917],
                               [0.3229598, 0.9414962, 0.09634271],
                               [0.8397913, -0.3320272, 0.4295446]])

    Scapula_TranslationVect = np.array([-0.1128911, 0.5031109, 0.1692766])

    Clavicula_RotMat = np.matrix([[-0.3585338, 0.1005447, -0.9280863],
                                  [0.2404237, 0.9705905, 0.01227003],
                                  [0.9020254, -0.2187348, -0.3721629]])

    Clavicula_TranslationVect = np.array([-0.03355151, 0.4586141, 0.0207])

    Clavicula_x = np.array([1, 0, 0])

    # Points coordinates in their local segment coordinates

    Local_Clavicula_scj = np.array([0, 0, 0])

    Local_Scapula_acj = np.array([0.006071, -0.003599, -0.030331]) + np.array([Scapula_Offset, 0, 0])

    Local_Clavicula_acj = np.array([0.155254, 0.00298894, -0.006588967])

    # Converts points to the global reference frame

    Global_Clavicula_scj = np.dot(Clavicula_RotMat, np.atleast_2d(Local_Clavicula_scj).T) + np.atleast_2d(Clavicula_TranslationVect).T

    Global_Clavicula_x = np.dot(Clavicula_RotMat, np.atleast_2d(Clavicula_x).T) + np.atleast_2d(Clavicula_TranslationVect).T

    # x vector in global reference frame
    Global_Clavicula_x = Global_Clavicula_x - np.atleast_2d(Clavicula_TranslationVect).T

    Global_Scapula_acj = np.dot(Scapula_RotMat, np.atleast_2d(Local_Scapula_acj).T) + np.atleast_2d(Scapula_TranslationVect).T

    # Coordinates without any segment transform
    Clavicula_acjVector = Local_Clavicula_acj - Local_Clavicula_scj
    Clavicula_acjDistance = np.linalg.norm(Clavicula_acjVector)

    # Cos(Angle)
    Clavicula_acjAngle = (np.dot(Clavicula_acjVector.T, Clavicula_x.T)) / (1 * Clavicula_acjDistance)

    # Coordinates after acromion offset
    Global_Clavicula_Origin = Clavicula_TranslationVect

    Transformed_Clavicula_acjVector = Global_Scapula_acj.T - Global_Clavicula_Origin
    Transformed_Clavicula_acjDistance = np.linalg.norm(Transformed_Clavicula_acjVector)

    # Cos(Angle)
    Transformed_Clavicula_acjAngle = (np.dot(Transformed_Clavicula_acjVector, Global_Clavicula_x)) / (1 * Transformed_Clavicula_acjDistance)

    Clavicula_ScaleFactor = (Transformed_Clavicula_acjDistance * Transformed_Clavicula_acjAngle) / (Clavicula_acjDistance * Clavicula_acjAngle)

    return float(Clavicula_ScaleFactor), Global_Scapula_acj
