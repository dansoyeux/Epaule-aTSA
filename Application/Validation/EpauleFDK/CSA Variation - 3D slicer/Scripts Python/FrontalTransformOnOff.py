# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 12:38:30 2023

@author: Dan
Frontal Transform On/OFF
"""

def FrontalTransformOnOff(On=bool):
    
    ScapulaNode = getNode("Scapula - Rotation repère")
    GleneNode = getNode("Variation CSA - Matrice de rotation glene")
    
    AxeTransverse = getNode ("Scapula - Axe transverse")
    CentreGlene = getNode ("Centre Glene Implant")
    AxeCSA = getNode ("Variation CSA - Axe Centre Glene Antéropostérieur Scapula")
    AxeCSA2 = getNode ("Variation CSA - Axe GHProth Antéropostérieur")
    
    xScapula = getNode ("X Scapula")
    yScapula = getNode ("Y Scapula")
    zScapula = getNode ("Z Scapula")
    ScapulaEnd = getNode("Scapula End")
    NewScapulaEnd = getNode("New Scapula End")
    
    #Transform
    TransformScapula = getNode("Scapula - Rotation plan frontal")
    TransformGlene = getNode("Glene - Rotation plan frontal")
    
    
    
    #Transforme la glene et la scapula dans plan frontal
    if On==True:
        ScapulaNode.SetAndObserveTransformNodeID(TransformScapula.GetID())
        AxeTransverse.SetAndObserveTransformNodeID(TransformScapula.GetID())
        AxeCSA.SetAndObserveTransformNodeID(TransformScapula.GetID())
        AxeCSA2.SetAndObserveTransformNodeID(TransformScapula.GetID())
        xScapula.SetAndObserveTransformNodeID(TransformScapula.GetID())
        yScapula.SetAndObserveTransformNodeID(TransformScapula.GetID())
        zScapula.SetAndObserveTransformNodeID(TransformScapula.GetID())
        ScapulaEnd.SetAndObserveTransformNodeID(TransformScapula.GetID())
        NewScapulaEnd.SetAndObserveTransformNodeID(TransformScapula.GetID())
        
        GleneNode.SetAndObserveTransformNodeID(TransformGlene.GetID()) 
        CentreGlene.SetAndObserveTransformNodeID(TransformGlene.GetID()) 
    #Désactive la transformation de la glene et de la scapula dans plan frontal
    if On==False:
        ScapulaNode.SetAndObserveTransformNodeID(None)
        AxeTransverse.SetAndObserveTransformNodeID(None)
        AxeCSA.SetAndObserveTransformNodeID(None)
        AxeCSA2.SetAndObserveTransformNodeID(None)
        
        xScapula.SetAndObserveTransformNodeID(None)
        yScapula.SetAndObserveTransformNodeID(None)
        zScapula.SetAndObserveTransformNodeID(None)
        ScapulaEnd.SetAndObserveTransformNodeID(None)
        NewScapulaEnd.SetAndObserveTransformNodeID(None)
        
        GleneNode.SetAndObserveTransformNodeID(None)
        CentreGlene.SetAndObserveTransformNodeID(None)