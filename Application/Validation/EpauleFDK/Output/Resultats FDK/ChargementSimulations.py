# import Anybody_LoadOutput.LoadOutput as LoadOutput
# import Anybody_Tools as LoadOutputTools

from Anybody_Package.Anybody_LoadOutput.LoadOutput import define_variables_to_load
from Anybody_Package.Anybody_LoadOutput.LoadOutput import load_simulation_cases
from Anybody_Package.Anybody_LoadOutput.LoadOutput import load_simulation
from Anybody_Package.Anybody_LoadOutput.LoadOutput import create_compared_simulations

from Anybody_Package.Anybody_LoadOutput.Tools import save_results_to_file
from Anybody_Package.Anybody_LoadOutput.Tools import array_to_dictionary

import numpy as np

import pandas as pd

# %% Setup des variables à charger

# Muscles
MuscleDictionary = {"Deltoideus lateral": ["deltoideus_lateral", "_part_", [1, 4]],
                    "Deltoideus posterior": ["deltoideus_posterior", "_part_", [1, 4]],
                    "Deltoideus anterior": ["deltoideus_anterior", "_part_", [1, 4]],
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

                    "Pectoralis minor": ["pectoralis_minor", "_", [1, 4]],
                    "Latissimus dorsi": ["latissimus_dorsi", "_", [1, 11]],
                    "Triceps long head": ["Triceps_LH", "_", [1, 2]],
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

MuscleDictionary_MyDeltoideusWrapping = {"Deltoideus lateral": ["My_deltoideus_lateral", "_part_", [1, 4]],
                                         "Deltoideus posterior": ["My_deltoideus_posterior", "_part_", [1, 4]],
                                         "Deltoideus anterior": ["deltoideus_anterior", "_part_", [1, 4]],
                                         "Supraspinatus": ["supraspinatus", "_", [1, 6]],
                                         "Infraspinatus": ["infraspinatus", "_", [1, 6]],
                                         "Serratus anterior": ["serratus_anterior", "_", [1, 6]],
                                         "Lower trapezius": ["trapezius_scapular", "_part_", [1, 3]],
                                         "Middle trapezius": ["trapezius_scapular", "_part_", [4, 6]],
                                         "Upper trapezius": ["trapezius_clavicular", "_part_", [1, 6]],
                                         "Biceps brachii long head": ["biceps_brachii_caput_longum", "", []],
                                         "Biceps brachii short head": ["biceps_brachii_caput_breve", "", []],
                                         "Pectoralis minor": ["pectoralis_minor", "_", [1, 4]],
                                         "Pectoralis major clavicular": ["pectoralis_major_clavicular", "_part_", [1, 5]],
                                         "Pectoralis major sternal": ["pectoralis_major_thoracic", "_part_", [1, 10]],

                                         "Pectoralis major": [["pectoralis_major_thoracic", "_part_", [1, 10]],
                                                              ["pectoralis_major_clavicular", "_part_", [1, 5]]
                                                              ],

                                         "Latissimus dorsi": ["latissimus_dorsi", "_", [1, 11]],
                                         "Triceps long head": ["Triceps_LH", "_", [1, 2]],
                                         "Subscapularis": ["subscapularis", "_", [1, 6]],
                                         "Upper Subscapularis": ["subscapularis", "_", [1, 2]],
                                         "Downward Subscapularis": ["subscapularis", "_", [3, 6]],
                                         "Teres minor": ["teres_minor", "_", [1, 6]],
                                         "Teres major": ["teres_major", "_", [1, 6]],
                                         "Rhomboideus": ["rhomboideus", "_", [1, 3]],
                                         "Levator scapulae": ["levator_scapulae", "_", [1, 4]],
                                         "Sternocleidomastoid clavicular": ["Sternocleidomastoid_caput_clavicular", "", []],
                                         "Sternocleidomastoid sternum": ["Sternocleidomastoid_caput_Sternum", "", []],
                                         "Coracobrachialis": ["coracobrachialis", "_", [1, 6]]
                                         }

MuscleVariableDictionary = {"Fm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Fm", "VariableDescription": "Force musculaire [Newton]"},
                            "Ft": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Ft", "VariableDescription": "Force musculaire totale [Newton]"},
                            "Activity": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "CorrectedActivity", "VariableDescription": "Activité Musculaire [%]", "MultiplyFactor": 100, "combine_muscle_part_operations": ["max", "mean"]},

                            "F origin": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Force Musculaire à l'origine du muscle [N]", "select_matrix_line": 0,
                                         "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                         "combine_muscle_part_operations": ["total", "mean"]},

                            "F insertion": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Force Musculaire à l'insertion du muscle [N]", "select_matrix_line": 1,
                                            "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                            "combine_muscle_part_operations": ["total", "mean"]},
                            "MomentArm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "MomentArm", "VariableDescription": "Bras de levier du muscle [mm]",
                                              "combine_muscle_part_operations": ["mean"], "MultiplyFactor": 1000}
                            }

