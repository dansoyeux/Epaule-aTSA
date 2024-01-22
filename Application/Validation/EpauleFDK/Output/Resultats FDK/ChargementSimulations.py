# import Anybody_LoadOutput.LoadOutput as LoadOutput
# import Anybody_Tools as LoadOutputTools

from Anybody_Package.Anybody_LoadOutput.LoadOutput import define_variables_to_load
from Anybody_Package.Anybody_LoadOutput.LoadOutput import load_simulation_cases
from Anybody_Package.Anybody_LoadOutput.LoadOutput import load_simulation
from Anybody_Package.Anybody_LoadOutput.LoadOutput import create_compared_simulations

from Anybody_Package.Anybody_LoadOutput.Tools import save_results_to_file

from Anybody_Package.Anybody_LoadOutput.LoadLiterature import load_literature_data
from Anybody_Package.Anybody_LoadOutput.LoadOutput import combine_simulation_cases

import numpy as np

import pandas as pd

# %% Setup des variables à charger

# Muscles
MuscleDictionary = {"Triceps long head": ["Triceps_LH", "_", [1, 2]],
                    "Deltoideus lateral": ["deltoideus_lateral", "_part_", [1, 4]],
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

                            "F origin": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the origin [N]", "select_matrix_line": 0,
                                         "rotation_matrix_path": "Output.Seg.Scapula.GlenImplantPos.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                         "combine_muscle_part_operations": ["total", "mean"]},

                            "F insertion": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the insertion [N]", "select_muscle_RefFrame_output": "insertion",
                                            "rotation_matrix_path": "Output.Seg.Scapula.GlenImplantPos.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                            "combine_muscle_part_operations": ["total", "mean"]
                                            },


                            "F origin direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the origin", "select_matrix_line": 0,
                                                   "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                                   "combine_muscle_part_operations": ["mean"], "vect_dir": True},

                            "F insertion direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the insertion", "select_muscle_RefFrame_output": "insertion",
                                                      "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                                      "combine_muscle_part_operations": ["mean"], "vect_dir": True},

                            "MomentArm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "MomentArm", "VariableDescription": "Lever arm [mm]",
                                          "combine_muscle_part_operations": ["mean"], "MultiplyFactor": 1000}
                            }

MuscleVariableDictionary_NoMomentArm = {"Ft": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Ft", "VariableDescription": "Muscle force [N]"},
                                        # "Fm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Fm", "VariableDescription": "Muscle force [N]"},
                                        # "Activity": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "CorrectedActivity", "VariableDescription": "Muscle activity [%]", "MultiplyFactor": 100, "combine_muscle_part_operations": ["max", "mean"]},

                                        "F origin": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the origin [N]", "select_matrix_line": 0,
                                                     "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                                     "combine_muscle_part_operations": ["total", "mean"]},

                                        "F origin direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the origin", "select_matrix_line": 0,
                                                               "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                                               "combine_muscle_part_operations": ["mean"], "vect_dir": True},

                                        "F insertion": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the insertion [N]", "select_muscle_RefFrame_output": "insertion",
                                                        "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                                        "combine_muscle_part_operations": ["total", "mean"]
                                                        },
                                        "F insertion direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the insertion", "select_muscle_RefFrame_output": "insertion",
                                                                  "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                                                  "combine_muscle_part_operations": ["mean"], "vect_dir": True}

                                        }

