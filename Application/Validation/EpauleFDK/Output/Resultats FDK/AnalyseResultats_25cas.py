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
COP_contour = define_COP_contour("GleneContour", "pp")


# %% Nom des cas de simulation

OldCaseNames = ["middle-normal", "middle-long",
                "up-normal", "up-short",
                "down-long"]

# Tilt acromion
xUpCases_3 = ["xup-xshort", "xup-normal", "xup-xlong"]
UpCases_3 = ["up-xshort", "up-normal", "up-xlong"]
MiddleCases_3 = ["middle-xshort", "middle-normal", "middle-xlong"]
DownCases_3 = ["down-xshort", "down-normal", "down-xlong"]
xDownCases_3 = ["xdown-xshort", "xdown-normal", "xdown-xlong"]


# Longueur d'acromion
xShortCases_3 = ["xdown-xshort", "middle-xshort", "xup-xshort"]
ShortCases_3 = ["xdown-short", "middle-short", "xup-short"]
NormalCases_3 = ["xdown-normal", "middle-normal", "xup-normal"]
LongCases_3 = ["xdown-long", "middle-long", "xup-long"]
xLongCases_3 = ["xdown-xlong", "middle-xlong", "xup-xlong"]

CaseNames_3 = [*xDownCases_3, *MiddleCases_3, *xUpCases_3]
UpDownCases_3 = [*xUpCases_3, *xDownCases_3]

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
# With xdown, middle, xup
CasesVariables_5 = {"Tilt": {"Large Downtilt": xDownCases_5, "Downtilt": DownCases_5, "Normal tilt": MiddleCases_5, "Uptilt": UpCases_5, "Large Uptilt": xUpCases_5},
                    "Acromion": {"Very short acromion": xShortCases_5, "Short acromion": ShortCases_5, "Normal acromion": NormalCases_5, " Long acromion": LongCases_5, "Very long acromion": xLongCases_5}}

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

# Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types")

Results_GlenoidLocalAxis_MR_Polynomial = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial")

Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage")

Results_GlenoidLocalAxis_MR_Polynomial_Fixed_Hill = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_Fixed_Hill")

Results_GlenoidLocalAxis_MR_Polynomial_Better_Initialpos = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_Better_Initialpos")

Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage")

Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage")

Results_GlenoidLocalAxis_MR_Polynomial_Elevation = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_Elevation")

Results_GlenoidLocalAxis_MR_MinMaxStrics_Elevation_no_recentrage = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_MinMaxStrics_Elevation_no_recentrage")

# Results_GlenoidLocalAxis_MR_Polynomial_180deg = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_180deg")

# Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange")

# Results_GlenoidLocalAxis_MR_Polynomial_delt_post_scaling = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_delt_post_scaling")

# Results_GlenoidLocalAxis_MR_Polynomial_delt_post_scaling_Elevation = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_Elevation")


# Results_GlenoidLocalAxis_MR_Polynomial_NewWrapping = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_NewWrapping")

# Results_GlenoidLocalAxis_NewWrapping_NewAMMR = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_NewWrapping_NewAMMR")

# Results_GlenoidLocalAxis_NewWrapping_FullRange = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_NewWrapping_FullRange")

# Results_GlenoidLocalAxis_NewWrapping_NoghProth = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_NewWrapping_NoghProth")

Results_GlenoidLocalAxis_MR_Polynomial_140deg_no_recentrage = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_140deg_no_recentrage")

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


# FDK Polynomial avec Ball And Socket
Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket = Results_GlenoidLocalAxis_MR_Polynomial.copy()
Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket["Ball And Socket"] = Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"]

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

variables_to_add_scapula = {"ForceContact GlenImplant": ["Total", "AP", "IS", "ML"],
                            "SpringForce scapula": ["Total", "AP", "IS", "ML"]
                            }


muscles_to_add_scapula_origin = ["Deltoideus lateral",
                                 "Deltoideus posterior",
                                 "Subscapularis",
                                 "Infraspinatus",
                                 "Supraspinatus",
                                 "Triceps long head",
                                 "Biceps brachii long head",
                                 "Biceps brachii short head",
                                 "Teres major",
                                 "Teres minor",
                                 "Coracobrachialis"
                                 ]

muscles_to_add_scapula_insertion = ["Levator scapulae",
                                    "Serratus anterior",
                                    "Lower trapezius",
                                    "Middle trapezius",
                                    "Rhomboideus",
                                    "Pectoralis minor"
                                    ]

muscle_variables_to_add_scapula = {"F insertion": {"component_sum_order": ["Total", "Total_AP", "Total_IS", "Total_ML"],
                                                   "muscles_to_add": muscles_to_add_scapula_insertion},
                                   "F origin": {"component_sum_order": ["Total", "Total_AP", "Total_IS", "Total_ML"],
                                                "muscles_to_add": muscles_to_add_scapula_origin}
                                   }

Results_GlenoidLocalAxis_MR_Polynomial = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial, "FTotal scapula", ["Total", "AP", "IS", "ML"], "Force totale sur la scapula (glene) [N]", variables_to_add_scapula, muscle_variables_to_add_scapula)


"""sur l'humérus"""
variables_to_add_humerus = {"ForceContact HumImplant glene": ["Total", "AP", "IS", "ML"],
                            "SpringForce humerus": ["Total", "AP", "IS", "ML"]
                            }

muscles_to_add_humerus_insertion = ["Deltoideus lateral",
                                    "Deltoideus posterior",
                                    "Deltoideus anterior",
                                    "Subscapularis",
                                    "Infraspinatus",
                                    "Supraspinatus",
                                    "Pectoralis major clavicular",
                                    "Pectoralis major sternal",
                                    "Coracobrachialis",
                                    "Teres major",
                                    "Teres minor",
                                    "Latissimus dorsi",
                                    "Triceps long head",
                                    ]

muscle_variables_to_add_humerus = {"F insertion": {"component_sum_order": ["Total", "Total_AP", "Total_IS", "Total_ML"],
                                                   "muscles_to_add": muscles_to_add_humerus_insertion}
                                   }

Results_GlenoidLocalAxis_MR_Polynomial = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial, "FTotal humerus", ["Total", "AP", "IS", "ML"], "Force totale sur l'humérus (glene)[N]", variables_to_add_humerus, muscle_variables_to_add_humerus)

"""Sans forces de contact"""
variables_to_add_humerus_no_fcontact = {"SpringForce humerus": ["Total", "AP", "IS", "ML"]}

Results_GlenoidLocalAxis_MR_Polynomial = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial, "FTotal humerus no Fcontact", ["Total", "AP", "IS", "ML"], "Force totale sur l'humérus no Fcontact (glene) [N]", variables_to_add_humerus_no_fcontact, muscle_variables_to_add_humerus)

"""Force totale muscles"""
Results_GlenoidLocalAxis_MR_Polynomial = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial, "FTotal muscles", ["Total", "AP", "IS", "ML"], "Force totale des muscles sur l'humérus (glene) [N]", muscle_variables_to_add=muscle_variables_to_add_humerus)

"""Sans springforce"""
variables_to_add_humerus_no_springforce = {"ForceContact humerus": ["Total", "AP", "IS", "ML"]}
Results_GlenoidLocalAxis_MR_Polynomial = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial, "FTotal humerus no SpringForce", ["Total", "AP", "IS", "ML"], "Force totale sur l'humérus no SpringForce (glene) [N]", variables_to_add_humerus_no_springforce, muscle_variables_to_add_humerus)

# %% COP

# # par catégories tilt et acromion
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13])

# # 3x3
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="center left", figsize=[15, 13])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="center left", figsize=[15, 13])

# # COPy et COPx
# # # 25 cas
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "COP", "COP en AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "COP", "COP en IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, "Abduction", "COP", "COP en AP", composante_y=["AP"], legend_position="center left", figsize=[15, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, "Abduction", "COP", "COP en IS", composante_y=["IS"], legend_position="center left", figsize=[15, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # # CSA
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_9, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[15, 14])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[15, 14])


# %% GHLin
"""
Translation dans repère implant, orientation implant
GHLin ISB
"""
# # par catégories tilt et acromion
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, COP_contour, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[0.8, -2.1], annotation_reference_offset=[0, 7])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, COP_contour, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_3, **CasesVariables_Acromion_3_Tilt_3}, COP_contour, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, COP_contour, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])

# # CSA
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, COP_contour, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])

# # Sans contour
# # par catégories tilt et acromion
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, None, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.8, -2.1], annotation_reference_offset=[0, 5], xlim=[-2.5, 2.5], ylim=[0, 10])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_3, **CasesVariables_Acromion_3_Tilt_3}, None, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], annotation_offset=[4, -2.1], annotation_reference_offset=[0, 5], xlim=[-2.5, 2.5], ylim=[0, 10])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, None, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="center left", figsize=[20, 16], annotation_offset=[4, -2.1], annotation_reference_offset=[0, 5], xlim=[-2.5, 2.5], ylim=[0, 10])

# # CSA
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, None, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="center left", figsize=[20, 14], annotation_offset=[1.8, -2.1], annotation_reference_offset=[0, 7], xlim=[-2.5, 2.5], ylim=[0, 10])

"""
Translation dans repère implant, orientation implant
GHLin ISB Relative
"""
# # par catégories tilt et acromion
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, COP_contour, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[0.8, -2.1], annotation_reference_offset=[0, 7])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, COP_contour, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])

# # CSA
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, COP_contour, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 14], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])

# # Sans contour
# # par catégories tilt et acromion
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, None, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.8, -2.1], annotation_reference_offset=[0, 5], xlim=[0, 5], ylim=[0, 7])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, None, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[4, -2.1], annotation_reference_offset=[0, 5], xlim=[0, 5], ylim=[0, 7])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, None, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[4, -2.1], annotation_reference_offset=[0, 5], xlim=[0, 5], ylim=[0, 7])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, None, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="center left", figsize=[20, 16], annotation_offset=[4, -2.1], annotation_reference_offset=[0, 5], xlim=[0, 5], ylim=[0, 7])

# # CSA
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, None, figure_title="Déplacement absolu de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="center left", figsize=[20, 14], annotation_offset=[1.8, -2.1], annotation_reference_offset=[0, 7], xlim=[0, 5], ylim=[0, 7])

"""
Translation dans repère implant, orientation implant
GHLin Absolute
"""

# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, None, figure_title="Déplacement absolu de la tête humérale (GHLin Absolute)", variable="GHLin Absolute", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], graph_annotation_on=False, same_lim=True)
# # mis à zéro
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, None, figure_title="Déplacement absolu de la tête humérale (GHLin Absolute zero)", variable="GHLin Absolute zero", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], graph_annotation_on=False, same_lim=True)

# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, None, figure_title="Déplacement absolu de la tête humérale (GHLin Absolute)", variable="GHLin Absolute", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], graph_annotation_on=False, same_lim=True)
# # mis à zéro
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, None, figure_title="Déplacement absolu de la tête humérale (GHLin Absolute zero)", variable="GHLin Absolute zero", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], graph_annotation_on=False, same_lim=True)

# %% Forces dans le repère humérus (pour comparer à Bergmann)