MuscleVariableDictionary_NoMomentArm = {"Fm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Fm", "VariableDescription": "Force musculaire [Newton]"},
                                       "Ft": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Ft", "VariableDescription": "Force musculaire totale [Newton]"},
                                       "Activity": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "CorrectedActivity", "VariableDescription": "Activité Musculaire [%]", "MultiplyFactor": 100, "combine_muscle_part_operations": ["max", "mean"]},

                                "F origin": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Force Musculaire à l'origine du muscle [N]", "select_matrix_line": 0,
                                         "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                         "combine_muscle_part_operations": ["total", "mean"]},

                            "F insertion": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Force Musculaire à l'insertion du muscle [N]", "select_matrix_line": 1,
                                            "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                            "combine_muscle_part_operations": ["total", "mean"]},
                            # "MomentArm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "MomentArm", "VariableDescription": "Bras de levier du muscle [mm]",
                            #                  "combine_muscle_part_operations": ["mean"], "MultiplyFactor": 1000}
                            }

# Variables
FDK_VariableDictionary = {"Elevation": {"VariablePath": "Output.Model.BodyModel.Right.ShoulderArm.InterfaceFolder.ScapulaHumerus.Elevation.Pos",
                                        "VariableDescription": "Angle d'élévation dans le plan de la scapula [°]", "MultiplyFactor": 180 / np.pi},
                          "Abduction": {"VariablePath": "Output.rotD", "VariableDescription": "Angle d'abduction [°]"},

                          "Temps": {"VariablePath": "Output.Abscissa.t", "VariableDescription": "Temps [s]"},

                          # "ContactArea": {"VariablePath": "Output.Jnt.ProtheseContact.ContactArea", "VariableDescription": "Surface de contact [cm^2]", "MultiplyFactor": 10000},
                          # "GHLin Absolute": {"VariablePath": "Output.Jnt.GHLin_Absolute.Pos", "VariableDescription": "Déplacement Linéaire de l'humérus [mm]", "MultiplyFactor": 1000,
                          #                    "SequenceComposantes": ["ML", "IS", "AP"], "Composantes_Inverse_Direction": [False, False, True]},

                          # "GHLin Absolute Amplitude": {"VariablePath": "Output.Jnt.GHLin_Absolute.Pos", "VariableDescription": "Déplacement Linéaire de l'humérus [mm]", "MultiplyFactor": 1000,
                          #                              "SequenceComposantes": ["ML", "IS", "AP"], "Composantes_Inverse_Direction": [False, False, True], "offset": [0, 0, 0]},


                          # "Eps": {"VariablePath": "Output.Jnt.SpringForce.Eps", "VariableDescription": "Déplacement relatif de l'humérus  [mm]", "MultiplyFactor": 1000,
                          #         "SequenceComposantes": ["AP", "IS", "ML"]},

                          # "GHLin": {"VariablePath": "Output.Jnt.GHLin.Pos", "VariableDescription": "Déplacement Linéaire de l'humérus par rapport au centre de l'implant [mm]",
                          #           "MultiplyFactor": 1000, "SequenceComposantes": ["AP", "IS", "ML"]},

                          # "GHLin Relative": {"VariablePath": "Output.Jnt.GHLin.Pos", "VariableDescription": "Déplacement Linéaire de l'humérus par rapport au centre de l'implant [mm]",
                          #                    "MultiplyFactor": 1000, "SequenceComposantes": ["AP", "IS", "ML"], "offset": [0, 0, 0]},

                          "GHLin ISB": {"VariablePath": "Output.Jnt.GHLin_ISB.Pos", "VariableDescription": "Déplacement Linéaire (ISB) de l'humérus par rapport au centre de l'implant [mm]", "MultiplyFactor": 1000,
                                        "SequenceComposantes": ["AP", "IS", "ML"], "Composantes_Inverse_Direction": [False, False, True]},

                          "GHLin ISB Relative": {"VariablePath": "Output.Jnt.GHLin_ISB.Pos", "VariableDescription": "Déplacement Linéaire (ISB) de l'humérus par rapport au centre de l'implant [mm]", "MultiplyFactor": 1000,
                                                 "SequenceComposantes": ["AP", "IS", "ML"], "Composantes_Inverse_Direction": [False, False, True], "offset": [0, 0, 0]},

                          "COP": {"VariablePath": "Output.FileOut.COPlocalImplant", "VariableDescription": "Position du centre de pression", "MultiplyFactor": 1000,
                                  "SequenceComposantes": ["AP", "IS", "ML"]},

                          "SpringForce": {"VariablePath": "Output.Jnt.SpringForce.F", "VariableDescription": "Force de ressort [Newton]"},

                          # Dans le repère de l'humérus ISB
                          "ForceContact": {"VariablePath": "Output.FileOut.ContactForce", "VariableDescription": "Force de contact [Newton]",
                                           "SequenceComposantes": ["AP", "IS", "ML"]},

                          "ForceTolError": {"VariablePath": "Output.ForceDepKinError.Val", "VariableDescription": "Erreure de force FDK [Newton]"}

                          }