# Variables
FDK_VariableDictionary = {"Elevation": {"VariablePath": "Output.Model.BodyModel.Right.ShoulderArm.InterfaceFolder.ScapulaHumerus.Elevation.Pos",
                                        "VariableDescription": "Elevation angle in the scapular plane [°]", "MultiplyFactor": 180 / np.pi},

                          "Abduction": {"VariablePath": "Output.rotD", "VariableDescription": "Abduction angle [°]"},

                          # "Temps": {"VariablePath": "Output.Abscissa.t", "VariableDescription": "Time [s]"},

                          "ContactArea": {"VariablePath": "Output.Jnt.ProtheseContact.ContactArea", "VariableDescription": "Contact area [cm^2]", "MultiplyFactor": 10000},

                          "GHLin ISB": {"VariablePath": "Output.Jnt.GHLin_ISB.Pos", "VariableDescription": "Linear displacement (ISB) of the humerus [mm]", "MultiplyFactor": 1000,
                                        "SequenceComposantes": ["AP", "IS", "ML"]},

                          "GHLin Absolute": {"VariablePath": "Output.Jnt.GHLin_Absolute.Pos", "VariableDescription": "Absolute Linear displacement of the humerus [mm]", "MultiplyFactor": 1000,
                                             "SequenceComposantes": ["ML", "IS", "AP"], "Composantes_Inverse_Direction": [False, False, True]},

                          "GHLin Absolute zero": {"VariablePath": "Output.Jnt.GHLin_Absolute.Pos", "VariableDescription": "Absolute Linear displacement of the humerus [mm]", "MultiplyFactor": 1000,
                                                  "SequenceComposantes": ["ML", "IS", "AP"], "Composantes_Inverse_Direction": [False, False, True], "offset": [0, 0, 0]},

                          # "GHLin": {"VariablePath": "Output.Jnt.GHLin.Pos", "VariableDescription": "Linear displacement of the humerus [mm]", "MultiplyFactor": 1000,
                          #           "SequenceComposantes": ["AP", "IS", "ML"]},


                          "GHLin ISB Relative": {"VariablePath": "Output.Jnt.GHLin_ISB.Pos", "VariableDescription": "Relative linear displacement (ISB) of the humerus [mm]", "MultiplyFactor": 1000,
                                                 "SequenceComposantes": ["AP", "IS", "ML"], "offset": [0, 0, 0]},

                          "COP": {"VariablePath": "Output.FileOut.COPlocalImplant", "VariableDescription": "Center of Pressure [mm]", "MultiplyFactor": 1000,
                                  "SequenceComposantes": ["AP", "IS", "ML"]},

                          # Dans le repère de l'humérus ISB (pour comparaison avec bergmann)
                          "ForceContact": {"VariablePath": "Output.FileOut.ContactForce", "VariableDescription": "Contact force on the humerus [N]",
                                           "SequenceComposantes": ["AP", "IS", "ML"]},

                          # Force sur l'humérus Dans le repère de l'implant glene (humerus = master)
                          "ForceContact HumImplant glene": {"VariablePath": "Output.Jnt.ProtheseContact.Fmaster", "VariableDescription": "Contact force on the humerus [N]",
                                                            "SequenceComposantes": ["AP", "IS", "ML"], "rotation_matrix_path": "Output.Seg.Scapula.GlenImplantPos.Axes", "inverse_rotation": True},

                          # Force sur la scapula Dans le repère de la scapula ISB (scapula = slave)
                          "ForceContact scapula": {"VariablePath": "Output.Jnt.ProtheseContact.Fslave", "VariableDescription": "Contact force on the scapula [N]",
                                                   "SequenceComposantes": ["AP", "IS", "ML"], "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True},

                          # Force sur la scapula Dans le repère de l'implant (scapula = slave)
                          "ForceContact GlenImplant": {"VariablePath": "Output.Jnt.ProtheseContact.Fslave", "VariableDescription": "Contact force on the scapula [N]",
                                                       "SequenceComposantes": ["AP", "IS", "ML"], "rotation_matrix_path": "Output.Seg.Scapula.GlenImplantPos.Axes", "inverse_rotation": True},

                          # Force sur l'humerus Dans le repère de la scapula ISB (humerus = master)
                          "ForceContact humerus": {"VariablePath": "Output.Jnt.ProtheseContact.Fmaster", "VariableDescription": "Contact force on the humérus [N]",
                                                   "SequenceComposantes": ["AP", "IS", "ML"], "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True},

                          "ForceTolError": {"VariablePath": "Output.ForceDepKinError.Val", "VariableDescription": "FDK force error [N]"},


                          # Dans le repère ISB de la scapula (inverser la force car appliquée dans sens inverse for some reason)
                          "SpringForce scapula": {"VariablePath": "Output.Jnt.SpringForce.F", "VariableDescription": "Spring force on the scapula [N]", "SequenceComposantes": ["AP", "IS", "ML"],
                                                  "Composantes_Inverse_Direction": [True, True, True]},

                          # Dans le repère ISB de la scapula (for some reason GHLin a premiere ref frame = scapula mais force appliquée sur humérus avec le bon signe)
                          "SpringForce humerus": {"VariablePath": "Output.Jnt.SpringForce.F", "VariableDescription": "Spring force on the l'humérus [N]", "SequenceComposantes": ["AP", "IS", "ML"]},

                          # Dans repère scapula
                          # # Dans le repère ISB de la scapula (inverser la force car appliquée dans sens inverse for some reason)
                          # "SpringForce scapula": {"VariablePath": "Output.FileOut.SpringForce_Scapula_ISB", "VariableDescription": "Spring force on the scapula [N]", "SequenceComposantes": ["AP", "IS", "ML"],
                          #                         "Composantes_Inverse_Direction": [True, True, True]},

                          # # Dans le repère ISB de la scapula (for some reason GHLin a premiere ref frame = scapula mais force appliquée sur humérus avec le bon signe)
                          # "SpringForce humerus": {"VariablePath": "Output.FileOut.SpringForce_Scapula_ISB", "VariableDescription": "Spring force on the l'humérus [N]", "SequenceComposantes": ["AP", "IS", "ML"]},


                          }


BallAndSocket_VariableDictionary = {"Abduction": {"VariablePath": "Output.rotD", "VariableDescription": "Abduction angle [°]"},
                                    "Elevation": {"VariablePath": "Output.Model.BodyModel.Right.ShoulderArm.InterfaceFolder.ScapulaHumerus.Elevation.Pos",
                                                  "VariableDescription": "Elevation angle in the scapular plane [°]", "MultiplyFactor": 180 / np.pi}
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

BallAndSocket_Variables = define_variables_to_load(BallAndSocket_VariableDictionary, MuscleDictionary, MuscleVariableDictionary_NoMomentArm, BallAndSocket_ConstantsDictionary)

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

# Tilt acromion
xUpCases_3 = ["xup-xshort", "xup-normal", "xup-xlong"]
UpCases_3 = ["up-xshort", "up-normal", "up-xlong"]
MiddleCases_3 = ["middle-xshort", "middle-normal", "middle-xlong"]
DownCases_3 = ["down-xshort", "down-normal", "down-xlong"]
xDownCases_3 = ["xdown-xshort", "xdown-normal", "xdown-xlong"]

CaseNames_3 = [*xDownCases_3, *MiddleCases_3, *xUpCases_3]
UpDownCases_3 = [*xUpCases_3, *xDownCases_3]


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
Abduction 25 cas
sans scaling du deltoide postérieur
"""
# no_delt_post_scaling_dir = "../SaveData/Macro_Results_no_delt_post_scaling"
# date = "30-10-"
# Files = [date + CaseName + description + "-MR_Polynomial-no-delt-post-scaling" for CaseName in CaseNames_5]
# Results_GlenoidLocalAxis_MR_Polynomial = load_simulation_cases(no_delt_post_scaling_dir, Files, CaseNames_5, FDK_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_MR_Polynomial, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial")

"""Abduction 25 cas
Avec force de recentrage constante
"""
# no_recentrage_dir = "../SaveData/Macro_Results_no_recentrage"
# date = "04-01-"
# Files = [date + CaseName + description + "-MR_Polynomial-no-recentrage" for CaseName in CaseNames_5]

# Failed_no_recentrage = [False, False, False, False, False,
#                         False, False, False, False, False,
#                         False, False, False, False, False,
#                         False, False, False, False, False,
#                         False, False, False, False, False
#                         ]

# Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage = load_simulation_cases(no_recentrage_dir, Files, CaseNames_5, FDK_Variables, Failed=Failed_no_recentrage)


# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage")

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


"""No recentrage small abduction"""
# no_delt_post_scaling_dir = r"../SaveData/SmallAbduction_no_recentrage"
# date = "30-10-"
# Files = [date + CaseName + description + "-MR_Polynomial-SmallAbduction-no-delt-post-scaling-no-recentrage" for CaseName in CaseNames_5]
# Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage = load_simulation_cases(no_delt_post_scaling_dir, Files, CaseNames_5, FDK_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage")

"""Fixed Hill muscles parameters"""
# no_delt_post_scaling_dir = r"../SaveData/Macro_Results_fixed_hill_param"
# date = "30-10-"

# Files = [date + CaseName + description + "-MR_Polynomial-hill-parameter-middle-normal" for CaseName in CaseNames_3]
# Results_GlenoidLocalAxis_MR_Polynomial_Fixed_Hill = load_simulation_cases(no_delt_post_scaling_dir, Files, CaseNames_3, FDK_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_MR_Polynomial_Fixed_Hill, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_Fixed_Hill")

"""Better initialpos"""
# initialpos_dir = "../SaveData/Better_initialpos"
# date = "04-01-"
# Files = [date + CaseName + description + "-MR_Polynomial" for CaseName in CaseNames_5]
# Results_GlenoidLocalAxis_MR_Polynomial_Better_Initialpos = load_simulation_cases(initialpos_dir, Files, CaseNames_5, FDK_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_GlenoidLocalAxis_MR_Polynomial_Better_Initialpos, SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_Better_Initialpos")


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


# %% chargement new littérature depuis excel

Results_literature = load_literature_data("Template_importation_littérature", "Anybody_Package/Template")
save_results_to_file(Results_literature, SaveSimulationsDirectory, "Results_literature")
