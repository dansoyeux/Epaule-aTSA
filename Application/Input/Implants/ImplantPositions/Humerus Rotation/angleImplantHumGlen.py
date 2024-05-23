# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 11:08:15 2023

@author: Dan
"""

import numpy as np




#%% functions

""""
Converts a string containing the anybody definition of a matrix and converts it to an numpy.array
"""    
def AnyMatrix2Array(string):
    import numpy as np
    string = string.replace(" ","")
    matrix = []
    if string[0:2]=="{{":
        Type = "Matrix"
        rows = string.split("},{")
        rows[0] = rows[0].replace("{{","")
        rows[-1] = rows[-1].replace("}}","")
    else:
        
        rows = string.split("},{")
        rows[0] = rows[0].replace("{","")
        rows[-1] = rows[-1].replace("}","")
        
        if len(rows[0].split(","))==1:
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

"""
Input : rotation matrix and translation vector to a 4x4 matrix for a 3d slicer transform
"""
def TransformMatrix(RotMat=None,Vect=None):
    import numpy as np
    
    if RotMat is None:
        RotMat = np.eye(3)
    if Vect is None:
        Vect = np.zeros(3)
    
    Mat = np.eye(4)
    
    Mat[0:3,0:3]= RotMat
    Mat[0:3,3] = Vect
    return Mat


"""
Function to set the 4x4 transform matrix to a transform in 3d slicer from arrays
"""
def SetTransformMatrix(TransformName, RotMat=False,Vect=False):
    
    TransformMat = TransformMatrix(RotMat,Vect)
    
    Transform = getNode(TransformName)
    Transform.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(TransformMat))



#%%


RGlen_Laur = AnyMatrix2Array("{{0.8050566, 0.1937416, 0.5606676},{-0.2223788, 0.9748026, -0.01753679},{-0.5499378, -0.1105625, 0.8278553}}")

RHum_Laur = AnyMatrix2Array("{{0.7227381, -0.445036, -0.5287653},{-0.269066, -0.8859063, 0.3778538},{-0.636595, -0.1308165, -0.7600223}}")

TGlen_Laur = AnyMatrix2Array("{0.004691832, 0.3991605, 0.1470714}")
THum_Laur = AnyMatrix2Array("{0.0300267, 0.399928, 0.1831996}")


RHum_Me = AnyMatrix2Array("{{0.6925968, -0.539241, -0.4790916},{-0.3472148, -0.8314023, 0.4338342},{-0.6322591, -0.1341245, -0.763059}}")

RGlen_Me = AnyMatrix2Array("{{0.7857383, 0.2247054, 0.5763009},{-0.3680464, 0.9186501, 0.1436099},{-0.497149, -0.3249453, 0.8045206}}")


RHum_Laur_Local = np.dot(RHum_Laur,RGlen_Laur)





def Angle(RGlen,RHum):
    
    from scipy.spatial.transform import Rotation  
    
    RGlen = Rotation.from_matrix(RGlen)
    RHum = Rotation.from_matrix(RHum)
    
    
    AngGlen = RGlen.as_euler('xyz',degrees = True)
    AngHum = RHum.as_euler('xyz',degrees = True)
    
        
    return AngGlen,AngHum

AngGlen,AngHum = Angle(RGlen_Laur,RHum_Laur)

DiffLaur = AngHum[1] - AngGlen[1]

print(DiffLaur)

AngGlen_Me,AngHum_Me = Angle(RGlen_Me,RHum_Me)

DiffMe = AngHum_Me[1] - AngGlen_Me[1]

print(DiffMe)




#%%


# RotInv = getNode("RotHumLocal")



# RotHumLocal..SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(RHum_Laur_Local))


# np.array([[ 0.80505656, -0.2223788 , -0.54993781,0],
#        [ 0.19374159,  0.97480261, -0.11056248,0],
#        [ 0.56066757, -0.01753678,  0.82785526,0],
#        [0,0,0,0]])


# RotGlenTransform = getNode("RotGlen")
# RotHumTransform = getNode("RotHum")
# RGlen_Laur = np.array([[0.8050566, 0.1937416, 0.5606676, 0],
#                   [-0.2223788, 0.9748026, -0.01753679, 0],
#                   [-0.5499378, -0.1105625, 0.8278553,0],
#                   [0,0,0,0]])

# RHum_Laur = np.array([[0.7227381, -0.445036, -0.5287653,0],
#                        [-0.269066, -0.8859063, 0.3778538,0],
#                        [-0.636595, -0.1308165, -0.7600223,0],
#                        [0,0,0,0]])

# RotGlenTransform.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(RGlen_Laur))
# RotHumTransform.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(RHum_Laur))

# RotInv.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(Inv))