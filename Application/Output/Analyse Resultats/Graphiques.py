# import Anybody_LoadOutput.Tools as LoadOutputTools

from Anybody_Package.Anybody_LoadOutput.Tools import load_results_from_file

from Anybody_Package.Anybody_Graph.GraphFunctions import graph
from Anybody_Package.Anybody_Graph.GraphFunctions import COP_graph
from Anybody_Package.Anybody_Graph.GraphFunctions import muscle_graph
from Anybody_Package.Anybody_Graph.GraphFunctions import muscle_bar_plot
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
Results_aTSA_fr = load_results_from_file(SaveSimulationsDirectory, "Results_aTSA_fr")
Results_BallAndSocket = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket")
Results_literature = load_results_from_file(SaveSimulationsDirectory, "Results_literature")

scores_moment = load_results_from_file(SaveSimulationsDirectory, "scores_moment")
scores_shear = load_results_from_file(SaveSimulationsDirectory, "scores_shear")

# %% taille des textes dans les graphiques

# Contrôle de la taille de la police globale
matplotlib.rcParams.update({'font.size': 13})

# Contrôle des tailles de chaque partie partie du graphique
# Liste des paramètres que l'on peut changer :
# https://renenyffenegger.ch/notes/development/languages/Python/libraries/matplotlib/rcParams/list
# Default values available here : https://matplotlib.org/stable/users/explain/customizing.html

# Titre des cases des subplots (12)
matplotlib.rcParams.update({'axes.titlesize': 20})

# Titre du graphique (12)
matplotlib.rcParams.update({'figure.titlesize': 20})

# Nom des axes (10)
matplotlib.rcParams.update({'axes.labelsize': 20})

# Graduations des axes (10)
matplotlib.rcParams.update({'xtick.labelsize': 16})
matplotlib.rcParams.update({'ytick.labelsize': 16})

# Taille des graduations (3.5)
matplotlib.rcParams.update({'xtick.major.size': 8})
matplotlib.rcParams.update({'ytick.major.size': 8})

# Légende (10)
matplotlib.rcParams.update({'legend.fontsize': 18})

# Distance between the title of a plot and the plot in points (6)
matplotlib.rcParams.update({'axes.titlepad': 12})

# %% Setup des couleurs et légendes

# Définition des styles des simulations dans les graphiques (couleurs, forme de ligne taille...)
# Noms des couleurs : https://matplotlib.org/stable/gallery/color/named_colors.html
# Types de marqueurs : https://matplotlib.org/stable/api/markers_api.html
# Type de lignes : https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html

SimulationsLineStyleDictionary_article = {
    # Glen xdown
    "xdown-xshort": {"color": "#648FFF", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 2},
    "xdown-short": {"color": "#785EF0", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 2},
    "xdown-normal": {"color": "#DC267F", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},
    "xdown-long": {"color": "#FE6100", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},
    "xdown-xlong": {"color": "#FFB000", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},

    # Glen neutral
    "neutral-xshort": {"color": "#648FFF", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 2},
    "neutral-short": {"color": "#785EF0", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 2},
    "neutral-normal": {"color": "#DC267F", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},
    "neutral-long": {"color": "#FE6100", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},
    "neutral-xlong": {"color": "#FFB000", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},

    # Glen up
    "up-xshort": {"color": "#648FFF", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 2},
    "up-short": {"color": "#785EF0", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 2},
    "up-normal": {"color": "#DC267F", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 2},
    "up-long": {"color": "#FE6100", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},
    "up-xlong": {"color": "#FFB000", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2},

    "Ball And Socket": {"color": "black", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},
    "Joint Sphérique": {"color": "black", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},

}


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
    "neutral-normal": {"color": "grey", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 4},
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
    "Joint Sphérique": {"color": "black", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},

    # data de validation
    "Dal Maso superior": {"color": "black", "marker": "o", "markersize": 5, "linestyle": "-", "linewidth": 1},
    "Dal Maso inferior": {"color": "grey", "marker": "o", "markersize": 5, "linestyle": "-", "linewidth": 1},
    "Bergmann 2007": {"color": "black", "marker": "+", "markersize": 8, "linestyle": "-", "linewidth": 0.3},
    "Bergmann_2007": {"color": "black", "marker": "+", "markersize": 8, "linestyle": "-", "linewidth": 0.3},
    "Wickham": {"color": "darkorange", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3},

    "CSA=12°": {"color": 'violet', "linestyle": "--"},
    "CSA=16°": {"color": 'purple', "linestyle": "--"},
    "CSA=20°": {"color": 'lightblue', "linestyle": "--"},
    "CSA=23°": {"color": 'cornflowerblue', "linestyle": "--"},
    "CSA=31°": {"color": 'greenyellow', "linestyle": "-"},
    "CSA=36°": {"color": 'mediumseagreen', "linestyle": "-"},
    "CSA=40°": {"color": 'orange', "linestyle": "-."},
    "CSA=44°": {"color": 'red', "linestyle": "-."},
    "CSA=48°": {"color": 'darkred', "linestyle": "-."}

}

