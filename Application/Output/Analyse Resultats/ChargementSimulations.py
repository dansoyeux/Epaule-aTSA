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
MuscleDictionary = {"Deltoid lateral": ["deltoideus_lateral", "_part_", [1, 4]],
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

                    "Pectoralis minor": ["pectoralis_minor", "_", [1, 4]],
                    "Latissimus dorsi": ["latissimus_dorsi", "_", [1, 11]],
                    "Upper Subscapularis": ["subscapularis", "_", [1, 2]],
                    "Downward Subscapularis": ["subscapularis", "_", [3, 6]],
                    "Subscapularis": ["subscapularis", "_", [1, 6]],
                    "Teres minor": ["teres_minor", "_", [1, 6]],
                    "Teres major": ["teres_major", "_", [1, 6]],
                    "Triceps long head": ["Triceps_LH", "_", [1, 2]],
                    "Rhomboideus": ["rhomboideus", "_", [1, 3]],
                    "Levator scapulae": ["levator_scapulae", "_", [1, 4]],
                    "Sternocleidomastoid clavicular": ["Sternocleidomastoid_caput_clavicular", "", []],
                    "Sternocleidomastoid sternum": ["Sternocleidomastoid_caput_Sternum", "", []],
                    "Coracobrachialis": ["coracobrachialis", "_", [1, 6]]
                    }

MuscleVariableDictionary = {"Ft": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Ft", "VariableDescription": "Muscle force [N]"},

                            "MomentArm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "MomentArm", "VariableDescription": "Moment arm [mm]",
                                          "combine_muscle_part_operations": ["mean"], "MultiplyFactor": 1000},

                            # "Activity": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "CorrectedActivity", "VariableDescription": "Muscle activity [%]", "MultiplyFactor": 100, "combine_muscle_part_operations": ["max", "mean"]},

                            # Dans repère scapula
                            "F origin": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the origin [N]", "select_matrix_line": 0,
                                         "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                         "combine_muscle_part_operations": ["total", "mean"]},

                            "F insertion": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force at the insertion [N]", "select_muscle_RefFrame_output": "insertion",
                                            "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                            "combine_muscle_part_operations": ["total", "mean"]
                                            },

                            # "F surface": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force on the muscle wraping surface [N]", "select_muscle_RefFrame_output": "surface",
                            #               "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"]},

                            # "F via": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Muscle force on the muscle via point [N]", "select_muscle_RefFrame_output": "via",
                            #           "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"]},

                            # "F origin direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the origin", "select_matrix_line": 0,
                            #                        "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                            #                        "combine_muscle_part_operations": ["mean"], "vect_dir": True},

                            # "F insertion direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the insertion", "select_muscle_RefFrame_output": "insertion",
                            #                           "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                            #                           "combine_muscle_part_operations": ["mean"], "vect_dir": True},
                            }


# Variables
FDK_VariableDictionary = {"Abduction": {"VariablePath": "Output.Simulation_Outputs.AbductionAngle", "VariableDescription": "Abduction angle [°]"},

                          "ContactArea": {"VariablePath": "Output.Simulation_Outputs.ContactArea", "VariableDescription": r'Contact area [$cm^2$]', "MultiplyFactor": 10000},

                          "Time": {"VariablePath": "Output.Abscissa.t", "VariableDescription": "Time"},

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
                          # Compression = force positive
                          "ContactForce glenoid": {"VariablePath": "Output.Simulation_Outputs.ContactForce_GlenImplant", "VariableDescription": "Contact force on the glenoid implant [N]",
                                                   "SequenceComposantes": ["AP", "IS", "ML"], "Composantes_Inverse_Direction": [False, False, True]},

                          "ForceDepKinError": {"VariablePath": "Output.Simulation_Outputs.ForceDepKinError", "VariableDescription": "FDK Error [N]"}
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
                                                   "GlenImplantPosition", "GlenImplantCenter", "HumImplantPosition", "HumImplantRotation", "HumImplantCenter", "AcromionOffset"],
                           }

BallAndSocket_ConstantsDictionary = {"AnybodyFileOutPath": "Main.Study.FileOut",
                                     "Anybody version": ["AMMRVersion", "AnybodyVersion"],
                                     "Paramètres de simulation": ["Case", "MuscleRecruitment", "nstep", "GHReactions", "Movement"],
                                     "Mannequin": ["GlenohumeralFlexion", "GlenohumeralAbduction", "GlenohumeralExternalRotation"],
                                     }

FDK_Variables = define_variables_to_load(FDK_VariableDictionary, MuscleDictionary, MuscleVariableDictionary, FDK_ConstantsDictionary)
BallAndSocket_Variables = define_variables_to_load(BallAndSocket_VariableDictionary, MuscleDictionary, MuscleVariableDictionary, BallAndSocket_ConstantsDictionary)

