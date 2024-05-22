# import Anybody_LoadOutput.LoadOutput as LoadOutput
# import Anybody_Tools as LoadOutputTools

from Anybody_Package.Anybody_LoadOutput.LoadOutput import define_variables_to_load
from Anybody_Package.Anybody_LoadOutput.LoadOutput import load_simulation_cases
from Anybody_Package.Anybody_LoadOutput.LoadOutput import load_simulation
from Anybody_Package.Anybody_LoadOutput.LoadOutput import create_compared_simulations

from Anybody_Package.Anybody_LoadOutput.Tools import save_results_to_file
from Anybody_Package.Anybody_LoadOutput.Tools import load_results_from_file
from Anybody_Package.Anybody_LoadOutput.Tools import array_to_dictionary

from Anybody_Package.Anybody_LoadOutput.LoadLiterature import load_literature_data
from Anybody_Package.Anybody_LoadOutput.LoadOutput import combine_simulation_cases

import numpy as np

import pandas as pd

# %% Setup des variables à charger

# Muscles
MuscleDictionary = {"Triceps long head": ["Triceps_LH", "_", [1, 2]],
                    "Deltoid lateral": ["deltoideus_lateral", "_part_", [1, 4]],
                    "Deltoid posterior": ["deltoideus_posterior", "_part_", [1, 4]],
                    "Deltoid anterior": ["deltoideus_anterior", "_part_", [1, 4]],
                    "Supraspinatus": ["supraspinatus", "_", [1, 6]],
                    "Infraspinatus": ["infraspinatus", "_", [1, 6]],
                    "Serratus anterior": ["serratus_anterior", "_", [1, 6]],
                    "Lower trapezius": ["trapezius_scapular", "_part_", [1, 3]],
                    "Middle trapezius": ["trapezius_scapular", "_part_", [4, 6]],
                    "Upper trapezius": ["trapezius_clavicular", "_part_", [1, 6]],

                    "Biceps brachii long head": ["biceps_brachii_caput_longum", "", []],
                    "Biceps brachii short head": ["biceps_brachii_caput_breve", "", []],
                    "Pectoralis major clavicular": ["pectoralis_major_clavicular", "_part_", [1, 5]],
                    "Pectoralis major sternal": ["pectoralis_major_thoracic", "_part_", [1, 10]],

                    "Pectoralis major": [["pectoralis_major_thoracic", "_part_", [1, 10]],
                                         ["pectoralis_major_clavicular", "_part_", [1, 5]]
                                         ],

                    "Pectoralis minor": ["pectoralis_minor", "_", [1, 3]],
                    "Latissimus dorsi": ["latissimus_dorsi", "_", [1, 11]],
                    "Upper Subscapularis": ["subscapularis", "_", [1, 2]],
                    "Downward Subscapularis": ["subscapularis", "_", [3, 6]],
                    "Subscapularis": ["subscapularis", "_", [1, 6]],
                    "Teres minor": ["teres_minor", "_", [1, 6]],
                    "Teres major": ["teres_major", "_", [1, 6]],
                    "Rhomboideus": ["rhomboideus", "_", [1, 3]],
                    "Levator scapulae": ["levator_scapulae", "_", [1, 4]],
                    "Sternocleidomastoid clavicular": ["Sternocleidomastoid_caput_clavicular", "", []],
                    "Sternocleidomastoid sternum": ["Sternocleidomastoid_caput_Sternum", "", []],
                    "Coracobrachialis": ["coracobrachialis", "_", [1, 6]]
                    }

