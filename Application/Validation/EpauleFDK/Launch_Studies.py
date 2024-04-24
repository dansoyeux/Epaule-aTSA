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

import os

# %% nombre de simulation en parallèle

# 50 min pour 5 simulations en parallèle 15-120°
# sera toujours fait en 5 fois, faudrait passer à 7 pour vraiment faire différence car serait fait en 4 fois donc plus court


#  4h10 pour 25 simulations avec 5 en parallèle pour petit ordi CHUM

# max chum = 12 (6 cores), max chez moi 8 (4 cores)

# 5 = pas de bruit au chum + encore utilisable pour autre chose
num_processes = 6


# %% Paramètres mouvement et modèle

BallAndSocket = 0

SmallAbduction = 0

# ArmMovement = "Abduction"
ArmMovement = "Elevation"

startangle = 15

endangle = 120

"""-------------------------------------On ne peut pas changer le nombre de steps à un nombre différent de celui mis dans anybody sinon bug-------------------------------------"""
nstep = 70


MuscleRecruitmentType = "MR_Polynomial"
# MuscleRecruitmentType = "MR_MinMaxStrict"

# %% Caliubration parameter
# Load the muscle calibration parameters from a file

load_muscle_parameter_from_file = False

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

"""-------------------------------------WARNING ON-------------------------------------"""
CustomFDKOn = "On"
"""-------------------------------------WARNING ON-------------------------------------"""

# CustomFDKOn = "CustomForce"

# %% Cas de simulation

# 30 Cases to run
tilt_list = ["xdown", "down", "neutral", "middle", "up", "xup"]
acromion_list = ["xshort", "short", "normal", "long", "xlong"]

# Dossier de résultats
m_ResultFolder = "SaveData/const_speed/"

# 9 Cases to run
# tilt_list = ["xdown", "xup"]
# acromion_list = ["xshort", "xlong"]


# %% Nom du fichier de sortie

file_date = "04-01"

os.mkdir(f"./Output/{m_ResultFolder}")

# %% Paramétrage nom fichier

if BallAndSocket == 0 and not endangle == 120 and startangle == 15:
    file_description = f'GlenoidAxisTilt-{MuscleRecruitmentType}-{endangle}deg'
elif BallAndSocket == 0 and endangle == 120 and startangle == 0:
    file_description = f'GlenoidAxisTilt-{MuscleRecruitmentType}-0-120deg'

elif BallAndSocket == 1 and not endangle == 180 and startangle == 15:
    file_description = f'BallAndSocket-{MuscleRecruitmentType}-{endangle}deg'
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

        ])

        # Type of Run_EpauleFDK study
        if load_muscle_parameter_from_file:
            # Loads the muscle parameters from a file
            macrolist[-1][-1] = OperationRun('Main.Study.LoadCalibration_RunEpauleFDK')
        else:
            macrolist[-1][-1] = OperationRun('Main.Study.RunEpauleFDK')

    # if endangle == 180:
    #     app = AnyPyProcess(timeout=3600 * 2, num_processes=num_processes)
    #     app.start_macro(macrolist)

# %% Launch study without timeout
# if not endangle == 180:
app = AnyPyProcess(timeout=3600 * 100, num_processes=num_processes)
app.start_macro(macrolist)