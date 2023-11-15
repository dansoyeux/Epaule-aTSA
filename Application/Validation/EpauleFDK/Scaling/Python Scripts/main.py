# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:42:02 2023

@author: dan
File used to create the morphing points and grid and to scale the acromion and clavicula
"""

import numpy as np

import PickedPoints2AnybodyScaling as pp

Offset = {}
AddPoint = {}

# Points to add in the morphing points
AddPoint["PointNames"] = ["gh",
                          "Origin",
                          "acj",
                          "deltoideus lateral 1 org",
                          "deltoideus lateral 2 org",
                          "deltoideus lateral 3 org",
                          "deltoideus lateral 4 org",
                          "deltoideus posterior 1 org",
                          "deltoideus posterior 2 org",
                          "deltoideus posterior 3 org",
                          "deltoideus posterior 4 org",
                          "brachi_longum_org"]

AddPoint["Coordinates"] = np.array([[0.023398, -0.050863, -0.034381],  # gh
                                    [0.0, 0.0, 0.0],  # origin
                                    [0.006071, -0.003599, -0.030331],  # acj
                                    [0.02856498, -0.01142701, -0.001132002],  # lateral org 1
                                    [0.03856498, -0.008426996, -0.014132],  # lateral org 2
                                    [0.04056498, -0.008426984, -0.03313199],  # lateral org 3
                                    [0.03714399, -0.006523975, -0.04578298],  # lateral org 4
                                    [-0.08196395, -0.01098702, 0.01323703],  # posterior org 1
                                    [-0.03696398, -0.007987012, 0.009237012],  # posterior org 2
                                    [-0.01196399, -0.007987012, 0.009237004],  # posterior org 3
                                    [0.01503599, -0.01398702, 0.009236999],  # posterior org 4
                                    [-0.01799998, -0.024529, -0.02424197]  # brachi longum org

                                    ])

# Points of the scapula to offset
Offset["OffsetPoints"] = [
    'AcrEnd',
    # 'acj',
    # 'AcrInf_1',
    # 'AcrInf_2',
    # 'AcrInf_3',

    # 'AcrMed',
    # 'AcrMed_1',
    # 'AcrMed_2',


    'AcrPost',
    'AcrPost_1',


    'AcrLat',
    'AcrLat_1',
    'Acr1_1',
    'Acr1_2',

    # Muscles insertions in the scapula
    "deltoideus lateral 1 org",
    "deltoideus lateral 2 org",
    "deltoideus lateral 3 org",
    "deltoideus lateral 4 org",
    "deltoideus posterior 4 org",
    # "deltoideus posterior 1 org",
    # "deltoideus posterior 2 org",
    # "deltoideus posterior 3 org",
    # "brachi_longum_org",




    # 'Acr2_1',
    # 'Acr2_2',

    # 'Origin',
    # 'gh',





    # 'Spine1',
    # 'Spine2',
    # 'TS1',
    # 'TS2',
    # 'AS',
    # 'AI',
    # 'TubIG',
    # 'Lat1_1',
    # 'Lat1_2',
    # 'Lat2_1',
    # 'Lat2_2',
    # 'Med1_1',
    # 'Med1_2',
    # 'Med2_1',
    # 'Med2_2',
    # 'Col',
    # 'Notch',
    # 'CorAnt1_1',
    # 'CorAnt1_2',
    # 'CorAnt2_1',
    # 'CorAnt2_2',
    # 'CorAnt3_1',
    # 'CorAnt3_2',
    # 'CorAnt4_1',
    # 'CorAnt4_2',
    # 'CorMed1',
    # 'CorMed2',
    # 'CorMed3',
    # 'CorMed3_1',
    # 'CorMed4',
    # 'Fosse',
    # 'GlenS',
    # 'GlenI',
    # 'GlenI_up',
    # 'GlenP',
    # 'GlenA',
    # 'GlenC',
    # 'GlenAS',
    # 'GlenSP',
    # 'GlenIP',
    # 'GlenIA',
    # 'GlenIA_1',
    # 'Spine3',
    # 'Spine4',
    # 'Spine5',
    # 'Spine6',
    # 'Spine7',
    # 'BordSup1',
    # 'BordSup2',
    # 'BordSup3',
    # 'BordSup4',
    # 'CorGlen',
    # 'CorD_C'
]

Offset["OffsetName"] = "Main.AcromionScaling.AcromionOffset"

Offset["OffsetFactor"] = np.array([1, 0, 0])

# Picked points file
dataPath = "../Scapula/scapula_generique_picked_points.pp"


PickedPointsSource, PickedPointsTarget = pp.PickedPoints2AnyPoints(dataPath, Offset, AddPoint)

# Generate a grid of points
Grid = pp.PointGridAnybody(-0.16, 0.05, -0.14, 0.018, -0.09, 0.013, 10, 10, 10)