MuscleVariableDictionary = {"Ft": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Ft", "VariableDescription": "Muscle force [N]"},
                            # "Fm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Fm", "VariableDescription": "Muscle force [N]"},
                            # "Activity": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "CorrectedActivity", "VariableDescription": "Muscle activity [%]", "MultiplyFactor": 100, "combine_muscle_part_operations": ["max", "mean"]},

                            # Dans repère scapula
                            # "F origin": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the origin [N]", "select_matrix_line": 0,
                            #              "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                            #              "combine_muscle_part_operations": ["total", "mean"]},

                            # "F insertion": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the insertion [N]", "select_muscle_RefFrame_output": "insertion",
                            #                 "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                            #                 "combine_muscle_part_operations": ["total", "mean"]
                            #                 },

                            # "F origin": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the origin [N]", "select_matrix_line": 0,
                            #               "rotation_matrix_path": "Output.Seg.Scapula.GlenImplantPos.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                            #               "combine_muscle_part_operations": ["total", "mean"]},

                            # "F insertion": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the insertion [N]", "select_muscle_RefFrame_output": "insertion",
                            #                 "rotation_matrix_path": "Output.Seg.Scapula.GlenImplantPos.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                            #                 "combine_muscle_part_operations": ["total", "mean"]
                            #                 },

                            "F origin direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the origin", "select_matrix_line": 0,
                                                   "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                                   "combine_muscle_part_operations": ["mean"], "vect_dir": True},

                            "F insertion direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the insertion", "select_muscle_RefFrame_output": "insertion",
                                                      "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                                      "combine_muscle_part_operations": ["mean"], "vect_dir": True},

                            "MomentArm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "MomentArm", "VariableDescription": "Moment arm [mm]",
                                          "combine_muscle_part_operations": ["mean"], "MultiplyFactor": 1000}
                            }

MuscleVariableDictionary_NoMomentArm = {"Ft": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Ft", "VariableDescription": "Muscle force [N]"},

                                        # Not used when using Hill model
                                        # "Fm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Fm", "VariableDescription": "Muscle force [N]"},

                                        # Muscle Activity for Hill muscles
                                        # "Activity": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "CorrectedActivity", "VariableDescription": "Muscle activity [%]", "MultiplyFactor": 100, "combine_muscle_part_operations": ["max", "mean"]},

                                        # "F origin": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the origin [N]", "select_matrix_line": 0,
                                        #              "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                        #              "combine_muscle_part_operations": ["total", "mean"]},

                                        # "F origin direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the origin", "select_matrix_line": 0,
                                        #                        "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                        #                        "combine_muscle_part_operations": ["mean"], "vect_dir": True},

                                        # "F insertion": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the insertion [N]", "select_muscle_RefFrame_output": "insertion",
                                        #                 "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                        #                 "combine_muscle_part_operations": ["total", "mean"]
                                        #                 },
                                        # "F insertion direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the insertion", "select_muscle_RefFrame_output": "insertion",
                                        #                           "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                        #                           "combine_muscle_part_operations": ["mean"], "vect_dir": True}

                                        }

# Variables
FDK_VariableDictionary = {"Abduction": {"VariablePath": "Output.Simulation_Outputs.AbductionAngle", "VariableDescription": "Abduction angle [°]"},

                          "ContactArea": {"VariablePath": "Output.Simulation_Outputs.ContactArea", "VariableDescription": r'Contact area [$cm^2$]', "MultiplyFactor": 10000},

                          "Time": {"VariablePath": "Output.Abscissa.t", "VariableDescription": "Time", "MultiplyFactor": 10000},

                          "MaxPenetration": {"VariablePath": "Output.Simulation_Outputs.MaxPenetration", "VariableDescription": 'Maximal penetration of the implants [mm]', "MultiplyFactor": 1000},

                          # Position of the center of pressure on the glenoid implant
                          "COP": {"VariablePath": "Output.Simulation_Outputs.COP_glenoid", "VariableDescription": "Center of Pressure [mm]", "MultiplyFactor": 1000,
                                  "SequenceComposantes": ["AP", "IS", "ML"],
                                  # Offset in mediolateral so that the center of the glenoid implant surface corresponds to (0,0,0) (24.5 for the GleneCeraver_T3)
                                  "offset": [0, 0, -24.5]},

                          # Dans le repère de l'humérus ISB (pour comparaison avec bergmann et al.)
                          "ContactForce humerus": {"VariablePath": "Output.Simulation_Outputs.ContactForce_humerus", "VariableDescription": "Contact force on the humeral implant [N]",
                                                   "SequenceComposantes": ["AP", "IS", "ML"]},

                          # Force sur l'humerus Dans le repère de l'implant glénoïdien
                          "ContactForce glenoid": {"VariablePath": "Output.Simulation_Outputs.ContactForce_GlenImplant", "VariableDescription": "Contact force on the glenoid implant [N]",
                                                   "SequenceComposantes": ["AP", "IS", "ML"]},

                          "ForceTolError": {"VariablePath": "Output.Simulation_Outputs.ForceDepKinError", "VariableDescription": "FDK Error [N]"}
                          }