"""Forces"""
# # graph simple 9 cas
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 1}, subplot_title="Total", composante_y=["Total"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 2}, subplot_title="Antéropostérieur", composante_y=["AP"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 3}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 4}, subplot_title="Médiolatéral", composante_y=["ML"], xlim=[0, 120], grid_x_step=15, grid_y_step=50, same_lim=True, legend_position="center left")

# # sans same_lim
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 1}, subplot_title="Total", composante_y=["Total"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 2}, subplot_title="Antéropostérieur", composante_y=["AP"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 3}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 4}, subplot_title="Médiolatéral", composante_y=["ML"], xlim=[0, 120], grid_x_step=15, grid_y_step=50, legend_position="center left")

# # 25 cas
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 1}, subplot_title="Total", composante_y=["Total"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 2}, subplot_title="Antéropostérieur", composante_y=["AP"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 3}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 4}, subplot_title="Médiolatéral", composante_y=["ML"], xlim=[0, 120], grid_x_step=15, grid_y_step=50, same_lim=True, legend_position="center left")

# # sans same_lim
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 1}, subplot_title="Total", composante_y=["Total"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 2}, subplot_title="Antéropostérieur", composante_y=["AP"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 3}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact dans le repère de l'humérus", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 4}, subplot_title="Médiolatéral", composante_y=["ML"], xlim=[0, 120], grid_x_step=15, grid_y_step=50, legend_position="center left")

# # forces par catégorie
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[24, 13], xlim=[0, 120], same_lim=True, grid_x_step=15)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[24, 13], xlim=[0, 120], same_lim=True, grid_x_step=15)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[14, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # CSA
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_9, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[14, 14], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[14, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)


# # Forces par catégories par composantes
# # 3x3
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # Forces par catégories par composantes
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)


# # CSA par composantes
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[14, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[14, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[14, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)


# # Comparaison avec Bergmann 2007
# CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial = Results_GlenoidLocalAxis_MR_Polynomial.copy()
# CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial["Bergmann_2007"] = Results_literature["ForceContact"]["Bergmann 2007"]

# PremadeGraphs.graph_by_case_categories(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Bergmann, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[14, 13])

# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [1, 2], "number": 1}, figsize=[15, 8], subplot_title="Angle d'abduction", xlim=[0, 120], grid_x_step=15, same_lim=True)
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Elevation", "ForceContact", "Force de contact", cases_on=CaseNames_3, subplot={"dimension": [1, 2], "number": 2}, subplot_title="Angle d'élévation", xlim=[0, 120], grid_x_step=15, same_lim=True)

# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_5, "Bergmann_2007"], subplot={"dimension": [1, 2], "number": 1}, figsize=[15, 8], subplot_title="Angle d'abduction", xlim=[0, 120], grid_x_step=15, same_lim=True)
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Elevation", "ForceContact", "Force de contact", cases_on=CaseNames_5, subplot={"dimension": [1, 2], "number": 2}, subplot_title="Angle d'élévation", xlim=[0, 120], grid_x_step=15, same_lim=True, legend_position="center left")

# # 1x3
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Contact Force", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 1}, figsize=[15, 8], subplot_title="Mediolateral", composante_y=["ML"])
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Contact Force", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 2}, subplot_title="Inferosuperior", composante_y=["IS"])
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Contact Force", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 3}, subplot_title="Anteroposterior", composante_y=["AP"], xlim=[0, 120], grid_x_step=15, same_lim=True)

# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_5, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 1}, subplot_title="Médiolatéral", composante_y=["ML"])
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_5, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 2}, figsize=[15, 8], subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_5, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 3}, figsize=[15, 8], subplot_title="Antéropostérieur", composante_y=["AP"], xlim=[0, 120], grid_x_step=15, same_lim=True, legend_position="center left")

# # 2x2
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Contact Force", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [2, 2], "number": 1}, figsize=[15, 12], subplot_title="Total", composante_y=["Total"])
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Contact Force", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [2, 2], "number": 2}, subplot_title="Anteroposterior", composante_y=["AP"])
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Contact Force", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [2, 2], "number": 3}, subplot_title="Inferosuperior", composante_y=["IS"])
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Contact Force", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [2, 2], "number": 4}, subplot_title="Mediolateral", composante_y=["ML"], xlim=[0, 120], grid_x_step=15, same_lim=True)


# # par catégorie 3x3
# PremadeGraphs.graph_by_case_categories(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Bergmann, "Abduction", "ForceContact", "Forces de contact Totale", legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Bergmann, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Bergmann, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Bergmann, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # par catégorie 5x5
# PremadeGraphs.graph_by_case_categories(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5_Bergmann, "Abduction", "ForceContact", "Forces de contact Totale", legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5_Bergmann, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5_Bergmann, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5_Bergmann, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# %% Force de contact dans le repère de la scapula

# # Forces par catégories par composantes
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact scapula", "Forces de contact Totale dans le repère de la scapula", composante_y=["Total"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact scapula", "Forces de contact AP dans le repère de la scapula", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact scapula", "Forces de contact IS dans le repère de la scapula", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact scapula", "Forces de contact ML dans le repère de la scapula", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # Forces par catégories par composantes
# # 3x3
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact scapula", "Forces de contact Totale dans le repère de la scapula", composante_y=["Total"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact scapula", "Forces de contact AP dans le repère de la scapula", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact scapula", "Forces de contact IS dans le repère de la scapula", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact scapula", "Forces de contact ML dans le repère de la scapula", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # graph simple 9 cas
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 1}, subplot_title="Total", composante_y=["Total"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 2}, subplot_title="Antéropostérieur", composante_y=["AP"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 3}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 4}, subplot_title="Médiolatéral", composante_y=["ML"], xlim=[0, 120], grid_x_step=15, grid_y_step=50, same_lim=True, legend_position="center left")
# # sans same_lim
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 1}, subplot_title="Total", composante_y=["Total"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 2}, subplot_title="Antéropostérieur", composante_y=["AP"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 3}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 4}, subplot_title="Médiolatéral", composante_y=["ML"], xlim=[0, 120], grid_x_step=15, grid_y_step=50, legend_position="center left")
# # 25 cas
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 1}, subplot_title="Total", composante_y=["Total"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 2}, subplot_title="Antéropostérieur", composante_y=["AP"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 3}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 4}, subplot_title="Médiolatéral", composante_y=["ML"], xlim=[0, 120], grid_x_step=15, grid_y_step=50, same_lim=True, legend_position="center left")
# # sans same_lim
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 1}, subplot_title="Total", composante_y=["Total"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 2}, subplot_title="Antéropostérieur", composante_y=["AP"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 3}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact scapula", "Force de contact dans le repère de la scapula", cases_on=CaseNames_5, subplot={"dimension": [1, 4], "number": 4}, subplot_title="Médiolatéral", composante_y=["ML"], xlim=[0, 120], grid_x_step=15, grid_y_step=50, legend_position="center left")


# %% Force de contact dans le repère de la glène

"""Forces sur l'implant glenoidien"""
# # Forces par catégories par composantes
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact GlenImplant", "Forces de contact Totale sur l'implant glénoidien dans le repère de la glène", composante_y=["Total"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact GlenImplant", "Forces de contact AP sur l'implant glénoidien dans le repère de la glène", composante_y=["AP"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact GlenImplant", "Forces de contact IS sur l'implant glénoidien dans le repère de la glène", composante_y=["IS"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact GlenImplant", "Forces de contact ML sur l'implant glénoidien dans le repère de la glène", composante_y=["ML"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # # Forces par catégories par composantes
# # 3x3
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact GlenImplant", "Forces de contact Totale sur l'implant glénoidien dans le repère de la glène", composante_y=["Total"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact GlenImplant", "Forces de contact AP sur l'implant glénoidien dans le repère de la glène", composante_y=["AP"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact GlenImplant", "Forces de contact IS sur l'implant glénoidien dans le repère de la glène", composante_y=["IS"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact GlenImplant", "Forces de contact ML sur l'implant glénoidien dans le repère de la glène", composante_y=["ML"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # Graph simple
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact GlenImplant", "Force de contact sur l'implant glénoidien dans le repère de la glene", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 1}, subplot_title="Total", composante_y=["Total"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact GlenImplant", "Force de contact sur l'implant glénoidien dans le repère de la glene", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 2}, subplot_title="Antéropostérieur", composante_y=["AP"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact GlenImplant", "Force de contact sur l'implant glénoidien dans le repère de la glene", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 3}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact GlenImplant", "Force de contact sur l'implant glénoidien dans le repère de la glene", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 4}, subplot_title="Médiolatéral", composante_y=["ML"], xlim=[0, 120], grid_x_step=15, grid_y_step=50, same_lim=True)

"""Forces sur l'implant huméral"""
# # Forces par catégories par composantes
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact HumImplant glene", "Forces de contact Totale sur l'implant huméral dans le repère de la glène", composante_y=["Total"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact HumImplant glene", "Forces de contact AP sur l'implant huméral dans le repère de la glène", composante_y=["AP"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact HumImplant glene", "Forces de contact IS sur l'implant huméral dans le repère de la glène", composante_y=["IS"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact HumImplant glene", "Forces de contact ML sur l'implant huméral dans le repère de la glène", composante_y=["ML"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # Forces par catégories par composantes
# # 3x3
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact HumImplant glene", "Forces de contact Totale sur l'implant huméral dans le repère de la glène", composante_y=["Total"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact HumImplant glene", "Forces de contact AP sur l'implant huméral dans le repère de la glène", composante_y=["AP"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact HumImplant glene", "Forces de contact IS sur l'implant huméral dans le repère de la glène", composante_y=["IS"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact HumImplant glene", "Forces de contact ML sur l'implant huméral dans le repère de la glène", composante_y=["ML"], legend_position="center left", figsize=[24, 16], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # Graph simple
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact HumImplant glene", "Force de contact sur l'implant huméral dans le repère de la glene", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 1}, subplot_title="Total", composante_y=["Total"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact HumImplant glene", "Force de contact sur l'implant huméral dans le repère de la glene", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 2}, subplot_title="Antéropostérieur", composante_y=["AP"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact HumImplant glene", "Force de contact sur l'implant huméral dans le repère de la glene", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 3}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact HumImplant glene", "Force de contact sur l'implant huméral dans le repère de la glene", cases_on=CaseNames_3, subplot={"dimension": [1, 4], "number": 4}, subplot_title="Médiolatéral", composante_y=["ML"], xlim=[0, 120], grid_x_step=15, grid_y_step=50, same_lim=True, legend_position="center left")

# %% Muscles Activity

# # Activité 9 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", cases_on=CaseNames_3_BallAndSocket, composante_y=["Max"], figsize=[24, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", cases_on=CaseNames_3_BallAndSocket, composante_y=["Max"], figsize=[24, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", cases_on=CaseNames_3_BallAndSocket, composante_y=["Max"], figsize=[16, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_actifs, [4, 3], "Abduction", "Activity", "Activation maximale des muscles", cases_on=CaseNames_3_BallAndSocket, composante_y=["Max"], figsize=[24, 20], grid_x_step=15, xlim=[0, 120], same_lim=True)

# # sans same_lim
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", cases_on=CaseNames_3_BallAndSocket, composante_y=["Max"], figsize=[24, 14], grid_x_step=15, xlim=[0, 120], same_lim=False)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", cases_on=CaseNames_3_BallAndSocket, composante_y=["Max"], figsize=[24, 14], grid_x_step=15, xlim=[0, 120], same_lim=False)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", cases_on=CaseNames_3_BallAndSocket, composante_y=["Max"], figsize=[16, 14], grid_x_step=15, xlim=[0, 120], same_lim=False)


# # Activité 25 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", cases_on=CaseNames_5, composante_y=["Max"], grid_x_step=15, xlim=[0, 120])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", cases_on=CaseNames_5, composante_y=["Max"], grid_x_step=15, xlim=[0, 120])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", cases_on=CaseNames_5, composante_y=["Max"], grid_x_step=15, xlim=[0, 120])

# # Activité rassemblé par catégories sans les parties des muscles
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3, Muscles_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Activité rassemblé par catégories avec les parties des muscles (9 cas)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3, Muscles_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Activité rassemblé par catégories avec les parties des muscles (25 cas)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_5, Muscles_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # CSA par catégories
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_9, Muscles_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], legend_position="center left", figsize=[14, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_6, Muscles_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], legend_position="center left", figsize=[14, 13], grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Muscles par parties individuelles
# # 25 cas
# PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, AllMuscles_List, "Abduction", "Activity", composante_y_muscle_combined=["Max"], cases_on="all", grid_x_step=15, xlim=[0, 120], same_lim=True)
# # 9 cas
# PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, AllMuscles_List, "Abduction", "Activity", composante_y_muscle_combined=["Max"], cases_on=CaseNames_3, grid_x_step=15, xlim=[0, 120], same_lim=True)


