# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 16:01:37 2023

@author: Dan
"""


import numpy as np
import math

import matplotlib.pyplot as plt

# to import csv files
import pandas as pd


# Imports the library to import .h5 and AnyFileOut
import Anybody_LoadOutput as LoadOutput

# Imports the library to make custom graphs
import Anybody_Graph as Graph


# %% Plot Variables setup

GleneContour = Graph.DefineGleneContour("GleneContour")


# %% Load Marta's Results
"""
-------------------------------------------------------------------------------
LOAD MARTA'S RESULTS
-------------------------------------------------------------------------------
"""


def LoadMartadata():
    datacsv = pd.read_csv(r'DataMarta.csv', dtype=np.float64)

    dataMarta = {}
    # global Cases
    Cases = ["Case 1", "Case 2", "Case 3", "Case 4", "Case 5"]

    # Parcours les 25 colonnes, chaque cas a 5 variables
    for i in range(0, 25, 5):
        Angle = pd.Series.to_numpy(datacsv.iloc[:, i])
        Angle = Angle[~np.isnan(Angle)]

        Force = pd.Series.to_numpy(datacsv.iloc[:, i + 1])
        Force = Force[~np.isnan(Force)]

        COPx = pd.Series.to_numpy(datacsv.iloc[:, i + 2])
        COPx = COPx[~np.isnan(COPx)]
        COPy = pd.Series.to_numpy(datacsv.iloc[:, i + 3])
        COPy = COPy[~np.isnan(COPy)]

        COP = np.array([COPx, COPy]).T

        COPMax = pd.Series.to_numpy(datacsv.iloc[:, i + 4])
        MaxAngle, Maxx, Maxy = COPMax[0], COPMax[1], COPMax[2]

        Case = {}

        Case["Angle"] = LoadOutput.ArrayToDictionnary(
            Angle, VariableDescription="Angle d'abduction [°]")
        Case["ForceContact"] = LoadOutput.ArrayToDictionnary(
            Force, VariableDescription="Force de contact [Newton]")
        Case["COP"] = LoadOutput.ArrayToDictionnary(
            COP, VariableDescription="Position du centre de pression [mm]")

        # Maximal COPy position
        Case["COP"]["Max y Angle"] = {}
        Case["COP"]["Max y Angle"]["y"] = Maxy

        # x positon when COPy is maximal
        Case["COP"]["Max y Angle"]["x"] = Maxx

        # Angle when COPy is maximal
        Case["COP"]["Max y Angle"]["Angle"] = MaxAngle

        dataMarta[Cases[int(i / 5)]] = Case

    return dataMarta


dataMarta = LoadMartadata()


# %% Load Lauranne's Results
"""
-------------------------------------------------------------------------------
LOAD LAURANNE'S RESULTS
-------------------------------------------------------------------------------
"""
dataLauranne = {}
dataLauranne["Anybody"] = LoadOutput.LoadResultsLauranne('DataLauranne')

dataLauranne["FDKArticle"] = LoadOutput.LoadResultsLauranne(
    'DataLauranne_OLDFDK')
dataLauranne["Graphiques"] = LoadOutput.LoadGraphLauranne()


dataLauranneNewgh = {}
dataLauranneNewgh["Case 1"] = LoadOutput.LoadResultsLauranne(
    'DataLauranne_case1-New-ghProth')
dataLauranneNewgh["Case 3"] = LoadOutput.LoadResultsLauranne(
    'DataLauranne_case3-New-ghProth')

# %% BERGMANN DATA
"""
-------------------------------------------------------------------------------
BERGMANN DATA
-------------------------------------------------------------------------------
"""


def LoadDataBergmann():
    BodyWeight = 75 * 9.81

    # Data of bergmann in abduction without the 2kg load
    # dataBergmann = {"Angle": {"Total":np.array([15,30,45,75])},"ForceContact":{"Total":np.array([21,35,51,85])/100*BodyWeight}}

    Angle = np.array([15, 30, 45, 75]).T
    ForceContact = np.array([21, 35, 51, 85]).T / 100 * BodyWeight

    dataBergmann = {}

    dataBergmann["Angle"] = LoadOutput.ArrayToDictionnary(
        Angle, VariableDescription="Angle d'abduction [°]")
    dataBergmann["ForceContact"] = LoadOutput.ArrayToDictionnary(
        ForceContact, VariableDescription="Force de contact [Newton]")

    return dataBergmann


dataBergmann = LoadDataBergmann()

# %%                                                  OLD RESULTS
"""
-------------------------------------------------------------------------------
LÉGENDE DES NOMS DES DICTIONNAIRES STOCKANT MES RÉSULTATS


