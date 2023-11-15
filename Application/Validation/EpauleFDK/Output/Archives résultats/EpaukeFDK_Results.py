# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 16:01:37 2023

@author: Dan
"""


import numpy as np
import math

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

    # module to import csv files
    import pandas as pd
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

# %%                                                  RESULTS
"""
-------------------------------------------------------------------------------
LÉGENDE DES NOMS DES DICTIONNAIRES STOCKANT MES RÉSULTATS

GlenoidLocalAxis : glenoid implant tourné autour de l'axe local de l'implant et
en mettant une correction constante de -21 d'external rotation sur le mannequin=


-------------------------------------------------------------------------------
"""

CaseNumberSequence = [6, 1, 2, 5, 3, 7, 4]

UpCases = ["up_short", "up_normal"]
MiddleCases = ["middle_short", "middle_normal", "middle_long"]
DownCases = ["down_normal", "down_long"]

CaseNames = [*MiddleCases, *UpCases, *DownCases]
UpDownCases = [*UpCases, *DownCases]


OldCaseNames = ["middle_normal", "middle_long",
                "up_normal", "up_short",
                "down_long"]

SaveDatadir = '../SaveData/Variation_CSA/'


"""
Correction of the humeral implant position to be exactly on the edge of the new humeral bone STL (not the old one)
"""

date = "Results-25-08-case"
description = "-droit-GlenoidAxisTilt-EnFace-CustomForce-CorrectionHumerusPos"

Files = [date + str(CaseNumber) + description for CaseNumber in CaseNumberSequence]

Results_GlenoidLocalAxis = LoadOutput.LoadSimulationCases(SaveDatadir, Files, CaseNames, AddConstants=True)

# En position neutre
Results_GlenoidLocalAxis_Neutre = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-25-08-case0-droit-GlenoidAxisTilt-EnFace-CustomForce-CorrectionHumerusPos', AddConstants=True)


# %%                                                CODE TEMPLATES

"""Séparation des COP des 5 cas sur 2 subplots"""
# Graph.COPGraph(DATA, "Position du centre de pression", GleneContour, CasesOn=MiddleCases, Subplot={"Dimension": [1, 2], "Number": 1})
# Graph.COPGraph(DATA, "Position du centre de pression", GleneContour, CasesOn=UpDownCases, Subplot={"Dimension": [1, 2], "Number": 2})

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


# %%                                        COP au centre sans new Wrapping et local tilt axis ExtRot = cste

Graph.COPGraph(Results_GlenoidLocalAxis, "Correction humeral implant position", GleneContour, CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression", DrawPeakCOPAngleOn=False)
Graph.Graph(Results_GlenoidLocalAxis, "Angle", "ForceContact", "Correction humeral implant position", CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Forces de contact entre les implants")

Graph.COPGraph(Results_GlenoidLocalAxis, "Position du centre de pression", GleneContour, CasesOn=MiddleCases, Subplot={"Dimension": [1, 2], "Number": 1})
Graph.COPGraph(Results_GlenoidLocalAxis, "Position du centre de pression", GleneContour, CasesOn=UpDownCases, Subplot={"Dimension": [1, 2], "Number": 2})

# Si juste 4 muscles et prend les noms de muscles dans le cas 1
for index, MuscleName in enumerate(list(Results_GlenoidLocalAxis[CaseNames[0]]["Muscles"].keys())):
    Graph.MuscleGraph(Results_GlenoidLocalAxis, MuscleName, "Angle", "Activity", "Activation des muscles", CasesOn="all", SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1})

# Si juste 4 muscles et prend les noms de muscles dans le cas 1
for index, MuscleName in enumerate(list(Results_GlenoidLocalAxis[CaseNames[0]]["Muscles"].keys())):
    Graph.MuscleGraph(Results_GlenoidLocalAxis, MuscleName, "Angle", "Ft", "Forces musculaires", CasesOn="all", SubplotTitle=MuscleName, Subplot={"Dimension": [2, 2], "Number": index + 1})