BallAndSocket_VariableDictionary = {"Abduction": {"VariablePath": "Output.rotD", "VariableDescription": "Angle d'abduction [°]"},
                                    "Elevation": {"VariablePath": "Output.Model.BodyModel.Right.ShoulderArm.InterfaceFolder.ScapulaHumerus.Elevation.Pos",
                                                  "VariableDescription": "Angle d'élévation dans le plan de la scapula [°]", "MultiplyFactor": 180 / np.pi}
                                    }

# Constantes
FDK_ConstantsDictionary = {"AnybodyFileOutPath": "Main.Study.FileOut",
                           "Paramètres de simulation": ["Case", "MuscleRecruitment", "nStep", "tEnd", "GHReactions", "Movement"],
                           "Mannequin": ["GlenohumeralFlexion", "GlenohumeralAbduction", "GlenohumeralExternalRotation"],

                           "ParametresFDK": ["k0", "k1", "k2", "k3", "k4", "kz", "kd", "ForceTol", "UseAdaptiveForceTolOnOff", "MaxIteration",
                                             "Perturbation", "PerturbationSymmetricOnOff", "LocalSearchOnOff", "MaxNewtonStep"],

                           "Positions initiales": ["px", "py", "pz"],

                           "Paramètres implants": ["HumerusName", "GlenoidName", "Case", "RotationAxis", "GleneImplantTiltAngle", "GlenImplantRotation",
                                                   "GlenImplantPosition", "GlenImplantCenter", "HumImplantPosition", "HumImplantRotation", "AcromionOffset"],
                           "MyMuscleWrapping": ["WrappingSurfaceShape", "LateralWrapping_RadiusX", "LateralWrapping_Radius", "LateralWrapping_RadiusHeight", "PosteriorWrapping_RadiusX", "PosteriorWrapping_Radius", "PosteriorWrapping_RadiusHeight"]
                           }

BallAndSocket_ConstantsDictionary = {"AnybodyFileOutPath": "Main.Study.FileOut",
                                     "Paramètres de simulation": ["Case", "MuscleRecruitment", "nstep", "GHReactions", "Movement"],
                                     "Mannequin": ["GlenohumeralFlexion", "GlenohumeralAbduction", "GlenohumeralExternalRotation"],
                                     }


FDK_Variables = define_variables_to_load(FDK_VariableDictionary, MuscleDictionary, MuscleVariableDictionary, FDK_ConstantsDictionary)

FDK_Variables_NoMomentArm = define_variables_to_load(FDK_VariableDictionary, MuscleDictionary, MuscleVariableDictionary_NoMomentArm)