Results : vieux résultats avec problème penché
Neutre : quand l'implant glenoïdien n'a subi aucune rotation (Matrice de rotation comme Lauranne)
ResultsDroit : problème penché fixed avec les driver pelvis
Antero : quand la glene est tournée autour de l'axe anteropostérieur de la scapula
GlenTilt : quand la glène est tournée de l'axe anteropostérieur de l'implant glenoidien'
EnFace : quand la rotation externe a été corrigée pour que l'implant humeral soit en face comme le modèle Lauranne pour chaque cas (7° de différence)
EnFace0 : quand la rotation externe a été corrigée pour que l'implant humeral soit excatement en face (axes x environ parallèles)
EnFace21 : correction de -21° d'external rotation pour que le cas neutre soit positionné comme Lauranne. Pour tous les cas ExtRot = -21°
NoFlexion : Driver qui fixe la flexion GH à 0
GHReactions_Circle : Results when GHReactions with nodes modified to be on a circle on the glenoid implant
GHReactions_Edge : Results when GHReactions with nodes modified to be on the edge of the implant
GHReactions_old: When the normal AMMR GHReactions are activated
CustomSpringForce : ki du FDK modifiés pour centrer le COP sur tous les cas
FitCOPMarta : ki modifiés pour avoir un COP initial proche de celui de Marta
Elevation : when the movement is an elevation in the scapular plane and not an abduction in the frontal plane
Oldgh : mon modèle avec même définition du node scapula.gh que Lauranne et pas le centre de la sphère fit sur la glene
-------------------------------------------------------------------------------
"""


SaveDatadir = '../SaveData/Variation_CSA/'

h5Path = ['Results_16-06-case1-2.229deg-up-anteroposterior',  # Case  1
          # Case  2 (CHANGER)
          'Results_16-06-case1-2.229deg-up-anteroposterior',
          'Results_16-06-case3-11.435deg-up-anteroposterior',  # Case 3
          'Results_16-06-case4-7.587deg-down-anteroposterior',  # Case 4
          'Results_16-06-case5-11.435deg-up-anteroposterior'
          ]


OldCaseNames = ["Case 1", "Case 2", "Case 3", "Case 4", "Case 5"]
# Results = LoadOutput.LoadSimulations(SaveDatadir, h5Path, OldCaseNames)


# ResultsNeutre = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_16-06-case0-no-rotation')
# ResultsNeutreFaibleForce = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_29-06-neutre-px-pour-faible-Fcontact')
# ResultsAntero = {"Case 1": LoadOutput.LoadResultsh5(SaveDatadir, 'Results_21-06-case1-test-axis-anteroscapula')}

# ResultsNeutreDroit = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_30-06-case0-pas-penche-en-avant')
# ResultsNeutreDroit_NoFlexion = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_30-06-neutre-no-flexion')

# # ResultsOldgh
# ResultsOldgh = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_21-06-case0-test-old-gh')
# ResultsOldgh_FDKCorrectedFactors = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_21-06-case0-test-old-gh-biglianieq-corrected-factors')
# ResultsOldgh_ForceFDK_x2 = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_21-06-case0-test-old-gh-Forcefdk-x2')
# ResultsOldgh_ForceFDK_x5 = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_21-06-case0-test-old-gh-Forcefdk-x5')


# # Results new gh
# Results_ForceFDK_x2 = {}
# Results_ForceFDK_x2["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_21-06-case1-test-Forcefdk-x2')
# Results_ForceFDK_x2["Case 3"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_21-06-case3-test-Forcefdk-x2')


# ResultsDroit_NoFlexion = {}
# ResultsDroit_NoFlexion["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_30-06-case1-no-flexion')
# ResultsDroit_NoFlexion["Case 3"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_04-07-case3-no-flexion-ExtRot_-15deg')

# ResultsDroit = {}
# ResultsDroit["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_04-07-case1-pas-penche-en-avant')

# ResultsDroit["Case 3"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_04-07-case3-pas-penche-en-avant')
# ResultsDroit["Case 4"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_04-07-case4-pas-penche-en-avant')
# ResultsDroit["Case 5"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_04-07-case5-pas-penche-en-avant')


# # Droit et avec axe anteropostérieur scapula comme axe de rotations
# ResultsDroitAntero = {}
# ResultsDroitAntero["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_05-07-case1-droit-antero')
# # ResultsDroitAntero["Case 2"] = LoadOutput.LoadResultsh5(SaveDatadir,'Results_05-07-case2-droit-antero')
# ResultsDroitAntero["Case 3"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_05-07-case3-droit-antero')
# ResultsDroitAntero["Case 4"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_05-07-case4-droit-antero')
# ResultsDroitAntero["Case 5"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_05-07-case5-droit-antero')

# ResultsDroitAntero60 = {}
# ResultsDroitAntero60["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_05-07-case1-droit-antero-nstep60')

# ResultsDroitAnteroBiglianieq = {}
# ResultsDroitAnteroBiglianieq["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_05-07-case1-droit-antero-biglianieq')

# # K0 = 1 with bigliani model
# ResultsDroitAnteroBiglianieq_k0_1 = {}
# ResultsDroitAnteroBiglianieq_k0_1["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_07-07-case1-droit-antero-k0=1')

# ResultsDroitAnteroBiglianieq_k0_01 = {}
# ResultsDroitAnteroBiglianieq_k0_01["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results_07-07-case1-droit-antero-k0=0,1')

# # ResultsDroitAntero_FSpring_10 = {}
# # ResultsDroitAntero_FSpring_10["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir,'Results_07-07-case1-droit-antero-testF=10')

# # Puts every ki =0 except k0 to have a constant spring force
# ResultsDroitAntero_Fspring_Cste = {}
# ResultsDroitAntero_Fspring_Cste["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-11-07-case1-antero-SpringForce-Constante', AddConstants=True)


# # Résultats en face (ExtRot = -21)
# ResultsDroitEnFace = {}
# ResultsDroitEnFace["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-11-07-case1-ExtRot_-21deg-not-antero', AddConstants=True)


# # 21° angle correction (même angle que en face case 1)
# ResultsDroitEnFace21Antero = {}
# ResultsDroitEnFace21Antero["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-17-07-case1-antero-Droit-EnFace21', AddConstants=True)
# ResultsDroitEnFace21Antero["Case 2"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-17-07-case2-antero-Droit-EnFace21', AddConstants=True, Failed=8)
# ResultsDroitEnFace21Antero["Case 3"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-17-07-case3-antero-Droit-EnFace21', AddConstants=True)
# ResultsDroitEnFace21Antero["Case 4"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-17-07-case4-antero-EnFace21', AddConstants=True)
# ResultsDroitEnFace21Antero["Case 5"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-17-07-case5-antero-EnFace21', AddConstants=True)

# # 15° External rotation to be en face en antéro
# ResultsDroitEnFaceAntero = {}
# ResultsDroitEnFaceAntero["Case 3"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-11-07-case3-ExtRot_-16deg-antero', AddConstants=True)
# ResultsDroitEnFaceAntero["Case 5"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-14-07-case5-EnFace-ExtRot_-16deg-ScapulaTiltAxis', AddConstants=True)

# # 15° External rotation to be en face en antéro
# ResultsDroitEnFace0Antero = {}
# ResultsDroitEnFace0Antero["Case 3"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-14-07-case3-EnFace_0deg-ScapulaTiltAxis', AddConstants=True)
# ResultsDroitEnFace0Antero["Case 5"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-14-07-case5-EnFace_0deg-ScapulaTiltAxis', AddConstants=True)


# # 20° External rotation to be en face avec GlenTilt autour glenoid x axis
# ResultsDroitEnFaceGlenTilt = {}
# ResultsDroitEnFaceGlenTilt["Case 3"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-11-07-case3-ExtRot_-20deg-Glenoid-TiltAxis', AddConstants=True)

# # Influence paramètre AdaptativeForceTol
# ResultsDroitEnFace21AnteroAdaptativeForceTol = {}
# ResultsDroitEnFace21AnteroAdaptativeForceTol["Case 4"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-17-07-case4-antero-EnFace21-AdaptativeForceTol', AddConstants=True)

# # Incluence longueur Acromion sur décrochage case 2
# ResultsDroitAnteroEnFace_ExtensionVariation = {}
# ResultsDroitAnteroEnFace_ExtensionVariation["8mm Extension (Half)"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-17-07-middletilt-AcromionOffset_halfextended-antero', AddConstants=True)
# # One step failed to solve FDK (forceTol too high) but the simulation continued
# ResultsDroitAnteroEnFace_ExtensionVariation["10mm Extension"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-18-07-middletilt-AcromionOffset_10mm-antero', AddConstants=True)
# # Failed at multiple steps and COP makes jumps at some points
# ResultsDroitAnteroEnFace_ExtensionVariation["12mm Extension"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-18-07-middletilt-AcromionOffset_12mm-antero', AddConstants=True)
# ResultsDroitAnteroEnFace_ExtensionVariation["16.9mm Extension (Full)"] = ResultsDroitEnFace21Antero["Case 2"]

# # Test case 2 ForceTol
# ResultsDroitAnteroEnFace_VariationForceTol = {}
# ResultsDroitAnteroEnFace_VariationForceTol["ForceTol = 0.001"] = ResultsDroitEnFace21Antero["Case 2"]
# # Pénétration humérus dans acromion
# ResultsDroitAnteroEnFace_VariationForceTol["ForceTol = 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-19-07-case2-droit-antero-ForceTol_1', AddConstants=True, Failed=18)
# ResultsDroitAnteroEnFace_VariationForceTol["ForceTol = 5"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-18-07-case2-droit-antero-ForceTol_5', AddConstants=True)
# ResultsDroitAnteroEnFace_VariationForceTol["ForceTol = 10"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-18-07-case2-droit-antero-ForceTol_10', AddConstants=True)
# ResultsDroitAnteroEnFace_VariationForceTol["ForceTol = 10 Adaptative On"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-18-07-case2-droit-antero-ForceTol_10-AdaptativOn', AddConstants=True, Failed=21)
# ResultsDroitAnteroEnFace_VariationForceTol["ForceTol = 20"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-18-07-case2-droit-antero-ForceTol_20', AddConstants=True)


# Results with GHReactions force activated
"""
Won't work anymore cause uses old GHReactions
To load it, comment the part where we charge the CavityNodes position
"""
# ResultsDroitEnteroEnface_GHReactions_old = {}
# ResultsDroitEnteroEnface_GHReactions_old["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir,'Results-19-07-case1-droit-antero-GHReactions_On',AddConstants=True,GHReactions=False)
# ResultsDroitEnteroEnface_GHReactions_old["Case 4"] = LoadOutput.LoadResultsh5(SaveDatadir,'Results-19-07-case4-droit-antero-GHReactions_On',AddConstants=True,GHReactions=False)

# ResultsDroitEnteroEnface_GHReactions_old_Strength_x2 = {}
# ResultsDroitEnteroEnface_GHReactions_old_Strength_x2["Case 4"] = LoadOutput.LoadResultsh5(SaveDatadir,'Results-19-07-case4-droit-antero-GHReactions_Pull_strength_x2',AddConstants=True,GHReactions=True)

# ResultsDroitEnteroEnface_GHReactions_old_Strength_x5={}
# ResultsDroitEnteroEnface_GHReactions_old_Strength_x5["Case 4"] = LoadOutput.LoadResultsh5(SaveDatadir,'Results-19-07-case4-droit-antero-GHReactions_Pull_strength_x5',AddConstants=True,GHReactions=True)
"""
--------------------------------------------------------------------
"""

# """GHReactions Circle"""
# ResultsDroitEnteroEnface_GHReactions_Circle = {}
# ResultsDroitEnteroEnface_GHReactions_Circle["Case 2"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-26-07-case2-droit-antero-EnFace-GHReactions_Circle', AddConstants=True, GHReactions="Circle")

# ResultsDroitEnteroEnface_GHReactions_Circle_Strength_x5 = {}
# ResultsDroitEnteroEnface_GHReactions_Circle_Strength_x5["Case 4"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-19-07-case4-droit-antero-GHReactions_Circle-Pull_strength_x5', AddConstants=True, GHReactions="Circle")

# """Initial Spring Force"""
# ResultsDroitEnteroEnface_InitialSpringForce = {}
# ResultsDroitEnteroEnface_InitialSpringForce["Case 4"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-19-07-case4-droit-antero-InitialForce_On', AddConstants="Circle")

# """Custom spring Force"""
# ResultsDroitenteroEnFace_CustomSpringForce = {}
# ResultsDroitenteroEnFace_CustomSpringForce["Case 1"] = ResultsDroitEnFace21Antero["Case 1"]
# ResultsDroitenteroEnFace_CustomSpringForce["Case 2"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-19-07-case2-droit-antero-EnFace-CustomForce', AddConstants=True)
# ResultsDroitenteroEnFace_CustomSpringForce["Case 3"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-19-07-case3-droit-antero-EnFace-CustomForce', AddConstants=True)
# ResultsDroitenteroEnFace_CustomSpringForce["Case 4"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-19-07-case4-droit-antero-EnFace-CustomForce', AddConstants=True)
# ResultsDroitenteroEnFace_CustomSpringForce["Case 5"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-19-07-case5-droit-antero-EnFace-CustomForce', AddConstants=True)

# """Fit COP Marta"""
# ResultsDroitenteroEnFace_FitCOPMarta = {}
# ResultsDroitenteroEnFace_FitCOPMarta["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-25-07-case1-droit-antero-EnFace-CustomForce_FitCOPMarta', AddConstants=True)
# ResultsDroitenteroEnFace_FitCOPMarta["Case 3"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-25-07-case3-droit-antero-EnFace-CustomForce_FitCOPMarta', AddConstants=True)

# ResultsDroitenteroEnFace_FitCOPMarta_1 = {}
# ResultsDroitenteroEnFace_FitCOPMarta_1["Case 3"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-25-07-case3-droit-antero-EnFace-CustomForce_FitCOPMarta_1', AddConstants=True)

# ResultsDroitenteroEnFace_FitCOPMarta_GHReactions_Circle = {}
# ResultsDroitenteroEnFace_FitCOPMarta_GHReactions_Circle["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-25-07-case1-droit-antero-EnFace-CustomForce_FitCOPMarta-GHReactions', AddConstants=True, GHReactions="Circle")

# """GHReactions Edge"""
# ResultsDroitEnteroEnface_GHReactions_Edge = {}
# ResultsDroitEnteroEnface_GHReactions_Edge["Case 2"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-26-07-case2-droit-antero-EnFace-GHReactions_Edge', AddConstants=True, GHReactions="Edge")

# ResultsDroitEnteroEnface_GHReactions_Edge_ForceTol_1 = {}
# ResultsDroitEnteroEnface_GHReactions_Edge_ForceTol_1["Case 2"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-26-07-case2-droit-antero-EnFace-GHReactions_Edge-ForceTol_1', AddConstants=True, GHReactions="Edge")


# """Arm elevation"""
# ResultsDroitAntero_Elevation = {}
# ResultsDroitAntero_Elevation["Case 1"] = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-28-07-case1-droit-antero-EnFace-Elevation', AddConstants=True)

# """Results CustomForce + Tilt LocalGlenoid old"""
# ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Old = {}
# ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Old["Case 1"] = LoadOutput.LoadResultsh5(
#     SaveDatadir, 'Results-31-07-case1-droit-GlenoidAxisTilt-EnFace-CustomForce', AddConstants=True)

# ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Old["Case 2"] = LoadOutput.LoadResultsh5(
#     SaveDatadir, 'Results-31-07-case2-droit-GlenoidAxisTilt-EnFace-CustomForce', AddConstants=True)

# ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Old["Case 3"] = LoadOutput.LoadResultsh5(
#     SaveDatadir, 'Results-31-07-case3-droit-GlenoidAxisTilt-EnFace-CustomForce', AddConstants=True)

# ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Old["Case 4"] = LoadOutput.LoadResultsh5(
#     SaveDatadir, 'Results-31-07-case4-droit-GlenoidAxisTilt-EnFace-CustomForce', AddConstants=True)

# ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Old["Case 5"] = LoadOutput.LoadResultsh5(
#     SaveDatadir, 'Results-31-07-case5-droit-GlenoidAxisTilt-EnFace-CustomForce', AddConstants=True)


"""new Deltoid wrapping"""
ResultsDroitEnFaceAnteroTiltLocalGlenoid_NewDeltoideusLateralWrapping_Cylinder = {}
ResultsDroitEnFaceAnteroTiltLocalGlenoid_NewDeltoideusLateralWrapping_Cylinder["Case 5"] = LoadOutput.LoadResultsh5(
    SaveDatadir, 'Results-08-08-case5-droit-GlenoidAxisTilt-EnFace-NewDeltoideusLateralWrapping-Cylinder', AddConstants=True)

ResultsDroitEnFaceAnteroTiltLocalGlenoid_NewDeltoideusLateralWrapping_Ellipsoid = {}
ResultsDroitEnFaceAnteroTiltLocalGlenoid_NewDeltoideusLateralWrapping_Ellipsoid["Case 5"] = LoadOutput.LoadResultsh5(
    SaveDatadir, 'Results-08-08-case5-droit-GlenoidAxisTilt-EnFace-NewDeltoideusLateralWrapping-Ellipsoid', AddConstants=True)

"""new Deltoid wrapping avec custom force"""
ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_NewDeltoideusLateralWrapping_Cylinder = {}
ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_NewDeltoideusLateralWrapping_Cylinder["Case 5"] = LoadOutput.LoadResultsh5(
    SaveDatadir, 'Results-07-08-case5-droit-GlenoidAxisTilt-EnFace-CustomForce-NewDeltoideusLateralWrapping-Cylinder', AddConstants=True)

ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_NewDeltoideusLateralWrapping_Ellipsoid = {}
ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_NewDeltoideusLateralWrapping_Ellipsoid["Case 5"] = LoadOutput.LoadResultsh5(
    SaveDatadir, 'Results-07-08-case5-droit-GlenoidAxisTilt-EnFace-CustomForce-NewDeltoideusLateralWrapping-Ellipsoid', AddConstants=True)

"""Glenoid local tilt axis + custom force pour centrer COP"""

Files = ['Results-22-08-case1-droit-GlenoidAxisTilt-EnFace-CustomForce',
         'Results-22-08-case2-droit-GlenoidAxisTilt-EnFace-CustomForce',
         'Results-22-08-case3-droit-GlenoidAxisTilt-EnFace-CustomForce',
         'Results-22-08-case4-droit-GlenoidAxisTilt-EnFace-CustomForce',
         'Results-22-08-case5-droit-GlenoidAxisTilt-EnFace-CustomForce'
         ]

ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce = LoadOutput.LoadSimulationCases(SaveDatadir, Files, OldCaseNames, AddConstants=True)

ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Neutre = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-22-08-case0-droit-GlenoidAxisTilt-EnFace-CustomForce', AddConstants=True)


ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Neutre_LeftArmOn = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-30-08-case0-droit-GlenoidAxisTilt-EnFace-CustomForce-CorrectionHumerusPos-LeftArmOn', AddConstants=True)

# %%                                                        NEW RESULTS

"""Correction of the humeral implant position to be exactly on the edge of the new humeral bone STL (not the old one), Case 1 failing why though :/"""


CaseSequence = [6, 1, 2, 5, 3, 7, 4]

date = "Results-25-08-case"
description = "-droit-GlenoidAxisTilt-EnFace-CustomForce-CorrectionHumerusPos"

Files = [date + str(CaseNumber) + description for CaseNumber in CaseSequence]

CaseNames = ["Case " + str(CaseNumber) for CaseNumber in CaseSequence]

ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos = LoadOutput.LoadSimulationCases(SaveDatadir, Files, CaseNames, AddConstants=True)

# En position neutre
ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos_Neutre = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-25-08-case0-droit-GlenoidAxisTilt-EnFace-CustomForce-CorrectionHumerusPos', AddConstants=True)


# %%                                                CODE TEMPLATES

"""Séparation des COP des 5 cas sur 2 subplots"""
# Graph.COPGraph(DATA, "Position du centre de pression", GleneContour, CasesOn=["Case 1", "Case 2", "Case 3"], Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(DATA, "Position du centre de pression", GleneContour, CasesOn=["Case 4", "Case 5"], Subplot={"Dimension": [1, 2], "Number": 2})

"""COP et contact Force de tous les cas"""
# Graph.COPGraph(DATA, "TITRE", GleneContour, CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression")
# Graph.Graph(DATA , "Angle", "ForceContact", "TITRE", CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Forces de contact entre les implants")

"""Comparaison COP et ForceContact entre plusieurs données"""
# comp = {"NOM_1": DATA1, "NOM_2": DATA2}

# for Case in DATA1:
#     Graph.COPGraph(comp, "TITRE " + Graph.GetCaseDescription(Case), GleneContour, Compare=True, CasesOn=[Case], Subplot={"Dimension": [1, 2], "Number": 1})
#     Graph.Graph(comp, "Angle", "ForceContact", "TITRE " + Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

"""Graph de l'activation des muscles si 4 muscles (donc subplot 2x2)"""
# # Si juste 4 muscles et prend les noms de muscles dans le cas 1, enlever ["Case 1"] si pas de cas de simulation et le CasesOn
# for index, MuscleName in enumerate(list(DATA["Case 1"]["Muscles"].keys())):
#     Graph.MuscleGraph(DATA, MuscleName, "Angle", "Activity", "Activation des muscles", CasesOn="all", SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1})

