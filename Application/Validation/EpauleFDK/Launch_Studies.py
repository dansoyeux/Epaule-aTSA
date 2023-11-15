# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 18:35:53 2023

@author: user
"""

from anypytools.macro_commands import (MacroCommand, Load, SetValue, SetValue_random, Dump, SaveDesign,
                                       LoadDesign, SaveValues, LoadValues, UpdateValues, OperationRun)
from anypytools import AnyPyProcess

from anypytools import AnyMacro

# %% nombre de simulation en parallèle

# 50 min pour 5 simulations en parallèle 15-120°
# sera toujours fait en 5 fois, faudrait passer à 7 pour vraiment faire différence car serait fait en 4 fois donc plus court


#  4h10 pour 25 simulations avec 5 en parallèle

# max chum = 12 (6 cores), max chez moi 8 (4 cores)

# 6 = pas de bruit au chum + encore utilisable pour autre chose
num_processes = 5

# %% Paramètres mouvement et modèle

BallAndSocket = 0

ArmMovement = "Abduction"
# ArmMovement = "Elevation"

startangle = 15
endangle = 120

# Simulation parameters
# 40 avec equation Fourier Lauranne marche bien pour 120°
nstep = 70
MuscleRecruitmentType = "MR_Polynomial"

# %% Paramètres FDK

"""
  CustomFDKOn : Off : laisse le modele de Lauranne
  CustomFDKOn : On : Met une autre force que Lauranne mais la même pour tous les cas
  CustomFDKOn : CustomForce : Force différente selon le cas
"""
# CustomFDKOn = "On"
CustomFDKOn = "CustomForce"

# %% Cas de simulation

# Cases to run
tilt_list = ["xdown", "down", "middle", "up", "xup"]
acromion_list = ["xshort", "short", "normal", "long", "xlong"]

# # Cases to run
# tilt_list = ["down", "middle", "up"]
# acromion_list = ["short", "normal", "long"]

# %% Nom du fichier de sortie

file_date = "30-10"

# Dossier de résultats
m_ResultFolder = "SaveData/Macro_Results/"

if BallAndSocket == 0 and endangle == 180 and startangle == 15:
    file_description = f'GlenoidAxisTilt-{MuscleRecruitmentType}-180deg'

if BallAndSocket == 0 and endangle == 120 and startangle == 0:
    file_description = f'GlenoidAxisTilt-{MuscleRecruitmentType}-0-120deg'

elif BallAndSocket == 1 and endangle == 180 and startangle == 15:
    file_description = f'BallAndSocket-{MuscleRecruitmentType}-180deg'
if BallAndSocket == 0 and endangle == 120 and startangle == 15:
    file_description = f'GlenoidAxisTilt-{MuscleRecruitmentType}'
elif BallAndSocket == 1 and endangle == 120 and startangle == 15:
    file_description = f'BallAndSocket-{MuscleRecruitmentType}'

# NO DELTOID POSTERIOR SCALING
file_description += "-no-delt-post-scaling"

if ArmMovement == "Elevation":
    file_description += "-Elevation"

if CustomFDKOn == "On":
    file_description += "-no-recentrage"


# %% Script lancement simulation


macrolist = []

for tilt in tilt_list:

    for acromion in acromion_list:

        CSA_case = f"{tilt}-{acromion}"
        file_name = f'"{file_date}-{CSA_case}-{file_description}"'

        macrolist.append([
            Load('EpauleFDK.Main.any',
                 defs={'CSA_Tilt': f'"{tilt}"',
                       'AnyOutputFileOn': 1,
                       'SmallAbductionOn': 0,
                       'CustomFDKOn': f"{CustomFDKOn}",
                       'ArmMovement': f"{ArmMovement}",
                       'CSA_Acromion_Length': f'"{acromion}"',
                       "m_ResultFile": file_name,
                       'm_ResultFolder': f'"{m_ResultFolder}"',
                       'MuscleRecruitmentType': MuscleRecruitmentType,
                       'BallAndSocket': BallAndSocket
                       },  # fin defs
                 ),  # fin Load

            SetValue('Main.Model.ModelEnvironmentConnection.Drivers.startangle', startangle),
            SetValue('Main.Model.ModelEnvironmentConnection.Drivers.endangle', endangle),
            SetValue('Main.Study.nStep', nstep),

            OperationRun('Main.Study.RunEpauleFDK')

        ])

# %% Launch study
app = AnyPyProcess(timeout=3600 * 100, num_processes=num_processes)
app.start_macro(macrolist)