# # Comparaison avec la littérature
# PremadeGraphs.muscle_graph_from_list(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, Muscle_Comp_Main, [3, 3], "Abduction", "Activity", "Recrutement Polynomial : Activation maximale des muscles", cases_on=CompWickham_CasesNames_3, composante_y=["Max"], figsize=[24, 16], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, Muscle_Comp_Aux, [2, 3], "Abduction", "Activity", "Recrutement Polynomial : Activation maximale des muscles", cases_on=CompWickham_CasesNames_3, composante_y=["Max"], figsize=[24, 16], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, Muscles_Comp_actifs, [4, 3], "Abduction", "Activity", "Recrutement Polynomial : Activation maximale des muscles", cases_on=[*CompWickham_CasesNames_3, "Ball And Socket"], composante_y=["Max"], figsize=[24, 20], legend_position="center left", grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Comparaison avec Wicham par catégories
# PremadeGraphs.muscle_graph_by_case_categories(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Wickham, Muscles_Comp_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], muscle_part_on=False, figsize=[16, 10], same_lim=True)

# # Muscles qui varient
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation, [3, 2], "Abduction", "Activity", "Activation influencés par le CSA", composante_y=["Max"], cases_on=CaseNames_3_BallAndSocket, figsize=[14, 14], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation, [3, 2], "Abduction", "Activity", "Activation influencés par le CSA", composante_y=["Max"], cases_on=CaseNames_3_BallAndSocket, figsize=[14, 14])

# # Muscles qui varient2
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation_faible, [3, 3], "Abduction", "Activity", "Activation influencés par le CSA", composante_y=["Max"], cases_on=CaseNames_3_BallAndSocket, figsize=[14, 14], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation_faible, [3, 3], "Abduction", "Activity", "Activation influencés par le CSA", composante_y=["Max"], cases_on=CaseNames_3_BallAndSocket, figsize=[14, 14])

# %% Contact area

# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, CasesVariables_5, "Abduction", "ContactArea", "Surface de contact entre les deux implants", legend_position="center left", figsize=[24, 13], xlim=[0, 120], same_lim=True, grid_x_step=15)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, CasesVariables_3, "Abduction", "ContactArea", "Surface de contact entre les deux implants", legend_position="center left", figsize=[24, 13], xlim=[0, 120], same_lim=True, grid_x_step=15)

# %% Muscles Ft

"""
Par catégories
"""
# # Ft 9 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Force musculaire : Muscles actifs (Ft > 10N)", cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[0, 120], ylim=[0, 200], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Force musculaire : Muscles peu actifs (10 N > Ft > 5N)", cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[0, 120], ylim=[0, 20], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Force musculaire : Muscles inactifs (Ft < 5N)", cases_on=CaseNames_3_BallAndSocket, figsize=[16, 14], xlim=[0, 120], ylim=[0, 20], legend_position="center left", grid_x_step=15)

# # sans same_lim
# # Ft 9 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Force musculaire : Muscles actifs (Ft > 10N)", cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Force musculaire : Muscles peu actifs (10 N > Ft > 5N)", cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Force musculaire : Muscles inactifs (Ft < 5N)", cases_on=CaseNames_3_BallAndSocket, figsize=[16, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)

# # Ft 25 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Force musculaire : Muscles actifs (Ft > 10N)", cases_on=[*CaseNames_5, "Ball And Socket"], figsize=[24, 14], xlim=[0, 120], ylim=[0, 200], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Force musculaire : Muscles peu actifs (10 N > Ft > 5N)", cases_on=[*CaseNames_5, "Ball And Socket"], figsize=[24, 14], xlim=[0, 120], ylim=[0, 20], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Force musculaire : Muscles inactifs (Ft < 5N)", cases_on=[*CaseNames_5, "Ball And Socket"], figsize=[16, 14], xlim=[0, 120], ylim=[0, 20], legend_position="center left", grid_x_step=15)

"""
Muscles qui varient
"""
# # Muscles qui varient
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation, [3, 2], "Abduction", "Ft", "Activation influencés par le CSA", cases_on=CaseNames_3_BallAndSocket, figsize=[14, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation, [3, 2], "Abduction", "Ft", "Activation influencés par le CSA", cases_on=CaseNames_3_BallAndSocket, figsize=[14, 14], grid_x_step=15, xlim=[0, 120])

# # Muscles qui varient faiblement
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation, [3, 2], "Abduction", "Ft", "Activation influencés par le CSA", cases_on=CaseNames_3_BallAndSocket, figsize=[14, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation_faible, [3, 3], "Abduction", "Ft", "Activation influencés par le CSA", cases_on=CaseNames_3_BallAndSocket, figsize=[14, 14], grid_x_step=15, xlim=[0, 120])


"""
par catégories
"""
# # Ft rassemblé par catégories sans les parties des muscles
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3_Ball_And_Socket, list_muscle_variation, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Ft rassemblé par catégories sans les parties des muscles
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_5_Ball_And_Socket, list_muscle_variation, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Ft rassemblé par catégories avec les parties des muscles (9 cas)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3, list_muscle_variation, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Ft rassemblé par catégories avec les parties des muscles (25 cas)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_5, list_muscle_variation, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # CSA par catégories
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_9, list_muscle_variation, "Abduction", "Ft", legend_position="center left", figsize=[14, 14], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_6, list_muscle_variation, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)


"""Muscles qui varient peu"""
# Ft rassemblé par catégories sans les parties des muscles
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3_Ball_And_Socket, list_muscle_variation_faible, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # CSA par catégories
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_9, list_muscle_variation_faible, "Abduction", "Ft", legend_position="center left", figsize=[14, 14], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_6, list_muscle_variation_faible, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Ft rassemblé par catégories avec les parties des muscles (9 cas)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3, list_muscle_variation_faible, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Ft rassemblé par catégories avec les parties des muscles (25 cas)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_5, list_muscle_variation_faible, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

"""
Muscles par parties
"""
# # Muscles par parties individuelles
# # 25 cas
# PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, AllMuscles_List, "Abduction", "Ft", cases_on="all", grid_x_step=15, xlim=[0, 120], legend_position="center left", same_lim=True)

# # 9 cas
# PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, AllMuscles_List, "Abduction", "Ft", cases_on=CaseNames_3, grid_x_step=15, xlim=[0, 120], same_lim=True)

# %% Analyse 180° abduction avec conflit acromion pris en compte

# # forces par catégorie
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", figure_title="Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", figure_title="Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", figure_title="Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13])


# # COP
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="max_x", annotation_reference_offset=[-3.5, -1], annotation_offset=[-0.4, 2.1])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg, CasesVariables_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="max_x", annotation_reference_offset=[-3.5, -1], annotation_offset=[-0.4, 2.1])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg, CasesVariables_3, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="min_y", annotation_reference_offset=[-5.5, -1], annotation_offset=[-0.4, 2.1])


# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg, CasesVariables_5, "ForceTolError", "Abduction", "ForceTolError", legend_position="center left", figsize=[24, 13])

# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg, CasesVariables_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13])

# comp = {"120": Results_GlenoidLocalAxis_MR_Polynomial, "180": Results_GlenoidLocalAxis_MR_Polynomial_180deg}

# list_case = ["middle-normal", "xup-normal", "xdown-normal"]
# COP_graph(comp, "COP abduction à 180°", COP_contour, cases_on=[list_case[0]], compare=True, subplot={"dimension": [1, 3], "number": 1}, legend_position="lower center", figsize=[24, 13], composantes=["AP", "IS"])
# COP_graph(comp, "COP abduction à 180°", COP_contour, cases_on=[list_case[1]], compare=True, subplot={"dimension": [1, 3], "number": 2}, legend_position="lower center", figsize=[24, 13], composantes=["AP", "IS"])
# COP_graph(comp, "COP abduction à 180°", COP_contour, cases_on=[list_case[2]], compare=True, subplot={"dimension": [1, 3], "number": 3}, legend_position="lower center", figsize=[24, 13], composantes=["AP", "IS"])

# graph(comp, "Abduction", "ForceContact", "Forces de contact abduction à 180°", compare=True, cases_on=[list_case[0]], subplot={"dimension": [1, 3], "number": 1}, legend_position="lower center", figsize=[24, 13])
# graph(comp, "Abduction", "ForceContact", "Forces de contact abduction à 180°", compare=True, cases_on=[list_case[1]], subplot={"dimension": [1, 3], "number": 2}, legend_position="lower center", figsize=[24, 13])
# graph(comp, "Abduction", "ForceContact", "Forces de contact abduction à 180°", compare=True, cases_on=[list_case[2]], subplot={"dimension": [1, 3], "number": 3}, legend_position="lower center", figsize=[24, 13])


# graph(Results_GlenoidLocalAxis_MR_Polynomial_180deg, "Temps", "Abduction", "Forces de contact abduction à 180°", cases_on="all", legend_position="lower center", label="120°")
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Temps", "Abduction", "Forces de contact abduction à 180°", cases_on="all", legend_position="lower center", label="180°", add_graph=True)

# %% Analyse 180° abduction full range

# # forces par catégorie
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13])

# # COP
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="min_y", annotation_reference_offset=[-2.5, -1], annotation_offset=[-0.4, 2.1])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, CasesVariables_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="min_y", annotation_reference_offset=[-2.5, -1], annotation_offset=[-0.4, 2.1])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, CasesVariables_3, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="min_y", annotation_reference_offset=[-2.5, -1], annotation_offset=[-0.4, 2.1])