"""Graph des forces musculaires s'il y a 4 muscles """
# # Si juste 4 muscles et prend les noms de muscles dans le cas 1, enlever ["Case 1"] si pas de cas de simulation et le CasesOn
# for index, MuscleName in enumerate(list(DATA["Case 1"]["Muscles"].keys())):
#     Graph.MuscleGraph(DATA, MuscleName, "Angle", "Ft", "Forces musculaires", CasesOn="all", SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1})

"""Graph d'une variable cas par cas sans comparer"""
# for Case in DATA1:
#     Graph.COPGraph(DATA1, "TITRE " + Graph.GetCaseDescription(Case), GleneContour, CasesOn=[Case])
#     Graph.Graph(DATA1, "Angle", "ForceContact", "TITRE " + Graph.GetCaseDescription(Case), CasesOn=[Case])

"""Toutes les composantes_y et total activés"""
# Graph.Graph(DATA, "Angle", "NOM_VARIABLE_Y", "TITRE", Composante_y=["x", "y", "z", "Total"])


"""Composantes_y de GHLin"""
# Graph.Graph(DATA, "Angle", "GHLin", "TITRE", Composante_y=["AP", "IS", "ML", "Total"])


# %% Résultats neutres

# Graph.COPGraph(ResultsNeutre, 'Résultats Lauranne Anybody', GleneContour)
# Graph.Graph(ResultsNeutre, "Angle", "ForceContact", 'Nouveaux Résultats Neutre')