BallAndSocket_VariableDictionary = {"Abduction": {"VariablePath": "Output.Simulation_Outputs.AbductionAngle", "VariableDescription": "Abduction angle [°]"}
                                    }

# Constantes
FDK_ConstantsDictionary = {"AnybodyFileOutPath": "Main.Study.FileOut",
                           "Anybody version": ["AMMRVersion", "AnybodyVersion"],
                           "Paramètres de simulation": ["Case", "MuscleRecruitment", "nStep", "tEnd", "GHReactions", "Movement"],
                           "Mannequin": ["GlenohumeralFlexion", "GlenohumeralAbduction", "GlenohumeralExternalRotation"],

                           "ParametresFDK": ["k0", "k1", "k2", "k3", "k4", "kz", "kd", "ForceTol", "UseAdaptiveForceTolOnOff", "MaxIteration",
                                             "Perturbation", "PerturbationSymmetricOnOff", "LocalSearchOnOff", "MaxNewtonStep"],

                           "Positions initiales": ["px", "py", "pz"],

                           "Paramètres implants": ["HumerusName", "GlenoidName", "Case", "RotationAxis", "GleneImplantInclinationAngle", "GleneImplantVersionAngle", "GlenImplantRotation",
                                                   "GlenImplantPosition", "GlenImplantCenter", "HumImplantPosition", "HumImplantRotation", "AcromionOffset"],
                           "MyMuscleWrapping": ["WrappingSurfaceShape", "LateralWrapping_RadiusX", "LateralWrapping_Radius", "LateralWrapping_RadiusHeight", "PosteriorWrapping_RadiusX", "PosteriorWrapping_Radius", "PosteriorWrapping_RadiusHeight"]
                           }

BallAndSocket_ConstantsDictionary = {"AnybodyFileOutPath": "Main.Study.FileOut",
                                     "Paramètres de simulation": ["Case", "MuscleRecruitment", "nstep", "GHReactions", "Movement"],
                                     "Mannequin": ["GlenohumeralFlexion", "GlenohumeralAbduction", "GlenohumeralExternalRotation"],
                                     }

FDK_Variables = define_variables_to_load(FDK_VariableDictionary, MuscleDictionary, MuscleVariableDictionary, FDK_ConstantsDictionary)

FDK_Variables_NoMomentArm = define_variables_to_load(FDK_VariableDictionary, MuscleDictionary, MuscleVariableDictionary_NoMomentArm)

BallAndSocket_Variables = define_variables_to_load(BallAndSocket_VariableDictionary, MuscleDictionary, MuscleVariableDictionary_NoMomentArm, BallAndSocket_ConstantsDictionary)

# %% Nom des cas de simulation

# Tilt acromion
xUpCases_3 = ["xup-xshort", "xup-normal", "xup-xlong"]
UpCases_3 = ["up-xshort", "up-normal", "up-xlong"]
MiddleCases_3 = ["middle-xshort", "middle-normal", "middle-xlong"]
NeutralCases_3 = ["neutral-xshort", "neutral-normal", "neutral-xlong"]
DownCases_3 = ["down-xshort", "down-normal", "down-xlong"]
xDownCases_3 = ["xdown-xshort", "xdown-normal", "xdown-xlong"]


# Longueur d'acromion
xShortCases_3 = ["xdown-xshort", "middle-xshort", "xup-xshort"]
ShortCases_3 = ["xdown-short", "middle-short", "xup-short"]
NormalCases_3 = ["xdown-normal", "middle-normal", "xup-normal"]
LongCases_3 = ["xdown-long", "middle-long", "xup-long"]
xLongCases_3 = ["xdown-xlong", "middle-xlong", "xup-xlong"]

# Longueur d'acromion
xShortCases_36 = ["xdown-xshort", "neutral-xshort", "up-xshort"]
ShortCases_36 = ["xdown-short", "neutral-short", "up-short"]
NormalCases_36 = ["xdown-normal", "neutral-normal", "up-normal"]
LongCases_36 = ["xdown-long", "neutral-long", "up-long"]
xLongCases_36 = ["xdown-xlong", "neutral-xlong", "up-xlong"]

CaseNames_3 = [*xDownCases_3, *MiddleCases_3, *xUpCases_3]
CaseNames_36 = [*xDownCases_3, *NeutralCases_3, *UpCases_3]
UpDownCases_3 = [*xUpCases_3, *xDownCases_3]