"""
Muscles
"""

# # Activité 9 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", cases_on=CaseNames_3, composante_y=["Max"], figsize=[24, 16])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", cases_on=CaseNames_3, composante_y=["Max"], figsize=[24, 16])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", cases_on=CaseNames_3, composante_y=["Max"], figsize=[24, 16])

# %% Ball And Socket full range

# # Activité 9 cas
# PremadeGraphs.muscle_graph_from_list(Results_BallAndSocket_FullRange, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", cases_on="all", composante_y=["Max"], figsize=[24, 16])
# PremadeGraphs.muscle_graph_from_list(Results_BallAndSocket_FullRange, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", cases_on="all", composante_y=["Max"], figsize=[24, 16])
# PremadeGraphs.muscle_graph_from_list(Results_BallAndSocket_FullRange, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", cases_on="all", composante_y=["Max"], figsize=[24, 16])

# comp_full_range = {"FDK": Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, "Ball And Socket": Results_BallAndSocket_FullRange}

# for Case in MiddleCases_5:
#     # Activité 9 cas
#     PremadeGraphs.muscle_graph_from_list(comp_full_range, Muscles_Main, [3, 3], "Abduction", "Activity", f"{Case} : Muscles principaux : Activation maximale des muscles", cases_on=[Case], compare=True, composante_y=["Max"], figsize=[24, 16])
#     PremadeGraphs.muscle_graph_from_list(comp_full_range, Muscles_Aux, [3, 3], "Abduction", "Activity", f"{Case} : Muscles auxiliaires : Activation maximale des muscles", cases_on=[Case], compare=True, composante_y=["Max"], figsize=[24, 16])
#     PremadeGraphs.muscle_graph_from_list(comp_full_range, Muscles_Extra, [2, 3], "Abduction", "Activity", f"{Case} : Muscles extras : Activation maximale des muscles", cases_on=[Case], compare=True, composante_y=["Max"], figsize=[24, 16])


# %% Elevation plan scapula

# # par catégories tilt et acromion
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_delt_post_scaling_Elevation, CasesVariables_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13])

# %% force des muscles projetées

"""Catégories de muscles"""
# # insertion
# composante = "Total_AP"
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "F insertion", f"Force projetée insertion {composante} : Muscles actifs (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "F insertion", f"Force projetée insertion {composante} : Muscles peu actifs (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "F insertion", f"Force projetée insertion {composante} : Muscles inactifs (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)

# composante = "Total_IS"
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "F insertion", f"Force projetée insertion {composante} : Muscles actifs (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "F insertion", f"Force projetée insertion {composante} : Muscles peu actifs (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "F insertion", f"Force projetée insertion {composante} : Muscles inactifs (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)

# composante = "Total_ML"
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "F insertion", f"Force projetée insertion {composante} : Muscles actifs (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "F insertion", f"Force projetée insertion {composante} : Muscles peu actifs (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "F insertion", f"Force projetée insertion {composante} : Muscles inactifs (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)

# # origine
# composante = "Total_AP"
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "F origin", f"Force projetée origine {composante} : Muscles actifs (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "F origin", f"Force projetée origine {composante} : Muscles peu actifs (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "F origin", f"Force projetée origine {composante} : Muscles inactifs (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)

# composante = "Total_IS"
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "F origin", f"Force projetée origine {composante} : Muscles actifs (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "F origin", f"Force projetée origine {composante} : Muscles peu actifs (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "F origin", f"Force projetée origine {composante} : Muscles inactifs (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)

# composante = "Total_ML"
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "F origin", f"Force projetée origine {composante} : Muscles actifs (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "F origin", f"Force projetée origine {composante} : Muscles peu actifs (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "F origin", f"Force projetée origine {composante} : Muscles inactifs (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_BallAndSocket, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)


"""Tous les muscles"""
# for muscle_name in AllMuscles_List:
#     # force muscle projetée origine
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 1}, subplot_title="Total origine", composante_y=["Total"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 2}, subplot_title="AP origine", composante_y=["Total_AP"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 3}, subplot_title="IS origine", composante_y=["Total_IS"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 4}, subplot_title="ML origine", composante_y=["Total_ML"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])

#     # force muscle projetée insertion
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 5}, subplot_title="Total insertion", composante_y=["Total"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 6}, subplot_title="AP insertion", composante_y=["Total_AP"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 7}, subplot_title="IS insertion", composante_y=["Total_IS"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 8}, subplot_title="ML insertion", composante_y=["Total_ML"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13], grid_x_step=15, xlim=[15, 120], same_lim=True)

# # sans same_lim pour mieux voir qui varie
# for muscle_name in AllMuscles_List:
#     # force muscle projetée origine
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 1}, subplot_title="Total origine", composante_y=["Total"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 2}, subplot_title="AP origine", composante_y=["Total_AP"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 3}, subplot_title="IS origine", composante_y=["Total_IS"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 4}, subplot_title="ML origine", composante_y=["Total_ML"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])

#     # force muscle projetée insertion
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 5}, subplot_title="Total insertion", composante_y=["Total"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 6}, subplot_title="AP insertion", composante_y=["Total_AP"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 7}, subplot_title="IS insertion", composante_y=["Total_IS"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 8}, subplot_title="ML insertion", composante_y=["Total_ML"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13], grid_x_step=15, xlim=[15, 120])


"""Muscles qui varient"""
# for muscle_name in list_muscle_variation:
#     # force muscle projetée origine
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 1}, subplot_title="Total origine", composante_y=["Total"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 2}, subplot_title="AP origine", composante_y=["Total_AP"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 3}, subplot_title="IS origine", composante_y=["Total_IS"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 4}, subplot_title="ML origine", composante_y=["Total_ML"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])

#     # force muscle projetée insertion
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 5}, subplot_title="Total insertion", composante_y=["Total"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 6}, subplot_title="AP insertion", composante_y=["Total_AP"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 7}, subplot_title="IS insertion", composante_y=["Total_IS"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 8}, subplot_title="ML insertion", composante_y=["Total_ML"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13], grid_x_step=15, xlim=[15, 120], same_lim=True)

# for muscle_name in list_muscle_variation:
#     # force muscle projetée origine
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 1}, subplot_title="Total origine", composante_y=["Total"], cases_on=CaseNames_5_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 2}, subplot_title="AP origine", composante_y=["Total_AP"], cases_on=CaseNames_5_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 3}, subplot_title="IS origine", composante_y=["Total_IS"], cases_on=CaseNames_5_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 4}, subplot_title="ML origine", composante_y=["Total_ML"], cases_on=CaseNames_5_BallAndSocket, legend_position="center left", figsize=[20, 13])

#     # force muscle projetée insertion
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 5}, subplot_title="Total insertion", composante_y=["Total"], cases_on=CaseNames_5_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 6}, subplot_title="AP insertion", composante_y=["Total_AP"], cases_on=CaseNames_5_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 7}, subplot_title="IS insertion", composante_y=["Total_IS"], cases_on=CaseNames_5_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 8}, subplot_title="ML insertion", composante_y=["Total_ML"], cases_on=CaseNames_5_BallAndSocket, legend_position="center left", figsize=[20, 13], grid_x_step=15, xlim=[15, 120], same_lim=True)

"""Muscles actifs"""
# 9 cas
# for muscle_name in list_muscles_actifs:
#     # force muscle projetée origine
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 1}, subplot_title="Total origine", composante_y=["Total"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 2}, subplot_title="AP origine", composante_y=["Total_AP"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 3}, subplot_title="IS origine", composante_y=["Total_IS"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 4}, subplot_title="ML origine", composante_y=["Total_ML"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])

#     # force muscle projetée insertion
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 5}, subplot_title="Total insertion", composante_y=["Total"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 6}, subplot_title="AP insertion", composante_y=["Total_AP"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 7}, subplot_title="IS insertion", composante_y=["Total_IS"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 8}, subplot_title="ML insertion", composante_y=["Total_ML"], cases_on=CaseNames_3_BallAndSocket, legend_position="center left", figsize=[20, 13], grid_x_step=15, xlim=[15, 120], same_lim=True)


# # middle-normal seulement insertion
# for muscle_name in list_muscles_actifs:
#     # force muscle projetée origine
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 1}, subplot_title="Total insertion", composante_y=["Total"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13], graph_annotation_on=True, annotation_reference_offset=[0, 8], annotation_mode="max", update_ylim=True, update_xlim=True)
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 2}, subplot_title="AP insertion", composante_y=["Total_AP"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13], graph_annotation_on=True, annotation_reference_offset=[0, 8], annotation_mode="max")
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 3}, subplot_title="IS insertion", composante_y=["Total_IS"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13], graph_annotation_on=True, annotation_reference_offset=[0, 8], annotation_mode="max")
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère capula", subplot={"dimension": [2, 4], "number": 4}, subplot_title="ML insertion", composante_y=["Total_ML"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13], graph_annotation_on=True, annotation_reference_offset=[0, 8], annotation_mode="max", grid_x_step=15, xlim=[15, 120], same_lim=True)

#     # force muscle projetée origine
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 5}, subplot_title="Total insertion", composante_y=["Total"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13], graph_annotation_on=True, annotation_reference_offset=[0, 8], annotation_mode="min")
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 6}, subplot_title="AP insertion", composante_y=["Total_AP"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13], graph_annotation_on=True, annotation_reference_offset=[0, 8], annotation_mode="min")
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 7}, subplot_title="IS insertion", composante_y=["Total_IS"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13], graph_annotation_on=True, annotation_reference_offset=[0, 8], annotation_mode="min")
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère capula", subplot={"dimension": [2, 4], "number": 8}, subplot_title="ML insertion", composante_y=["Total_ML"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13], graph_annotation_on=True, annotation_reference_offset=[0, 8], annotation_mode="min", grid_x_step=15, xlim=[15, 120], same_lim=True)

# # insertion et origine
# for muscle_name in list_muscles_actifs:
#     # force muscle projetée origine
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 1}, subplot_title="Total origine", composante_y=["Total"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 2}, subplot_title="AP origine", composante_y=["Total_AP"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 3}, subplot_title="IS origine", composante_y=["Total_IS"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 4}, subplot_title="ML origine", composante_y=["Total_ML"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13])

#     # force muscle projetée insertion
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 5}, subplot_title="Total insertion", composante_y=["Total"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 6}, subplot_title="AP insertion", composante_y=["Total_AP"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 7}, subplot_title="IS insertion", composante_y=["Total_IS"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 4], "number": 8}, subplot_title="ML insertion", composante_y=["Total_ML"], cases_on=["middle-normal"], legend_position="center left", figsize=[20, 13], grid_x_step=15, xlim=[15, 120], same_lim=True)