FDK_Variables_MyDeltoideusWrapping = define_variables_to_load(FDK_VariableDictionary, MuscleDictionary_MyDeltoideusWrapping, MuscleVariableDictionary, FDK_ConstantsDictionary)

BallAndSocket_Variables = define_variables_to_load(BallAndSocket_VariableDictionary, MuscleDictionary, MuscleVariableDictionary, BallAndSocket_ConstantsDictionary)

# %% Nom des cas de simulation

OldCaseNames = ["middle-normal", "middle-long",
                "up-normal", "up-short",
                "down-long"]

# Tilt acromion
xUpCases = ["xup-xshort", "xup-normal"]
MiddleCases = ["middle-xshort", "middle-normal", "middle-xlong"]
DownCases = ["xdown-normal", "xdown-xlong"]

# Longueur d'acromion
ShortCases = ["middle-xshort", "xup-xshort"]
NormalCases = ["middle-normal", "xup-normal", "xdown-normal"]
LongCases = ["xmiddle-xlong", "xdown-xlong"]

CaseNames = [*MiddleCases, *xUpCases, *DownCases]
UpDownCases = [*xUpCases, *DownCases]

CSA_20_Cases = ["middle-xshort", "xdown-normal"]
CSA_30_Cases = ["middle-normal", "xup-xshort", "xdown-xlong"]
CSA_40_Cases = ["middle-xlong", "xup-normal"]

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

# More cases
xDownCases_5 = ["xdown-xshort", "xdown-short", "xdown-normal", "xdown-long", "xdown-xlong"]
DownCases_5 = ["down-xshort", "down-short", "down-normal", "down-long", "down-xlong"]
MiddleCases_5 = ["middle-xshort", "middle-short", "middle-normal", "middle-long", "middle-xlong"]
UpCases_5 = ["up-xshort", "up-short", "up-normal", "up-long", "up-xlong"]
xUpCases_5 = ["xup-xshort", "xup-short", "xup-normal", "xup-long", "xup-xlong"]

xShortCases_5 = ["xdown-xshort", "down-xshort", "middle-xshort", "up-xshort", "xup-xshort"]
ShortCases_5 = ["xdown-short", "down-short", "middle-short", "up-short", "xup-short"]
NormalCases_5 = ["xdown-normal", "down-normal", "middle-normal", "up-normal", "xup-normal"]
LongCases_5 = ["xdown-long", "down-long", "middle-long", "up-long", "xup-long"]
xLongCases_5 = ["xdown-xlong", "down-xlong", "middle-xlong", "up-xlong", "xup-xlong"]

CaseNames_5 = [*xDownCases_5, *DownCases_5, *MiddleCases_5, *UpCases_5, *xUpCases_5]


# %%                                                Résultats FDK

SaveDataDir = r"../SaveData/Variation_CSA"
# SaveDataDir_Macro = r"../SaveData/Macro_Results"
description = "-GlenoidAxisTilt"

# Chemin d'accès au dossier dans lequel les fichiers doivent être sauvegardés
SaveSimulationsDirectory = "Saved Simulations"


# # Pour tests
# date = "06-10-"
# Files = [date + CaseName + description + "-MR_Polynomial" for CaseName in ["middle-normal"]]

# aa = load_simulation_cases(SaveDataDir, Files, ["middle-normal"], FDK_Variables_NoMomentArm)

"""
Results and polynomial recruitment
Without new wrapping with xshorts
with 25 cases
"""

# date = "06-10-"
# Files = [date + CaseName + description + "-MR_Polynomial" for CaseName in CaseNames_5]

# Results_GlenoidLocalAxis_MR_Polynomial_delt_post_scaling = load_simulation_cases(SaveDataDir, Files, CaseNames_5, FDK_Variables_NoMomentArm)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_MR_Polynomial_delt_post_scaling, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_delt_post_scaling")

"""
Abduction 25 cas
sans scaling du deltoide postérieur
"""
# no_delt_post_scaling_dir = "../SaveData/Macro_Results_no_delt_post_scaling"
# date = "30-10-"
# Files = [date + CaseName + description + "-MR_Polynomial-no-delt-post-scaling" for CaseName in CaseNames_5]
# Results_GlenoidLocalAxis_MR_Polynomial = load_simulation_cases(no_delt_post_scaling_dir, Files, CaseNames_5, FDK_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_MR_Polynomial, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial")