# More cases
xDownCases_5 = ["xdown-xshort", "xdown-short", "xdown-normal", "xdown-long", "xdown-xlong"]
DownCases_5 = ["down-xshort", "down-short", "down-normal", "down-long", "down-xlong"]
MiddleCases_5 = ["middle-xshort", "middle-short", "middle-normal", "middle-long", "middle-xlong"]
NeutralCases_5 = ["neutral-xshort", "neutral-short", "neutral-normal", "neutral-long", "neutral-xlong"]
UpCases_5 = ["up-xshort", "up-short", "up-normal", "up-long", "up-xlong"]
xUpCases_5 = ["xup-xshort", "xup-short", "xup-normal", "xup-long", "xup-xlong"]

xShortCases_5 = ["xdown-xshort", "down-xshort", "middle-xshort", "up-xshort", "xup-xshort"]
ShortCases_5 = ["xdown-short", "down-short", "middle-short", "up-short", "xup-short"]
NormalCases_5 = ["xdown-normal", "down-normal", "middle-normal", "up-normal", "xup-normal"]
LongCases_5 = ["xdown-long", "down-long", "middle-long", "up-long", "xup-long"]
xLongCases_5 = ["xdown-xlong", "down-xlong", "middle-xlong", "up-xlong", "xup-xlong"]

xShortCases_6 = ["xdown-xshort", "down-xshort", "neutral-xshort", "middle-xshort", "up-xshort", "xup-xshort"]
ShortCases_6 = ["xdown-short", "down-short", "neutral-short", "middle-short", "up-short", "xup-short"]
NormalCases_6 = ["xdown-normal", "down-normal", "neutral-normal", "middle-normal", "up-normal", "xup-normal"]
LongCases_6 = ["xdown-long", "down-long", "neutral-long", "middle-long", "up-long", "xup-long"]
xLongCases_6 = ["xdown-xlong", "down-xlong", "neutral-xlong", "middle-xlong", "up-xlong", "xup-xlong"]

CaseNames_5 = [*xDownCases_5, *DownCases_5, *MiddleCases_5, *UpCases_5, *xUpCases_5]
CaseNames_6 = [*xDownCases_5, *DownCases_5, *NeutralCases_5, *MiddleCases_5, *UpCases_5, *xUpCases_5]

CaseNames_5_Tilt_3_Acromion = [*xDownCases_3, *DownCases_3, *MiddleCases_3, *UpCases_3, *xUpCases_3]

tilt_names_3 = ["xdown", "middle", "xup"]
tilt_names_5 = ["xdown", "down", "up", "xup"]
acromion_names_3 = ["xshort", "normal", "xlong"]
acromion_names_5 = ["xshort", "short", "normal", "long", "xlong"]

# Pour avoir tri par tilts
CaseNames_3_Tilt_5_Acromion = [f"{tilt}-{acromion}" for tilt in tilt_names_3 for acromion in acromion_names_5]

CompWickham_CasesNames_3 = [*CaseNames_3, "Wickham", "Ball And Socket"]

CaseNames_3_BallAndSocket = [*CaseNames_3, "Ball And Socket"]
CaseNames_5_BallAndSocket = [*CaseNames_5, "Ball And Socket"]

# 9 CSA différents
CSA_12_Cases = ["xdown-xshort"]
CSA_16_Cases = ["xdown-short", "down-xshort"]
CSA_20_Cases = ["xdown-normal", "down-short", "middle-xshort"]
CSA_25_Cases = ["xdown-long", "down-normal", "middle-short", "up-xshort"]
CSA_30_Cases = ["xdown-xlong", "down-long", "middle-normal", "up-short", "xup-xshort"]
CSA_35_Cases = ["down-xlong", "middle-long", "up-normal", "xup-short"]
CSA_40_Cases = ["middle-xlong", "up-long", "xup-normal"]
CSA_45_Cases = ["up-xlong", "xup-long"]
CSA_50_Cases = ["xup-xlong"]

# %%                                                Résultats FDK

SaveDataDir = r"../SaveData/Variation_CSA"
# SaveDataDir_Macro = r"../SaveData/Macro_Results"
description = "-GlenoidAxisTilt"

