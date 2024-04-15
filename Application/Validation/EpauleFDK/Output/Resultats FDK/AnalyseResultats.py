# import Anybody_LoadOutput.Tools as LoadOutputTools

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

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# %% taille des textes dans les graphiques

# Contrôle de la taille de la police globale
# matplotlib.rcParams.update({'font.size': 10})

# Contrôle des tailles de chaque partie partie du graphique
# Liste des paramètres que l'on peut changer :
# https://renenyffenegger.ch/notes/development/languages/Python/libraries/matplotlib/rcParams/list
# Default values available here : https://matplotlib.org/stable/users/explain/customizing.html


# Titre des cases des subplots (12)
matplotlib.rcParams.update({'axes.titlesize': 18})

# Titre du graphique (12)
matplotlib.rcParams.update({'figure.titlesize': 18})

# Nom des axes (10)
matplotlib.rcParams.update({'axes.labelsize': 16})

# Graduations des axes (10)
matplotlib.rcParams.update({'xtick.labelsize': 14})
matplotlib.rcParams.update({'ytick.labelsize': 14})

# Taille des graduations (3.5)
matplotlib.rcParams.update({'xtick.major.size': 6})
matplotlib.rcParams.update({'ytick.major.size': 6})

# Légende (10)
matplotlib.rcParams.update({'legend.fontsize': 10})

# %% Setup des couleurs et légendes