# Chemin d'accès au dossier dans lequel les fichiers doivent être sauvegardés
SaveSimulationsDirectory = "Saved Simulations"

# %% Variables en français

# Muscles
MuscleDictionary_fr = {"Deltoid latéral": ["deltoideus_lateral", "_part_", [1, 4]],
                       "Deltoid postérieur": ["deltoideus_posterior", "_part_", [1, 4]],
                       "Deltoid antérieur": ["deltoideus_anterior", "_part_", [1, 4]],
                       "Supraépineux": ["supraspinatus", "_", [1, 6]],
                       "Infraépineux": ["infraspinatus", "_", [1, 6]],
                       "Dentelé antérieur": ["serratus_anterior", "_", [1, 6]],
                       "Trapèze inférieur": ["trapezius_scapular", "_part_", [1, 3]],
                       "Trapèze moyen": ["trapezius_scapular", "_part_", [4, 6]],
                       "Trapèze supérieur": ["trapezius_clavicular", "_part_", [1, 6]],

                       "Biceps brachial long": ["biceps_brachii_caput_longum", "", []],
                       "Biceps brachial court": ["biceps_brachii_caput_breve", "", []],
                       "Grand pectoral claviculaire": ["pectoralis_major_clavicular", "_part_", [1, 5]],
                       "Grand pectoral sternal": ["pectoralis_major_thoracic", "_part_", [1, 10]],

                       "Grand pectoral": [["pectoralis_major_thoracic", "_part_", [1, 10]],
                                          ["pectoralis_major_clavicular", "_part_", [1, 5]]
                                          ],

                       "Petit pectoral": ["pectoralis_minor", "_", [1, 4]],
                       "Grand dorsal": ["latissimus_dorsi", "_", [1, 11]],
                       "Subscapulaire supérieur": ["subscapularis", "_", [1, 2]],
                       "Subscapulaire inférieur": ["subscapularis", "_", [3, 6]],
                       "Subscapulaire": ["subscapularis", "_", [1, 6]],
                       "Petit rond": ["teres_minor", "_", [1, 6]],
                       "Grand rond": ["teres_major", "_", [1, 6]],
                       "Triceps long": ["Triceps_LH", "_", [1, 2]],
                       "Rhomboïde": ["rhomboideus", "_", [1, 3]],
                       "Levator scapulae": ["levator_scapulae", "_", [1, 4]],
                       "Sternocleidomastoid claviculaire": ["Sternocleidomastoid_caput_clavicular", "", []],
                       "Sternocleidomastoid sternum": ["Sternocleidomastoid_caput_Sternum", "", []],
                       "Coracobrachialis": ["coracobrachialis", "_", [1, 6]]
                       }

MuscleVariableDictionary_fr = {"Ft": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Ft", "VariableDescription": "Force musculaire [N]"},

                               "MomentArm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "MomentArm", "VariableDescription": "Bras de levier [mm]",
                                             "combine_muscle_part_operations": ["mean"], "MultiplyFactor": 1000},

                               # "Activity": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "CorrectedActivity", "VariableDescription": "Muscle activity [%]", "MultiplyFactor": 100, "combine_muscle_part_operations": ["max", "mean"]},

                               # Dans repère scapula
                               "F origin": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Force musculaire à l'origine [N]", "select_matrix_line": 0,
                                            "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                            "combine_muscle_part_operations": ["total", "mean"]},

                               "F insertion": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Force musculaire à l'insertion [N]", "select_muscle_RefFrame_output": "insertion",
                                               "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                               "combine_muscle_part_operations": ["total", "mean"]
                                               },

                               # "F surface": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Force musculaire sur les surfaces de contournement [N]", "select_muscle_RefFrame_output": "surface",
                               #               "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"]},

                               # "F via": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Force musculaire sur les via point [N]", "select_muscle_RefFrame_output": "via",
                               #           "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"]},

                               # "F origin direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the origin", "select_matrix_line": 0,
                               #                        "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                               #                        "combine_muscle_part_operations": ["mean"], "vect_dir": True},

                               # "F insertion direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the insertion", "select_muscle_RefFrame_output": "insertion",
                               #                           "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                               #                           "combine_muscle_part_operations": ["mean"], "vect_dir": True},
                               }