# Chemin d'accès au dossier dans lequel les fichiers doivent être sauvegardés
SaveSimulationsDirectory = "Saved Simulations"

"""Results"""
result_dir = "../Result Files"
files = ["Anybody_" + CaseName for CaseName in CaseNames_6]
Results = load_simulation_cases(result_dir, files, CaseNames_6, FDK_Variables)
save_results_to_file(Results, SaveSimulationsDirectory, "Results")

"""
Élévation no recentrage, constant speed
"""

# Elevation_dir_const_speed = "../SaveData/const_speed"
# Files = ["04-01-" + CaseName + description + "-MR_Polynomial-Elevation-no-recentrage" for CaseName in CaseNames_6]

# Results_Elevation_no_recentrage = load_simulation_cases(Elevation_dir_const_speed, Files, CaseNames_6, FDK_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_Elevation_no_recentrage, SaveSimulationsDirectory, "Results_Elevation_no_recentrage")

"""
Élévation no recentrage
"""

# Elevation_dir = "../SaveData/Elevation_no_recentrage"
# Files = ["04-01-" + CaseName + description + "-MR_Polynomial-Elevation-no-recentrage" for CaseName in CaseNames_6]

# Results_Elevation_no_recentrage_smoothed_speed = load_simulation_cases(Elevation_dir, Files, CaseNames_6, FDK_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_Elevation_no_recentrage_smoothed_speed, SaveSimulationsDirectory, "Results_Elevation_no_recentrage_smoothed_speed")

"""Elevation no recentrage minmaxstrict"""

# Elevation_minmax_dir = "../SaveData/Elevation_no_recentrage_MinMaxStrict"
# Files = ["04-01-" + CaseName + description + "-MR_MinMaxStrict-Elevation-no-recentrage" for CaseName in CaseNames_5]

# Results_MR_MinMaxStrict_Elevation_no_recentrage = load_simulation_cases(Elevation_minmax_dir, Files, CaseNames_5, FDK_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_MR_MinMaxStrict_Elevation_no_recentrage, SaveSimulationsDirectory, "Results_MR_MinMaxStrict_Elevation_no_recentrage")


# %% Long range
"""
Results and polynomial recruitment
Without new wrapping with xshorts
normal cases with 180 abduction

WITHOUT MOMENT ARM
"""
# Macros_results_dir2 = r"../SaveData/Macro_80step_180deg"
# date = "06-10-"

# # First failed step (lose contact or FDK error over 0.001)
# Failed_180_Simulation = [51, 50, 50, 49, 48,
#                          53, 53, 52, 51, 50,
#                          56, 55, 54, 52, 52,
#                          False, 65, 57, 55, 54,
#                          False, False, 58, 57, 57
#                          ]

# # En prenant en compte aussi conflit avec acromion (juste la pointe, pas en-dessous)
# Failed_180_Acromion = [51, 50, 50, 49, 48,
#                        53, 53, 52, 51, 50,
#                        56, 55, 54, 52, 52,
#                        60, 57, 55, 53, 52,
#                        54, 58, 51, 50, 50
#                        ]

# # Avec premier contact avec acromion
# Failed_180 = [51, 50, 50, 49, 48,
#               53, 53, 52, 51, 50,
#               56, 55, 54, 52, 52,
#               36, 34, 31, 28, 27,
#               29, 26, 24, 21, 13
#               ]

# # Avec premier contact avec acromion
# Files = [date + CaseName + description + "-MR_Polynomial-180deg" for CaseName in CaseNames_5]
# Results_180deg = load_simulation_cases(Macros_results_dir2, Files, CaseNames_5, FDK_Variables_NoMomentArm, Failed=Failed_180)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_180deg, SaveSimulationsDirectory, "Results_180deg")

"""
En ne prenant pas en compte conflit avec acromion
"""
# Results_180deg_FullRange = load_simulation_cases(Macros_results_dir2, Files, CaseNames_5, FDK_Variables_NoMomentArm, Failed=Failed_180_Simulation)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_180deg_FullRange, SaveSimulationsDirectory, "Results_180deg_FullRange")

"""Elevation minmax"""
# minmax_dir = "../SaveData/MinMaxStrict"
# Files = ["04-01-" + CaseName + description + "-MR_MinMaxStrict-120deg-Elevation-no-recentrage" for CaseName in CaseNames_3]