SimulationDescriptionDictionary = {
    # Nom des cas de simulation
    "xdown-xshort": "-10° inclination    ; -10.8 mm acromion length",
    "xdown-short": "-10° inclination    ; -5.7 mm acromion length",
    "xdown-normal": "-10° inclination    ; +0.0 mm acromion length",
    "xdown-long": "-10° inclination    ; +6.6 mm acromion length",
    "xdown-xlong": "-10° inclination    ; +13.4 mm acromion length",

    "down-xshort": "-5° inclination    ; -10.8 mm acromion length",
    "down-short": "-5° inclination    ; -5.7 mm acromion length",
    "down-normal": "-5° inclination    ; +0.0 mm acromion length",
    "down-long": "-5° inclination    ; +6.6 mm acromion length",
    "down-xlong": "-5° inclination    ; +13.4 mm acromion length",

    "middle-xshort": "5° inclination     ; -10.8 mm acromion length",
    "middle-short": "5° inclination     ; -5.7 mm acromion length",
    "middle-normal": "5° inclination     ; +0.0 mm acromion length",
    "middle-long": "5° inclination     ; +6.6 mm acromion length",
    "middle-xlong": "5° inclination     ; +13.4 mm acromion length",

    "neutral-xshort": "  0°  inclination    ; -10.8 mm acromion length",
    "neutral-short": "  0°  inclination    ; -5.7 mm acromion length",
    "neutral-normal": "  0°  inclination    ; +0.0 mm acromion length",
    "neutral-long": "  0°  inclination    ; +6.6 mm acromion length",
    "neutral-xlong": "  0°  inclination    ; +13.4 mm acromion length",

    "up-xshort": "10° inclination     ; -10.8 mm acromion length",
    "up-short": "10° inclination     ; -5.7 mm acromion length",
    "up-normal": "10° inclination     ; +0.0 mm acromion length",
    "up-long": "10° inclination     ; +6.6 mm acromion length",
    "up-xlong": "10° inclination     ; +13.4 mm acromion length",

    "xup-xshort": "15°  inclination    ; -10.8 mm acromion length",
    "xup-short": "15°  inclination    ; -5.7 mm acromion length",
    "xup-normal": "15°  inclination    ; +0.0 mm acromion length",
    "xup-long": "15°  inclination    ; +6.6 mm acromion length",
    "xup-xlong": "15°  inclination    ; +13.4 mm acromion length",

    # # Nom des cas de simulation
    # "xdown-xshort": "CSA = 12° : -10° inclination    ; -10.8 mm acromion length",
    # "xdown-short": "CSA = 16° : -10° inclination    ; -5.7 mm acromion length",
    # "xdown-normal": "CSA = 20° : -10° inclination    ; +0.0 mm acromion length",
    # "xdown-long": "CSA = 23° : -10° inclination    ; +6.6 mm acromion length",
    # "xdown-xlong": "CSA = 31° : -10° inclination    ; +13.4 mm acromion length",

    # "down-xshort": "CSA = 16° : -5° inclination    ; -10.8 mm acromion length",
    # "down-short": "CSA = 20° : -5° inclination    ; -5.7 mm acromion length",
    # "down-normal": "CSA = 23° : -5° inclination    ; +0.0 mm acromion length",
    # "down-long": "CSA = 31° : -5° inclination    ; +6.6 mm acromion length",
    # "down-xlong": "CSA = 36° : -5° inclination    ; +13.4 mm acromion length",

    # "middle-xshort": "CSA = 20° : 5° inclination     ; -10.8 mm acromion length",
    # "middle-short": "CSA = 23° : 5° inclination     ; -5.7 mm acromion length",
    # "middle-normal": "CSA = 31° : 5° inclination     ; +0.0 mm acromion length",
    # "middle-long": "CSA = 36° : 5° inclination     ; +6.6 mm acromion length",
    # "middle-xlong": "CSA = 40° : 5° inclination     ; +13.4 mm acromion length",

    # "neutral-xshort": "CSA = 20° : 0.0° inclination    ; -10.8 mm acromion length",
    # "neutral-short": "CSA = 23° : 0.0° inclination    ; -5.7 mm acromion length",
    # "neutral-normal": "CSA = 31° : 0.0° inclination    ; +0.0 mm acromion length",
    # "neutral-long": "CSA = 36° : 0.0° inclination    ; +6.6 mm acromion length",
    # "neutral-xlong": "CSA = 40° : 0.0° inclination    ; +13.4 mm acromion length",

    # "up-xshort": "CSA = 23° : 10° inclination     ; -10.8 mm acromion length",
    # "up-short": "CSA = 31° : 10° inclination     ; -5.7 mm acromion length",
    # "up-normal": "CSA = 36° : 10° inclination     ; +0.0 mm acromion length",
    # "up-long": "CSA = 40° : 10° inclination     ; +6.6 mm acromion length",
    # "up-xlong": "CSA = 46° : 10° inclination     ; +13.4 mm acromion length",

    # "xup-xshort": "CSA = 31° : 15° inclination     ; -10.8 mm acromion length",
    # "xup-short": "CSA = 36° : 15° inclination     ; -5.7 mm acromion length",
    # "xup-normal": "CSA = 40° : 15° inclination     ; +0.0 mm acromion length",
    # "xup-long": "CSA = 46° : 15° inclination     ; +6.6 mm acromion length",
    # "xup-xlong": "CSA = 48° : 15° inclination     ; +13.4 mm acromion length",

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
    "CSA=25°": "CSA=23° (4 cases)",
    "CSA=27°": "CSA=27° (5 cases)",
    "CSA=30°": "CSA=31° (5 cases)",
    "CSA=35°": "CSA=36° (4 cases)",
    "CSA=40°": "CSA=40° (3 cases)",
    "CSA=45°": "CSA=44° (2 cases)",
    "CSA=50°": "CSA=48° (1 case)"

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
xShortCases_36 = ["xdown-xshort", "neutral-xshort", "xup-xshort"]
ShortCases_36 = ["xdown-short", "neutral-short", "xup-short"]
NormalCases_36 = ["xdown-normal", "neutral-normal", "xup-normal"]
LongCases_36 = ["xdown-long", "neutral-long", "xup-long"]
xLongCases_36 = ["xdown-xlong", "neutral-xlong", "xup-xlong"]

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

CasesVariables_36 = {"Tilt": {"Large Downtilt": xDownCases_3, "Neutral tilt": NeutralCases_3, "xUptilt": xUpCases_3},
                     "Acromion": {"Very short acromion": xShortCases_36, "Normal acromion": NormalCases_36, "Very long acromion": xLongCases_36}}

# With xdown, middle, xup
CasesVariables_5 = {"Tilt": {"Large Downtilt": xDownCases_5, "Downtilt": DownCases_5, "Normal tilt": MiddleCases_5, "xUptilt": xUpCases_5, "Large Uptilt": xUpCases_5},
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

Muscles_coiffe = ["Subscapularis",
                  "Infraspinatus",
                  "Supraspinatus",
                  "Teres minor"
                  ]

Muscles_coiffe_fr = ["Subscapulaire",
                     "Infraépineux",
                     "Supraépineux",
                     "Petit rond"
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
                      "CasesCategories_5": CasesVariables_5,
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

# Graphiques avec tous les résultats
my_graphs.all_variables_graphs(Results_aTSA, Results_BallAndSocket["normal"], Results_literature, "Graphiques/aTSA", "Tous les résultats", save_graph=True, composante_on=False, **graph_parameters_6)

# %% Résultats classés par CSA et moyennes par CSA

# 9 CSA différents
CSA_12_Cases = ["xdown-xshort"]
CSA_16_Cases = ["xdown-short", "down-xshort"]
CSA_20_Cases = ["xdown-normal", "down-short", "neutral-xshort"]
CSA_23_Cases = ["xdown-long", "down-normal", "neutral-short", "middle-xshort"]
CSA_27_Cases = ["xdown-xlong", "down-long", "neutral-normal", "middle-short", "up-xshort"]
CSA_31_Cases = ["down-xlong", "neutral-long", "middle-normal", "up-short", "xup-xshort"]
CSA_36_Cases = ["neutral-xlong", "middle-long", "up-normal", "xup-short"]
CSA_40_Cases = ["middle-xlong", "up-long", "xup-normal"]
CSA_44_Cases = ["up-xlong", "xup-long"]
CSA_48_Cases = ["xup-xlong"]

# CSA
CasesVariables_CSA_9 = {"CSA Faible": {"CSA = 12°": CSA_12_Cases, "CSA = 16°": CSA_16_Cases, "CSA = 20°": CSA_20_Cases},
                        "CSA Moyen": {"CSA = 23°": CSA_23_Cases, "CSA = 31°": CSA_31_Cases, "CSA = 36°": CSA_36_Cases},
                        "CSA Élevé": {"CSA = 40°": CSA_40_Cases, "CSA = 44°": CSA_44_Cases, "CSA = 48°": CSA_48_Cases}}

# Les 6 qui sont dans la range de CSA
CasesVariables_CSA_6 = {"CSA Moyen": {"CSA = 23°": CSA_23_Cases, "CSA = 31°": CSA_31_Cases, "CSA = 36°": CSA_36_Cases},
                        "CSA Élevé": {"CSA = 40°": CSA_40_Cases, "CSA = 44°": CSA_44_Cases, "CSA = 48°": CSA_48_Cases}
                        }

# Liste des CSA
list_csa_short = ["CSA=23°",
                  "CSA=31°",
                  "CSA=36°",
                  "CSA=40°"
                  ]

list_csa_long = ["CSA=20°",
                 "CSA=23°",
                 "CSA=31°",
                 "CSA=36°",
                 "CSA=40°",
                 "CSA=44°"
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
               "CSA=23°": CSA_23_Cases, "CSA=31°": CSA_31_Cases, "CSA=36°": CSA_36_Cases,
               "CSA=40°": CSA_40_Cases, "CSA=44°": CSA_44_Cases, "CSA=50°": CSA_48_Cases}

# Fait la moyenne de toutes les variables par valeur de CSA
Results_aTSA_CSA = {**combine_simulation_cases(Results_aTSA, combine_CSA, operation="mean"), **Results_aTSA}

# Graphiques avec tous les résultats classés par CSA
# my_graphs.all_variables_graphs(Results_aTSA_CSA, Results_BallAndSocket["normal"], Results_literature, "Graphiques/aTSA", "Classé par CSA", save_graph=True, composante_on=False, **graph_parameters_par_CSA)

# %% Figures article

# my_graphs.figures_article(Results_aTSA, COP_contour, SimulationsLineStyleDictionary, list_muscles_actifs, CaseNames_6, save_figure=False)

# %% Figures mémoire

# Graphique d'exemple du package (Chapitre 4 mémoire)

# PremadeGraphs.muscle_graph_from_list(Results_aTSA, Muscles_Main, [3, 3], "Abduction", "Ft", "Muscle forces", hide_center_axis_labels=True, cases_on=CaseNames_3, xlim=[0, 120], grid_x_step=15, same_lim=True, figsize=[20, 10])

# PremadeGraphs.graph_all_muscle_fibers(Results_aTSA, ["Deltoid lateral"], "Abduction", "Ft", hide_center_axis_labels=True, cases_on=CaseNames_3, xlim=[0, 120], grid_x_step=15, same_lim=True)

# muscle_graph(Results_aTSA, "Deltoid lateral", "Abduction", "F insertion", "Direction of the deltoid lateral's force", cases_on=CaseNames_3, xlim=[0, 120], grid_x_step=15, same_lim=True, subplot={"dimension": [1, 3], "number": 1}, subplot_title="Anterior-posterior axis", composante_y=["Total_AP"], figsize=[18, 10])
# muscle_graph(Results_aTSA, "Deltoid lateral", "Abduction", "F insertion", "Direction of the deltoid lateral's force", cases_on=CaseNames_3, xlim=[0, 120], grid_x_step=15, same_lim=True, subplot={"dimension": [1, 3], "number": 2}, subplot_title="Inferior-posterior axis", composante_y=["Total_IS"])
# muscle_graph(Results_aTSA, "Deltoid lateral", "Abduction", "F insertion", "Direction of the deltoid lateral's force on its insertion", cases_on=CaseNames_3, xlim=[0, 120], grid_x_step=15, same_lim=True, subplot={"dimension": [1, 3], "number": 3}, subplot_title="Medial-lateral axis", composante_y=["Total_ML"])

# COP_graph(Results_aTSA, COP_contour, composantes=["AP", "IS"], figure_title="Position of the Center of Pressure on the glenoid implant", cases_on=["xdown-short", "middle-normal", "xup-long"], annotation_offset=[3, -2.1], annotation_reference_offset=[1, 3], graph_annotation_on=True, COP_first_point_size=15, COP_first_point_mew=4, xlim=[-17, 17], ylim=[-19, 22], grid_x_step=5, figsize=[18, 10], draw_COP_points_on=False)
# COP_graph(Results_aTSA, COP_contour, composantes=["AP", "IS"], figure_title="Position of the Center of Pressure on the glenoid implant", cases_on=["neutral-normal"], graph_annotation_on=False, COP_first_point_size=15, COP_first_point_mew=4, xlim=[-17, 17], ylim=[-19, 22], grid_x_step=5, figsize=[18, 10], draw_COP_points_on=False)

# # Discussion générale coiffe des rotateurs
# define_simulations_line_style(SimulationsLineStyleDictionary_article)


# 12 (Ft > 10 N)
# list_muscles_actifs_fr = ["Deltoid latéral",
#                           "Deltoid antérieur",
#                           "Deltoid postérieur",
#                           "Trapèze inférieur",
#                           "Trapèze moyen",
#                           "Trapèze supérieur",
#                           "Dentelé antérieur",
#                           "Subscapulaire",
#                           "Triceps long",
#                           "Rhomboïde",
#                           "Supraépineux",
#                           "Infraépineux",
#                           ]

# # 3 (10 N > Ft > 5N)
# list_muscles_peu_actif_fr = ["Biceps brachial long",
#                              "Biceps brachial court",
#                              "Levator scapulae"
#                              ]

# # 9 (Ft < 5N)
# list_muscles_inactifs_fr = ["Grand pectoral claviculaire",
#                             "Grand pectoral sternal",
#                             "Petit pectoral",
#                             "Grand rond",
#                             "Petit rond",
#                             "Sternocleidomastoid sternum",
#                             "Sternocleidomastoid claviculaire",
#                             "Grand dorsal",
#                             "Coracobrachialis"
#                             ]


# # Activation de la coiffe des rotateurs
# PremadeGraphs.muscle_graph_from_list(Results_aTSA, Muscles_coiffe_fr, [2, 2], "Abduction", "Ft", "Activation de la coiffe", hide_center_axis_labels=True, cases_on=["neutral-normal"], label="CSA = 28°")
# PremadeGraphs.muscle_graph_from_list(Results_aTSA, Muscles_coiffe_fr, [2, 2], "Abduction", "Ft", "Activation de la coiffe", hide_center_axis_labels=True, cases_on=["up-long"], label="CSA = 46°", add_graph=True, same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_BallAndSocket, Muscles_coiffe_fr, [2, 2], "Abduction", "Ft", "Force of the Rotator cuff muscles", hide_center_axis_labels=True, xlim=[0, 120], grid_x_step=15, ylim=[0, None], cases_on=["normal"], add_graph=True, label="Joint Sphérique")

# define_simulations_line_style(SimulationsLineStyleDictionary)

# PremadeGraphs.muscle_graph_from_list(Results_aTSA_fr, list_muscles_actifs_fr, [4, 3], "Abduction", "Ft", "Muscles actifs (Ft > 10N)", cases_on=CaseNames_36, figsize=[24, 14], ylim=[0, 200], hide_center_axis_labels=True, xlim=[0, 120], grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_aTSA_fr, list_muscles_peu_actif_fr, [1, 3], "Abduction", "Ft", "Muscles peu actifs (10 N > Ft > 5N)", cases_on=CaseNames_36, figsize=[24, 14], ylim=[0, 20], hide_center_axis_labels=True, xlim=[0, 120], grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_aTSA_fr, list_muscles_inactifs_fr, [3, 3], "Abduction", "Ft", "Muscles inactifs (Ft < 5N)", cases_on=CaseNames_36, figsize=[24, 14], ylim=[0, 20], hide_center_axis_labels=True, xlim=[0, 120], grid_x_step=15)

# %% graph surface score

def score_surface(score_df, title):
    z = score_df.to_numpy(dtype="float64")

    acromion_x = np.array([-10.8, -5.7, 0, 7.85, 13.4])
    inclinaison_y = np.array([-10, -5, 0, 5, 10, 15])

    (x, y) = np.meshgrid(acromion_x, inclinaison_y)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=[12, 10])
    surf = ax.plot_surface(x, y, z, cmap=matplotlib.colormaps.get_cmap('RdYlGn_r'), linewidth=0.4, edgecolor="black")
    ax.set_proj_type('ortho')

    ax.tick_params(axis='x', which='major', pad=9)
    ax.tick_params(axis='y', which='major', pad=8)
    ax.tick_params(axis='z', which='major', pad=12)

    ax.set_xlim(-10.8, 13.4)
    ax.set_ylim(-10, 15)
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


# %%

# Results = Results_aTSA

# for case in Results:
#     Results[case]["Angular Velocity"] = Results[case]["COP"]


#     # Liste de tous les muscles (combine muscle main et aux)
#     muscle_list = [*Muscles_Main, *Muscles_Aux]

#     for muscle_name in muscle_list:

#         Results[case]["Muscles"][muscle_name][muscle_name]["LmtDot"] = Results[case]["Muscles"][muscle_name][muscle_name]["MomentArm"]

# for case in Results:

#     # Liste de tous les muscles (combine muscle main et aux)
#     muscle_list = [*Muscles_Main, *Muscles_Aux]

#     # Parcours les muscles
#     for muscle_name in muscle_list:

#         # Liste des composantes
#         composantes_list = ["AP", "IS", "ML"]

#         # Parcours chaque composante
#         for composante in composantes_list:

#             # noms : MomentArmAP ; MomentArmIS ; MomentArmML
#             variable_name = "MomentArm" + composante

#             Results[case]["Muscles"][muscle_name][muscle_name][variable_name] = {"Description": "Moment arm X", "SequenceComposantes": ["Total"]}

#             Results[case]["Muscles"][muscle_name][muscle_name][variable_name]["Total"] = Results[case]["Muscles"][muscle_name][muscle_name]["LmtDot"]["Mean"] / Results[case]["Angular Velocity"][composante]

# %% graphique soutenance

# list_muscles_actifs_fr = ["Deltoid latéral",
#                           "Deltoid antérieur",
#                           "Deltoid postérieur",
#                           "Subscapulaire",
#                           "Dentelé antérieur",
#                           "Triceps long",
#                           "Trapèze inférieur",
#                           "Trapèze moyen",
#                           "Trapèze supérieur",
#                           "Infraépineux",
#                           "Supraépineux",
#                           "Rhomboïde"]

# list_muscles_1 = ["Deltoid latéral",
#                   "Deltoid antérieur",
#                   "Deltoid postérieur",
#                   "Rhomboïde",
#                   "Trapèze inférieur",
#                   "Trapèze supérieur",
#                   "Subscapulaire",
#                   "Infraépineux",
#                   "Supraépineux",
#                   ]


# Categories_Article = {"line": {"Inclinaison inférieure": ["xdown-xshort", "xdown-normal", "xdown-xlong"],
#                                 "Inclinaison neutre": ["neutral-xshort", "neutral-normal", "neutral-xlong"],
#                                 "Inclinaison supérieure": ["up-xshort", "up-normal", "up-xlong"]
#                                 }}


# PremadeGraphs.muscle_graph_from_list(Results_aTSA_fr, list_muscles_1, [3, 3], "Abduction", "Ft", "", cases_on=["xdown-xshort", "neutral-normal", "neutral-long", "xup-long"], grid_x_step=15, xlim=[15, 120], hide_center_axis_labels=True, figsize=[18, 14], legend_label_per_column=10, same_lim=True, ylim=[0, None], legend_on=False)

# graph(Results_aTSA_fr, "Abduction", "ContactForce glenoid", composante_y=["Shear"], cases_on=["xdown-xshort", "neutral-normal", "neutral-long", "xup-long"], grid_x_step=15, xlim=[15, 120], hide_center_axis_labels=True, figsize=[18, 14], subplot={"dimension": [1, 3], "number": 1}, subplot_title="Cisaillement", ylim=[0, None])
# graph(Results_aTSA_fr, "Abduction", "ContactForce glenoid", composante_y=["ML"], cases_on=["xdown-xshort", "neutral-normal", "neutral-long", "xup-long"], grid_x_step=15, xlim=[15, 120], hide_center_axis_labels=True, figsize=[18, 14], subplot={"dimension": [1, 3], "number": 2}, subplot_title="Compression", ylim=[0, None])
# graph(Results_aTSA_fr, "Abduction", "Instability Ratio", cases_on=["xdown-xshort", "neutral-normal", "neutral-long", "xup-long"], grid_x_step=15, xlim=[15, 120], hide_center_axis_labels=True, figsize=[18, 14], subplot={"dimension": [1, 3], "number": 3}, subplot_title="Ratio", ylim=[0, None])

# # Activation de la coiffe des rotateurs
# PremadeGraphs.muscle_graph_from_list(Results_BallAndSocket, Muscles_coiffe, [2, 2], "Abduction", "Ft", "Force of the Rotator cuff muscles", hide_center_axis_labels=True, cases_on=["normal"], label="Joint Sphérique")
# PremadeGraphs.muscle_graph_from_list(Results_aTSA_fr, Muscles_coiffe_fr, [2, 2], "Abduction", "Ft", "Activation de la coiffe", hide_center_axis_labels=True, cases_on=["xdown-xshort", "neutral-normal", "xup-long"], add_graph=True, same_lim=True, xlim=[0, 120], grid_x_step=15, ylim=[0, None])

# SimulationsLineStyleDictionary_presentation = {
#     # Glen xdown
#     "xdown-xshort": {"color": "#648FFF", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},
#     "xdown-short": {"color": "#785EF0", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},
#     "xdown-normal": {"color": "#DC267F", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},
#     "xdown-long": {"color": "#FE6100", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},
#     "xdown-xlong": {"color": "#FFB000", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},

#     # Glen neutral
#     "neutral-xshort": {"color": "#648FFF", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 4},
#     "neutral-short": {"color": "#785EF0", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 4},
#     "neutral-normal": {"color": "#DC267F", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 4},
#     "neutral-long": {"color": "#FE6100", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 4},
#     "neutral-xlong": {"color": "#FFB000", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 4},

#     # Glen up
#     "up-xshort": {"color": "#648FFF", "marker": "", "markersize": 1, "linestyle": ".-", "linewidth": 4},
#     "up-short": {"color": "#785EF0", "marker": "", "markersize": 1, "linestyle": ".-", "linewidth": 4},
#     "up-normal": {"color": "#DC267F", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 4},
#     "up-long": {"color": "#FE6100", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 4},
#     "up-xlong": {"color": "#FFB000", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 4},

# }


# define_simulations_line_style(SimulationsLineStyleDictionary_presentation)

# PremadeGraphs.graph_by_case_categories(Results_aTSA_fr, Categories_Article, "Abduction", "Instability Ratio", "Ratio d'instabilité", hide_center_axis_labels=True, same_lim=True, grid_x_step=15, xlim=[15, 120], ylim=[0, 0.55], figsize=[20, 9])

# PremadeGraphs.COP_graph_by_case_categories(Results_aTSA_fr, Categories_Article, COP_contour, composantes=["AP", "IS"], draw_COP_points_on=False, legend_x=["Postérieur", "Antérieur"], legend_y=["Inférieur", "Supérieur"], graph_annotation_on=False, COP_first_point_size=15, COP_first_point_mew=4, xlim=[-17, 17], ylim=[-19, 22], grid_x_step=5, figsize=[20, 9], hide_center_axis_labels=True)

# SimulationsLineStyleDictionary_presentation_2 = {
#     "xdown-xshort": {"color": "#648FFF", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 4},
#     "neutral-normal": {"color": "k", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 4},
#     "neutral-long": {"color": "#FFB000", "marker": "", "markersize": 1, "linestyle": (0, (3, 3)), "linewidth": 4},
#     "xup-long": {"color": "#DC267F", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},
#     "Joint Sphérique": {"color": "lime", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 4},
# }

# define_simulations_line_style(SimulationsLineStyleDictionary_presentation_2)

# COP_graph(Results_aTSA, COP_contour, cases_on=["xdown-xshort", "neutral-normal", "neutral-long", "xup-long"], composantes=["AP", "IS"], draw_COP_points_on=False, legend_x=["Postérieur", "Antérieur"], legend_y=["Inférieur", "Supérieur"], graph_annotation_on=False, COP_first_point_size=15, COP_first_point_mew=4, xlim=[-17, 17], ylim=[-19, 22], grid_x_step=5, figsize=[20, 9], hide_center_axis_labels=True)


# import pandas as pd

# import numpy as np

# moment_CSA_20 = [None, 85, 139, 152, None]
# moment_CSA_25 = [None, 96, 146, 172, 200]
# moment_CSA_30 = [136, 142, 183, 194, 220]
# moment_CSA_35 = [None, 139, 167, 205, 213]
# moment_CSA_40 = [None, 165, 247, 274, None]


# min_moment = np.array([85, 96, 136, 139, 165])
# max_moment = np.array([152, 200, 220, 213, 274])

# variation = np.round((max_moment - min_moment) / min_moment * 100)
# print(f"moment : {variation}")

# cat_1 = [moment_CSA_20[0], moment_CSA_30[0], moment_CSA_40[0]]
# cat_2 = [moment_CSA_20[1], moment_CSA_30[1], moment_CSA_40[1]]
# cat_3 = [moment_CSA_20[2], moment_CSA_30[2], moment_CSA_40[2]]
# cat_4 = [moment_CSA_20[3], moment_CSA_30[3], moment_CSA_40[3]]
# cat_5 = [moment_CSA_20[4], moment_CSA_30[4], moment_CSA_40[4]]

# cat_1 = [moment_CSA_20[0], moment_CSA_25[0], moment_CSA_30[0], moment_CSA_35[0], moment_CSA_40[0]]
# cat_2 = [moment_CSA_20[1], moment_CSA_25[1], moment_CSA_30[1], moment_CSA_35[1], moment_CSA_40[1]]
# cat_3 = [moment_CSA_20[2], moment_CSA_25[2], moment_CSA_30[2], moment_CSA_35[2], moment_CSA_40[2]]
# cat_4 = [moment_CSA_20[3], moment_CSA_25[3], moment_CSA_30[3], moment_CSA_35[3], moment_CSA_40[3]]
# cat_5 = [moment_CSA_20[4], moment_CSA_25[4], moment_CSA_30[4], moment_CSA_35[4], moment_CSA_40[4]]

# index = ["CSA = 20°", "CSA = 31°", "CSA = 40°"]
# index = ["CSA = 20°", "CSA = 23°", "CSA = 31°", "CSA = 36°", "CSA = 40°"]
# df = pd.DataFrame({"1": cat_1,
#                    "2": cat_2,
#                    "3": cat_3,
#                    "4": cat_4,
#                    "5": cat_5,
#                    }, index=index)

# ax = df.plot.bar(rot=45, legend=False, title="Moment", ylim=[0, 350])

# CSA_20_Cases = ["xdown-normal", "down-short", "middle-xshort"]
# CSA_23_Cases = ["xdown-long", "down-normal", "middle-short", "up-xshort"]
# CSA_31_Cases = ["xdown-xlong", "down-long", "middle-normal", "up-short", "xup-xshort"]
# CSA_36_Cases = ["down-xlong", "middle-long", "up-normal", "xup-short"]
# CSA_40_Cases = ["middle-xlong", "up-long", "xup-normal"]

# # shear_CSA_20 = [4300, 2413, None, None, 4502]
# # shear_CSA_30 = [5669, 5951, 4258, 3997, 6632]
# # shear_CSA_40 = [7487, 8331, None, None, 4882]

# shear_CSA_20 = [None, 2413, 4300, 4502, None]
# shear_CSA_25 = [None, 2713, 4437, 5319, 5989]
# shear_CSA_30 = [3997, 4258, 5669, 5951, 6632]
# shear_CSA_35 = [None, 4094, 4989, 6270, 7103]
# shear_CSA_40 = [None, 4882, 7487, 8331, None]


# min_shear = np.array([2413, 2717, 3997, 4094, 4882])
# max_shear = np.array([4502, 5989, 6632, 7103, 8331])

# variation = np.round((max_shear - min_shear) / min_shear * 100)
# print(f"shear : {variation}")

# cat_1 = [shear_CSA_20[0], shear_CSA_30[0], shear_CSA_40[0]]
# cat_2 = [shear_CSA_20[1], shear_CSA_30[1], shear_CSA_40[1]]
# cat_3 = [shear_CSA_20[2], shear_CSA_30[2], shear_CSA_40[2]]
# cat_4 = [shear_CSA_20[3], shear_CSA_30[3], shear_CSA_40[3]]
# cat_5 = [shear_CSA_20[4], shear_CSA_30[4], shear_CSA_40[4]]

# cat_1 = [shear_CSA_20[0], shear_CSA_25[0], shear_CSA_30[0], shear_CSA_35[0], shear_CSA_40[0]]
# cat_2 = [shear_CSA_20[1], shear_CSA_25[1], shear_CSA_30[1], shear_CSA_35[1], shear_CSA_40[1]]
# cat_3 = [shear_CSA_20[2], shear_CSA_25[2], shear_CSA_30[2], shear_CSA_35[2], shear_CSA_40[2]]
# cat_4 = [shear_CSA_20[3], shear_CSA_25[3], shear_CSA_30[3], shear_CSA_35[3], shear_CSA_40[3]]
# cat_5 = [shear_CSA_20[4], shear_CSA_25[4], shear_CSA_30[4], shear_CSA_35[4], shear_CSA_40[4]]

# # min_shear = [min(shear_CSA_20), min(shear_CSA_30), min(shear_CSA_40)]
# # max_shear = [max(shear_CSA_20), max(shear_CSA_30), max(shear_CSA_40)]

# index = ["CSA = 20°", "CSA = 31°", "CSA = 40°"]
# index = ["CSA = 20°", "CSA = 23°", "CSA = 31°", "CSA = 23°", "CSA = 40°"]
# df = pd.DataFrame({"1": cat_1,
#                    "2": cat_2,
#                    "3": cat_3,
#                    "4": cat_4,
#                    "5": cat_5,
#                    }, index=index)

# ax = df.plot.bar(rot=45, legend=False, title="Cisaillement", ylim=[0, 10000])


# %%

# PremadeGraphs.COP_graph_by_case_categories(Results_aTSA, CasesVariables_6, COP_contour, composantes=["AP", "IS"], legend_position="center left", figsize=[24, 14], legend_on=False, graph_annotation_on=False)
# PremadeGraphs.COP_graph_by_case_categories(Results_aTSA, CasesVariables_36, COP_contour, composantes=["AP", "IS"], legend_position="center left", figsize=[24, 14], legend_on=False, graph_annotation_on=False)
# PremadeGraphs.COP_graph_by_case_categories(Results_aTSA, CasesVariables_5, COP_contour, composantes=["AP", "IS"], legend_position="center left", figsize=[24, 14], legend_on=False, graph_annotation_on=False)

# PremadeGraphs.muscle_graph_from_list(Results_aTSA, list_muscles_actifs, [3, 4], "Abduction", "Ft", "muscles actifs", cases_on="all", legend_position="center left", figsize=[24, 14], legend_on=False)
