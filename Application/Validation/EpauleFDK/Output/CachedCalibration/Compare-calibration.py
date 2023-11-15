# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:55:11 2023

@author: Dan
"""


def get_slack_length_from_anyset(file_name):
    """
    gets the slack length from a .anyset filed with saved calibration results

    file_name : string : name of the .anyset file
              : without the .anyset extension in the name

    """

    import numpy as np

    f = open(f"{file_name}.anyset", "r")
    text = f.read()

    text = text.split(";")
    del text[-1]
    muscles_array = np.zeros_like(text)
    slack_lengths = np.zeros_like(text, dtype=float)

    for lin in range(len(slack_lengths)):
        slack_lengths[lin] = float(text[lin].split(" = ")[1])
        muscles_array[lin] = text[lin].split(".")[-3]

    return muscles_array, slack_lengths


middle_normal = get_slack_length_from_anyset("CachedCalibrationResults-middle-normal")
xup_normal = get_slack_length_from_anyset("CachedCalibrationResults-xup-normal")

diff = middle_normal[1] - xup_normal[1]

max_diff = max(diff)