# Results_MR_MinMaxStrict_Elevation_no_recentrage = load_simulation_cases(minmax_dir, Files, CaseNames_3, FDK_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_MR_MinMaxStrict_Elevation_no_recentrage, SaveSimulationsDirectory, "Results_MR_MinMaxStrict_Elevation_no_recentrage")

# %%                                                Résultats Ball and Socket
"""
Résultats sains avec différents scaling acromion
120° abduction
"""

# BallAndSocket_Files = [f"08-09-BallAndSocket-{CaseName}" for CaseName in ["short", "normal", "long"]]

# Results_BallAndSocket = load_simulation_cases(SaveDataDir, BallAndSocket_Files, MiddleCases_3, BallAndSocket_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_BallAndSocket, SaveSimulationsDirectory, "Results_BallAndSocket")

"""
Résultats Ball And Socket avec différents critères de recrutement musculaires
"""
# Muscle_Recruitment_Types = ["MR_MinMaxStrict", "MR_Linear", "MR_Quadratic", "MR_QuadraticAux", "MR_Polynomial", "MR_MinMaxAux"]

# BallAndSocket_Muscle_Recruitment_Files = [f"08-09-BallAndSocket-normal-{Type}" for Type in Muscle_Recruitment_Types]
# Results_BallAndSocket_Muscle_Recruitment = load_simulation_cases(SaveDataDir, BallAndSocket_Muscle_Recruitment_Files, Muscle_Recruitment_Types, BallAndSocket_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_BallAndSocket_Muscle_Recruitment, SaveSimulationsDirectory, "Results_BallAndSocket_MuscleRecruitmentStudy")


"""
Full range Ball And Socket
180° abduction
"""

# files_full_range = [f"08-09-BallAndSocket-{CaseName}-MR_Polynomial-180deg" for CaseName in ["xshort", "short", "normal", "long", "xlong"]]
# Results_BallAndSocket_FullRange = load_simulation_cases(SaveDataDir, files_full_range, MiddleCases_5, BallAndSocket_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_BallAndSocket_FullRange, SaveSimulationsDirectory, "Results_BallAndSocket_FullRange")

# """
# Ball and socket avec full range
# """
# Results_BallAndSocket_FullRange = load_simulation_cases(SaveDataDir, ["08-09-BallAndSocket-normal-FullRange"], ["middle-normal"], BallAndSocket_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_BallAndSocket_FullRange, SaveSimulationsDirectory, "Results_BallAndSocket_FullRange")

# %% Sauvegarde des dictionnaires de variables

# # Chemin d'accès au dossier dans lequel les fichiers doivent être sauvegardés
SaveVariablesDirectory = "Saved VariablesDictionary"

save_results_to_file(FDK_Variables, SaveVariablesDirectory, "FDK_Variables")

# %% chargement new littérature depuis excel

Results_literature = load_literature_data("Template_importation_littérature", "Anybody_Package/Template")
save_results_to_file(Results_literature, SaveSimulationsDirectory, "Results_literature")

# %% Calculs supplémentaires

Results = load_results_from_file(SaveSimulationsDirectory, "Results")


def instability_ratio(Results):
    """Function that calculates the instability ratio for each simulation case
    IR = (|Fx| + |Fy|)/|Fz|
    """

    for case in Results:
        Results[case]["ContactForce glenoid"]["Shear"] = abs(Results[case]["ContactForce glenoid"]["IS"]) + abs(Results[case]["ContactForce glenoid"]["AP"])
        Results[case]["Instability Ratio"] = {"Description": "Instability ratio", "SequenceComposantes": "Total"}
        Results[case]["Instability Ratio"]["Total"] = Results[case]["ContactForce glenoid"]["Shear"] / abs(Results[case]["ContactForce glenoid"]["ML"])

    return Results


