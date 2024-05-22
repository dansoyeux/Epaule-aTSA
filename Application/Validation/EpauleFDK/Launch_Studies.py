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

num_processes = 6

# %% Paramètres mouvement et modèle

BallAndSocket = 0

SmallAbduction = 0

# ArmMovement = "Abduction"
ArmMovement = "Elevation"

startangle = 15

endangle = 120

MuscleRecruitmentType = "MR_Polynomial"
# MuscleRecruitmentType = "MR_MinMaxStrict"


# %% Cas de simulation

# 30 Cases to run
tilt_list = ["xdown", "down", "neutral", "middle", "up", "xup"]
acromion_list = ["xshort", "short", "normal", "long", "xlong"]

# Dossier de résultats
ResultFolder = "Result Files"

# 9 Cases to run
# tilt_list = ["xdown", "xup"]
# acromion_list = ["xshort", "xlong"]


# %% Nom du fichier de sortie


os.mkdir(f"./Output/{ResultFolder}")

# %% Script lancement simulation

macrolist = []

if SmallAbduction == 1:
    startangle = 15
    endangle = 15.5

for tilt in tilt_list:

    for acromion in acromion_list:

        CSA_case = f"{tilt}-{acromion}"
        file_name = f'"Anybody_{CSA_case}"'

        macrolist.append([
            Load('EpauleFDK.Main.any',
                 defs={'CSA_Tilt': f'"{tilt}"',
                       'AutoSaveOption': 1,
                       'SmallAbductionOn': SmallAbduction,
                       'ArmMovement': f"{ArmMovement}",
                       'CSA_Acromion_Length': f'"{acromion}"',
                       "ResultFile": file_name,
                       'ResultFolder': f'"{ResultFolder}"',
                       'MuscleRecruitmentType': MuscleRecruitmentType,
                       'BallAndSocket': BallAndSocket,
                       },  # fin defs
                 ),  # fin Load

            SetValue('Main.Model.ModelEnvironmentConnection.Drivers.startangle', startangle),
            SetValue('Main.Model.ModelEnvironmentConnection.Drivers.endangle', endangle),

        ])

        macrolist[-1][-1] = OperationRun('Main.Study.RunApplication')

# %% Launch study without timeout
# if not endangle == 180:
app = AnyPyProcess(timeout=3600 * 100, num_processes=num_processes, keep_logfiles=True,
                   warnings_to_include=["OBJ1", "Penetration of surface", "Failed to resolve force-dependent kinematics"],
                   fatal_warnings=True, logfile_prefix=f"Output/{ResultFolder}/logfile")

app.start_macro(macrolist)