# %% Comparaison neutre avec Lauranne

# comp1 = {"Lauranne Code": dataLauranne["Anybody"], "Lauranne Article": dataLauranne["Graphiques"], "Nouveaux Résultats": ResultsNeutre}
# Graph.COPGraph(comp1, 'Comparaison Lauranne', GleneContour, Compare=True)


# comp2 = {"Lauranne Code": dataLauranne["Anybody"], "Nouveaux Résultats": ResultsNeutre, "Bergmann": dataBergmann}
# comp2 = {"Lauranne Code": dataLauranne["Anybody"], "Nouveaux Résultats": ResultsNeutre, "Nouveaux Résultats Faicle Fcontact": ResultsNeutreFaibleForce}
# Graph.Graph(comp2, "Angle", "ForceContact", 'Comparaison Neutre', Compare=True)
# Graph.COPGraph(comp2, 'Comparaison Lauranne', GleneContour, Compare=True)


# compNeutre = {"Neutre penché": ResultsNeutre, "Neutre pas penché": ResultsNeutreDroit, "Lauranne": dataLauranne["Anybody"], }

# Graph.COPGraph(compNeutre, "Comparaison Neutres", GleneContour, Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(compNeutre, "Angle", "ForceContact", "Comparaison Neutres", Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# %%Résultats Marta seule


# Graph.Graph(dataMarta, "Angle", "ForceContact", 'Résultats Marta', CasesOn="all")


# Graph.COPGraph(dataMarta, "Résultats Marta", GleneContour, CasesOn=["Case 1", "Case 2", "Case 3"], Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(dataMarta, "Résultats Marta", GleneContour, CasesOn=["Case 4", "Case 5"], Subplot={"Dimension": [1, 2], "Number": 2})


# %% Résultats seuls


"""
------------------------------------------------------------------------
Droit Seul
------------------------------------------------------------------------
"""

# Graph.COPGraph(ResultsDroit, "Résultats droit", GleneContour, CasesOn=["Case 1", "Case 3"], Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(ResultsDroit, "Résultats droit", GleneContour, CasesOn=["Case 4", "Case 5"], Subplot={"Dimension": [1, 2], "Number": 2})

# Graph.COPGraph(ResultsDroitAntero, "Résultats droit antero", GleneContour, CasesOn=["Case 1", "Case 3"], Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(ResultsDroitAntero, "Résultats droit antero", GleneContour, CasesOn=["Case 4", "Case 5"], Subplot={"Dimension": [1, 2], "Number": 2})

# Graph.COPGraph(Results, "Résultats penché", GleneContour, CasesOn=["Case 1", "Case 3"], Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(Results, "Résultats penché", GleneContour, CasesOn=["Case 4", "Case 5"], Subplot={"Dimension": [1, 2], "Number": 2})

# %% Comparaison droit/droit antéro

# comp5 = {"Marta": dataMarta, "Résultats Droit": ResultsDroit, "Résultats Droit antero": ResultsDroitAntero}

# for Case in ["Case 1", "Case 3", "Case 4", "Case 5"]:

#     Graph.COPGraph(comp5, Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
#     Graph.Graph(comp5, "Angle", "ForceContact", Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# comp7 = {"Marta": dataMarta, "Résultats Droit": ResultsDroit, "Résultats Droit antero": ResultsDroitAntero, "Résultats Droit Sans Flexion": ResultsDroit_NoFlexion}

# for Case in ["Case 1", "Case 3"]:
#     Graph.COPGraph(comp7, Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
#     Graph.Graph(comp7, "Angle", "ForceContact", Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# %% Comparaison En Face (variation angle ExternalRotation)

# # Case 1
# comp6 = {"Marta": dataMarta, "Résultats Droit": ResultsDroit, "Résultats Droit en face": ResultsDroitEnFace}
# Graph.COPGraph(comp6, Graph.GetCaseDescription("Case 1"), GleneContour, CasesOn=["Case 1"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(comp6, "Angle", "ForceContact", Graph.GetCaseDescription("Case 1"), CasesOn=["Case 1"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# # Case 3
# comp8 = {"Marta": dataMarta, "Résultats Droit": ResultsDroit, "Résultats Droit antero": ResultsDroitAntero, "Résultats Droit antéro en face -16": ResultsDroitEnFaceAntero}
# Graph.COPGraph(comp8, Graph.GetCaseDescription("Case 3"), GleneContour, CasesOn=["Case 3"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.Graph(comp8, "Angle", "ForceContact", Graph.GetCaseDescription("Case 3"), CasesOn=["Case 3"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# comp9 = {"Marta": dataMarta, "Résultats Droit": ResultsDroit, "Résultats Droit antero": ResultsDroitAntero, "Résultats Droit antéro en face -16": ResultsDroitEnFaceAntero, "Résultats droit antéro parfait en face -10": ResultsDroitEnFace0Antero}
# Graph.COPGraph(comp9, Graph.GetCaseDescription("Case 3"), GleneContour, CasesOn=["Case 3"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.Graph(comp9, "Angle", "ForceContact", Graph.GetCaseDescription("Case 3"), CasesOn=["Case 3"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# # Case 5
# comp8 = {"Marta": dataMarta, "Résultats Droit": ResultsDroit, "Résultats Droit antero": ResultsDroitAntero, "Résultats Droit antéro en face -16": ResultsDroitEnFaceAntero}
# Graph.COPGraph(comp8, Graph.GetCaseDescription("Case 5"), GleneContour, CasesOn=["Case 5"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.Graph(comp8, "Angle", "ForceContact", Graph.GetCaseDescription("Case 5"), CasesOn=["Case 5"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# comp9 = {"Marta": dataMarta, "Résultats Droit": ResultsDroit, "Résultats Droit antero": ResultsDroitAntero, "Résultats Droit antéro en face -16": ResultsDroitEnFaceAntero, "Résultats droit antéro parfait en face -10": ResultsDroitEnFace0Antero}
# Graph.COPGraph(comp9, Graph.GetCaseDescription("Case 5"), GleneContour, CasesOn=["Case 5"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.Graph(comp9, "Angle", "ForceContact", Graph.GetCaseDescription("Case 5"), CasesOn=["Case 5"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# %% Comparaison Marta/tilt dans code Lauranne
# comp3 = {"Lauranne New gh": dataLauranneNewgh, "Lauranne": {"Case 1": dataLauranne["Anybody"], "Case 3": dataLauranne["Anybody"]}, "Marta": dataMarta, "Résultats Droit": ResultsDroit}