def score(Results):

    cases_list = list(Results.keys())

    # list of tilts and acromion lengths
    tilts = [case.split("-")[0] for case in cases_list]
    tilts = list(dict.fromkeys(tilts))  # removes duplicates

    acromion = [case.split("-")[1] for case in cases_list]
    acromion = list(dict.fromkeys(acromion))  # removes duplicates

    # Creates an empty table that will store the scores
    empty_scores_dataframe = pd.DataFrame(index=tilts, columns=acromion)

    # Creates a dictionary for each scores with empty tables
    scores_moment = {"Total": empty_scores_dataframe.copy(),
                     "AP": empty_scores_dataframe.copy(),
                     "IS": empty_scores_dataframe.copy(),
                     "ML": empty_scores_dataframe.copy()
                     }

    scores_shear = {"Total": empty_scores_dataframe.copy(),
                    "AP": empty_scores_dataframe.copy(),
                    "IS": empty_scores_dataframe.copy()
                    }

    for case in cases_list:

        time = Results[case]["Time"]["Total"]

        current_tilt = case.split("-")[0]
        current_acromion = case.split("-")[1]

        # COP in meter
        COP = np.array([Results[case]["COP"]["AP"],
                        Results[case]["COP"]["IS"],
                        Results[case]["COP"]["ML"]]).T / 1000

        # -ML pour remettre compression = négatif
        ContactForce = np.array([Results[case]["ContactForce glenoid"]["AP"],
                                 Results[case]["ContactForce glenoid"]["IS"],
                                 -Results[case]["ContactForce glenoid"]["ML"]]).T

        moment = np.zeros([len(COP), 4])

        # Calcul des moments et de son score pour chaque pas de temps (COP x Contact force)
        for step in range(len(COP)):

            # calculates moments
            moment[step, 0:3] = np.cross(COP[step, :], ContactForce[step, :])

            # Total score = norm(moment)
            moment[step, 3] = np.linalg.norm(moment[step, 0:3])

        # stocke le score de ce cas dans le tableau (intégrale du score)
        scores_moment["AP"].at[current_tilt, current_acromion] = np.trapz(abs(moment[:, 0]), time)
        scores_moment["IS"].at[current_tilt, current_acromion] = np.trapz(abs(moment[:, 1]), time)
        scores_moment["ML"].at[current_tilt, current_acromion] = np.trapz(abs(moment[:, 2]), time)
        scores_moment["Total"].at[current_tilt, current_acromion] = np.trapz(moment[:, 3], time)

        shear = np.array([Results[case]["ContactForce glenoid"]["AP"],
                          Results[case]["ContactForce glenoid"]["IS"],
                          np.zeros(len(Results[case]["ContactForce glenoid"]["AP"]))]).T

        # Last column is the root of the squared sum of AP and IS shear
        shear[:, 2] = np.sqrt(shear[:, 0]**2 + shear[:, 1]**2)

        # integral of the shear forces
        scores_shear["AP"].at[current_tilt, current_acromion] = np.trapz(abs(shear[:, 0]), time)
        scores_shear["IS"].at[current_tilt, current_acromion] = np.trapz(abs(shear[:, 1]), time)
        scores_shear["Total"].at[current_tilt, current_acromion] = np.trapz(shear[:, 2], time)

        # Save shear scores in the variables and in a new variable named score
        Results[case]["ContactForce glenoid"]["TotalShear"] = shear[:, 2]
        Results[case]["Moment"] = array_to_dictionary(moment, "Moment on the glenoid implant [N.m]", SequenceComposantes=["AP", "IS", "ML", "Total"])

        # Contribution des forces au moment
        Results[case]["Moment"]["AP_shearIS"] = abs(ContactForce[:, 1] * COP[:, 2])
        Results[case]["Moment"]["AP_compression"] = abs(ContactForce[:, 2] * COP[:, 1])

        Results[case]["Moment"]["IS_shearAP"] = abs(ContactForce[:, 0] * COP[:, 2])
        Results[case]["Moment"]["IS_compression"] = abs(ContactForce[:, 2] * COP[:, 0])

        # ratio contribution shear/totalmoment
        Results[case]["Moment"]["AP_ratio"] = Results[case]["Moment"]["AP_shearIS"] / abs(moment[:, 0])
        Results[case]["Moment"]["IS_ratio"] = Results[case]["Moment"]["IS_shearAP"] / abs(moment[:, 1])

    return Results, scores_moment, scores_shear


Results = instability_ratio(Results)
Results, scores_moment, scores_shear = score(Results)

# Sauvegarde des scores en .pkl
save_results_to_file(scores_moment, SaveSimulationsDirectory, "scores_moment")
save_results_to_file(scores_shear, SaveSimulationsDirectory, "scores_shear")

save_results_to_file(Results, SaveSimulationsDirectory, "Results")