# Variables
FDK_VariableDictionary_fr = {"Abduction": {"VariablePath": "Output.Simulation_Outputs.AbductionAngle", "VariableDescription": "Angle d'abduction [°]"},

                             "ContactArea": {"VariablePath": "Output.Simulation_Outputs.ContactArea", "VariableDescription": r'Surface de contact [$cm^2$]', "MultiplyFactor": 10000},

                             # test
                             "ForceMeasure Infraspinatus": {"VariablePath": "Output.Simulation_Outputs.ContactForce_humerus", "VariableDescription": 'Force [N]', "SequenceComposantes": ["AP", "IS", "ML"], "MultiplyFactor": 3},
                             "ForceMeasure Supraspinatus": {"VariablePath": "Output.Simulation_Outputs.ContactForce_humerus", "VariableDescription": 'Force [N]', "SequenceComposantes": ["AP", "IS", "ML"], "MultiplyFactor": 2},
                             "ForceMeasure Subscapularis": {"VariablePath": "Output.Simulation_Outputs.ContactForce_humerus", "VariableDescription": 'Force [N]', "SequenceComposantes": ["AP", "IS", "ML"], "MultiplyFactor": -3},
                             "ForceMeasure Deltoid anterior": {"VariablePath": "Output.Simulation_Outputs.ContactForce_humerus", "VariableDescription": 'Force [N]', "SequenceComposantes": ["AP", "IS", "ML"], "MultiplyFactor": 2},
                             "ForceMeasure Deltoid posterior": {"VariablePath": "Output.Simulation_Outputs.ContactForce_humerus", "VariableDescription": 'Force [N]', "SequenceComposantes": ["AP", "IS", "ML"], "MultiplyFactor": -1},
                             "ForceMeasure Deltoid lateral": {"VariablePath": "Output.Simulation_Outputs.ContactForce_humerus", "VariableDescription": 'Force [N]', "SequenceComposantes": ["AP", "IS", "ML"], "MultiplyFactor": 1},

                             "Time": {"VariablePath": "Output.Abscissa.t", "VariableDescription": "Temps"},

                             "MaxPenetration": {"VariablePath": "Output.Simulation_Outputs.MaxPenetration", "VariableDescription": 'Pénétration maximale des implants [mm]', "MultiplyFactor": 1000},

                             # Position of the center of pressure on the glenoid implant
                             "COP": {"VariablePath": "Output.Simulation_Outputs.COP_glenoid", "VariableDescription": "Centre de pression [mm]", "MultiplyFactor": 1000,
                                     "SequenceComposantes": ["AP", "IS", "ML"],
                                     # Offset in mediolateral so that the center of the glenoid implant surface corresponds to (0,0,0) (24.5 for the GleneCeraver_T3)
                                     "offset": [0, 0, -24.5]},

                             # Dans le repère de l'humérus ISB (pour comparaison avec bergmann et al.)
                             "ContactForce humerus": {"VariablePath": "Output.Simulation_Outputs.ContactForce_humerus", "VariableDescription": "Force de contact sur l'implant huméral [N]",
                                                      "SequenceComposantes": ["AP", "IS", "ML"]},

                             # Force sur l'humerus Dans le repère de l'implant glénoïdien
                             # Compression = force positive
                             "ContactForce glenoid": {"VariablePath": "Output.Simulation_Outputs.ContactForce_GlenImplant", "VariableDescription": "Force de contact sur l'implant glénoïdien [N]",
                                                      "SequenceComposantes": ["AP", "IS", "ML"], "Composantes_Inverse_Direction": [False, False, True]},

                             "ForceDepKinError": {"VariablePath": "Output.Simulation_Outputs.ForceDepKinError", "VariableDescription": "FDK Error [N]"}
                             }


FDK_Variables_fr = define_variables_to_load(FDK_VariableDictionary_fr, MuscleDictionary_fr, MuscleVariableDictionary_fr, FDK_ConstantsDictionary)


# %% Calculs supplémentaires


