# This markups point list node specifies the center of rotation
#rotationAxisMarkupsNode = getNode("Variation CSA - Axe GH antéropostérieur")


# rotationAxisMarkupsNode = getNode("Variation CSA - Axe GHProth Antéropostérieur")
# rotationAxisMarkupsNode = getNode("Variation CSA - Axe Centre Glene Antéropostérieur Scapula")

rotationAxisMarkupsNode = getNode("Variation CSA - Axe centre Up/Down Axis")

# rotationAxisMarkupsNode = getNode("Variation CSA - Axe centre Up/Down Axis Copy")

# rotationAxisMarkupsNode = getNode("X Glene")

#Get frontal transform node
TransformFrontal = getNode("Glene - Rotation plan frontal")


# This transform can be edited in Transforms module (Edit / Rotation / IS slider)
rotationTransformNode = getNode("Variation CSA - Rotation glene")
# This transform has to be applied to the image, model, etc.
finalTransformNode = getNode("Variation CSA - Matrice de rotation glene")

def updateFinalTransform(unusedArg1=None, unusedArg2=None, unusedArg3=None):
  import numpy as np
  
  #Get inverse transform matrix to frontal plane
  TransformMatrixFrontal = vtk.vtkMatrix4x4()
  TransformFrontal.GetMatrixTransformFromWorld(TransformMatrixFrontal)
  
  TransformMatrixFrontal = slicer.util.arrayFromVTKMatrix(TransformMatrixFrontal)
  RotationMat = TransformMatrixFrontal[:3,:3]
  TranslationVect = TransformMatrixFrontal[:3,3]
  
  rotationAxisPoint1_World = np.zeros(3)
  rotationAxisMarkupsNode.GetNthControlPointPositionWorld(0, rotationAxisPoint1_World)
  rotationAxisPoint2_World = np.zeros(3)
  rotationAxisMarkupsNode.GetNthControlPointPositionWorld(1, rotationAxisPoint2_World)
  
  
  #Transform points from World coordinate to local scapula coordinate
  rotationAxisPoint1_World = np.dot(RotationMat,np.atleast_2d(rotationAxisPoint1_World).T) + np.atleast_2d(TranslationVect).T
  rotationAxisPoint2_World = np.dot(RotationMat,np.atleast_2d(rotationAxisPoint2_World).T) + np.atleast_2d(TranslationVect).T
  
  
  
  axisDirectionZ_World = rotationAxisPoint2_World-rotationAxisPoint1_World
  axisDirectionZ_World = axisDirectionZ_World/np.linalg.norm(axisDirectionZ_World)
  # Get transformation between world coordinate system and rotation axis aligned coordinate system
  worldToRotationAxisTransform = vtk.vtkMatrix4x4()
  p=vtk.vtkPlaneSource()
  p.SetNormal(axisDirectionZ_World)
  axisOrigin = np.array(p.GetOrigin())
  axisDirectionX_World = np.array(p.GetPoint1())-axisOrigin
  axisDirectionY_World = np.array(p.GetPoint2())-axisOrigin
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
  
  ShowAngle()
  CSA()
  
# Manual initial update
updateFinalTransform()

# Automatic update when point is moved or transform is modified
rotationTransformNodeObserver = rotationTransformNode.AddObserver(slicer.vtkMRMLTransformNode.TransformModifiedEvent, updateFinalTransform)
rotationAxisMarkupsNodeObserver = rotationAxisMarkupsNode.AddObserver(slicer.vtkMRMLMarkupsNode.PointModifiedEvent, updateFinalTransform)

# Execute these lines to stop automatic updates:
#rotationTransformNode.RemoveObserver(rotationTransformNodeObserver)
#rotationAxisMarkupsNode.RemoveObserver(rotationAxisMarkupsNodeObserver)