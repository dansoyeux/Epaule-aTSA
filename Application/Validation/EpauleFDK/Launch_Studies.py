# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 18:35:53 2023

@author: user
"""

from anypytools.macro_commands import (MacroCommand, Load, SetValue, SetValue_random, Dump, SaveDesign,
                                       LoadDesign, SaveValues, LoadValues, UpdateValues, OperationRun)
from anypytools import AnyPyProcess

from anypytools import AnyMacro

import numpy as np

# %% nombre de simulation en parallèle

# 50 min pour 5 simulations en parallèle 15-120°
# sera toujours fait en 5 fois, faudrait passer à 7 pour vraiment faire différence car serait fait en 4 fois donc plus court


#  4h10 pour 25 simulations avec 5 en parallèle pour petit ordi CHUM

# max chum = 12 (6 cores), max chez moi 8 (4 cores)

# 5 = pas de bruit au chum + encore utilisable pour autre chose
num_processes = 5


# %% Paramètres mouvement et modèle

BallAndSocket = 0

SmallAbduction = 0

ArmMovement = "Abduction"
# ArmMovement = "Elevation"

startangle = 15

endangle = 120

nstep = 70
MuscleRecruitmentType = "MR_Polynomial"


# %% Caliubration parameter
# Load the muscle calibration parameters from a file

"""WARNING TRUE"""
load_muscle_parameter_from_file = True
"""WARNING TRUE"""

CALIBRATION_PARAMETER_CHOICE = "AUTO"
CALIBRATION_PARAMETER_CHOICE = "middle-normal"

if load_muscle_parameter_from_file is False:
    CALIBRATION_PARAMETER_CHOICE = "AUTO"

# %% Paramètres FDK

"""
  CustomFDKOn : Off : laisse le modele de Lauranne
  CustomFDKOn : On : Met une autre force que Lauranne mais la même pour tous les cas
  CustomFDKOn : CustomForce : Force différente selon le cas