def additional_calculations(Results, fr=False):

    def instability_ratio(Results, fr=False):
        """Function that calculates the instability ratio for each simulation case
        IR = √(F_AP²,F_IS²)/|Fz|
        """

        for case in Results:
            Results[case]["ContactForce glenoid"]["Shear"] = np.sqrt((Results[case]["ContactForce glenoid"]["IS"])**2 + (Results[case]["ContactForce glenoid"]["AP"])**2)

            if fr:
                Results[case]["Instability Ratio"] = {"Description": "Ratio d'instabilité", "SequenceComposantes": ["Total"]}
            else:
                Results[case]["Instability Ratio"] = {"Description": "Instability ratio", "SequenceComposantes": ["Total"]}

            Results[case]["Instability Ratio"]["Total"] = Results[case]["ContactForce glenoid"]["Shear"] / abs(Results[case]["ContactForce glenoid"]["ML"])

        return Results

    def score(Results, fr=False):

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

    def delt_lateral_angle(Results, fr=False):
        """Calculates the direction of the deltoid lateral force on its origin and insertion in the scapula reference frame"""

        if fr:
            muscle_name = "Deltoid latéral"
            description = "Angle de la force musuclaire[°]"
        else:
            muscle_name = "Deltoid lateral"
            description = "Muscle force angle [°]"

        for case_name, case_data in Results.items():
            delt_direction_IS_origin = case_data["Muscles"][muscle_name][muscle_name]["F origin"]["Total_IS"]
            delt_direction_ML_origin = case_data["Muscles"][muscle_name][muscle_name]["F origin"]["Total_ML"]

            # Angle par rapport à la verticale
            force_angle_origin = np.arctan2(delt_direction_IS_origin, delt_direction_ML_origin) * 180 / np.pi

            delt_direction_IS_insertion = case_data["Muscles"][muscle_name][muscle_name]["F insertion"]["Total_IS"]
            delt_direction_ML_insertion = case_data["Muscles"][muscle_name][muscle_name]["F insertion"]["Total_ML"]

            # Angle par rapport à la verticale
            force_angle_insertion = np.arctan2(delt_direction_IS_insertion, delt_direction_ML_insertion) * 180 / np.pi

            case_data["Muscles"][muscle_name][muscle_name]["Force Angle"] = {"Description": description,
                                                                             "SequenceComposantes": ["Insertion", "Origin"],
                                                                             "Origin": force_angle_origin,
                                                                             "Insertion": force_angle_insertion
                                                                             }
        return Results

    Results = delt_lateral_angle(Results, fr)
    Results = instability_ratio(Results, fr)
    Results, scores_moment, scores_shear = score(Results, fr)

    return Results, scores_moment, scores_shear


# %% Nom des cas de simulation

xDownCases_5 = ["xdown-xshort", "xdown-short", "xdown-normal", "xdown-long", "xdown-xlong"]
DownCases_5 = ["down-xshort", "down-short", "down-normal", "down-long", "down-xlong"]
MiddleCases_5 = ["middle-xshort", "middle-short", "middle-normal", "middle-long", "middle-xlong"]
NeutralCases_5 = ["neutral-xshort", "neutral-short", "neutral-normal", "neutral-long", "neutral-xlong"]
UpCases_5 = ["up-xshort", "up-short", "up-normal", "up-long", "up-xlong"]
xUpCases_5 = ["xup-xshort", "xup-short", "xup-normal", "xup-long", "xup-xlong"]

CaseNames_6 = [*xDownCases_5, *DownCases_5, *NeutralCases_5, *MiddleCases_5, *UpCases_5, *xUpCases_5]

# %%                                                Résultats aTSA

# # pour tests
# aTSA_dir = "../Result Files/aTSA"
# Casetest = ["middle-normal"]
# files = ["PJ178_Anybody_aTSA_" + CaseName for CaseName in Casetest]
# aa = load_simulation_cases(aTSA_dir, files, Casetest, FDK_Variables)


aTSA_dir = "../Result Files/aTSA"
files = ["PJ178_Anybody_aTSA_" + CaseName for CaseName in CaseNames_6]

Results_aTSA = load_simulation_cases(aTSA_dir, files, CaseNames_6, FDK_Variables)
Results_aTSA, scores_moment, scores_shear = additional_calculations(Results_aTSA)

# Résultats en français
Results_aTSA_fr = load_simulation_cases(aTSA_dir, files, CaseNames_6, FDK_Variables_fr)
Results_aTSA_fr, scores_moment, scores_shear = additional_calculations(Results_aTSA_fr, fr=True)

# Sauvegarde des scores et des résultats en .pkl
save_results_to_file(scores_moment, SaveSimulationsDirectory, "scores_moment")
save_results_to_file(scores_shear, SaveSimulationsDirectory, "scores_shear")
save_results_to_file(Results_aTSA, SaveSimulationsDirectory, "Results_aTSA")
save_results_to_file(Results_aTSA_fr, SaveSimulationsDirectory, "Results_aTSA_fr")

# %%                                                Résultats Ball and Socket

# BalAndSocket_Cases = ["xshort", "short", "normal", "long", "xlong"]

# BallAndSocket_dir = "../Result Files/BallAndSocket"
# BallAndSocket_Files = [f"PJ178_Anybody_BallAndSocket_{CaseName}" for CaseName in BalAndSocket_Cases]

# Results_BallAndSocket = load_simulation_cases(BallAndSocket_dir, BallAndSocket_Files, BalAndSocket_Cases, BallAndSocket_Variables)

# # Sauvegarde de la simulation en .pkl
# save_results_to_file(Results_BallAndSocket, SaveSimulationsDirectory, "Results_BallAndSocket")

# %% chargement données littérature depuis excel

Results_literature = load_literature_data("data_literature", "")
save_results_to_file(Results_literature, SaveSimulationsDirectory, "Results_literature")
