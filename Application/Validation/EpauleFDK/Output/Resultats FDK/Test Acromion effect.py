# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:32:05 2024

@author: Dan
"""
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

length = [-6.6,
          -7.6,
          -8.6,
          -9.6,
          -10.6,
          -11.6,
          -12.6,
          -13.6,
          -14.6,
          
          
          -5.6,
          -4.6,
          -3.6,
          -2.6,
          -1.6,
          -0.6
          ]

MuscleDictionary = {"Deltoid lateral": ["deltoideus_lateral", "_part_", [1, 4]]}

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

VariableDictionary = {"Abduction": {"VariablePath": "Output.rotD", "VariableDescription": "Abduction angle [°]"},
                      }


MuscleVariableDictionary = {"F origin direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the origin", "select_matrix_line": 0,
                                                   "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                                   "combine_muscle_part_operations": ["mean"], "vect_dir": True},

                            "F insertion direction": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Direction of the muscle force at the insertion", "select_muscle_RefFrame_output": "insertion",
                                                      "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                                                      "combine_muscle_part_operations": ["mean"], "vect_dir": True},

                            "MomentArm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "MomentArm", "VariableDescription": "Moment arm [mm]",
                                          "combine_muscle_part_operations": ["mean"], "MultiplyFactor": 1000}
                            }

Variables = define_variables_to_load(VariableDictionary=VariableDictionary, MuscleDictionary=MuscleDictionary, MuscleVariableDictionary=MuscleVariableDictionary, ConstantsDictionary=FDK_ConstantsDictionary)

dir_name = "../SaveData/Acromion_shortening_effect"
Files = []
case_names = []
for index in range(len(length)):
    Files.append(f"04-01-neutral-short-GlenoidAxisTilt-MR_Polynomial_{index}")

list_length = list(map(str, length))

Results = load_simulation_cases(dir_name, Files, list_length, Variables)

for case_name, case_data in Results.items():
    delt_direction_IS_origin = case_data["Muscles"]["Deltoid lateral"]["Deltoid lateral"]["F origin direction"]["IS"]
    delt_direction_ML_origin = case_data["Muscles"]["Deltoid lateral"]["Deltoid lateral"]["F origin direction"]["ML"]

    # Angle par rapport à la verticale
    force_angle_origin = np.arctan2(delt_direction_IS_origin, delt_direction_ML_origin) * 180 / np.pi

    delt_direction_IS_insertion = case_data["Muscles"]["Deltoid lateral"]["Deltoid lateral"]["F insertion direction"]["IS"]
    delt_direction_ML_insertion = case_data["Muscles"]["Deltoid lateral"]["Deltoid lateral"]["F insertion direction"]["ML"]

    # Angle par rapport à la verticale
    force_angle_insertion = np.arctan2(delt_direction_IS_insertion, delt_direction_ML_insertion) * 180 / np.pi

    case_data["Muscles"]["Deltoid lateral"]["Deltoid lateral"]["Force Angle"] = {"Description": "Muscle force angle [°]",
                                                                                 "SequenceComposantes": ["Insertion", "Origin"],
                                                                                 "Origin": force_angle_origin,
                                                                                 "Insertion": force_angle_insertion
                                                                                 }

from Anybody_Package.Anybody_LoadOutput.Tools import load_results_from_file

from Anybody_Package.Anybody_Graph.GraphFunctions import graph
from Anybody_Package.Anybody_Graph.GraphFunctions import COP_graph
from Anybody_Package.Anybody_Graph.GraphFunctions import muscle_graph
from Anybody_Package.Anybody_Graph.GraphFunctions import define_simulations_line_style
from Anybody_Package.Anybody_Graph.GraphFunctions import define_simulation_description
from Anybody_Package.Anybody_Graph.GraphFunctions import define_COP_contour

from Anybody_Package.Anybody_Graph import PremadeGraphs

from Anybody_Package.Anybody_LoadOutput.LoadLiterature import load_literature_data
from Anybody_Package.Anybody_LoadOutput.LoadOutput import combine_simulation_cases
from Anybody_Package.Anybody_LoadOutput.LoadOutput import sum_result_variables

from Anybody_Package.Anybody_LoadOutput.Tools import result_dictionary_to_excel

SimulationsLineStyleDictionary = {
    "-0.6": {"color": "#ff00cc", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-1.6": {"color": "#ee34d2", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-2.6": {"color": "#9c27b0", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-3.6": {"color": "#50bfe6", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-4.6": {"color": "#16d0cb", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-5.6": {"color": "#aaf0d1", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-6.6": {"color": "#66ff66", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-7.6": {"color": "#ccff00", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-8.6": {"color": "#ffff66", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-9.6": {"color": "#ffcc33", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-10.6": {"color": "#ff9933", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-11.6": {"color": "#ff9966", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-12.6": {"color": "#ff6037", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-13.6": {"color": "#fd5b78", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "-14.6": {"color": "#ff355e", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
}

define_simulations_line_style(SimulationsLineStyleDictionary)

Results = dict(sorted(Results.items()))

muscle_graph(Results, "Deltoid lateral", "Abduction", "Force Angle", figure_title="Angle", cases_on="all", composante_y=["Origin"], grid_y_step=2)