"""
Results and polynomial recruitment
Without new wrapping with xshorts
normal cases with 180 abduction

WITHOUT MOMENT ARM
"""
Macros_results_dir = r"../SaveData/Macro_Results"
Macros_results_dir2 = r"../SaveData/Macro_80step_180deg"
date = "06-10-"

# First failed step (lose contact or FDK error over 0.001)
Failed_180_Simulation = [51, 50, 50, 49, 48,
                         53, 53, 52, 51, 50,
                         56, 55, 54, 52, 52,
                         False, 65, 57, 55, 54,
                         False, False, 58, 57, 57
                         ]

# En prenant en compte aussi conflit avec acromion (juste la pointe, pas en-dessous)
Failed_180_Acromion = [51, 50, 50, 49, 48,
                       53, 53, 52, 51, 50,
                       56, 55, 54, 52, 52,
                       60, 57, 55, 53, 52,
                       54, 58, 51, 50, 50
                       ]

# Avec premier contact avec acromion
Failed_180 = [51, 50, 50, 49, 48,
              53, 53, 52, 51, 50,
              56, 55, 54, 52, 52,
              36, 34, 31, 28, 27,
              29, 26, 24, 21, 13
              ]

# # Avec premier contact avec acromion
# Files = [date + CaseName + description + "-MR_Polynomial-180deg" for CaseName in CaseNames_5]
# Results_GlenoidLocalAxis_MR_Polynomial_180deg = load_simulation_cases(Macros_results_dir2, Files, CaseNames_5, FDK_Variables_NoMomentArm, Failed=Failed_180)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_MR_Polynomial_180deg, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_180deg")

"""
En ne prenant pas en compte conflit avec acromion
"""
# Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange = load_simulation_cases(Macros_results_dir2, Files, CaseNames_5, FDK_Variables_NoMomentArm, Failed=Failed_180_Simulation)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange")

"""
Élévation
"""

# Elevation_dir = "../SaveData/No_delt_post_scaling_Elevation"
# Files = [date + CaseName + description + "-MR_Polynomial-no-delt-post-scaling-Elevation" for CaseName in CaseNames_5]

# Results_GlenoidLocalAxis_MR_Polynomial_Elevation = load_simulation_cases(Elevation_dir, Files, CaseNames_5, FDK_Variables_NoMomentArm)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_MR_Polynomial_Elevation, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_Elevation")


# %% autres tests
# """
# Normal cases with different recruitment types
# """

# TypesFiles = ["08-09-middle-normal-GlenoidAxisTilt",
#               "08-09-middle-normal-GlenoidAxisTilt-MR_Polynomial",
#               ]

# TypesCases = ["MR_QuadraticAux",
#               "MR_Polynomial",
#               ]

# Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types = load_simulation_cases(SaveDataDir, TypesFiles, TypesCases, FDK_Variables)
# Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types["MR_MinMaxStrict"] = load_simulation(SaveDataDir, "08-09-middle-normal-GlenoidAxisTilt-MR_MinMaxStrict", FDK_Variables, Failed=28)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types")

# """
# Results new AMMR
# """
# FDK_Files = ["20-09-middle-normal-GlenoidAxisTilt-MR_Polynomial-NEW-AMMR"]

# Results_GlenoidLocalAxis_NewWrapping_NewAMMR = load_simulation_cases(SaveDataDir, FDK_Files, ["middle-normal"], FDK_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_NewWrapping_NewAMMR, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_NewWrapping_NewAMMR")

# """Bigger Range"""
# Results_GlenoidLocalAxis_NewWrapping_FullRange = load_simulation_cases(SaveDataDir, ["08-09-middle-normal-GlenoidAxisTilt-MR_Polynomial-FullRange"], ["middle-normal"], FDK_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_NewWrapping_FullRange, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_NewWrapping_FullRange")

# %%                                                Résultats Ball and Socket
"""
Résultats sains avec différents scaling acromion
120° abduction
"""