# Définition des styles des simulations dans les graphiques (couleurs, forme de ligne taille...)
# Noms des couleurs : https://matplotlib.org/stable/gallery/color/named_colors.html
# Types de marqueurs : https://matplotlib.org/stable/api/markers_api.html
# Type de lignes : https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
SimulationsLineStyleDictionary = {
    # Glen xdown
    "xdown-xshort": {"color": "lightblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},
    "xdown-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "xdown-normal": {"color": "cornflowerblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "xdown-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "xdown-xlong": {"color": "midnightblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},

    # Glen down
    "down-xshort": {"color": "violet", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2.5},
    "down-short": {"color": "magenta", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "down-normal": {"color": "mediumorchid", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "down-long": {"color": "blueviolet", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "down-xlong": {"color": "purple", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2.5},

    # glen normal
    "middle-xshort": {"color": "lime", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "middle-short": {"color": "greenyellow", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 2.5},
    "middle-normal": {"color": "mediumseagreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "middle-long": {"color": "darkolivegreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "middle-xlong": {"color": "darkgreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 2},

    # glen neutral
    "neutral-xshort": {"color": "lightgray", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": None},
    "neutral-short": {"color": "lightgray", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 2.5},
    "neutral-normal": {"color": "grey", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "neutral-long": {"color": "black", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "neutral-xlong": {"color": "black", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},

    # Glen up
    "up-xshort": {"color": "yellow", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3},
    "up-short": {"color": "gold", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},
    "up-normal": {"color": "orange", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},
    "up-long": {"color": "salmon", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},
    "up-xlong": {"color": "orangered", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},

    # Glen xup
    "xup-xshort": {"color": "pink", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},
    "xup-short": {"color": "deeppink", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},
    "xup-normal": {"color": "red", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},
    "xup-long": {"color": "indianred", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},
    "xup-xlong": {"color": "darkred", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},

    # Type gh joint
    "FDK": {"color": "tab:blue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "FDK Full Range": {"color": "tab:red", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "Ball And Socket": {"color": "black", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},

    "Résultats": {"color": "darkorange"},

    # data de validation
    "Lauranne": {"color": 'hotpink'},
    "Marta": {"color": 'darkturquoise'},
    "Dal Maso superior": {"color": "black", "marker": "o", "markersize": 5, "linestyle": "-", "linewidth": 1},
    "Dal Maso inferior": {"color": "grey", "marker": "o", "markersize": 5, "linestyle": "-", "linewidth": 1},
    "Bergmann 2007": {"color": "black", "marker": "+", "markersize": 8, "linestyle": "-", "linewidth": 0.3},
    "Bergmann_2007": {"color": "black", "marker": "+", "markersize": 8, "linestyle": "-", "linewidth": 0.3},
    "Wickham": {"color": "darkorange", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3},

    "CSA=12°": {"color": 'violet', "linestyle": "--"},
    "CSA=16°": {"color": 'purple', "linestyle": "--"},
    "CSA=20°": {"color": 'lightblue', "linestyle": "--"},
    "CSA=25°": {"color": 'cornflowerblue', "linestyle": "--"},
    "CSA=30°": {"color": 'greenyellow', "linestyle": "-"},
    "CSA=35°": {"color": 'mediumseagreen', "linestyle": "-"},
    "CSA=40°": {"color": 'orange', "linestyle": "-."},
    "CSA=45°": {"color": 'red', "linestyle": "-."},
    "CSA=50°": {"color": 'darkred', "linestyle": "-."}

}

SimulationsLineStyleDictionary_Small_abduction = {
    # Glen xdown
    "xdown-xshort": {"color": "lightblue", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},
    "xdown-short": {"color": "deepskyblue", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": None},
    "xdown-normal": {"color": "cornflowerblue", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": None},
    "xdown-long": {"color": "mediumblue", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": None},
    "xdown-xlong": {"color": "midnightblue", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2},

    # Glen down
    "down-xshort": {"color": "violet", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2.5},
    "down-short": {"color": "magenta", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": None},
    "down-normal": {"color": "mediumorchid", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": None},
    "down-long": {"color": "blueviolet", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": None},
    "down-xlong": {"color": "purple", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-.", "linewidth": 2.5},

    # glen normal
    "middle-xshort": {"color": "lime", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-", "linewidth": None},
    "middle-short": {"color": "greenyellow", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-", "linewidth": 2.5},
    "middle-normal": {"color": "mediumseagreen", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-", "linewidth": None},
    "middle-long": {"color": "darkolivegreen", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-", "linewidth": None},
    "middle-xlong": {"color": "darkgreen", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "-", "linewidth": 2},

    # Glen up
    "up-xshort": {"color": "yellow", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "--", "linewidth": 3},
    "up-short": {"color": "gold", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "--", "linewidth": 2},
    "up-normal": {"color": "orange", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "--", "linewidth": 2},
    "up-long": {"color": "salmon", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "--", "linewidth": 2},
    "up-xlong": {"color": "orangered", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "--", "linewidth": 2},

    # Glen xup
    "xup-xshort": {"color": "pink", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "--", "linewidth": 2},
    "xup-short": {"color": "deeppink", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "--", "linewidth": 2},
    "xup-normal": {"color": "red", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "--", "linewidth": 2},
    "xup-long": {"color": "indianred", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "--", "linewidth": 2},
    "xup-xlong": {"color": "darkred", "marker": "+", "markersize": 10, "mew": 2.5, "linestyle": "--", "linewidth": 2},

    # Type gh joint
    "FDK": {"color": "tab:blue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "FDK Full Range": {"color": "tab:red", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "Ball And Socket": {"color": "black", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},

    "Résultats": {"color": "darkorange"},

    # data de validation
    "Lauranne": {"color": 'hotpink'},
    "Marta": {"color": 'darkturquoise'},
    "Dal Maso supérieur": {"color": "black", "marker": "o", "markersize": 5, "linestyle": "-", "linewidth": 1},
    "Dal Maso inférieur": {"color": "grey", "marker": "o", "markersize": 5, "linestyle": "-", "linewidth": 1},
    "Bergmann 2007": {"color": "black", "marker": "o", "markersize": 8, "linestyle": "-", "linewidth": 0.3},
    "Bergmann_2007": {"color": "black", "marker": "o", "markersize": 8, "linestyle": "-", "linewidth": 0.3},
    "Wickham": {"color": "darkorange", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3}
}


SimulationDescriptionDictionary = {
    # Nom des cas de simulation
    "xdown-xshort": "CSA = 12° : Large Downtilt      -  Very short acromion",
    "xdown-short": "CSA = 16° : Large Downtilt      -  Short acromion",
    "xdown-normal": "CSA = 20° : Large Downtilt      -  Normal acromion",
    "xdown-long": "CSA = 25° : Large Downtilt      -   Long acromion",
    "xdown-xlong": "CSA = 30° : Large Downtilt      -  Very long acromion",

    "down-xshort": "CSA = 16° : Downtilt             -  Very short acromion",
    "down-short": "CSA = 20° : Downtilt             -  Short acromion",
    "down-normal": "CSA = 25° : Downtilt             -  Normal acromion",
    "down-long": "CSA = 30° : Downtilt             -   Long acromion",
    "down-xlong": "CSA = 35° : Downtilt             -  Very long acromion",

    "middle-xshort": "CSA = 20° : Normal tilt         -  Very short acromion",
    "middle-short": "CSA = 25° : Normal tilt         -  Short acromion",
    "middle-normal": "CSA = 30° : Normal tilt         -  Normal acromion",
    "middle-long": "CSA = 35° : Normal tilt         -   Long acromion",
    "middle-xlong": "CSA = 40° : Normal tilt         -  Very long acromion",

    "neutral-xshort": "CSA = 20° : Neutral tilt         -  Very short acromion",
    "neutral-short": "CSA = 25° : Neutral tilt         -  Short acromion",
    "neutral-normal": "CSA = 30° : Neutral tilt         -  Normal acromion",
    "neutral-long": "CSA = 35° : Neutral tilt         -   Long acromion",
    "neutral-xlong": "CSA = 40° : Neutral tilt         -  Very long acromion",

    "up-xshort": "CSA = 25° : Uptilt             -  Very short acromion",
    "up-short": "CSA = 30° : Uptilt             -  Short acromion",
    "up-normal": "CSA = 35° : Uptilt             -  Normal acromion",
    "up-long": "CSA = 40° : Uptilt             -   Long acromion",
    "up-xlong": "CSA = 45° : Uptilt             -  Very long acromion",

    "xup-xshort": "CSA = 30° : Large uptilt      -  Very short acromion",
    "xup-short": "CSA = 35° : Large uptilt      -  Short acromion",
    "xup-normal": "CSA = 40° : Large uptilt      -  Normal acromion",
    "xup-long": "CSA = 45° : Large uptilt      -   Long acromion",
    "xup-xlong": "CSA = 50° : Large uptilt      -  Very long acromion",

    # Nom des composantes
    "AP": "Axe antéropostérieur (Anterior = +)",
    "IS": "Axe inférosupérieur (Superior = +)",
    "ML": "Axe médiolatéral (Lateral = +)",

    # Nom des datas de validation
    "Wickham": "Wickham et al. 2010, n=24",
    "Bergmann_2007": "Bergmann et al. 2007",
    "Bergmann_2011": "Bergmann et al. 2011",

    # Description des CSA moyens
    "CSA=12°": "CSA=12° (1 case)",
    "CSA=16°": "CSA=16° (2 cases)",
    "CSA=20°": "CSA=20° (3 cases)",
    "CSA=25°": "CSA=25° (4 cases)",
    "CSA=30°": "CSA=30° (5 cases)",
    "CSA=35°": "CSA=35° (4 cases)",
    "CSA=40°": "CSA=40° (3 cases)",
    "CSA=45°": "CSA=45° (2 cases)",
    "CSA=50°": "CSA=50° (1 case)"

}

# Fonctions pour définir les légendes et styles des graphiques en fonction des noms des simulations dans les dictionnaires
define_simulations_line_style(SimulationsLineStyleDictionary)
define_simulation_description(SimulationDescriptionDictionary)

# Fonction pour définir le contour qui sera dessiné par la fonction COP_graph
# GleneContour.pp contient la moitié droite de l'implant
COP_contour = define_COP_contour("GleneContour", "pp")

# ajoute les points de la partie gauche par symétrie de la partie droite
COP_contour_sym = COP_contour.copy()[::-1]
COP_contour_sym[:, 0] = COP_contour_sym[:, 0] * -1
COP_contour = np.concatenate((COP_contour, COP_contour_sym))

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


# %% Catégories de simulation

# With xdown, middle, xup
CasesVariables_3 = {"Tilt": {"Large Downtilt": xDownCases_3, "Normal tilt": MiddleCases_3, "Large Uptilt": xUpCases_3},
                    "Acromion": {"Very short acromion": xShortCases_3, "Normal acromion": NormalCases_3, "Very long acromion": xLongCases_3}}

CasesVariables_36 = {"Tilt": {"Large Downtilt": xDownCases_3, "Neutral tilt": NeutralCases_3, "Uptilt": UpCases_3},
                     "Acromion": {"Very short acromion": xShortCases_36, "Normal acromion": NormalCases_36, "Very long acromion": xLongCases_36}}

# With xdown, middle, xup
CasesVariables_5 = {"Tilt": {"Large Downtilt": xDownCases_5, "Downtilt": DownCases_5, "Normal tilt": MiddleCases_5, "Uptilt": UpCases_5, "Large Uptilt": xUpCases_5},
                    "Acromion": {"Very short acromion": xShortCases_5, "Short acromion": ShortCases_5, "Normal acromion": NormalCases_5, " Long acromion": LongCases_5, "Very long acromion": xLongCases_5}}

# With xdown, middle, xup
CasesVariables_6 = {"Tilt": {"Large Downtilt": xDownCases_5, "Downtilt": DownCases_5, "Neutral tilt": NeutralCases_5, "Normal tilt": MiddleCases_5, "Uptilt": UpCases_5, "Large Uptilt": xUpCases_5},
                    "Acromion": {"Very short acromion": xShortCases_6, "Short acromion": ShortCases_6, "Normal acromion": NormalCases_6, " Long acromion": LongCases_6, "Very long acromion": xLongCases_6}}

# Tilt
CasesVariables_Tilt_5_Acromion_3 = {"Tilt": {"Large Downtilt": xDownCases_3, "Downtilt": DownCases_3, "Normal tilt": MiddleCases_3, "Uptilt": UpCases_3, "Large Uptilt": xUpCases_3}}
CasesVariables_Tilt_5_Acromion_5 = {"Tilt": {"Large Downtilt": xDownCases_5, "Downtilt": DownCases_5, "Normal tilt": MiddleCases_5, "Uptilt": UpCases_5, "Large Uptilt": xUpCases_5}}

CasesVariables_Tilt_3_Acromion_3 = {"Tilt": {"Large Downtilt": xDownCases_3, "Normal tilt": MiddleCases_3, "Large Uptilt": xUpCases_3}}
CasesVariables_Tilt_3_Acromion_5 = {"Tilt": {"Large Downtilt": xDownCases_5, "Normal tilt": MiddleCases_5, "Large Uptilt": xUpCases_5}}

# Acromion
CasesVariables_Acromion_5_Tilt_3 = {"Acromion": {"Very short acromion": xShortCases_3, "Short acromion": ShortCases_3, "Normal acromion": NormalCases_3, " Long acromion": LongCases_3, "Very long acromion": xLongCases_3}}
CasesVariables_Acromion_5_Tilt_5 = {"Acromion": {"Very short acromion": xShortCases_5, "Short acromion": ShortCases_5, "Normal acromion": NormalCases_5, " Long acromion": LongCases_5, "Very long acromion": xLongCases_5}}

CasesVariables_Acromion_3_Tilt_3 = {"Acromion": {"Very short acromion": xShortCases_3, "Normal acromion": NormalCases_3, "Very long acromion": xLongCases_3}}
CasesVariables_Acromion_3_Tilt_5 = {"Acromion": {"Very short acromion": xShortCases_5, "Normal acromion": NormalCases_5, "Very long acromion": xLongCases_5}}

# CSA
CasesVariables_CSA_9 = {"CSA Faible": {"CSA = 12°": CSA_12_Cases, "CSA = 16°": CSA_16_Cases, "CSA = 20°": CSA_20_Cases},
                        "CSA Moyen": {"CSA = 25°": CSA_25_Cases, "CSA = 30°": CSA_30_Cases, "CSA = 35°": CSA_35_Cases},
                        "CSA Élevé": {"CSA = 40°": CSA_40_Cases, "CSA = 45°": CSA_45_Cases, "CSA = 50°": CSA_50_Cases}}

# Les 6 qui sont dans la range de CSA
CasesVariables_CSA_6 = {"CSA Moyen": {"CSA = 20°": CSA_20_Cases, "CSA = 25°": CSA_25_Cases, "CSA = 30°": CSA_30_Cases},
                        "CSA Élevé": {"CSA = 35°": CSA_35_Cases, "CSA = 40°": CSA_40_Cases, "CSA = 45°": CSA_45_Cases}
                        }
"""
Avec Bergmann
"""

# With xdown, middle, xup
CasesVariables_3_Bergmann = {"Tilt": {"Large Downtilt": [*xDownCases_3, "Bergmann_2007"], "Normal tilt": [*MiddleCases_3, "Bergmann_2007"], "Large Uptilt": [*xUpCases_3, "Bergmann_2007"]},
                             "Acromion": {"Very short acromion": [*xShortCases_3, "Bergmann_2007"], "Normal acromion": [*NormalCases_3, "Bergmann_2007"], "Very long acromion": [*xLongCases_3, "Bergmann_2007"]}}
# With xdown, middle, xup
CasesVariables_5_Bergmann = {"Tilt": {"Large Downtilt": [*xDownCases_5, "Bergmann_2007"], "Downtilt": [*DownCases_5, "Bergmann_2007"], "Normal tilt": [*MiddleCases_5, "Bergmann_2007"], "Uptilt": [*UpCases_5, "Bergmann_2007"], "Large Uptilt": [*xUpCases_5, "Bergmann_2007"]},
                             "Acromion": {"Very short acromion": [*xShortCases_5, "Bergmann_2007"], "Short acromion": [*ShortCases_5, "Bergmann_2007"], "Normal acromion": [*NormalCases_5, "Bergmann_2007"], " Long acromion": [*LongCases_5, "Bergmann_2007"], "Very long acromion": [*xLongCases_5, "Bergmann_2007"]}}
# With xdown, middle, xup
CasesVariables_3_Wickham = {"Tilt": {"Large Downtilt": [*xDownCases_3, "Wickham"], "Normal tilt": [*MiddleCases_3, "Wickham"], "Large Uptilt": [*xUpCases_3, "Wickham"]},
                            "Acromion": {"Very short acromion": [*xShortCases_3, "Wickham"], "Normal acromion": [*NormalCases_3, "Wickham"], "Very long acromion": [*xLongCases_3, "Wickham"]}}
# With xdown, middle, xup
CasesVariables_5_Wickham = {"Tilt": {"Large Downtilt": [*xDownCases_5, "Wickham"], "Downtilt": [*DownCases_5, "Wickham"], "Normal tilt": [*MiddleCases_5, "Wickham"], "Uptilt": [*UpCases_5, "Wickham"], "Large Uptilt": [*xUpCases_5, "Wickham"]},
                            "Acromion": {"Very short acromion": [*xShortCases_5, "Wickham"], "Short acromion": [*ShortCases_5, "Wickham"], "Normal acromion": [*NormalCases_5, "Wickham"], " Long acromion": [*LongCases_5, "Wickham"], "Very long acromion": [*xLongCases_5, "Wickham"]}}

# With xdown, middle, xup
CasesVariables_3_Ball_And_Socket = {"Tilt": {"Large Downtilt": [*xDownCases_3, "Ball And Socket"], "Normal tilt": [*MiddleCases_3, "Ball And Socket"], "Large Uptilt": [*xUpCases_3, "Ball And Socket"]},
                                    "Acromion": {"Very short acromion": [*xShortCases_3, "Ball And Socket"], "Normal acromion": [*NormalCases_3, "Ball And Socket"], "Very long acromion": [*xLongCases_3, "Ball And Socket"]}}
# With xdown, middle, xup
CasesVariables_5_Ball_And_Socket = {"Tilt": {"Large Downtilt": [*xDownCases_5, "Ball And Socket"], "Downtilt": [*DownCases_5, "Ball And Socket"], "Normal tilt": [*MiddleCases_5, "Ball And Socket"], "Uptilt": [*UpCases_5, "Ball And Socket"], "Large Uptilt": [*xUpCases_5, "Ball And Socket"]},
                                    "Acromion": {"Very short acromion": [*xShortCases_5, "Ball And Socket"], "Short acromion": [*ShortCases_5, "Ball And Socket"], "Normal acromion": [*NormalCases_5, "Ball And Socket"], " Long acromion": [*LongCases_5, "Ball And Socket"], "Very long acromion": [*xLongCases_5, "Ball And Socket"]}}

# %%                                                Chargement des résultats FDK

# Chemin d'accès au dossier dans lequel les fichiers ont été sauvegardés
SaveSimulationsDirectory = "Saved Simulations"

Results_GlenoidLocalAxis_MR_Polynomial_Elevation = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_Elevation")

Results_GlenoidLocalAxis_MR_MinMaxStrict_Elevation_no_recentrage = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_MinMaxStrict_Elevation_no_recentrage")

Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage")

Results_GlenoidLocalAxis_MR_Polynomial_140deg_no_recentrage = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_140deg_no_recentrage")

moment_scores = load_results_from_file(SaveSimulationsDirectory, "moment_scores")
shear_scores = load_results_from_file(SaveSimulationsDirectory, "shear_scores")
moment_scores_36 = load_results_from_file(SaveSimulationsDirectory, "moment_scores_36")
shear_scores_36 = load_results_from_file(SaveSimulationsDirectory, "shear_scores_36")

# %%                                                Chargement des résultats BallAndSocket
Results_BallAndSocket = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket")

# Results_BallAndSocket_FullRange = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket_FullRange")

# études de muscle recruitment ball and socket
Results_BallAndSocket_Muscle_Recruitment = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket_MuscleRecruitmentStudy")

# Results_BallAndSocket_NewAMMR = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket_NewAMMR")

# Results_BallAndSocket_FullRange = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket_FullRange")
Results_literature = load_results_from_file(SaveSimulationsDirectory, "Results_literature")


# %% Chargement autres variables
# Chargement des dictionnaires de variable
SaveVariablesDirectory = "Saved VariablesDictionary"
FDK_Variables = load_results_from_file(SaveVariablesDirectory, "FDK_Variables")

# %% Liste des catégories de muscles

# 9 muscles --> graphique 3x3
Muscles_Main = ["Deltoideus anterior",
                "Deltoideus lateral",
                "Deltoideus posterior",
                "Lower trapezius",
                "Middle trapezius",
                "Upper trapezius",
                "Rhomboideus",
                "Supraspinatus",
                "Serratus anterior"
                ]

# 9 muscles --> graphique 3x3
# {"Nom_Muscle": composante_y}
Muscles_Aux = ["Pectoralis major clavicular",
               "Pectoralis major sternal",
               "Pectoralis minor",
               "Subscapularis",
               "Teres major",
               "Teres minor",
               "Infraspinatus",
               "Biceps brachii long head",
               "Biceps brachii short head",
               ]

# 6 muscles --> graphique 2x3
Muscles_Extra = ["Sternocleidomastoid sternum",
                 "Sternocleidomastoid clavicular",
                 "Latissimus dorsi",
                 "Levator scapulae",
                 "Coracobrachialis",
                 "Triceps long head",
                 ]


# Muscles qui varient
Muscles_Variation = ["Deltoideus anterior",
                     "Deltoideus lateral",
                     "Deltoideus posterior",
                     "Triceps long head"
                     ]

# Muscles for comparison with Wickham et al. data
# 3x3
Muscle_Comp_Main = ["Deltoideus anterior",
                    "Deltoideus lateral",
                    "Deltoideus posterior",
                    "Lower trapezius",
                    "Middle trapezius",
                    "Upper trapezius",
                    "Rhomboideus",
                    "Supraspinatus",
                    "Serratus anterior"
                    ]

# 2x3
Muscle_Comp_Aux = ["Pectoralis major",
                   "Pectoralis minor",
                   "Upper Subscapularis",
                   "Downward Subscapularis",
                   "Infraspinatus",
                   "Latissimus dorsi"
                   ]


# Muscles qui varient
Muscles_Comp_Variation = ["Deltoideus anterior",
                          "Deltoideus lateral",
                          "Deltoideus posterior"
                          ]

AllMuscles_List = list(FDK_Variables["Muscles"].keys())

Muscles_actifs = ["Deltoideus lateral",
                  "Deltoideus anterior",
                  "Deltoideus posterior",
                  "Subscapularis",
                  "Serratus anterior",
                  "Triceps long head",
                  "Lower trapezius",
                  "Middle trapezius",
                  "Upper trapezius",
                  "Infraspinatus",
                  "Supraspinatus",
                  "Rhomboideus"
                  ]

Muscles_inactifs = ["Pectoralis major clavicular",
                    "Pectoralis major sternal",
                    "Pectoralis minor",
                    "Teres major",
                    "Teres minor",
                    "Biceps brachii long head",
                    "Biceps brachii short head",
                    "Sternocleidomastoid sternum",
                    "Sternocleidomastoid clavicular",
                    "Latissimus dorsi",
                    "Levator scapulae",
                    "Coracobrachialis",
                    ]

Muscles_Comp_actifs = ["Deltoideus anterior",
                       "Deltoideus lateral",
                       "Deltoideus posterior",
                       "Lower trapezius",
                       "Middle trapezius",
                       "Upper trapezius",
                       "Rhomboideus",
                       "Supraspinatus",
                       "Serratus anterior",
                       "Downward Subscapularis",
                       "Upper Subscapularis",
                       "Infraspinatus"
                       ]

# 12 (Ft > 10 N)
list_muscles_actifs = ["Deltoideus lateral",
                       "Deltoideus anterior",
                       "Deltoideus posterior",
                       "Lower trapezius",
                       "Middle trapezius",
                       "Upper trapezius",
                       "Serratus anterior",
                       "Subscapularis",
                       "Triceps long head",
                       "Rhomboideus",
                       "Supraspinatus",
                       "Infraspinatus",
                       ]

# 3 (10 N > Ft > 5N)
list_muscles_peu_actif = ["Biceps brachii long head",
                          "Biceps brachii short head",
                          "Levator scapulae"
                          ]

# 9 (Ft < 5N)
list_muscles_inactifs = ["Pectoralis major clavicular",
                         "Pectoralis major sternal",
                         "Pectoralis minor",
                         "Teres major",
                         "Teres minor",
                         "Sternocleidomastoid sternum",
                         "Sternocleidomastoid clavicular",
                         "Latissimus dorsi",
                         "Coracobrachialis"
                         ]

# 7 (subscapulaire divisé en 2)
list_muscle_variation = ["Deltoideus anterior",
                         "Deltoideus lateral",
                         "Deltoideus posterior",
                         "Upper Subscapularis",
                         "Downward Subscapularis",
                         "Triceps long head",
                         "Infraspinatus"
                         ]

# 9
list_muscle_variation_faible = ["Pectoralis major clavicular",
                                "Levator scapulae",
                                "Serratus anterior",
                                "Lower trapezius",
                                "Upper trapezius",
                                "Supraspinatus",
                                "Rhomboideus",
                                "Biceps brachii short head",
                                "Coracobrachialis",
                                ]

# %% Forces totales sur la scapula et sur l'humérus

"""sur la scapula"""

# variables_to_add_scapula = {"ForceContact GlenImplant": ["Total", "AP", "IS", "ML"],
#                             "SpringForce scapula": ["Total", "AP", "IS", "ML"]
#                             }


# muscles_to_add_scapula_origin = ["Deltoideus lateral",
#                                  "Deltoideus posterior",
#                                  "Subscapularis",
#                                  "Infraspinatus",
#                                  "Supraspinatus",
#                                  "Triceps long head",
#                                  "Biceps brachii long head",
#                                  "Biceps brachii short head",
#                                  "Teres major",
#                                  "Teres minor",
#                                  "Coracobrachialis"
#                                  ]

# muscles_to_add_scapula_insertion = ["Levator scapulae",
#                                     "Serratus anterior",
#                                     "Lower trapezius",
#                                     "Middle trapezius",
#                                     "Rhomboideus",
#                                     "Pectoralis minor"
#                                     ]

# muscle_variables_to_add_scapula = {"F insertion": {"component_sum_order": ["Total", "Total_AP", "Total_IS", "Total_ML"],
#                                                    "muscles_to_add": muscles_to_add_scapula_insertion},
#                                    "F origin": {"component_sum_order": ["Total", "Total_AP", "Total_IS", "Total_ML"],
#                                                 "muscles_to_add": muscles_to_add_scapula_origin}
#                                    }

# Results_GlenoidLocalAxis_MR_Polynomial = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial, "FTotal scapula", ["Total", "AP", "IS", "ML"], "Force totale sur la scapula (glene) [N]", variables_to_add_scapula, muscle_variables_to_add_scapula)


"""sur l'humérus"""
# variables_to_add_humerus = {"ForceContact HumImplant glene": ["Total", "AP", "IS", "ML"],
#                             "SpringForce humerus": ["Total", "AP", "IS", "ML"]
#                             }

# muscles_to_add_humerus_insertion = ["Deltoideus lateral",
#                                     "Deltoideus posterior",
#                                     "Deltoideus anterior",
#                                     "Subscapularis",
#                                     "Infraspinatus",
#                                     "Supraspinatus",
#                                     "Pectoralis major clavicular",
#                                     "Pectoralis major sternal",
#                                     "Coracobrachialis",
#                                     "Teres major",
#                                     "Teres minor",
#                                     "Latissimus dorsi",
#                                     "Triceps long head",
#                                     ]

# muscle_variables_to_add_humerus = {"F insertion": {"component_sum_order": ["Total", "Total_AP", "Total_IS", "Total_ML"],
#                                                    "muscles_to_add": muscles_to_add_humerus_insertion}
#                                    }

# Results_GlenoidLocalAxis_MR_Polynomial = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial, "FTotal humerus", ["Total", "AP", "IS", "ML"], "Force totale sur l'humérus (glene)[N]", variables_to_add_humerus, muscle_variables_to_add_humerus)

"""Sans forces de contact"""
# variables_to_add_humerus_no_fcontact = {"SpringForce humerus": ["Total", "AP", "IS", "ML"]}

# Results_GlenoidLocalAxis_MR_Polynomial = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial, "FTotal humerus no Fcontact", ["Total", "AP", "IS", "ML"], "Force totale sur l'humérus no Fcontact (glene) [N]", variables_to_add_humerus_no_fcontact, muscle_variables_to_add_humerus)

"""Force totale muscles"""
# Results_GlenoidLocalAxis_MR_Polynomial = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial, "FTotal muscles", ["Total", "AP", "IS", "ML"], "Force totale des muscles sur l'humérus (glene) [N]", muscle_variables_to_add=muscle_variables_to_add_humerus)

"""Sans springforce"""
# variables_to_add_humerus_no_springforce = {"ForceContact humerus": ["Total", "AP", "IS", "ML"]}
# Results_GlenoidLocalAxis_MR_Polynomial = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial, "FTotal humerus no SpringForce", ["Total", "AP", "IS", "ML"], "Force totale sur l'humérus no SpringForce (glene) [N]", variables_to_add_humerus_no_springforce, muscle_variables_to_add_humerus)


# %% Moyenne par CSA

# result_dictionary = {key: result_dictionary[key] for key in CaseNames_3}
# combine_cases = {"CSA=12°": CSA_12_Cases,
#                   "CSA=16°": CSA_16_Cases,
#                   "CSA=20°": CSA_20_Cases,
#                   "CSA=25°": CSA_25_Cases,
#                   "CSA=30°": CSA_30_Cases,
#                   "CSA=35°": CSA_35_Cases,
#                   "CSA=40°": CSA_40_Cases,
#                   "CSA=45°": CSA_45_Cases,
#                   "CSA=50°": CSA_50_Cases
#                   }

# Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage_Par_CSA = combine_simulation_cases(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, combine_cases, "mean")
# Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage_Par_CSA = {**Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage_Par_CSA, **Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage}

list_csa_short = ["CSA=25°",
                  "CSA=30°",
                  "CSA=35°",
                  "CSA=40°"
                  ]

list_csa_long = ["CSA=20°",
                 "CSA=25°",
                 "CSA=30°",
                 "CSA=35°",
                 "CSA=40°",
                 "CSA=45°"
                 ]

# %% Save figures

# Parameters of the graphs
graph_parameters = {"xlim": [0, 120],
                    "legend_position": "center left",
                    "grid_x_step": 15,

                    # Catégories de muscles
                    "list_muscles_actifs": list_muscles_actifs,
                    "list_muscles_peu_actif": list_muscles_peu_actif,
                    "list_muscles_inactifs": list_muscles_inactifs,

                    # For graph by categories
                    "CasesCategories_5": CasesVariables_5,
                    "CasesCategories_3": CasesVariables_3,
                    "CaseNames_5": CaseNames_5,
                    "CaseNames_3": CaseNames_3,

                    # Pour moment arms
                    "muscle_list_by_categories": list_muscle_variation,

                    # Pour COP
                    "COP_contour": COP_contour
                    }

graph_parameters_3 = {"xlim": [0, 120],
                      "legend_position": "center left",
                      "grid_x_step": 15,

                      # Catégories de muscles
                      "list_muscles_actifs": list_muscles_actifs,
                      "list_muscles_peu_actif": list_muscles_peu_actif,
                      "list_muscles_inactifs": list_muscles_inactifs,

                      # For graph by categories
                      "CasesCategories_5": CasesVariables_3,
                      "CasesCategories_3": CasesVariables_3,
                      "CaseNames_5": CaseNames_3,
                      "CaseNames_3": CaseNames_3,

                      # Pour moment arms
                      "muscle_list_by_categories": list_muscle_variation,

                      # Pour COP
                      "COP_contour": COP_contour
                      }

# With neutral
graph_parameters_6 = {"xlim": [0, 120],
                      "legend_position": "center left",
                      "grid_x_step": 15,

                      # Catégories de muscles
                      "list_muscles_actifs": list_muscles_actifs,
                      "list_muscles_peu_actif": list_muscles_peu_actif,
                      "list_muscles_inactifs": list_muscles_inactifs,

                      # For graph by categories
                      "CasesCategories_5": CasesVariables_6,
                      "CasesCategories_3": CasesVariables_36,
                      "CaseNames_5": CaseNames_6,
                      "CaseNames_3": CaseNames_36,

                      # Pour moment arms
                      "muscle_list_by_categories": list_muscle_variation,

                      # Pour COP
                      "COP_contour": COP_contour
                      }

# Parameters of the graphs
graph_parameters_par_CSA = {"xlim": [0, 120],
                            "legend_position": "center left",
                            "grid_x_step": 15,

                            # Catégories de muscles
                            "list_muscles_actifs": list_muscles_actifs,
                            "list_muscles_peu_actif": list_muscles_peu_actif,
                            "list_muscles_inactifs": list_muscles_inactifs,

                            # For graph by categories
                            "CasesCategories_5": CasesVariables_CSA_9,
                            "CasesCategories_3": CasesVariables_CSA_6,
                            "CaseNames_5": list_csa_long,
                            "CaseNames_3": list_csa_short,

                            # Pour moment arms
                            "muscle_list_by_categories": list_muscle_variation,

                            # Pour COP
                            "COP_contour": COP_contour
                            }
"""Abduction (done)"""
# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_Polynomial, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Abduction", "Normal", save_graph=True, composante_on=False, **graph_parameters)
# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Abduction", "No recentrage", save_graph=True, composante_on=False, **graph_parameters)


"""Elevation (done)"""
# Recentrage
# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_Polynomial_Elevation, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Elevation", "Normal", save_graph=True, composante_on=False, **graph_parameters)

# # No recentrage
# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Elevation", "No recentrage", save_graph=True, composante_on=False, **graph_parameters)

# # Avec neutral
# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Elevation", "No recentrage with neutral", save_graph=True, composante_on=False, **graph_parameters_6)

"""Par CSA Elevation"""
# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage_Par_CSA, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Elevation/No recentrage", "Par CSA", save_graph=True, composante_on=False, **graph_parameters_par_CSA)

# %% 140 deg no recentrage

# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_140deg_no_recentrage, CasesVariables_3, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13])

# graph(Results_GlenoidLocalAxis_MR_Polynomial_140deg_no_recentrage, "Abduction", "ForceTolError", cases_on="all")

# %% Stability ratio

# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, CasesVariables_3, "Abduction", "ForceContact GlenImplant", composante_y=["Shear"], figure_title="Shear forces", xlim=[15, 120], same_lim=True)

# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, CasesVariables_3, "Abduction", "Instability Ratio", figure_title="Instability ratio", xlim=[15, 120], same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, CasesVariables_5, "Abduction", "Instability Ratio", figure_title="Instability ratio", xlim=[15, 120], same_lim=True, figsize=[24, 14])

# graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "Instability  Ratio", figure_title="Stability ratio", xlim=[15, 120], same_lim=True, figsize=[24, 14], cases_on=CaseNames_3)

# %% Figures article

"""Article"""

SimulationsLineStyleDictionary_article = {
    # Glen xdown
    "xdown-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 1.5},
    "xdown-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "xdown-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 1.5},
    "xdown-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "xdown-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},

    # Glen neutral
    "neutral-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 1.5},
    "neutral-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "neutral-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 1.5},
    "neutral-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "neutral-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},

    # Glen up
    "up-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 1.5},
    "up-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "up-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 1.5},
    "up-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "up-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},
}
define_simulations_line_style(SimulationsLineStyleDictionary_article)

Categories_Article = {"line": {"Downward inclination": ["xdown-xshort", "xdown-normal", "xdown-xlong"],
                               "Neutral inclination": ["neutral-xshort", "neutral-normal", "neutral-xlong"],
                               "Upward inclination": ["up-xshort", "up-normal", "up-xlong"]
                               }}

# # Article
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, Categories_Article, COP_contour, composantes=["AP", "IS"], graph_annotation_on=False, draw_COP_points_on=False, COP_first_point_size=10, COP_first_point_mew=2, xlim=[-17, 17], ylim=[-19, 22], grid_x_step=5, legend_position="lower center", hide_center_axis_labels=True)

# grid_steps_y = [50, 25, 50, 50]
# y_lims = {"Total": [0, 500],
#           "AP": [-50, 100],
#           "IS": [-150, 200],
#           "ML": [-500, 0]
#           }

# # Force de contact composante par compoasante
# for ind, composante in enumerate(["Total", "AP", "IS", "ML"]):
#     graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", figure_title=f"{composante}", subplot_title="Downtilt", composante_y=[composante], cases_on=["xdown-xshort", "xdown-normal", "xdown-xlong"], subplot={"dimension": [1, 3], "number": 1})
#     graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", figure_title=f"{composante}", subplot_title="Middle tilt", composante_y=[composante], cases_on=["neutral-xshort", "neutral-normal", "neutral-xlong"], subplot={"dimension": [1, 3], "number": 2})
#     graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", figure_title=f"{composante}", subplot_title="Uptilt", composante_y=[composante], cases_on=["xup-xshort", "xup-normal", "xup-xlong"], subplot={"dimension": [1, 3], "number": 3}, same_lim=True, grid_x_step=15, xlim=[15, 120], ylim=y_lims[composante], grid_y_step=grid_steps_y[ind])

# # Contact forces for neutral inclination
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", figure_title="Contact Forces on the glenoid implant, neutral inclination", subplot_title="Posterior-anterior shear", composante_y=["AP"], cases_on=["neutral-xshort", "neutral-normal", "neutral-xlong"], subplot={"dimension": [1, 3], "number": 1})
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", figure_title="Contact Forces on the glenoid implant, neutral inclination", subplot_title="Inferior-superior shear", composante_y=["IS"], cases_on=["neutral-xshort", "neutral-normal", "neutral-xlong"], subplot={"dimension": [1, 3], "number": 2})
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", figure_title="Contact Forces on the glenoid implant, neutral inclination", subplot_title="Compression force", composante_y=["ML"], cases_on=["neutral-xshort", "neutral-normal", "neutral-xlong"], subplot={"dimension": [1, 3], "number": 3}, same_lim=True, grid_x_step=15, xlim=[15, 120], grid_y_step=50, ylim=[-100, 400], hide_center_axis_labels=True)

# # Compression and shear, neutral inclination
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", figure_title="Contact Forces on the glenoid implant, neutral inclination", subplot_title="Shear forces", composante_y=["Shear"], cases_on=["neutral-xshort", "neutral-normal", "neutral-xlong"], subplot={"dimension": [1, 2], "number": 1})
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", figure_title="Contact Forces on the glenoid implant, neutral inclination", subplot_title="Compression forces", composante_y=["Compression"], cases_on=["neutral-xshort", "neutral-normal", "neutral-xlong"], subplot={"dimension": [1, 2], "number": 2}, same_lim=True, grid_x_step=15, xlim=[15, 120], grid_y_step=50)

# # instability ratio
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, Categories_Article, "Abduction", "Instability Ratio", figure_title="Instability ratio", grid_x_step=15, xlim=[15, 120], same_lim=True, legend_on=False, hide_center_axis_labels=True)

# %% Abstract

# SimulationsLineStyleDictionary_abstract = {
#     # Glen xdown
#     "xdown-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 3.5},
#     "xdown-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
#     "xdown-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3.5},
#     "xdown-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
#     "xdown-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 4.5},

#     # Glen xdown
#     "middle-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 3.5},
#     "middle-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
#     "middle-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3.5},
#     "middle-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
#     "middle-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 4.5},

#     # Glen xdown
#     "xup-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 3.5},
#     "xup-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
#     "xup-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3.5},
#     "xup-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
#     "xup-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 4.5},
# }

# define_simulations_line_style(SimulationsLineStyleDictionary_abstract)

# # Abstract
# COP_graph(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, COP_contour, figure_title="Downtilt", composantes=["AP", "IS"], cases_on=["xdown-xshort", "xdown-normal", "xdown-xlong"], graph_annotation_on=False, draw_COP_points_on=False, COP_first_point_size=20, COP_first_point_mew=4)
# COP_graph(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, COP_contour, figure_title="Uptilt", composantes=["AP", "IS"], cases_on=["xup-xshort", "xup-normal", "xup-xlong"], graph_annotation_on=False, draw_COP_points_on=False, COP_first_point_size=20, COP_first_point_mew=4)

# %% Présentations powerpoint

# SimulationsLineStyleDictionary_presentation = {
#     # Glen xdown
#     "xdown-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 3.5},
#     "xdown-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
#     "xdown-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3.5},
#     "xdown-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
#     "xdown-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 3},

#     # Glen xdown
#     "middle-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 3.5},
#     "middle-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
#     "middle-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3.5},
#     "middle-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
#     "middle-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 3},

#     # Glen xdown
#     "xup-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 3.5},
#     "xup-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
#     "xup-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3.5},
#     "xup-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
#     "xup-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 3},
# }
# define_simulations_line_style(SimulationsLineStyleDictionary_presentation)

# COP_graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, COP_contour, figure_title="Centre de pression", cases_on=MiddleCases_3, graph_annotation_on=False, composantes=["AP", "IS"], subplot={"dimension": [1, 2], "number": 1}, draw_COP_points_on=False, COP_first_point_size=10, COP_first_point_mew=2)
# COP_graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, COP_contour, figure_title="Centre de pression", cases_on=xUpCases_3, graph_annotation_on=False, composantes=["AP", "IS"], subplot={"dimension": [1, 2], "number": 2}, draw_COP_points_on=False, COP_first_point_size=10, COP_first_point_mew=2)


define_simulations_line_style(SimulationsLineStyleDictionary)

# %% variations forces de contact

# diff_force = {"Higher inclination": {"AP": [], "IS": [], "ML": [], "Abduction": Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage["up-normal"]["Abduction"]["Total"]},
#               "Lower inclination": {"AP": [], "IS": [], "ML": [], "Abduction": Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage["up-normal"]["Abduction"]["Total"]}
#               }

# for composante in ["AP", "IS", "ML"]:
#     diff_force["Higher inclination"][composante] = Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage["up-normal"]["ForceContact GlenImplant"][composante] - Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage["neutral-normal"]["ForceContact GlenImplant"][composante]
#     diff_force["Lower inclination"][composante] = Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage["xdown-normal"]["ForceContact GlenImplant"][composante] - Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage["neutral-normal"]["ForceContact GlenImplant"][composante]

# composante = "IS"
# inclination_variation = "Lower inclination"
# a_avant_90 = np.mean(diff_force[inclination_variation][composante][0:45])
# a_apres_90 = np.mean(diff_force[inclination_variation][composante][45:-1])

# %% Scores

# """CaseNames_36"""
# plt.subplots(2, 1, figsize=(20, 10))
# plt.subplot(2, 1, 1)
# bars = plt.bar(list(shear_scores_36.keys()), list(shear_scores_36.values()))
# # plt.grid(axis="y")
# plt.title("Total shear forces on the glenoid [N]")
# plt.bar_label(bars)

# plt.subplot(2, 1, 2)
# bars = plt.bar(list(moment_scores_36.keys()), list(moment_scores_36.values()))
# # plt.grid(axis="y")
# plt.title("Total moment on the glenoid [N.m]")
# plt.bar_label(bars)

# """CaseNames_6"""
# plt.subplots(2, 1, figsize=(70, 10))
# plt.subplot(2, 1, 1)
# bars = plt.bar(list(shear_scores.keys()), list(shear_scores.values()))
# # plt.grid(axis="y")
# plt.title("Total shear forces on the glenoid [N]")
# plt.bar_label(bars)

# plt.subplot(2, 1, 2)
# bars = plt.bar(list(moment_scores.keys()), list(moment_scores.values()))
# # plt.grid(axis="y")
# plt.title("Total moment on the glenoid [N.m]")
# plt.bar_label(bars)

# graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "Moment", composante_y=["AP+IS"], figure_title="Scores", xlim=[15, 120], figsize=[24, 14], cases_on=CaseNames_36, subplot={"dimension":[1, 2], "number": 1}, subplot_title="Moments on the glenoid", ylabel_on=False)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", composante_y=["TotalShear"], figure_title="Scores", xlim=[15, 120], figsize=[24, 14], cases_on=CaseNames_36, subplot={"dimension":[1, 2], "number": 2}, subplot_title="Shear on the glenoid", xlabel_on=False)