"""Muscles qui varient par catégorie et par composante"""
# # 25 cas
# # F origin
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, list_muscle_variation, "Abduction", "F origin", composante_y_muscle_combined=["Total"], legend_position="center left", figsize=[24, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, list_muscle_variation, "Abduction", "F origin", composante_y_muscle_combined=["Total_AP"], legend_position="center left", figsize=[24, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, list_muscle_variation, "Abduction", "F origin", composante_y_muscle_combined=["Total_IS"], legend_position="center left", figsize=[24, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, list_muscle_variation, "Abduction", "F origin", composante_y_muscle_combined=["Total_ML"], legend_position="center left", figsize=[24, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # F origin
# # 9 cas
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, list_muscle_variation, "Abduction", "F origin", composante_y_muscle_combined=["Total"], legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, list_muscle_variation, "Abduction", "F origin", composante_y_muscle_combined=["Total_AP"], legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, list_muscle_variation, "Abduction", "F origin", composante_y_muscle_combined=["Total_IS"], legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, list_muscle_variation, "Abduction", "F origin", composante_y_muscle_combined=["Total_ML"], legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # F insertion
# # 25 cas
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, list_muscle_variation, "Abduction", "F insertion", composante_y_muscle_combined=["Total"], legend_position="center left", figsize=[24, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, list_muscle_variation, "Abduction", "F insertion", composante_y_muscle_combined=["Total_AP"], legend_position="center left", figsize=[24, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, list_muscle_variation, "Abduction", "F insertion", composante_y_muscle_combined=["Total_IS"], legend_position="center left", figsize=[24, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, list_muscle_variation, "Abduction", "F insertion", composante_y_muscle_combined=["Total_ML"], legend_position="center left", figsize=[24, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # F insertion
# # 9 cas
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, list_muscle_variation, "Abduction", "F insertion", composante_y_muscle_combined=["Total"], legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, list_muscle_variation, "Abduction", "F insertion", composante_y_muscle_combined=["Total_AP"], legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, list_muscle_variation, "Abduction", "F insertion", composante_y_muscle_combined=["Total_IS"], legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, list_muscle_variation, "Abduction", "F insertion", composante_y_muscle_combined=["Total_ML"], legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)


# %% Direction des forces du deltoide

"""Direction des forces"""
# muscle_name = "Deltoideus lateral"
# n_part = 4

# # force muscle projetée origine
# muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F origin direction", f"{muscle_name} Mean : Direction de la force projetée sur l'origine dans le repère scapula", subplot={"dimension": [1, 3], "number": 1}, subplot_title="AP origine", composante_y=["AP"], cases_on=CaseNames_5, legend_position="center left", figsize=[14, 13])
# muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F origin direction", f"{muscle_name} Mean : Direction de la force projetée sur l'origine dans le repère scapula", subplot={"dimension": [1, 3], "number": 2}, subplot_title="IS origine", composante_y=["IS"], cases_on=CaseNames_5, legend_position="center left", figsize=[14, 13])
# muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F origin direction", f"{muscle_name} Mean : Direction de la force projetée sur l'origine dans le repère scapula", subplot={"dimension": [1, 3], "number": 3}, subplot_title="ML origine", composante_y=["ML"], cases_on=CaseNames_5, legend_position="center left", figsize=[14, 13], same_lim=True, xlim=[15, 120], grid_x_step=15, grid_y_step=0.25, ylim=[-1, 1])

# # parties du muscle
# for part_number in range(1, n_part + 1):
#     # force muscle projetée origine
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F origin direction", f"{muscle_name} {part_number} : Direction de la force projetée sur l'origine dans le repère scapula", muscle_part_on=[part_number], subplot={"dimension": [1, 3], "number": 1}, subplot_title="AP origine", composante_y=["AP"], cases_on=CaseNames_5, legend_position="center left", figsize=[14, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F origin direction", f"{muscle_name} {part_number} : Direction de la force projetée sur l'origine dans le repère scapula", muscle_part_on=[part_number], subplot={"dimension": [1, 3], "number": 2}, subplot_title="IS origine", composante_y=["IS"], cases_on=CaseNames_5, legend_position="center left", figsize=[14, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F origin direction", f"{muscle_name} {part_number} : Direction de la force projetée sur l'origine dans le repère scapula", muscle_part_on=[part_number], subplot={"dimension": [1, 3], "number": 3}, subplot_title="ML origine", composante_y=["ML"], cases_on=CaseNames_5, legend_position="center left", figsize=[14, 13], same_lim=True, xlim=[15, 120], grid_x_step=15, grid_y_step=0.25, ylim=[-1, 1])


# # force muscle projetée origine
# muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F insertion direction", f"{muscle_name} Total : Direction de la force projetée sur l'insertion dans le repère scapula", subplot={"dimension": [1, 3], "number": 1}, subplot_title="AP insertion", composante_y=["AP"], cases_on=CaseNames_5, legend_position="center left", figsize=[24, 13])
# muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F insertion direction", f"{muscle_name} Total : Direction de la force projetée sur l'insertion dans le repère scapula", subplot={"dimension": [1, 3], "number": 2}, subplot_title="IS insertion", composante_y=["IS"], cases_on=CaseNames_5, legend_position="center left", figsize=[24, 13])
# muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F insertion direction", f"{muscle_name} Total : Direction de la force projetée sur l'insertion dans le repère scapula", subplot={"dimension": [1, 3], "number": 3}, subplot_title="ML insertion", composante_y=["ML"], cases_on=CaseNames_5, legend_position="center left", figsize=[24, 13], same_lim=True, xlim=[15, 120], grid_x_step=15, ylim=[-1, 1], grid_y_step=0.25)


# # parties du muscle
# for part_number in range(1, n_part + 1):
#     # force muscle projetée origine
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F insertion direction", f"{muscle_name} {part_number} : Direction de la force projetée sur l'insertion dans le repère scapula", muscle_part_on=[part_number], subplot={"dimension": [1, 3], "number": 1}, subplot_title="AP insertion", composante_y=["AP"], cases_on=CaseNames_5, legend_position="center left", figsize=[24, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F insertion direction", f"{muscle_name} {part_number} : Direction de la force projetée sur l'insertion dans le repère scapula", muscle_part_on=[part_number], subplot={"dimension": [1, 3], "number": 2}, subplot_title="IS insertion", composante_y=["IS"], cases_on=CaseNames_5, legend_position="center left", figsize=[24, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial, muscle_name, "Abduction", "F insertion direction", f"{muscle_name} {part_number} : Direction de la force projetée sur l'insertion dans le repère scapula", muscle_part_on=[part_number], subplot={"dimension": [1, 3], "number": 3}, subplot_title="ML insertion", composante_y=["ML"], cases_on=CaseNames_5, legend_position="center left", figsize=[24, 13], same_lim=True, ylim=[-1, 1], grid_y_step=0.25, xlim=[15, 120], grid_x_step=15)

# # By category
# # 5x5
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, [muscle_name], "Abduction", "F insertion direction", composante_y_muscle_combined=["AP"], legend_position="center left", figsize=[24, 13])
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, [muscle_name], "Abduction", "F insertion direction", composante_y_muscle_combined=["IS"], legend_position="center left", figsize=[24, 13])
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, [muscle_name], "Abduction", "F insertion direction", composante_y_muscle_combined=["ML"], legend_position="center left", figsize=[24, 13])

# %% Moment arm

"""toutes les fibres"""
# 25 cas
# PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial, AllMuscles_List, "Abduction", "MomentArm", composante_y_muscle_combined=["Mean"], cases_on="all", grid_x_step=15, xlim=[0, 120], legend_position="center left")
# 9 cas
# PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial, AllMuscles_List, "Abduction", "MomentArm", composante_y_muscle_combined=["Mean"], cases_on=CaseNames_3, grid_x_step=15, xlim=[0, 120], legend_position="center left")

"""par catégories"""
# # Moment arm 25 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_actifs, [4, 3], "Abduction", "MomentArm", "Bras de levier : Muscles actifs (Ft > 10N)", composante_y=["Mean"], cases_on=CaseNames_5, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_peu_actif, [1, 3], "Abduction", "MomentArm", "Bras de levier : Muscles peu actifs (10 N > Ft > 5N)", composante_y=["Mean"], cases_on=CaseNames_5, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_inactifs, [3, 3], "Abduction", "MomentArm", "Bras de levier : Muscles inactifs (Ft < 5N)", composante_y=["Mean"], cases_on=CaseNames_5, figsize=[16, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])

# Moment arm 9 cas

# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_actifs, [4, 3], "Abduction", "MomentArm", "Bras de levier : Muscles actifs (Ft > 10N)", composante_y=["Mean"], cases_on=CaseNames_3, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_peu_actif, [1, 3], "Abduction", "MomentArm", "Bras de levier : Muscles peu actifs (10 N > Ft > 5N)", composante_y=["Mean"], cases_on=CaseNames_3, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_inactifs, [3, 3], "Abduction", "MomentArm", "Bras de levier : Muscles inactifs (Ft < 5N)", composante_y=["Mean"], cases_on=CaseNames_3, figsize=[16, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])

"""Muscles qui varient"""
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscle_variation, [4, 2], "Abduction", "MomentArm", "Bras de levier : Muscles qui varient", composante_y=["Mean"], cases_on=CaseNames_5, figsize=[14, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])

"""Par catégories"""
# # Ft rassemblé par catégories sans les parties des muscles
# PremadeGraphs.muscle_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_5, list_muscle_variation, "Abduction", "MomentArm", legend_position="center left", composante_y_muscle_combined=["Mean"], figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# %% Force totales sur la scapula et l'humérus

"""Forces totales sur l'humérus"""
# # 25 cas
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal humerus", "Force totale sur l'humérus", composante_y=["AP"], subplot_title="AP", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [1, 3], "number": 1})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal humerus", "Force totale sur l'humérus", composante_y=["IS"], subplot_title="IS", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [1, 3], "number": 2})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal humerus", "Force totale sur l'humérus", composante_y=["ML"], subplot_title="ML", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [1, 3], "number": 3}, same_lim=True, grid_x_step=15)

# # 9 cas
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal humerus", "Force totale sur l'humérus", composante_y=["AP"], subplot_title="AP", cases_on=CaseNames_3, legend_position="center left", subplot={"dimension": [1, 3], "number": 1})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal humerus", "Force totale sur l'humérus", composante_y=["IS"], subplot_title="IS", cases_on=CaseNames_3, legend_position="center left", subplot={"dimension": [1, 3], "number": 2})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal humerus", "Force totale sur l'humérus", composante_y=["ML"], subplot_title="ML", cases_on=CaseNames_3, legend_position="center left", subplot={"dimension": [1, 3], "number": 3}, same_lim=True, grid_x_step=15)

# # Par variables
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal humerus", "Force totale sur l'humérus AP", composante_y=["AP"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal humerus", "Force totale sur l'humérus IS", composante_y=["IS"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal humerus", "Force totale sur l'humérus ML", composante_y=["ML"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])

# # Par variables
# # 3x3
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal humerus", "Force totale sur l'humérus AP", composante_y=["AP"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal humerus", "Force totale sur l'humérus IS", composante_y=["IS"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal humerus", "Force totale sur l'humérus ML", composante_y=["ML"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])