# BallAndSocket_Files = [f"08-09-BallAndSocket-{CaseName}" for CaseName in ["short", "normal", "long"]]

# Results_BallAndSocket = load_simulation_cases(SaveDataDir, BallAndSocket_Files, MiddleCases, BallAndSocket_Variables)

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
# New AMMR
# """

# BallAndSocket_Files = ["08-09-BallAndSocket-normal-NEW-AMMR"]

# Results_BallAndSocket_NewAMMR = load_simulation_cases(SaveDataDir, BallAndSocket_Files, ["middle-normal"], BallAndSocket_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_BallAndSocket_NewAMMR, SaveSimulationsDirectory, "Results_BallAndSocket_NewAMMR")


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

save_results_to_file(FDK_Variables_MyDeltoideusWrapping, SaveVariablesDirectory, "FDK_Variables_MyDeltoideusWrapping")

# %% Sauvegarde data bergmann


def load_bergmann_data():
    BodyWeight = 75 * 9.81

    abduction = np.array([15, 30, 45, 75]).T

    # ForceContact = np.array([21, 35, 51, 85]).T / 100 * BodyWeight

    ForceContact_x = np.array([7.5, 13, 21, 34]).T
    ForceContact_y = np.array([-19, -31, -44, -74]).T
    ForceContact_z = np.array([4.5, 8.5, 16, 25]).T

    ForceContact = np.array([ForceContact_x, ForceContact_y, ForceContact_z]).T
    ForceContact = ForceContact / 100 * BodyWeight

    dataBergmann = {}

    dataBergmann["Abduction"] = array_to_dictionary(abduction, VariableDescription="Angle d'abduction [°]")
    dataBergmann["ForceContact"] = array_to_dictionary(ForceContact, VariableDescription="Force de contact [Newton]", SequenceComposantes=["AP", "IS", "ML"])

    return dataBergmann


dataBergmann_2007 = load_bergmann_data()
save_results_to_file(dataBergmann_2007, SaveSimulationsDirectory, "dataBergmann_2007")


# %% Data muscles Wickham

def load_data_wickham(SheetName, MinAngle, MaxAngle):

    from scipy.interpolate import UnivariateSpline

    File = pd.ExcelFile('Data Wikham et al/dataWickham.xlsx')

    dataWickham_raw = pd.read_excel(File, SheetName)

    Variables = pd.Series.to_numpy(dataWickham_raw.iloc[0, :])
    data = dataWickham_raw
    data = data.drop(index=[0])

    # Get muscles names
    Muscles = dataWickham_raw.columns.tolist()

    dataWickham = {}

    # Creates angles so that all the variables have the same angles
    # Will interpolate the datas with this angles
    Interpolated_Angle = np.linspace(MinAngle, MaxAngle, 100)

    # Convert these datas to dictionnary
    AngleDictionary = array_to_dictionary(Interpolated_Angle, VariableDescription="Angle d'abduction [°]")

    for index in range(0, len(Variables)):

        MuscleName = Muscles[index].replace(".1", "")

        Array = pd.Series(data.iloc[:, index]).dropna().to_numpy()
        Array = Array.astype('float')

        Variable = Variables[index]
        if Variable == "Abduction":
            Angle = Array

        # Once we reach activity, interpolates the data to have the activity for the Angles specified in Interpolated_Angle
        elif Variable == "Activity":
            Activity = Array

            # Interpolates the angle so that every data have the same angles
            Interpolation_Function = UnivariateSpline(Angle, Activity, s=5)

            Interpolated_Activity = Interpolation_Function(Interpolated_Angle)

            ActivityDictionary = array_to_dictionary(Interpolated_Activity, VariableDescription="Activité Musculaire [%]", MaximumOn=True)

            dataWickham[MuscleName] = {MuscleName: {"Activity": ActivityDictionary}}

    File.close()

    Results = {"Muscles": dataWickham}
    Results["Abduction"] = AngleDictionary

    return Results


# # Abduction
# dataWickham_abduction = load_data_wickham("Abduction", 15, 120)
# save_results_to_file(dataWickham_abduction, SaveSimulationsDirectory, "dataWickham_abduction")