"""

# CustomFDKOn = "On"
CustomFDKOn = "CustomForce"

# %% Cas de simulation

# 25 Cases to run
# tilt_list = ["xdown", "down", "middle", "up", "xup"]
# acromion_list = ["xshort", "short", "normal", "long", "xlong"]

# 9 Cases to run
tilt_list = ["xdown", "middle", "xup"]
acromion_list = ["xshort", "normal", "xlong"]

# # Cases to run
# tilt_list = ["down"]
# acromion_list = ["short"]

# %% Nom du fichier de sortie

file_date = "30-10"

# Dossier de résultats
m_ResultFolder = "SaveData/Macro_Results/"


if BallAndSocket == 0 and endangle == 180 and startangle == 15:
    file_description = f'GlenoidAxisTilt-{MuscleRecruitmentType}-180deg'
elif BallAndSocket == 0 and endangle == 120 and startangle == 0:
    file_description = f'GlenoidAxisTilt-{MuscleRecruitmentType}-0-120deg'

elif BallAndSocket == 1 and endangle == 180 and startangle == 15:
    file_description = f'BallAndSocket-{MuscleRecruitmentType}-180deg'
elif BallAndSocket == 0 and endangle == 120 and startangle == 15:
    file_description = f'GlenoidAxisTilt-{MuscleRecruitmentType}'

elif BallAndSocket == 1 and endangle == 120 and startangle == 15:
    file_description = f'BallAndSocket-{MuscleRecruitmentType}'

# Small abduction
if SmallAbduction == 1:
    file_description = f'GlenoidAxisTilt-{MuscleRecruitmentType}-SmallAbduction'

if ArmMovement == "Elevation":
    file_description += "-Elevation"

if CustomFDKOn == "On":
    file_description += "-no-recentrage"

if load_muscle_parameter_from_file:
    file_description += f"-hill-parameter-{CALIBRATION_PARAMETER_CHOICE}"

# %% Vitesses pour moment arm

"""Valeur doit rester de taille 70 comme sa valeur originelle et rester avec des floats"""


FourierAngularVelocity = np.array([1.46888E-18,
                                   0.001091833,
                                   0.002181402,
                                   0.00326645,
                                   0.004344728,
                                   0.005414001,
                                   0.006472053,
                                   0.00751669,
                                   0.008545748,
                                   0.009557093,
                                   0.01054863,
                                   0.011518303,
                                   0.012464103,
                                   0.013384069,
                                   0.014276294,
                                   0.01513893,
                                   0.015970188,
                                   0.016768345,
                                   0.017531748,
                                   0.018258813,
                                   0.018948034,
                                   0.019597982,
                                   0.02020731,
                                   0.020774756,
                                   0.021299143,
                                   0.021779384,
                                   0.022214484,
                                   0.022603541,
                                   0.022945749,
                                   0.023240398,
                                   0.023486878,
                                   0.023684678,
                                   0.023833387,
                                   0.023932699,
                                   0.023982406,
                                   0.023982406,
                                   0.023932699,
                                   0.023833387,
                                   0.023684678,
                                   0.023486878,
                                   0.023240398,
                                   0.022945749,
                                   0.022603541,
                                   0.022214484,
                                   0.021779384,
                                   0.021299143,
                                   0.020774756,
                                   0.02020731,
                                   0.019597982,
                                   0.018948034,
                                   0.018258813,
                                   0.017531748,
                                   0.016768345,
                                   0.015970188,
                                   0.01513893,
                                   0.014276294,
                                   0.013384069,
                                   0.012464103,
                                   0.011518303,
                                   0.01054863,
                                   0.009557093,
                                   0.008545748,
                                   0.00751669,
                                   0.006472053,
                                   0.005414001,
                                   0.004344728,
                                   0.00326645,
                                   0.002181402,
                                   0.001091833,
                                   1.46888E-18
                                   ])


# %% Script lancement simulation

macrolist = []

if SmallAbduction == 1:
    startangle = 15
    endangle = 15.5
    nstep = 1


for tilt in tilt_list:

    for acromion in acromion_list:

        CSA_case = f"{tilt}-{acromion}"
        file_name = f'"{file_date}-{CSA_case}-{file_description}"'

        macrolist.append([
            Load('EpauleFDK.Main.any',
                 defs={'CSA_Tilt': f'"{tilt}"',
                       'AnyOutputFileOn': 1,
                       'SmallAbductionOn': SmallAbduction,
                       'CustomFDKOn': f"{CustomFDKOn}",
                       'ArmMovement': f"{ArmMovement}",
                       'CSA_Acromion_Length': f'"{acromion}"',
                       "m_ResultFile": file_name,
                       'm_ResultFolder': f'"{m_ResultFolder}"',
                       'MuscleRecruitmentType': MuscleRecruitmentType,
                       'BallAndSocket': BallAndSocket,
                       'CALIBRATION_PARAMETER_CHOICE': f'"{CALIBRATION_PARAMETER_CHOICE}"'
                       },  # fin defs
                 ),  # fin Load

            SetValue('Main.Model.ModelEnvironmentConnection.Drivers.startangle', startangle),
            SetValue('Main.Model.ModelEnvironmentConnection.Drivers.endangle', endangle),
            SetValue('Main.Study.nStep', nstep),
            SetValue('Main.Study.EvaluateMomentArms.FourierAngularVelocity', FourierAngularVelocity),

        ])

        # Type of Run_EpauleFDK study
        if load_muscle_parameter_from_file:
            # Loads the muscle parameters from a file
            macrolist[-1][-1] = OperationRun('Main.Study.LoadCalibration_RunEpauleFDK')
        else:
            macrolist[-1][-1] = OperationRun('Main.Study.RunEpauleFDK')

# %% Launch study
app = AnyPyProcess(timeout=3600 * 100, num_processes=num_processes)
app.start_macro(macrolist)