"""Forces totales sur la scapula"""
# # 25 cas
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal scapula", "Force totale sur la scapula", composante_y=["AP"], subplot_title="AP", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [1, 3], "number": 1})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal scapula", "Force totale sur la scapula", composante_y=["IS"], subplot_title="IS", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [1, 3], "number": 2})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal scapula", "Force totale sur la scapula", composante_y=["ML"], subplot_title="ML", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [1, 3], "number": 3}, same_lim=True, grid_x_step=15)

# # 9 cas
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal scapula", "Force totale sur la scapula", composante_y=["AP"], subplot_title="AP", cases_on=CaseNames_3, legend_position="center left", subplot={"dimension": [1, 3], "number": 1})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal scapula", "Force totale sur la scapula", composante_y=["IS"], subplot_title="IS", cases_on=CaseNames_3, legend_position="center left", subplot={"dimension": [1, 3], "number": 2})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "FTotal scapula", "Force totale sur la scapula", composante_y=["ML"], subplot_title="ML", cases_on=CaseNames_3, legend_position="center left", subplot={"dimension": [1, 3], "number": 3}, same_lim=True, grid_x_step=15)

# # Par variables
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal scapula", "Force totale sur la scapula AP", composante_y=["AP"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal scapula", "Force totale sur la scapula IS", composante_y=["IS"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal scapula", "Force totale sur la scapula ML", composante_y=["ML"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal scapula", "Force totale sur la scapula ML", composante_y=["ML"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])

"""Force totale des muscles"""
# # Par variables
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal muscles", "Force totale muscles sur l'humérus AP", composante_y=["AP"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal muscles", "Force totale muscles sur l'humérus IS", composante_y=["IS"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal muscles", "Force totale muscles sur l'humérus ML", composante_y=["ML"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])

# # # Par variables
# # # 3x3
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal muscles", "Force totale muscles sur l'humérus AP", composante_y=["AP"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal muscles", "Force totale muscles sur l'humérus IS", composante_y=["IS"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal muscles", "Force totale muscles sur l'humérus ML", composante_y=["ML"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])

"""Sans force de contact ajoutée"""
# # Par variables
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal humerus no Fcontact", "Force totale sur l'humérus  no Fcontact AP", composante_y=["AP"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal humerus no Fcontact", "Force totale sur l'humérus  no Fcontact IS", composante_y=["IS"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal humerus no Fcontact", "Force totale sur l'humérus  no Fcontact ML", composante_y=["ML"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])

# # Par variables
# # 3x3
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal humerus no Fcontact", "Force totale sur l'humérus  no Fcontact AP", composante_y=["AP"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal humerus no Fcontact", "Force totale sur l'humérus  no Fcontact IS", composante_y=["IS"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal humerus no Fcontact", "Force totale sur l'humérus  no Fcontact ML", composante_y=["ML"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])

"""Sans spring force"""
# # Par variables
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal humerus no SpringForce", "Force totale sur l'humérus no SpringForce AP", composante_y=["AP"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal humerus no SpringForce", "Force totale sur l'humérus no SpringForce IS", composante_y=["IS"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "FTotal humerus no SpringForce", "Force totale sur l'humérus no SpringForce ML", composante_y=["ML"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])

# # Par variables
# # 3x3
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal humerus no SpringForce", "Force totale sur l'humérus no SpringForce AP", composante_y=["AP"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal humerus no SpringForce", "Force totale sur l'humérus no SpringForce IS", composante_y=["IS"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "FTotal humerus no SpringForce", "Force totale sur l'humérus no SpringForce ML", composante_y=["ML"], legend_position="center left", same_lim=True, grid_x_step=15, figsize=[26, 16])


# %% Déplacement de la scapula

# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "Scapula position", "Position de la scapula", composante_y=["AP"], subplot_title="Latéral AP", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [2, 3], "number": 1})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "Scapula position", "Position de la scapula", composante_y=["IS"], subplot_title="Latéral IS", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [2, 3], "number": 2})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "Scapula position", "Position de la scapula", composante_y=["ML"], subplot_title="Latéral ML", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [2, 3], "number": 3})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "Scapula position2", "Position de la scapula", composante_y=["AP"], subplot_title="Médial AP", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [2, 3], "number": 4})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "Scapula position2", "Position de la scapula", composante_y=["IS"], subplot_title="Médial IS", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [2, 3], "number": 5})
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "Scapula position2", "Position de la scapula", composante_y=["ML"], subplot_title="Médial ML", cases_on=CaseNames_5, legend_position="center left", subplot={"dimension": [2, 3], "number": 6})

# %% Spring force

# # Forces par catégories par composantes
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "SpringForce humerus", "Springforce sur l'humérus AP dans le repère de la scapula", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "SpringForce humerus", "Springforce sur l'humérus IS dans le repère de la scapula", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "SpringForce humerus", "Springforce sur l'humérus ML dans le repère de la scapula", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# %% Small abduction no recentrage

# # Style avec des croix car nstep=1
# define_simulations_line_style(SimulationsLineStyleDictionary_Small_abduction)

# Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, "FTotal humerus no SpringForce", ["Total", "AP", "IS", "ML"], "Force totale sur l'humérus no SpringForce [N]", variables_to_add_humerus_no_springforce, muscle_variables_to_add_humerus)
# Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, "FTotal muscles", ["Total", "AP", "IS", "ML"], "Force totale des muscles sur l'humérus [N]", muscle_variables_to_add=muscle_variables_to_add_humerus)
# Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, "FTotal humerus no Fcontact", ["Total", "AP", "IS", "ML"], "Force totale sur l'humérus no Fcontact [N]", variables_to_add_humerus_no_fcontact, muscle_variables_to_add_humerus)
# Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, "FTotal humerus", ["Total", "AP", "IS", "ML"], "Force totale sur l'humérus [N]", variables_to_add_humerus, muscle_variables_to_add_humerus)
# Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage = sum_result_variables(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, "FTotal scapula", ["Total", "AP", "IS", "ML"], "Force totale sur la scapula [N]", variables_to_add_scapula, muscle_variables_to_add_scapula)

# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, COP_contour, "COP", "COP sans recentrage", composantes=["AP", "IS"], figsize=[24, 13], graph_annotation_on=False)

# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "ForceContact", "Force de contact humérus AP", composante_y=["AP"], figsize=[24, 13], xlim=[0, 30], same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "ForceContact", "Force de contact humérus IS", composante_y=["IS"], figsize=[24, 13], xlim=[0, 30], same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "ForceContact", "Force de contact humérus ML", composante_y=["ML"], figsize=[24, 13], xlim=[0, 30], same_lim=True)

"""Forces totales sur l'humérus"""
# # Par variables
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal humerus", "Force totale sur l'humérus AP", composante_y=["AP"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal humerus", "Force totale sur l'humérus IS", composante_y=["IS"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal humerus", "Force totale sur l'humérus ML", composante_y=["ML"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])

"""Force totale des muscles"""
# # Par variables
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal muscles", "Force totale muscles sur l'humérus AP", composante_y=["AP"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal muscles", "Force totale muscles sur l'humérus IS", composante_y=["IS"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal muscles", "Force totale muscles sur l'humérus ML", composante_y=["ML"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])

"""Sans force de contact ajoutée"""
# # Par variables
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal humerus no Fcontact", "Force totale sur l'humérus  no Fcontact AP", composante_y=["AP"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal humerus no Fcontact", "Force totale sur l'humérus  no Fcontact IS", composante_y=["IS"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal humerus no Fcontact", "Force totale sur l'humérus  no Fcontact ML", composante_y=["ML"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])

"""Sans spring force"""
# # Par variables
# # 5x5
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal humerus no SpringForce", "Force totale sur l'humérus no SpringForce AP", composante_y=["AP"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal humerus no SpringForce", "Force totale sur l'humérus no SpringForce IS", composante_y=["IS"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "FTotal humerus no SpringForce", "Force totale sur l'humérus no SpringForce ML", composante_y=["ML"], legend_position="center left", xlim=[0, 30], same_lim=True, grid_x_step=15, figsize=[26, 16])

# define_simulations_line_style(SimulationsLineStyleDictionary)

# %% Fixed Hill parameters

# COP_graph(Results_GlenoidLocalAxis_MR_Polynomial_Fixed_Hill, COP_contour, variable="COP", composantes=["AP", "IS"], figure_title="COP en fixant paramètres de Hill", cases_on="all")


# case_names = ["down-short", "down-normal", "down-long", "middle-short", "middle-normal", "middle-long", "up-short", "up-normal", "up-long"]

# comp = {"Normal": Results_GlenoidLocalAxis_MR_Polynomial, "Fixed Hill parameters": Results_GlenoidLocalAxis_MR_Polynomial_Fixed_Hill}

# # COP
# for ind, case in enumerate(CaseNames_3):
#     COP_graph(comp, COP_contour, variable="COP", composantes=["AP", "IS"], figure_title="Effet de fixer les paramètres de Hill", cases_on=[case], compare=True, subplot={"dimension": [3, 3], "number": ind + 1}, figsize=[28, 16], subplot_title=case)

# # Translation
# for ind, case in enumerate(CaseNames_3):
#     COP_graph(comp, COP_contour, variable="GHLin ISB", composantes=["AP", "IS"], figure_title="Effet de fixer les paramètres de Hill", cases_on=[case], compare=True, subplot={"dimension": [3, 3], "number": ind + 1}, figsize=[28, 16], subplot_title=case)

# # force de contact
# for ind, case in enumerate(CaseNames_3):
#     graph(comp, "Abduction", "ForceContact", figure_title="Effet de fixer les paramètres de Hill", cases_on=[case], compare=True, subplot={"dimension": [3, 3], "number": ind + 1}, figsize=[28, 16], subplot_title=case)

# # Muscles
# for ind, case in enumerate(CaseNames_3):
#     PremadeGraphs.muscle_graph_from_list(comp, list_muscles_actifs, [4, 3], "Abduction", "Ft", figure_title=f"{case} : Force musculaire : Effet de fixer les paramètres de Hill", cases_on=[case], compare=True, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)
#     PremadeGraphs.muscle_graph_from_list(comp, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", figure_title=f"{case} : Force musculaire : Effet de fixer les paramètres de Hill", cases_on=[case], compare=True, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)
#     PremadeGraphs.muscle_graph_from_list(comp, list_muscles_inactifs, [3, 3], "Abduction", "Ft", figure_title=f"{case} : Force musculaire : Effet de fixer les paramètres de Hill", cases_on=[case], compare=True, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)
# %% Better initialpos

# comp = {"Normal": Results_GlenoidLocalAxis_MR_Polynomial, "Better initialpos": Results_GlenoidLocalAxis_MR_Polynomial_Better_Initialpos}

# COP
# for ind, case in enumerate(CaseNames_3):
#     COP_graph(comp, COP_contour, variable="COP", composantes=["AP", "IS"], figure_title="Better initialpos", cases_on=[case], compare=True, subplot={"dimension": [3, 3], "number": ind + 1}, figsize=[28, 16], subplot_title=case)