# Graph.COPGraph(comp3, Graph.GetCaseDescription(Case), GleneContour, CasesOn=["Case 1"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(comp3, "Angle", "ForceContact", Graph.GetCaseDescription(Case), CasesOn=["Case 1"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# Graph.COPGraph(comp3, Graph.GetCaseDescription(Case), GleneContour, CasesOn=["Case 3"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(comp3, "Angle", "ForceContact", Graph.GetCaseDescription(Case), CasesOn=["Case 3"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# %% Étude sensibilité force

# """
# influence amplitude de la force
# """
# comp4 = {"Résultats Neutre": ResultsNeutre, "Old gh and FDK force x2": ResultsOldgh_ForceFDK_x2, "Old gh and FDK force x5": ResultsOldgh_ForceFDK_x5, "Marta": dataMarta["Case 1"]}
# Graph.COPGraph(comp4, 'Comparaison Old gh', GleneContour, CasesOn='all', Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(comp4, "Angle", "ForceContact", 'Comparaison Old gh', CasesOn='all', Subplot={"Dimension": [1, 2], "Number": 2})


# comp5 = {"Résultats Neutre": ResultsNeutre, "Old gh and FDK force x2": ResultsOldgh_ForceFDK_x2, "Old gh and FDK force x5": ResultsOldgh_ForceFDK_x5}
# MuscleList = list(ResultsDroitEnFace21Antero["Case 4"]["Muscles"].keys())
# for Muscle in MuscleList:
#     Graph.MuscleGraph(comp5, Muscle, "Angle", "Ft", "Activation du " + Muscle, Compare=True)


# """
# changer entre bigliani eq et eq lauranne
# """
# comp11 = {"Marta": dataMarta, "equation FDK Lauranne": ResultsDroitAntero, "Bigliani": ResultsDroitAnteroBiglianieq}
# Graph.COPGraph(comp11, Graph.GetCaseDescription("Case 1"), GleneContour, ["Case 1"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.Graph(comp11, "Angle", "ForceContact", Graph.GetCaseDescription("Case 1"), CasesOn=['Case 1'], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# """
# Influence de k0
# """
# comp12 = {"Marta": dataMarta, "equation FDK Lauranne": ResultsDroitAntero, "Bigliani et k0=1": ResultsDroitAnteroBiglianieq_k0_1, "Bigliani et k0=0.1": ResultsDroitAnteroBiglianieq_k0_01}
# Graph.COPGraph(comp12, Graph.GetCaseDescription("Case 1"), GleneContour, ["Case 1"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.Graph(comp12, "Angle", "ForceContact", Graph.GetCaseDescription("Case 1"), CasesOn=['Case 1'], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# """
# Influence de Epsilon sur le COP et force
# # """
# # # Ne marchera plus car pas de F_10
# # comp13 = {"Marta":dataMarta,"equation FDK Lauranne":ResultsDroitAntero,"F=-10":ResultsDroitAntero_FSpring_10,"k1-k4 = 0":ResultsDroitAntero_Fspring_Cste}
# # Graph.COPGraph(comp13,Graph.GetCaseDescription("Case 1"),GleneContour,["Case 1"],Compare = True,Subplot = {"Dimension":[1,2],"Number":1},DrawPeakCOPAngleOn=False)
# # Graph.Graph(comp13,"Angle","ForceContact",Graph.GetCaseDescription("Case 1"),CasesOn = ['Case 1'],Compare = True,Subplot = {"Dimension":[1,2],"Number":2})

# %% Etude sensibilité nstep

# comp10 = {"nstep30": ResultsDroitAntero, "nstep60": ResultsDroitAntero60}

# Graph.Graph(comp10, "Angle", "ForceContact", "Sensibilité nStep", CasesOn=["Case 1"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(comp10, "sensibilité nStep", GleneContour, CasesOn=["Case 1"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# %% Test force/epsilon

def ForceLigament(k, Epsilon):
    vectx = np.array([1, Epsilon[0], Epsilon[0]**2,
                     Epsilon[0]**3, Epsilon[0]**4]).T
    vecty = np.array([1, Epsilon[1], Epsilon[1]**2,
                     Epsilon[1]**3, Epsilon[1]**4]).T
    Fx = - 1 * np.dot(k, vectx)
    Fy = - 1 * np.dot(k, vecty)

    FTotal = np.linalg.norm(np.array([Fx, Fy]))
    Fz = -0
    return Fx, Fy, Fz, FTotal


def ForceFDK(k, Epsilon):

    Fx, Fy, Fz, FTotal = [], [], [], []
    E = np.array([Epsilon["Ex"], Epsilon["Ey"]])
    for i in range(len(E[0])):
        fx, fy, fz, ftotal = ForceLigament(k, E[:, i])
        Fx.append(fx)
        Fy.append(fy)
        Fz.append(fz)
        FTotal.append(ftotal)
    return Fx, Fy, Fz, FTotal


# eq Bigliani
# kFDK = np.array([5.62, -1.68, 1.12, 0.9, -0.05])

# eq Lauranne
# kFDK = np.array([10.75, -7.787, 4.391, 0, -0.08637])

# test
# kFDK = np.array([0, -7.787, 4.391, 0, -0.08637])

# px = [-0.002+0.0005] * 15
# py = [0.003 - 0.004] * 15
# pz = [0.001 - 0.0048] * 15


# Forces = {}
# # Calcul Fspring
# Fx,Fy,Fz,FTotal = ForceFDK(kFDK,Results["Case 1"]["Epsilon"])
# Forces["GHLin - pi"] = {"SpringForce":{"ForceTotale":FTotal,"Fx":Fx,"Fy":Fy,"Fz":Fz},"Angle":Results["Case 1"]["Angle"]}

# Deplacement = {"Ex":Results["Case 1"]["Epsilon"]["Ex"] + px,"Ey":Results["Case 1"]["Epsilon"]["Ey"] + py,"Ez":Results["Case 1"]["Epsilon"]["Ez"] + pz}
# Fx,Fy,Fz,FTotal = ForceFDK(kFDK,Deplacement)
# Forces["GHLin"] = {"SpringForce":{"ForceTotale":FTotal,"Fx":Fx,"Fy":Fy,"Fz":Fz},"Angle":Results["Case 1"]["Angle"]}

# Elongation = {"Ex":Results["Case 1"]["Epsilon"]["Ex"]/px,"Ey":Results["Case 1"]["Epsilon"]["Ey"]/py,"Ez":Results["Case 1"]["Epsilon"]["Ez"]}
# Fx,Fy,Fz,FTotal = ForceFDK(kFDK,Elongation)
# Forces["Elongation %"] = {"SpringForce":{"ForceTotale":FTotal,"Fx":Fx,"Fy":Fy,"Fz":Fz},"Angle":Results["Case 1"]["Angle"]}

