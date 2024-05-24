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

from Anybody_Package.Anybody_LoadOutput.Tools import result_dictionary_to_excel

import my_graphs

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# %%                                                Chargement des résultats

# Chemin d'accès au dossier dans lequel les fichiers ont été sauvegardés
SaveSimulationsDirectory = "Saved Simulations"

Results_aTSA = load_results_from_file(SaveSimulationsDirectory, "Results_aTSA")
Results_BallAndSocket = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket")
Results_literature = load_results_from_file(SaveSimulationsDirectory, "Results_literature")

scores_moment = load_results_from_file(SaveSimulationsDirectory, "scores_moment")
scores_shear = load_results_from_file(SaveSimulationsDirectory, "scores_shear")

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
matplotlib.rcParams.update({'legend.fontsize': 15})

# Distance between the title of a plot and the plot in points (6)
matplotlib.rcParams.update({'axes.titlepad': 12})

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
    "Ball And Socket": {"color": "black", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},

    # data de validation
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
    "xdown-xshort": "CSA = 12° : -8.7° inclination    ; -12.1 mm acromion shift",
    "xdown-short": "CSA = 16° : -8.7° inclination    ; -6.6 mm acromion shift",
    "xdown-normal": "CSA = 20° : -8.7° inclination    ; +0.0 mm acromion shift",
    "xdown-long": "CSA = 25° : -8.7° inclination    ; +7.85 mm acromion shift",
    "xdown-xlong": "CSA = 30° : -8.7° inclination    ; +16.95 mm acromion shift",

    "down-xshort": "CSA = 16° : -3.0° inclination    ; -12.1 mm acromion shift",
    "down-short": "CSA = 20° : -3.0° inclination    ; -6.6 mm acromion shift",
    "down-normal": "CSA = 25° : -3.0° inclination    ; +0.0 mm acromion shift",
    "down-long": "CSA = 30° : -3.0° inclination    ; +7.85 mm acromion shift",
    "down-xlong": "CSA = 35° : -3.0° inclination    ; +16.95 mm acromion shift",

    "middle-xshort": "CSA = 20° : 2.9° inclination     ; -12.1 mm acromion shift",
    "middle-short": "CSA = 25° : 2.9° inclination     ; -6.6 mm acromion shift",
    "middle-normal": "CSA = 30° : 2.9° inclination     ; +0.0 mm acromion shift",
    "middle-long": "CSA = 35° : 2.9° inclination     ; +7.85 mm acromion shift",
    "middle-xlong": "CSA = 40° : 2.9° inclination     ; +16.95 mm acromion shift",

    "neutral-xshort": "CSA = 20° : 0.0° inclination     ; -12.1 mm acromion shift",
    "neutral-short": "CSA = 25° : 0.0° inclination     ; -6.6 mm acromion shift",
    "neutral-normal": "CSA = 30° : 0.0° inclination     ; +0.0 mm acromion shift",
    "neutral-long": "CSA = 35° : 0.0° inclination     ; +7.85 mm acromion shift",
    "neutral-xlong": "CSA = 40° : 0.0° inclination     ; +16.95 mm acromion shift",

    "up-xshort": "CSA = 25° : 9.0° inclination     ; -12.1 mm acromion shift",
    "up-short": "CSA = 30° : 9.0° inclination     ; -6.6 mm acromion shift",
    "up-normal": "CSA = 35° : 9.0° inclination     ; +0.0 mm acromion shift",
    "up-long": "CSA = 40° : 9.0° inclination     ; +7.85 mm acromion shift",
    "up-xlong": "CSA = 45° : 9.0° inclination     ; +16.95 mm acromion shift",

    "xup-xshort": "CSA = 30° : 15.2° inclination   ; -12.1 mm acromion shift",
    "xup-short": "CSA = 35° : 15.2° inclination   ; -6.6 mm acromion shift",
    "xup-normal": "CSA = 40° : 15.2° inclination   ; +0.0 mm acromion shift",
    "xup-long": "CSA = 45° : 15.2° inclination   ; +7.85 mm acromion shift",
    "xup-xlong": "CSA = 50° : 15.2° inclination   ; +16.95 mm acromion shift",

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
CaseNames_36x = [*xDownCases_3, *NeutralCases_3, *xUpCases_3]
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

# %% Liste des catégories de muscles