# # Translation
# for ind, case in enumerate(CaseNames_3):
#     COP_graph(comp, COP_contour, variable="GHLin ISB", composantes=["AP", "IS"], figure_title="Effet de fixer les paramètres de Hill", cases_on=[case], compare=True, subplot={"dimension": [3, 3], "number": ind + 1}, figsize=[28, 16], subplot_title=case)

# # force de contact
# for ind, case in enumerate(CaseNames_3):
#     graph(comp, "Abduction", "ForceContact", figure_title="Effet de fixer les paramètres de Hill", cases_on=[case], compare=True, subplot={"dimension": [3, 3], "number": ind + 1}, figsize=[28, 16], subplot_title=case)

# Muscles
# for ind, case in enumerate(CaseNames_5):
#     PremadeGraphs.muscle_graph_from_list(comp, list_muscles_actifs, [4, 3], "Abduction", "Ft", figure_title=f"{case} : Force musculaire : Effet de fixer les paramètres de Hill", cases_on=[case], compare=True, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)
#     PremadeGraphs.muscle_graph_from_list(comp, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", figure_title=f"{case} : Force musculaire : Effet de fixer les paramètres de Hill", cases_on=[case], compare=True, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)
#     PremadeGraphs.muscle_graph_from_list(comp, list_muscles_inactifs, [3, 3], "Abduction", "Ft", figure_title=f"{case} : Force musculaire : Effet de fixer les paramètres de Hill", cases_on=[case], compare=True, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)

# %% Moyenne par CSA

# result_dictionary = {key: result_dictionary[key] for key in CaseNames_3}
combine_cases = {"CSA=12°": CSA_12_Cases,
                 "CSA=16°": CSA_16_Cases,
                 "CSA=20°": CSA_20_Cases,
                 "CSA=25°": CSA_25_Cases,
                 "CSA=30°": CSA_30_Cases,
                 "CSA=35°": CSA_35_Cases,
                 "CSA=40°": CSA_40_Cases,
                 "CSA=45°": CSA_45_Cases,
                 "CSA=50°": CSA_50_Cases
                 }

Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA = combine_simulation_cases(Results_GlenoidLocalAxis_MR_Polynomial, combine_cases, "mean")
Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage_Par_CSA = combine_simulation_cases(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, combine_cases, "mean")
Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage_Par_CSA = {**Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage_Par_CSA, **Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage}

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

"""Résultats"""
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", figure_title="Force de contact rassemblé par CSA", cases_on=list_csa_long, subplot={"dimension": [1, 2], "number": 1}, subplot_title="Force de contact")
# COP_graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, COP_contour, variable="COP", composantes=["AP", "IS"], figure_title="COP rassemblés par CSA", cases_on=list_csa_long, subplot={"dimension": [1, 2], "number": 2}, subplot_title="COP")

# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", figure_title="Force de contact rassemblé par CSA", cases_on="all", subplot={"dimension": [1, 2], "number": 1}, subplot_title="Force de contact")
# COP_graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, COP_contour, variable="COP", composantes=["AP", "IS"], figure_title="COP rassemblés par CSA", cases_on="all", subplot={"dimension": [1, 2], "number": 2}, subplot_title="COP")

# # ForceContact
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["Total"], figure_title="Forces de contact par CSA", subplot_title="Total", cases_on="all", subplot={"dimension": [2, 2], "number": 1}, figsize=[16, 20], grid_x_step=15, errorbar=False, errorevery=14, error_capsize=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["AP"], figure_title="Forces de contact par CSA", subplot_title="AP", cases_on="all", subplot={"dimension": [2, 2], "number": 2}, figsize=[13, 16], grid_x_step=15, errorbar=False, errorevery=14, error_capsize=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["IS"], figure_title="Forces de contact par CSA", subplot_title="IS", cases_on="all", subplot={"dimension": [2, 2], "number": 3}, figsize=[13, 16], grid_x_step=15, errorbar=False, errorevery=14, error_capsize=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["ML"], figure_title="Forces de contact par CSA", subplot_title="ML", cases_on="all", subplot={"dimension": [2, 2], "number": 4}, figsize=[13, 16], grid_x_step=15, legend_position="center left", errorbar=False, errorevery=14, error_capsize=5)

# # ForceContact dans le repère de la scapula
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact scapula", composante_y=["Total"], figure_title="Forces de contact dans le repère de la scapula par CSA", subplot_title="Total", cases_on="all", subplot={"dimension": [2, 2], "number": 1}, figsize=[16, 20], grid_x_step=15, errorbar=False, errorevery=14, error_capsize=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact scapula", composante_y=["AP"], figure_title="Forces de contact dans le repère de la scapula  par CSA", subplot_title="AP", cases_on="all", subplot={"dimension": [2, 2], "number": 2}, figsize=[13, 16], grid_x_step=15, errorbar=False, errorevery=14, error_capsize=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact scapula", composante_y=["IS"], figure_title="Forces de contact dans le repère de la scapula  par CSA", subplot_title="IS", cases_on="all", subplot={"dimension": [2, 2], "number": 3}, figsize=[13, 16], grid_x_step=15, errorbar=False, errorevery=14, error_capsize=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact scapula", composante_y=["ML"], figure_title="Forces de contact dans le repère de la scapula  par CSA", subplot_title="ML", cases_on="all", subplot={"dimension": [2, 2], "number": 4}, figsize=[13, 16], grid_x_step=15, legend_position="center left", errorbar=False, errorevery=14, error_capsize=5)

# # COP
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["Total"], figure_title="COP par CSA", subplot_title="Total", cases_on="all", subplot={"dimension": [2, 2], "number": 1}, figsize=[16, 20], grid_x_step=15, errorbar=False, errorevery=14, error_capsize=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["AP"], figure_title="COP par CSA", subplot_title="AP", cases_on="all", subplot={"dimension": [2, 2], "number": 2}, figsize=[13, 16], grid_x_step=15, errorbar=False, errorevery=14, error_capsize=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["IS"], figure_title="COP par CSA", subplot_title="IS", cases_on="all", subplot={"dimension": [2, 2], "number": 3}, figsize=[13, 16], grid_x_step=15, errorbar=False, errorevery=14, error_capsize=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["ML"], figure_title="COP par CSA", subplot_title="ML", cases_on="all", subplot={"dimension": [2, 2], "number": 4}, figsize=[13, 16], grid_x_step=15, legend_position="center left", errorbar=False, errorevery=14, error_capsize=5)

# # Muscles
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Force musculaire : Muscles actifs (Ft > 10N)", cases_on="all", figsize=[24, 14], xlim=[0, 120], ylim=[0, 200], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Force musculaire : Muscles peu actifs (10 N > Ft > 5N)", cases_on="all", figsize=[24, 14], xlim=[0, 120], ylim=[0, 20], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Force musculaire : Muscles inactifs (Ft < 5N)", cases_on="all", figsize=[16, 14], xlim=[0, 120], ylim=[0, 20], legend_position="center left", grid_x_step=15)

# # Muscles sans same_lim
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Force musculaire : Muscles actifs (Ft > 10N)", cases_on="all", figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Force musculaire : Muscles peu actifs (10 N > Ft > 5N)", cases_on="all", figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Force musculaire : Muscles inactifs (Ft < 5N)", cases_on="all", figsize=[16, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)


"""Ecarts types"""
# # ForceContact
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["sd_Total"], figure_title="Ecart types des forces de contact par CSA", subplot_title="Total", cases_on=list_csa_long, subplot={"dimension": [2, 2], "number": 1}, figsize=[16, 20], grid_x_step=15)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["sd_AP"], figure_title="Ecart types des forces de contact par CSA", subplot_title="AP", cases_on=list_csa_long, subplot={"dimension": [2, 2], "number": 2}, figsize=[13, 16], grid_x_step=15)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["sd_IS"], figure_title="Ecart types des forces de contact par CSA", subplot_title="IS", cases_on=list_csa_long, subplot={"dimension": [2, 2], "number": 3}, figsize=[13, 16], grid_x_step=15)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["sd_ML"], figure_title="Ecart types des forces de contact par CSA", subplot_title="ML", cases_on=list_csa_long, subplot={"dimension": [2, 2], "number": 4}, figsize=[13, 16], grid_x_step=15, legend_position="center left")

# # COP
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["sd_Total"], figure_title="Ecart types COP par CSA", subplot_title="Total", cases_on=list_csa_long, subplot={"dimension": [2, 2], "number": 1}, figsize=[16, 20], grid_x_step=15)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["sd_AP"], figure_title="Ecart types COP par CSA", subplot_title="AP", cases_on=list_csa_long, subplot={"dimension": [2, 2], "number": 2}, figsize=[13, 16], grid_x_step=15)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["sd_IS"], figure_title="Ecart types COP par CSA", subplot_title="IS", cases_on=list_csa_long, subplot={"dimension": [2, 2], "number": 3}, figsize=[13, 16], grid_x_step=15)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["sd_ML"], figure_title="Ecart types COP par CSA", subplot_title="ML", cases_on=list_csa_long, subplot={"dimension": [2, 2], "number": 4}, figsize=[13, 16], grid_x_step=15, legend_position="center left")

# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Ecarts-types : Force musculaire : Muscles actifs (Ft > 10N)", composante_y=["sd_Total"], cases_on=list_csa_long, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, grid_y_step=5, same_lim=True, ylim=[0, 30])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Ecarts-types : Force musculaire : Muscles peu actifs (10 N > Ft > 5N)", composante_y=["sd_Total"], cases_on=list_csa_long, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Ecarts-types : Force musculaire : Muscles inactifs (Ft < 5N)", composante_y=["sd_Total"], cases_on=list_csa_long, figsize=[16, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True)

"""Valeurs avec errorbars"""
# # ForceContact
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["Total"], figure_title="Forces de contact par CSA", subplot_title="Total", cases_on=list_csa_short, subplot={"dimension": [2, 2], "number": 1}, figsize=[16, 20], grid_x_step=15, errorbar=True, errorevery=14, error_capsize=8, error_capthick=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["AP"], figure_title="Forces de contact par CSA", subplot_title="AP", cases_on=list_csa_short, subplot={"dimension": [2, 2], "number": 2}, figsize=[13, 16], grid_x_step=15, errorbar=True, errorevery=14, error_capsize=8, error_capthick=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["IS"], figure_title="Forces de contact par CSA", subplot_title="IS", cases_on=list_csa_short, subplot={"dimension": [2, 2], "number": 3}, figsize=[13, 16], grid_x_step=15, errorbar=True, errorevery=14, error_capsize=8, error_capthick=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "ForceContact", composante_y=["ML"], figure_title="Forces de contact par CSA", subplot_title="ML", cases_on=list_csa_short, subplot={"dimension": [2, 2], "number": 4}, figsize=[13, 16], grid_x_step=15, legend_position="center left", errorbar=True, errorevery=14, error_capsize=8, error_capthick=5)