# Forces["SpringForce"]=Results["Case 1"]
# Graph.Graph("Angle","SpringForce", Forces, "comparaison forces",CasesOn = 'all')
# Graph.Graph("Angle","SpringForce", Forces, "comparaison forces",CasesOn = 'Elongation %')


# %%                                                 Résultats powerpoint


# Graph.Graph(dataMarta, "Angle", "ForceContact", 'Résultats Marta', 'all')


# Graph.COPGraph(dataMarta, "Résultats Marta", GleneContour, CasesOn=["Case 1", "Case 2", "Case 3"], Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(dataMarta, "Résultats Marta", GleneContour, CasesOn=["Case 4", "Case 5"], Subplot={"Dimension": [1, 2], "Number": 2})


# """
# Résultats où tout le temps -21
# """

# Graph.COPGraph(ResultsDroitEnFace21Antero, "Résultats", GleneContour, CasesOn=["Case 1", "Case 2", "Case 3"], Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(ResultsDroitEnFace21Antero, "Résultats", GleneContour, CasesOn=["Case 4", "Case 5"], Subplot={"Dimension": [1, 2], "Number": 2})

# Graph.Graph(ResultsDroitEnFace21Antero, "Angle", "ForceContact", "Résultats", CasesOn='all')

# comp5 = {"Marta": dataMarta, "Résultats": ResultsDroitEnFace21Antero}

# for Case in ["Case 1", "Case 2", "Case 3", "Case 4", "Case 5"]:

#     Graph.COPGraph(comp5, Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
#     Graph.Graph(comp5, "Angle", "ForceContact", Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# %% Point limite d'instabilité extension acromion case 2

# List = list(ResultsDroitAnteroEnFace_ExtensionVariation.keys())
# List.remove("8mm Extension (Half)")

# Graph.COPGraph(ResultsDroitAnteroEnFace_ExtensionVariation, "Point limite d'instabilité extension acromion - glene normale", GleneContour, CasesOn=List, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.Graph(ResultsDroitAnteroEnFace_ExtensionVariation, "Angle", "ForceContact", "Point limite d'instabilité extension acromion - glene normale", CasesOn=List, Subplot={"Dimension": [1, 2], "Number": 2})

# ResultsDroitAnteroEnFace_ExtensionVariation["Marta"] = dataMarta["Case 2"]

# Graph.COPGraph(ResultsDroitAnteroEnFace_ExtensionVariation, "Point limite d'instabilité extension acromion - glene normale", GleneContour, CasesOn=["Marta", "10mm Extension"], Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.Graph(ResultsDroitAnteroEnFace_ExtensionVariation, "Angle", "ForceContact", "Point limite d'instabilité extension acromion - glene normale", CasesOn=["Marta", "10mm Extension"], Subplot={"Dimension": [1, 2], "Number": 2})


# List = list(ResultsDroitAnteroEnFace_ExtensionVariation.keys())
# List.remove("Marta")

# del ResultsDroitAnteroEnFace_ExtensionVariation["Marta"]

# Graph.Graph(ResultsDroitAnteroEnFace_ExtensionVariation, "Angle", "ForceTolError", 'FDK Force Tolerance Errors', Compare=True)

# %% Test ForceTol case 2

# List = list(ResultsDroitAnteroEnFace_VariationForceTol.keys())

# Graph.COPGraph(ResultsDroitAnteroEnFace_VariationForceTol, "Variation ForceTol", GleneContour, CasesOn=["ForceTol = 1"], DrawPeakCOPAngleOn=False)

# Graph.COPGraph(ResultsDroitAnteroEnFace_VariationForceTol, "Variation ForceTol", GleneContour, CasesOn=List[0:3], Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.COPGraph(ResultsDroitAnteroEnFace_VariationForceTol, "Variation ForceTol", GleneContour, CasesOn=List[3:-1], Subplot={"Dimension": [1, 2], "Number": 2}, DrawPeakCOPAngleOn=False)

# Graph.Graph(ResultsDroitAnteroEnFace_VariationForceTol, "Angle", "ForceTolError", 'Variation ForceTol', CasesOn='all', Subplot={"Dimension": [1, 2], "Number": 1})

# Graph.Graph(ResultsDroitAnteroEnFace_VariationForceTol, "Angle", "ForceContact", "Variation ForceTol", CasesOn='all', Subplot={"Dimension": [1, 2], "Number": 2})


# %% GHReactions on

# doesn't work anymore
"""
Reaction Circle VS Normal
"""

# comp18 = {"No Reactions":ResultsDroitEnFace21Antero,"Reactions Circle et Strength x5":ResultsDroitEnteroEnface_GHReactions_Strength_x5 ,"Reactions On et Strength x5":ResultsDroitEnteroEnface_GHReactions_old_Strength_x5}
# Graph.COPGraph(comp18, Graph.GetCaseDescription("Case 4"), GleneContour,CasesOn = ["Case 4"],Compare = True,Subplot = {"Dimension":[1,2],"Number":1},DrawPeakCOPAngleOn=False)
# Graph.Graph(comp18,"Angle","ForceContact",  Graph.GetCaseDescription("Case 4"),CasesOn = ["Case 4"], Compare=True,Subplot = {"Dimension":[1,2],"Number":2})

# MuscleList = list(ResultsDroitEnFace21Antero["Case 4"]["Muscles"].keys())
# for Muscle in MuscleList:
#     Graph.MuscleGraph("Angle","Ft", Muscle, comp18,Muscle + " :" + Graph.GetCaseDescription("Case 4"), CasesOn = ["Case 4"],Compare = True)


# # Graph with the edge nodes coordinates
# Graph.COPGraph(ResultsDroitEnteroEnface_GHReactions_Circle_Strength_x5, "Reactions Circle : " + Graph.GetCaseDescription("Case 4"), GleneContour,CasesOn = ["Case 4"],DrawGHReactionsNodes=True)


# %% initialSpringForce


# Graph.COPGraph(ResultsDroitEnteroEnface_InitialSpringForce, "Initial Spring Force : " + Graph.GetCaseDescription("Case 4"), GleneContour, CasesOn=["Case 4"], Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.Graph(ResultsDroitEnteroEnface_InitialSpringForce, "Angle", "ForceContact", "Initial Spring Force : " + Graph.GetCaseDescription("Case 4"), CasesOn=["Case 4"], Subplot={"Dimension": [1, 2], "Number": 2})

# %% Custom SpringForce pour même position initiale

# ResultsDroitenteroEnFace_CustomSpringForce["Case 1"] = ResultsDroitEnFace21Antero["Case 1"]
# comp19 = {"Marta": dataMarta, "Résultats Droit": ResultsDroitEnFace21Antero, "Centrer COP et Tilt Axis : Scapula Antero axis": ResultsDroitenteroEnFace_CustomSpringForce}

# for Case in list(ResultsDroitenteroEnFace_CustomSpringForce.keys()):
#     Graph.COPGraph(comp19, "COP centré : " + Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
#     Graph.Graph(comp19, "Angle", "ForceContact", "COP centré : " + Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# Graph.COPGraph(ResultsDroitenteroEnFace_CustomSpringForce, "Centrer COP et Tilt Axis : Scapula Antero axis", GleneContour, CasesOn=["Case 1", "Case 2", "Case 3"], Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(ResultsDroitenteroEnFace_CustomSpringForce, "Centrer COP et Tilt Axis : Scapula Antero axis", GleneContour, CasesOn=["Case 4", "Case 5"], Subplot={"Dimension": [1, 2], "Number": 2})
# Graph.Graph(ResultsDroitenteroEnFace_CustomSpringForce, "Angle", "ForceContact", "Centrer COP et Tilt Axis : Scapula Antero axis", CasesOn='all')

# %% Fit COPMarta


# comp21 = {"Marta": dataMarta, "Résultats Fit COP Marta k0 = [20,-10]": ResultsDroitenteroEnFace_FitCOPMarta, "Résultats Droit": ResultsDroitEnFace21Antero}
# Case = "Case 1"
# Graph.COPGraph(comp21, "Custom Spring Force " + Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=True, DrawGHReactionsNodes=True)
# Graph.Graph(comp21, "Angle", "ForceContact", "Custom Spring Force " + Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# comp20 = {"Marta": dataMarta, "Résultats Droit": ResultsDroitEnFace21Antero, "Résultats Fit COP Marta k0 = [16,-20]": ResultsDroitenteroEnFace_FitCOPMarta, "Résultats Fit COP Marta 2  k0 = [25,-20]": ResultsDroitenteroEnFace_FitCOPMarta_1}