# # Abduction Long Range
# dataWickham_abduction = load_data_wickham("Abduction", 1, 165.5)
# save_results_to_file(dataWickham_abduction, SaveSimulationsDirectory, "dataWickham_abduction_FullRange")

# # ADduction
# dataWickham_adduction = load_data_wickham("Adduction", 15, 120)
# save_results_to_file(dataWickham_adduction, SaveSimulationsDirectory, "dataWickham_adduction")

# %% data translation Dal Maso


def load_variable_from_excel(file_name, current_sheet_name, variables_description, SequenceComposantes_y, multiply_factors, min_x, max_x, n_points=100):
    """
    Toujours trier la variable x du plus petit au plus grand

    AJOUTER LES NOMS DE VARIABLES EN SORTIE,
    CONDENSER DANS UN DICTIONNAIRE
    """
    from scipy import interpolate

    Results = {}

    # nombre de variables pour chaque mesures, par défaut
    n_variables = 2

    # Number of lines on top that are not informations to loadheader line in excel
    n_header_line = 2

    File = pd.ExcelFile(file_name)

    # Définit les noms de variables comme la ligne de header entrée
    # Enlève les lignes avant cette ligne de variables
    data = pd.read_excel(File, current_sheet_name, header=n_header_line - 1, )

    File.close()

    # Liste des variables
    Variables = data.columns.to_numpy()[:n_variables]

    # numéro de la colomne à interpoler
    n_col_interpolate = 1
    # Nom de la variable qui sert d'interpolation (par défaut la première variable)
    var_interpolate = Variables[n_col_interpolate - 1]

    # Creates an empty array with the number of interpolated variables
    # array_interpolated_variable_y = np.empty((n_interpolate_points, len(Variables )))
    array_interpolated_variable_y = np.zeros((n_points, len(SequenceComposantes_y)))
    # array_interpolated_variable_y = np.array([[]])

    # Will interpolate the datas with these points
    interpolated_x = np.linspace(min_x, max_x, n_points)
    variable_y_index = 0

    for column_name in data.columns.to_list():

        # Dans le cas où on a la variable d'interpolation
        if var_interpolate in column_name:
            variable_x = data.loc[:, column_name].dropna().to_numpy()

        # quand on n'a pas la variable d'interpolation, interpole cette variable avec la variable en x
        else:
            # Gets the variable, enlève les NAN
            variable_y = data.loc[:, column_name].dropna().to_numpy()

            # calculates the spline interpolate function
            # interpolation_function = InterpolatedUnivariateSpline(variable_x, variable_y, s=5)

            # interpolated_variable_y = interpolation_function(interpolated_x)

            # calculates the spline interpolate function
            interpolation_function = interpolate.CubicSpline(variable_x, variable_y)

            interpolated_variable_y = interpolation_function(interpolated_x)

            # Adds the interpolated y variables to an array
            array_interpolated_variable_y[:, variable_y_index] = interpolated_variable_y
            variable_y_index += 1

    # Stocke le résultat de la variable x
    Results[var_interpolate] = array_to_dictionary(interpolated_x, variables_description[0], MultiplyFactor=multiply_factors[0])

    # Stocke la variable en y interpollée
    Results[Variables[1]] = array_to_dictionary(array_interpolated_variable_y, variables_description[1], MultiplyFactor=multiply_factors[1], SequenceComposantes=SequenceComposantes_y)

    return Results


multiply_factors = [1, 1]
variables_description = ["Angle d'abduction [°]", "Translation de la tête humérale [mm]"]
SequenceComposantes_y = ["ML", "AP", "IS"]
file_name = "Translations Dal Maso.xlsx"

# data_Dal_Maso_sup = load_variable_from_excel(file_name, "Dal Maso Supérieur", variables_description, SequenceComposantes_y, multiply_factors, 0, 90, n_points=100)
data_Dal_Maso_inf = load_variable_from_excel(file_name, "Dal Maso Inférieur", variables_description, SequenceComposantes_y, multiply_factors, 0, 90, n_points=100)


# save_results_to_file(data_Dal_Maso_sup, SaveSimulationsDirectory, "data_Dal_Maso_sup")
# save_results_to_file(data_Dal_Maso_inf, SaveSimulationsDirectory, "data_Dal_Maso_inf")