# # COP
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["Total"], figure_title="COP par CSA", subplot_title="Total", cases_on=list_csa_short, subplot={"dimension": [2, 2], "number": 1}, figsize=[16, 20], grid_x_step=15, errorbar=True, errorevery=14, error_capsize=8, error_capthick=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["AP"], figure_title="COP par CSA", subplot_title="AP", cases_on=list_csa_short, subplot={"dimension": [2, 2], "number": 2}, figsize=[13, 16], grid_x_step=15, errorbar=True, errorevery=14, error_capsize=8, error_capthick=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["IS"], figure_title="COP par CSA", subplot_title="IS", cases_on=list_csa_short, subplot={"dimension": [2, 2], "number": 3}, figsize=[13, 16], grid_x_step=15, errorbar=True, errorevery=14, error_capsize=8, error_capthick=5)
# graph(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, "Abduction", "COP", composante_y=["ML"], figure_title="COP par CSA", subplot_title="ML", cases_on=list_csa_short, subplot={"dimension": [2, 2], "number": 4}, figsize=[13, 16], grid_x_step=15, legend_position="center left", errorbar=True, errorevery=14, error_capsize=8, error_capthick=5)

# # Muscles
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Ecarts-types : Force musculaire : Muscles actifs (Ft > 10N)", composante_y=["Total"], cases_on=list_csa_short, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, errorbar=True, errorevery=14, error_capsize=8, error_capthick=5)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Ecarts-types : Force musculaire : Muscles peu actifs (10 N > Ft > 5N)", composante_y=["Total"], cases_on=list_csa_long, figsize=[24, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True, errorbar=True, errorevery=14, error_capsize=8, error_capthick=5)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_Par_CSA, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Ecarts-types : Force musculaire : Muscles inactifs (Ft < 5N)", composante_y=["Total"], cases_on=list_csa_long, figsize=[16, 14], xlim=[15, 120], legend_position="center left", grid_x_step=15, same_lim=True, errorbar=True, errorevery=14, error_capsize=8, error_capthick=5)

# %% Recentrage force constante

# comp = {"Normal": Results_GlenoidLocalAxis_MR_Polynomial, "no recentrage": Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage}

# for case in CaseNames_3:
#     graph(comp, "Abduction", "ForceContact GlenImplant", f"{case} : Forces de contact Totale sur l'implant glénoidien", composante_y=["Total"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True, compare=True, cases_on=[case])
#     PremadeGraphs.muscle_graph_from_list(comp, list_muscles_actifs, [3, 4], "Abduction", "Ft", f"{case}", cases_on=[case], compare=True, figsize=[24, 14])


# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "ForceContact GlenImplant", "Forces de contact Totale sur l'implant glénoidien dans le repère de la glène", composante_y=["Total"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "ForceContact GlenImplant", "Forces de contact AP sur l'implant glénoidien dans le repère de la glène", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "ForceContact GlenImplant", "Forces de contact IS sur l'implant glénoidien dans le repère de la glène", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, "Abduction", "ForceContact GlenImplant", "Forces de contact ML sur l'implant glénoidien dans le repère de la glène", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13])


# # par catégories tilt et acromion
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, None, figure_title="Déplacement absolu de la tête humérale (GHLin Absolute)", variable="GHLin Absolute", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], graph_annotation_on=False, xlim=[-2, 5], ylim=[0, 20])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, None, figure_title="Sans recentrage : Déplacement absolu de la tête humérale (GHLin Absolute)", variable="GHLin Absolute", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], graph_annotation_on=False, xlim=[-2, 5], ylim=[0, 20])


# # no recentrage
# # Translations absolues
# # mis à zéro
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, CasesVariables_5, None, figure_title="Sans recentrage : Déplacement absolu de la tête humérale (GHLin Absolute zero)", variable="GHLin Absolute zero", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], graph_annotation_on=False, xlim=[-2, 5], ylim=[0, 20])
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, None, figure_title="Déplacement absolu de la tête humérale (GHLin Absolute zero)", variable="GHLin Absolute zero", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], graph_annotation_on=False, xlim=[-2, 5], ylim=[0, 20])


# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, figure_title="Déplacement absolu de la tête humérale (GHLin Absolute zero)", variable_x="Abduction", variable_y="GHLin Absolute zero", composante_y=["IS"], legend_position="center left", figsize=[24, 13], graph_annotation_on=False, same_lim=True)


# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, None, figure_title="Sans recentrage : Déplacement absolu de la tête humérale (GHLin Absolute)", variable="GHLin Absolute", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], graph_annotation_on=False, same_lim=True)
# # mis à zéro
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, None, figure_title="Sans recentrage : Déplacement absolu de la tête humérale (GHLin Absolute zero)", variable="GHLin Absolute zero", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], graph_annotation_on=False, same_lim=True)


# %% Pénétration maximale des implants

# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "MaxPenetration", "MaxPenetration", cases_on=CaseNames_3)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "MaxPenetration", "MaxPenetration", legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

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
"""Normal (done)"""
# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_Polynomial, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Abduction", "Normal", save_graph=True, composante_on=False, **graph_parameters)
# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Abduction", "No recentrage", save_graph=True, composante_on=False, **graph_parameters)

"""Par CSA"""


# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage_Par_CSA, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Abduction/No recentrage", "Par CSA", save_graph=True, composante_on=False, **graph_parameters_par_CSA)


"""Elevation (done)"""
# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_Polynomial_Elevation, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Elevation", "Normal", save_graph=True, composante_on=False, **graph_parameters)
# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Elevation", "No recentrage", save_graph=True, composante_on=False, **graph_parameters)


# PremadeGraphs.my_graphs(Results_GlenoidLocalAxis_MR_MinMaxStrics_Elevation_no_recentrage, Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"], Results_literature, "Graphiques/Elevation", "MinMax No recentrage", save_graph=True, composante_on=False, **graph_parameters_3)


# %% 140 deg no recentrage

# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_140deg_no_recentrage, CasesVariables_3, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13])

# graph(Results_GlenoidLocalAxis_MR_Polynomial_140deg_no_recentrage, "Abduction", "ForceTolError", cases_on="all")
# %% Stability ratio

for case in Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage:
    Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage[case]["ForceContact GlenImplant"]["Shear"] = Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage[case]["ForceContact GlenImplant"]["IS"] + Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage[case]["ForceContact GlenImplant"]["AP"]

    Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage[case]["Stability Ratio"] = {"Description": "Stability ratio", "SequenceComposantes": "Total"}
    Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage[case]["Stability Ratio"]["Total"] = Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage[case]["ForceContact GlenImplant"]["Shear"] / abs(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage[case]["ForceContact GlenImplant"]["ML"])


# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, CasesVariables_3, "Abduction", "Stability Ratio", figure_title="Stability ratio", xlim=[15, 120], same_lim=True)
# PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, CasesVariables_5, "Abduction", "Stability Ratio", figure_title="Stability ratio", xlim=[15, 120], same_lim=True, figsize=[24, 14])

# graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "Stability Ratio", figure_title="Stability ratio", xlim=[15, 120], same_lim=True, figsize=[24, 14], cases_on=CaseNames_3)

# %% Figures article

SimulationsLineStyleDictionary_article = {
    # Glen xdown
    "xdown-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 1.5},
    "xdown-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "xdown-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 1.5},
    "xdown-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "xdown-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},

    # Glen xdown
    "middle-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 1.5},
    "middle-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "middle-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 1.5},
    "middle-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "middle-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},

    # Glen xdown
    "xup-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 1.5},
    "xup-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "xup-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 1.5},
    "xup-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "xup-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},
}
define_simulations_line_style(SimulationsLineStyleDictionary_article)

# Article
# PremadeGraphs.COP_graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, CasesVariables_Tilt_3_Acromion_3, COP_contour, composantes=["AP", "IS"], graph_annotation_on=False, draw_COP_points_on=False, COP_first_point_size=10, COP_first_point_mew=2, grid_x_step=5, grid_y_step=5, xlim=[-15, 15], ylim=[-20, 20], annotation_offset=[1.3, -3], annotation_reference_offset=[1, 1], COP_points_step=30)


# grid_steps_y = [50, 25, 50, 50]
# y_lims = {"Total": [0, 500],
#           "AP": [-50, 100],
#           "IS": [-150, 200],
#           "ML": [-500, 0]
#           }

# for ind, composante in enumerate(["Total", "AP", "IS", "ML"]):
#     graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", figure_title=f"{composante}", subplot_title="Downtilt", composante_y=[composante], cases_on=["xdown-xshort", "xdown-normal", "xdown-xlong"], subplot={"dimension": [1, 3], "number": 1})
#     graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", figure_title=f"{composante}", subplot_title="Middle tilt", composante_y=[composante], cases_on=["middle-xshort", "middle-normal", "middle-xlong"], subplot={"dimension": [1, 3], "number": 2})
#     graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, "Abduction", "ForceContact GlenImplant", figure_title=f"{composante}", subplot_title="Uptilt", composante_y=[composante], cases_on=["xup-xshort", "xup-normal", "xup-xlong"], subplot={"dimension": [1, 3], "number": 3}, same_lim=True, grid_x_step=15, xlim=[15, 120], ylim=y_lims[composante], grid_y_step=grid_steps_y[ind])

# instability ratio
PremadeGraphs.graph_by_case_categories(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, CasesVariables_Tilt_3_Acromion_3, "Abduction", "Stability Ratio", figure_title="Stability ratio", xlim=[15, 120], same_lim=True)


SimulationsLineStyleDictionary_abstract = {
    # Glen xdown
    "xdown-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 3.5},
    "xdown-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "xdown-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3.5},
    "xdown-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "xdown-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 4.5},

    # Glen xdown
    "middle-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 3.5},
    "middle-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "middle-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3.5},
    "middle-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "middle-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 4.5},

    # Glen xdown
    "xup-xshort": {"color": "#332288", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 3.5},
    "xup-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "xup-normal": {"color": "#117733", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3.5},
    "xup-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "xup-xlong": {"color": "#AA4499", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 4.5},
}

define_simulations_line_style(SimulationsLineStyleDictionary_abstract)

# # Abstract
# COP_graph(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, COP_contour, figure_title="Downtilt", composantes=["AP", "IS"], cases_on=["xdown-xshort", "xdown-normal", "xdown-xlong"], graph_annotation_on=False, draw_COP_points_on=False, COP_first_point_size=20, COP_first_point_mew=4)
# COP_graph(Results_GlenoidLocalAxis_MR_Polynomial_no_recentrage, COP_contour, figure_title="Uptilt", composantes=["AP", "IS"], cases_on=["xup-xshort", "xup-normal", "xup-xlong"], graph_annotation_on=False, draw_COP_points_on=False, COP_first_point_size=20, COP_first_point_mew=4)

# COP_graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, COP_contour, figure_title="Downtilt", composantes=["AP", "IS"], cases_on=["xdown-xshort", "xdown-normal", "xdown-xlong"], graph_annotation_on=False, draw_COP_points_on=False, COP_first_point_size=20, COP_first_point_mew=4)
# COP_graph(Results_GlenoidLocalAxis_MR_Polynomial_Elevation_no_recentrage, COP_contour, figure_title="Uptilt", composantes=["AP", "IS"], cases_on=["xup-xshort", "xup-normal", "xup-xlong"], graph_annotation_on=False, draw_COP_points_on=False, COP_first_point_size=20, COP_first_point_mew=4)


define_simulations_line_style(SimulationsLineStyleDictionary)