# Case = "Case 3"
# Graph.COPGraph(comp20, "Custom Spring Force " + Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.Graph(comp20, "Angle", "ForceContact", "Custom Spring Force " + Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# # Comparaison juste avec Marta


# comp22 = {"Marta": dataMarta, "Résultats Fit COP Marta k0 = [20,-10]": ResultsDroitenteroEnFace_FitCOPMarta}
# Case = "Case 1"
# Graph.COPGraph(comp22, "Custom Spring Force " + Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=True, DrawGHReactionsNodes=True)
# Graph.Graph(comp22, "Angle", "ForceContact", "Custom Spring Force " + Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# comp20 = {"Marta": dataMarta, "Résultats Fit COP Marta k0 = [16,-20]": ResultsDroitenteroEnFace_FitCOPMarta, "Résultats Fit COP Marta 2  k0 = [25,-20]": ResultsDroitenteroEnFace_FitCOPMarta_1}

# Case = "Case 3"
# Graph.COPGraph(comp20, "Custom Spring Force " + Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=False)
# Graph.Graph(comp20, "Angle", "ForceContact", "Custom Spring Force " + Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# # comparaison avec case1 fit + GHReactions
# comp21 = {"Résultats GHReactions et Fit COP Marta k0 = [20,-10]": ResultsDroitenteroEnFace_FitCOPMarta_GHReactions_Circle, "Résultats Fit COP Marta k0 = [20,-10]": ResultsDroitenteroEnFace_FitCOPMarta}
# Case = "Case 1"
# Graph.COPGraph(comp21, "Custom Spring Force " + Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=True, DrawGHReactionsNodes=True)
# Graph.Graph(comp21, "Angle", "ForceContact", "Custom Spring Force " + Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# %% test GHReactions case 2

# # Circle
# Graph.COPGraph(ResultsDroitEnteroEnface_GHReactions_Circle, Graph.GetCaseDescription("Case 2"), GleneContour, CasesOn=["Case 2"], DrawGHReactionsNodes=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(ResultsDroitEnteroEnface_GHReactions_Circle, "Angle", "ForceTolError", Graph.GetCaseDescription("Case 2"), CasesOn=["Case 2"], Subplot={"Dimension": [1, 2], "Number": 2})

# # Muscles activation
# MuscleList = list(ResultsDroitEnteroEnface_GHReactions_Circle["Case 2"]["Muscles"].keys())
# for Muscleindex, Muscle in enumerate(MuscleList):

#     Graph.MuscleGraph(ResultsDroitEnteroEnface_GHReactions_Edge, Muscle, "Angle", "Ft", Graph.GetCaseDescription("Case 2"), CasesOn=["Case 2"], Subplot={"Dimension": [2, 2], "Number": Muscleindex + 1}, SubplotTitle=Muscle)


# # Edge

# Graph.COPGraph(ResultsDroitEnteroEnface_GHReactions_Edge, Graph.GetCaseDescription("Case 2"), GleneContour, CasesOn=["Case 2"], DrawGHReactionsNodes=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(ResultsDroitEnteroEnface_GHReactions_Edge, "Angle", "ForceTolError", Graph.GetCaseDescription("Case 2"), CasesOn=["Case 2"], Subplot={"Dimension": [1, 2], "Number": 2})

# # Muscles activation
# MuscleList = list(ResultsDroitEnteroEnface_GHReactions_Edge["Case 2"]["Muscles"].keys())
# for Muscleindex, Muscle in enumerate(MuscleList):

#     Graph.MuscleGraph(ResultsDroitEnteroEnface_GHReactions_Edge, Muscle, "Angle", "Ft", Graph.GetCaseDescription("Case 2"), CasesOn=["Case 2"], Subplot={"Dimension": [2, 2], "Number": Muscleindex + 1}, SubplotTitle=Muscle)


# # Comparaiso edge/circle
# comp27 = {"GHReactions Edge": ResultsDroitEnteroEnface_GHReactions_Edge, "GHReactions Circle": ResultsDroitEnteroEnface_GHReactions_Circle}

# Graph.COPGraph(comp27, Graph.GetCaseDescription("Case 2"), GleneContour, CasesOn=["Case 2"], Compare=True, DrawGHReactionsNodes=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(comp27, "Angle", "ForceTolError", Graph.GetCaseDescription("Case 2"), CasesOn=["Case 2"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# # Muscles activation
# MuscleList = list(ResultsDroitEnteroEnface_GHReactions_Circle["Case 2"]["Muscles"].keys())
# for Muscleindex, Muscle in enumerate(MuscleList):

#     Graph.MuscleGraph(comp27, Muscle, "Angle", "Ft", Graph.GetCaseDescription("Case 2"), CasesOn=["Case 2"], Compare=True, Subplot={"Dimension": [2, 2], "Number": Muscleindex + 1}, SubplotTitle=Muscle)

# %% GHReactions Circle
# """Influence variation ForceTol"""
# comp = {"GHReactions Edge": ResultsDroitEnteroEnface_GHReactions_Edge, "GHReactions Edge ForceTol = 1": ResultsDroitEnteroEnface_GHReactions_Edge_ForceTol_1}
# Case = "Case 2"
# Graph.COPGraph(comp, "Custom Spring Force " + Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=True, DrawGHReactionsNodes=True)
# Graph.Graph(comp, "Angle", "ForceContact", "Custom Spring Force " + Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# %% Influence forme GHReactions

# comp = {"GHReactions Circle": ResultsDroitEnteroEnface_GHReactions_Circle, "GHReactions Edge": ResultsDroitEnteroEnface_GHReactions_Edge}

# Case = "Case 2"
# Graph.COPGraph(comp, "Custom Spring Force " + Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, DrawPeakCOPAngleOn=True, DrawGHReactionsNodes=True)
# Graph.Graph(comp, "Angle", "ForceContact", "Custom Spring Force " + Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# %% Arm Elevation

# Graph.COPGraph(ResultsDroitAntero_Elevation, "Résultats élévation", GleneContour, CasesOn=["Case 1"], Subplot={"Dimension": [1, 2], "Number": 1})

# Graph.Graph(ResultsDroitAntero_Elevation, "Angle", "ForceContact", "Résultats élévation", CasesOn=["Case 1"], Subplot={"Dimension": [1, 2], "Number": 2})

# comp = {"Résultats": ResultsDroitEnFace21Antero, "Résultats élévation": ResultsDroitAntero_Elevation}

# Graph.COPGraph(comp, "Résultats élévation", GleneContour, CasesOn=["Case 1"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})

# Graph.Graph(comp, "Angle", "ForceContact", "Résultats élévation", CasesOn=["Case 1"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# %%                                                 Tilt Local Glenoid Axis

# # Tous les cas
# Graph.COPGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, "Résultats Centré et Tilt Axis : glenoid axis", GleneContour, CasesOn=["Case 1", "Case 2", "Case 3"], Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, "Résultats Centré et Tilt Axis : glenoid axis", GleneContour, CasesOn=["Case 4", "Case 5"], Subplot={"Dimension": [1, 2], "Number": 2})

# Graph.Graph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, "Angle", "ForceContact", "Résultats Centré et Tilt Axis : glenoid axis", CasesOn='all')

# Graph.Graph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, "Angle", "ForceTolError", "Residual forces", CasesOn='all')

# # Comparaison avec Marta

# comp20 = {"Marta": dataMarta, "Axe tilt : Anteropostérieur Scapula": ResultsDroitEnFace21Antero, "Centré et Axe tilt : Anteropostérieur Scapula": ResultsDroitenteroEnFace_CustomSpringForce, "Axe tilt : Local Glenoid": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce}

# for Case in ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce.keys():

#     Graph.COPGraph(comp20, Graph.GetCaseDescription(Case), GleneContour, [Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
#     Graph.Graph(comp20, "Angle", "ForceContact", Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# %%                                                 Deltoid Lateral Wrapping