# 9 muscles --> graphique 3x3
Muscles_Main = ["Deltoid anterior",
                "Deltoid lateral",
                "Deltoid posterior",
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
Muscles_Variation = ["Deltoid anterior",
                     "Deltoid lateral",
                     "Deltoid posterior",
                     "Triceps long head"
                     ]

# Muscles for comparison with Wickham et al. data
# 3x3
Muscle_Comp_Main = ["Deltoid anterior",
                    "Deltoid lateral",
                    "Deltoid posterior",
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
Muscles_Comp_Variation = ["Deltoid anterior",
                          "Deltoid lateral",
                          "Deltoid posterior"
                          ]

Muscles_actifs = ["Deltoid lateral",
                  "Deltoid anterior",
                  "Deltoid posterior",
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

Muscles_Comp_actifs = ["Deltoid anterior",
                       "Deltoid lateral",
                       "Deltoid posterior",
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
list_muscles_actifs = ["Deltoid lateral",
                       "Deltoid anterior",
                       "Deltoid posterior",
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
list_muscle_variation = ["Deltoid anterior",
                         "Deltoid lateral",
                         "Deltoid posterior",
                         "Upper Subscapularis",
                         "Subscapularis",
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

# %% Graphiques toutes les variables

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
                    "COP_contour": COP_contour,

                    "hide_center_axis_labels": True

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
                      "COP_contour": COP_contour,

                      "hide_center_axis_labels": True
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
                      "COP_contour": COP_contour,

                      "hide_center_axis_labels": True
                      }

# Tous les résultats
# my_graphs.all_variables_graphs(Results_aTSA, Results_BallAndSocket["normal"], Results_literature, "Graphiques/aTSA", "Tous les résultats", save_graph=True, composante_on=False, **graph_parameters_6)

# %% Résultats classés par CSA et moyennes par CSA

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

# CSA
CasesVariables_CSA_9 = {"CSA Faible": {"CSA = 12°": CSA_12_Cases, "CSA = 16°": CSA_16_Cases, "CSA = 20°": CSA_20_Cases},
                        "CSA Moyen": {"CSA = 25°": CSA_25_Cases, "CSA = 30°": CSA_30_Cases, "CSA = 35°": CSA_35_Cases},
                        "CSA Élevé": {"CSA = 40°": CSA_40_Cases, "CSA = 45°": CSA_45_Cases, "CSA = 50°": CSA_50_Cases}}

# Les 6 qui sont dans la range de CSA
CasesVariables_CSA_6 = {"CSA Moyen": {"CSA = 20°": CSA_20_Cases, "CSA = 25°": CSA_25_Cases, "CSA = 30°": CSA_30_Cases},
                        "CSA Élevé": {"CSA = 35°": CSA_35_Cases, "CSA = 40°": CSA_40_Cases, "CSA = 45°": CSA_45_Cases}
                        }

# Liste des CSA
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
                            "COP_contour": COP_contour,

                            "hide_center_axis_labels": True
                            }

combine_CSA = {"CSA=12°": CSA_12_Cases, "CSA=16°": CSA_16_Cases, "CSA=20°": CSA_20_Cases,
               "CSA=25°": CSA_25_Cases, "CSA=30°": CSA_30_Cases, "CSA=35°": CSA_35_Cases,
               "CSA=40°": CSA_40_Cases, "CSA=45°": CSA_45_Cases, "CSA=50°": CSA_50_Cases}

# Fait la moyenne de toutes les variables par valeur de CSA
Results_aTSA_CSA = {**combine_simulation_cases(Results_aTSA, combine_CSA, operation="mean"), **Results_aTSA}

my_graphs.all_variables_graphs(Results_aTSA_CSA, Results_BallAndSocket["normal"], Results_literature, "Graphiques/aTSA", "Classé par CSA", save_graph=True, composante_on=False, **graph_parameters_par_CSA)

# %% Figures article

# my_graphs.figures_article(Results_aTSA, COP_contour, SimulationsLineStyleDictionary, list_muscles_actifs, CaseNames_36x, True)

# %% graph surface score


def score_surface(score_df, title):
    z = score_df.to_numpy(dtype="float64")

    acromion_x = np.array([-12.1, -6.6, 0, 7.85, 16.95])
    inclinaison_y = np.array([-8.7, -3.0, 0, 2.9, 9.0, 15.2])

    (x, y) = np.meshgrid(acromion_x, inclinaison_y)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=[12, 10])
    surf = ax.plot_surface(x, y, z, cmap=matplotlib.colormaps.get_cmap('RdYlGn_r'), linewidth=0.4, edgecolor="black")
    ax.set_proj_type('ortho')

    ax.tick_params(axis='x', which='major', pad=9)
    ax.tick_params(axis='y', which='major', pad=8)
    ax.tick_params(axis='z', which='major', pad=12)

    ax.set_xlim(-12.1, 16.95)
    ax.set_ylim(-8.7, 15.2)
    ax.set_zlim(0, np.max(z))
    ax.set_xticks(acromion_x)
    ax.set_yticks(inclinaison_y)

    ax.set_xlabel("Acromion lengthening [mm]", labelpad=15)
    ax.set_ylabel("Glenoin inclination [°]", labelpad=15)
    ax.set_zlabel(title, labelpad=22)
    ax.set_title(title)
    fig.colorbar(surf, shrink=0.5, aspect=9, pad=0.1)


# score_surface(scores_moment["Total"], "Total moment on the glenoid implant [N.m]")
# score_surface(scores_shear["Total"], "Total shear forces on the glenoid implant [N]")