# """With custom force"""
# comp21 = {"Résultats Tilt glenoid local custom force": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, "Résultats Tilt glenoid local with Lateral Deltoid wrapping cylinder": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_NewDeltoideusLateralWrapping_Cylinder,
#           "Résultats Tilt glenoid local with Lateral Deltoid wrapping ellipsoid": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_NewDeltoideusLateralWrapping_Ellipsoid}


# Graph.COPGraph(comp21, Graph.GetCaseDescription("Case 5"), GleneContour, ["Case 5"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(comp21, "Angle", "ForceContact", Graph.GetCaseDescription("Case 5"), CasesOn=["Case 5"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# """Without custom force"""
# comp21 = {"Résultats Tilt glenoid local with Lateral Deltoid wrapping cylinder": ResultsDroitEnFaceAnteroTiltLocalGlenoid_NewDeltoideusLateralWrapping_Cylinder,
#           "Résultats Tilt glenoid local with Lateral Deltoid wrapping ellipsoid": ResultsDroitEnFaceAnteroTiltLocalGlenoid_NewDeltoideusLateralWrapping_Ellipsoid}


# Graph.COPGraph(comp21, Graph.GetCaseDescription("Case 5"), GleneContour, ["Case 5"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(comp21, "Angle", "ForceContact", Graph.GetCaseDescription("Case 5"), CasesOn=["Case 5"], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})

# %%                                                local glenoid tilt axis + custom force

# # Comparaison avec Marta
# comp = {"Marta": dataMarta, "Custom Force pour centrer COP": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, "old custom Force": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Old}


# for Case in ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce:
#     Graph.COPGraph(comp, "Custom Force pour centrer COP " + Graph.GetCaseDescription(Case), GleneContour, Compare=True, CasesOn=[Case], Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression")
#     Graph.Graph(comp, "Angle", "ForceContact", "Custom Force pour centrer COP " + Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Force de contact")

# # Graph seuls

# Graph.COPGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, "Custom Force pour centrer COP", GleneContour, CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression")
# Graph.Graph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, "Angle", "ForceContact", "Custom Force pour centrer COP", CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Force de contact")

# Graph.COPGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, "Position du centre de pression", GleneContour, CasesOn=["Case 1", "Case 2", "Case 3"], Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, "Position du centre de pression", GleneContour, CasesOn=["Case 4", "Case 5"], Subplot={"Dimension": [1, 2], "Number": 2})
# Graph.Graph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, "Angle", "ForceContact", "Custom Force pour centrer COP", CasesOn="all")


# # Si juste 4 muscles et prend les noms de muscles dans le cas 1
# for index, MuscleName in enumerate(list(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce["Case 1"]["Muscles"].keys())):
#     Graph.MuscleGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce, MuscleName, "Angle", "Activity", "Activation des muscles", CasesOn="all", SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1})


# # Graph neutre
# Graph.COPGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Neutre, "Position neutre", GleneContour, Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression")
# Graph.Graph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Neutre, "Angle", "ForceContact", "Position neutre", Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Force de contact")

# # Si juste 4 muscles et prend les noms de muscles dans le cas 1
# for index, MuscleName in enumerate(list(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Neutre["Muscles"].keys())):
#     Graph.MuscleGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Neutre, MuscleName, "Angle", "Activity", "Activation des muscles", SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1})

# Graph.Graph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Neutre, "Angle", "GHLin", "Déplacement de l'humérus pour la position neutre", Composante_y=["AP", "IS", "ML", "Total"])


# %%                        Comparaison des neutres avec différent placement humerus

# comp = {"Old": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Neutre, "Fixed humeral pos": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos_Neutre}

# Graph.COPGraph(comp, "Comparaison des neutres", GleneContour, Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(comp, "Angle", "ForceContact", "Comparaison des neutres", Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})
# %%                                                Replacer l'implant huméral + custom force

# # Comparaison avec Marta et correction/no correction
# comp = {"corrected Humeral implant pos": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, "Old humeral implant pos": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce}

# for Case in ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce:
#     Graph.COPGraph(comp, "Influence correction humeral position " + Graph.GetCaseDescription(Case), GleneContour, Compare=True, CasesOn=[Case], Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression")
#     Graph.Graph(comp, "Angle", "ForceContact", "Influence correction humeral position " + Graph.GetCaseDescription(Case), CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Forces de contact entre les implants")

# # Résultats seuls

# Graph.COPGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, "Correction humeral implant position", GleneContour, CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression", DrawPeakCOPAngleOn=False)
# Graph.Graph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, "Angle", "ForceContact", "Correction humeral implant position", CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Forces de contact entre les implants")

Graph.COPGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, "Position du centre de pression", GleneContour, CasesOn=["Case 6", "Case 1", "Case 2"], Subplot={"Dimension": [1, 2], "Number": 1})
Graph.COPGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, "Position du centre de pression", GleneContour, CasesOn=["Case 5", "Case 3", "Case 7", "Case 4"], Subplot={"Dimension": [1, 2], "Number": 2})

# Graph.Graph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, "Angle", "ForceContact", "Forces de contact", CasesOn=["Case 6", "Case 1", "Case 2"], Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, "Angle", "ForceContact", "Forces de contact", CasesOn=["Case 5", "Case 3", "Case 7", "Case 4"], Subplot={"Dimension": [1, 2], "Number": 2})

# # Si juste 4 muscles et prend les noms de muscles dans le cas 1
# for index, MuscleName in enumerate(list(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos["Case 1"]["Muscles"].keys())):
#     Graph.MuscleGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, MuscleName, "Angle", "Activity", "Activation des muscles", CasesOn="all", SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1})

# # Si juste 4 muscles et prend les noms de muscles dans le cas 1
# for index, MuscleName in enumerate(list(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos["Case 1"]["Muscles"].keys())):
#     Graph.MuscleGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, MuscleName, "Angle", "Ft", "Forces musculaires", CasesOn="all", SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1})

# for index, MuscleName in enumerate(list(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos["Case 1"]["Muscles"].keys())):
#     Graph.MuscleGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, MuscleName, "Angle", "Activity", "Activité musculaire", CasesOn=["Case 1"], SubplotTitle=MuscleName, MusclePartOn="all", Subplot={"Dimension": [2, 2], "Number": index + 1})

# Graph.MuscleGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, "supraspinatus", "Angle", "Activity", "Activité musculaire", CasesOn=["Case 1"], SubplotTitle="supraspinatus", Composante_y=["Max"])

# for index, MuscleName in enumerate(list(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos["Case 1"]["Muscles"].keys())):
#     Graph.MuscleGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, MuscleName, "Angle", "Ft", "Activité musculaire", CasesOn=["Case 1"], SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1}, label="Ft")
#     Graph.MuscleGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos, MuscleName, "Angle", "Fm", "Activité musculaire", CasesOn=["Case 1"], SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1}, AddGraph=True, label="Fm")

# # """Graph neutre"""
# Graph.COPGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos_Neutre, "Position neutre", GleneContour, Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression")
# Graph.Graph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos_Neutre, "Angle", "ForceContact", "Position neutre", Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Forces de contact entre les implants")

# # Si juste 4 muscles et prend les noms de muscles dans le cas 1
# for index, MuscleName in enumerate(list(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos_Neutre["Muscles"].keys())):
#     Graph.MuscleGraph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos_Neutre, MuscleName, "Angle", "Activity", "Activation des muscles", SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1})

# Graph.Graph(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos_Neutre, "Angle", "GHLin", "Déplacement de l'humérus en Position neutre", Composante_y=["AP", "IS", "ML", "Total"])

# %% Comparaison influence partie gauche du corps ou non pour neutre

# comp = {"Left Off": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos_Neutre, "Left On": ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Neutre_LeftArmOn}

# Graph.COPGraph(comp, "Comparaison neutre avec left arm on/off", GleneContour, Compare=True, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.Graph(comp, "Angle", "ForceContact", "Comparaison neutre avec left arm on/off", Compare=True, Subplot={"Dimension": [1, 2], "Number": 2})


# for index, MuscleName in enumerate(list(ResultsDroitEnFaceAnteroTiltLocalGlenoid_CustomForce_Fixed_HumeralImplantPos_Neutre["Muscles"].keys())):
#     Graph.MuscleGraph(comp, MuscleName, "Angle", "Ft", "Activation des muscles", Compare=True, SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1})
