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

import matplotlib

# %% Setup des couleurs et légendes

# Contrôle de la taille de la police globale
# matplotlib.rcParams.update({'font.size': 10})

# Contrôle des tailles de chaque partie partie du graphique
# Titre des cases des subplots
# matplotlib.rcParams.update({'axes.titlesize': 12})

# Titre du graphique
# matplotlib.rcParams.update({'figure.titlesize': 12})

# Nom des axes
# matplotlib.rcParams.update({'axes.labelsize': 10})

# Graduations des axes
# matplotlib.rcParams.update({'xtick.labelsize': 10})
# matplotlib.rcParams.update({'ytick.labelsize': 10})

# Légende
# matplotlib.rcParams.update({'legend.fontsize': 10})


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
    "Dal Maso supérieur": {"color": "black", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3},
    "Dal Maso inférieur": {"color": "grey", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3},
    "Bergmann 2007": {"color": "black"},
    "Bergmann_2007": {"color": "black"},
    "Wickham": {"color": "darkorange", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3}
}


SimulationDescriptionDictionary = {
    # Nom des cas de simulation
    "xdown-xshort": "CSA = 12° : glene très basse      -  acromion très court",
    "xdown-short": "CSA = 16° : glene très basse      -  acromion court",
    "xdown-normal": "CSA = 20° : glene très basse      -  acromion normal",
    "xdown-long": "CSA = 25° : glene très basse      -  acromion long",
    "xdown-xlong": "CSA = 30° : glene très basse      -  acromion très long",

    "down-xshort": "CSA = 16° : Glene basse             -  Acromion très court",
    "down-short": "CSA = 20° : Glene basse             -  Acromion court",
    "down-normal": "CSA = 25° : Glene basse             -  Acromion normal",
    "down-long": "CSA = 30° : Glene basse             -  Acromion long",
    "down-xlong": "CSA = 35° : Glene basse             -  Acromion très long",

    "middle-xshort": "CSA = 20° : Glene normale         -  Acromion très court",
    "middle-short": "CSA = 25° : Glene normale         -  Acromion court",
    "middle-normal": "CSA = 30° : Glene normale         -  Acromion normal",
    "middle-long": "CSA = 35° : Glene normale         -  Acromion long",
    "middle-xlong": "CSA = 40° : Glene normale         -  Acromion très long",

    "up-xshort": "CSA = 25° : Glene haute             -  Acromion très court",
    "up-short": "CSA = 30° : Glene haute             -  Acromion court",
    "up-normal": "CSA = 35° : Glene haute             -  Acromion normal",
    "up-long": "CSA = 40° : Glene haute             -  Acromion long",
    "up-xlong": "CSA = 45° : Glene haute             -  Acromion très long",

    "xup-xshort": "CSA = 30° : Glene très haute      -  Acromion très court",
    "xup-short": "CSA = 35° : Glene très haute      -  Acromion court",
    "xup-normal": "CSA = 40° : Glene très haute      -  Acromion normal",
    "xup-long": "CSA = 45° : Glene très haute      -  Acromion long",
    "xup-xlong": "CSA = 50° : Glene très haute      -  Acromion très long",

    # Nom des composantes
    "AP": "Axe antéropostérieur (Antérieur = +)",
    "IS": "Axe inférosupérieur (Supérieur = +)",
    "ML": "Axe médiolatéral (Latéral = +)",

    # Nom des datas de validation
    "Wickham": "Wickham et al. 2010, n=24",
    "Bergmann_2007": "Bergmann et al. 2007",
    "Bergmann 2007": "Bergmann et al. 2007"
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

CompWickham_CasesNames_3 = [*CaseNames_3, "Wickham", "Ball And Socket"]

# %% Catégories de simulation

# With xdown, middle, xup
CasesVariables_3 = {"Tilt": {"Glene très basse": xDownCases_3, "Glène normale": MiddleCases_3, "Glène très haute": xUpCases_3},
                    "Acromion": {"Acromion très court": xShortCases_3, "Acromion normal": NormalCases_3, "Acromion très long": xLongCases_3}}
# With xdown, middle, xup
CasesVariables_5 = {"Tilt": {"Glene très basse": xDownCases_5, "Glene basse": DownCases_5, "Glène normale": MiddleCases_5, "Glène haute": UpCases_5, "Glène très haute": xUpCases_5},
                    "Acromion": {"Acromion très court": xShortCases_5, "Acromion court": ShortCases_5, "Acromion normal": NormalCases_5, "Acromion long": LongCases_5, "Acromion très long": xLongCases_5}}

# Tilt
CasesVariables_Tilt_5_Acromion_3 = {"Tilt": {"Glene très basse": xDownCases_3, "Glene basse": DownCases_3, "Glène normale": MiddleCases_3, "Glène haute": UpCases_3, "Glène très haute": xUpCases_3}}
CasesVariables_Tilt_5_Acromion_5 = {"Tilt": {"Glene très basse": xDownCases_5, "Glene basse": DownCases_5, "Glène normale": MiddleCases_5, "Glène haute": UpCases_5, "Glène très haute": xUpCases_5}}

CasesVariables_Tilt_3_Acromion_3 = {"Tilt": {"Glene très basse": xDownCases_3, "Glène normale": MiddleCases_3, "Glène très haute": xUpCases_3}}
CasesVariables_Tilt_3_Acromion_5 = {"Tilt": {"Glene très basse": xDownCases_5, "Glène normale": MiddleCases_5, "Glène très haute": xUpCases_5}}

# Acromion
CasesVariables_Acromion_5_Tilt_3 = {"Acromion": {"Acromion très court": xShortCases_3, "Acromion court": ShortCases_3, "Acromion normal": NormalCases_3, "Acromion long": LongCases_3, "Acromion très long": xLongCases_3}}
CasesVariables_Acromion_5_Tilt_5 = {"Acromion": {"Acromion très court": xShortCases_5, "Acromion court": ShortCases_5, "Acromion normal": NormalCases_5, "Acromion long": LongCases_5, "Acromion très long": xLongCases_5}}

CasesVariables_Acromion_3_Tilt_3 = {"Acromion": {"Acromion très court": xShortCases_3, "Acromion normal": NormalCases_3, "Acromion très long": xLongCases_3}}
CasesVariables_Acromion_3_Tilt_5 = {"Acromion": {"Acromion très court": xShortCases_5, "Acromion normal": NormalCases_5, "Acromion très long": xLongCases_5}}

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
CasesVariables_3_Bergmann = {"Tilt": {"Glene très basse": [*xDownCases_3, "Bergmann_2007"], "Glène normale": [*MiddleCases_3, "Bergmann_2007"], "Glène très haute": [*xUpCases_3, "Bergmann_2007"]},
                             "Acromion": {"Acromion très court": [*xShortCases_3, "Bergmann_2007"], "Acromion normal": [*NormalCases_3, "Bergmann_2007"], "Acromion très long": [*xLongCases_3, "Bergmann_2007"]}}
# With xdown, middle, xup
CasesVariables_5_Bergmann = {"Tilt": {"Glene très basse": [*xDownCases_5, "Bergmann_2007"], "Glene basse": [*DownCases_5, "Bergmann_2007"], "Glène normale": [*MiddleCases_5, "Bergmann_2007"], "Glène haute": [*UpCases_5, "Bergmann_2007"], "Glène très haute": [*xUpCases_5, "Bergmann_2007"]},
                             "Acromion": {"Acromion très court": [*xShortCases_5, "Bergmann_2007"], "Acromion court": [*ShortCases_5, "Bergmann_2007"], "Acromion normal": [*NormalCases_5, "Bergmann_2007"], "Acromion long": [*LongCases_5, "Bergmann_2007"], "Acromion très long": [*xLongCases_5, "Bergmann_2007"]}}
# With xdown, middle, xup
CasesVariables_3_Wickham = {"Tilt": {"Glene très basse": [*xDownCases_3, "Wickham"], "Glène normale": [*MiddleCases_3, "Wickham"], "Glène très haute": [*xUpCases_3, "Wickham"]},
                            "Acromion": {"Acromion très court": [*xShortCases_3, "Wickham"], "Acromion normal": [*NormalCases_3, "Wickham"], "Acromion très long": [*xLongCases_3, "Wickham"]}}
# With xdown, middle, xup
CasesVariables_5_Wickham = {"Tilt": {"Glene très basse": [*xDownCases_5, "Wickham"], "Glene basse": [*DownCases_5, "Wickham"], "Glène normale": [*MiddleCases_5, "Wickham"], "Glène haute": [*UpCases_5, "Wickham"], "Glène très haute": [*xUpCases_5, "Wickham"]},
                            "Acromion": {"Acromion très court": [*xShortCases_5, "Wickham"], "Acromion court": [*ShortCases_5, "Wickham"], "Acromion normal": [*NormalCases_5, "Wickham"], "Acromion long": [*LongCases_5, "Wickham"], "Acromion très long": [*xLongCases_5, "Wickham"]}}

# With xdown, middle, xup
CasesVariables_3_Ball_And_Socket = {"Tilt": {"Glene très basse": [*xDownCases_3, "Ball And Socket"], "Glène normale": [*MiddleCases_3, "Ball And Socket"], "Glène très haute": [*xUpCases_3, "Ball And Socket"]},
                                    "Acromion": {"Acromion très court": [*xShortCases_3, "Ball And Socket"], "Acromion normal": [*NormalCases_3, "Ball And Socket"], "Acromion très long": [*xLongCases_3, "Ball And Socket"]}}
# With xdown, middle, xup
CasesVariables_5_Ball_And_Socket = {"Tilt": {"Glene très basse": [*xDownCases_5, "Ball And Socket"], "Glene basse": [*DownCases_5, "Ball And Socket"], "Glène normale": [*MiddleCases_5, "Ball And Socket"], "Glène haute": [*UpCases_5, "Ball And Socket"], "Glène très haute": [*xUpCases_5, "Ball And Socket"]},
                                    "Acromion": {"Acromion très court": [*xShortCases_5, "Ball And Socket"], "Acromion court": [*ShortCases_5, "Ball And Socket"], "Acromion normal": [*NormalCases_5, "Ball And Socket"], "Acromion long": [*LongCases_5, "Ball And Socket"], "Acromion très long": [*xLongCases_5, "Ball And Socket"]}}


# %%                                                Chargement des résultats FDK

# Chemin d'accès au dossier dans lequel les fichiers ont été sauvegardés
SaveSimulationsDirectory = "Saved Simulations"

Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types")

Results_GlenoidLocalAxis_MR_Polynomial = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial")

Results_GlenoidLocalAxis_MR_Polynomial_180deg = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_180deg")

Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange")

Results_GlenoidLocalAxis_MR_Polynomial_delt_post_scaling = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_delt_post_scaling")

Results_GlenoidLocalAxis_MR_Polynomial_delt_post_scaling_Elevation = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_Elevation")


# Results_GlenoidLocalAxis_MR_Polynomial_NewWrapping = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_NewWrapping")

# Results_GlenoidLocalAxis_NewWrapping_NewAMMR = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_NewWrapping_NewAMMR")

# Results_GlenoidLocalAxis_NewWrapping_FullRange = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_NewWrapping_FullRange")

# Results_GlenoidLocalAxis_NewWrapping_NoghProth = load_results_from_file(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_NewWrapping_NoghProth")

# %%                                                Chargement des résultats BallAndSocket
Results_BallAndSocket = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket")

Results_BallAndSocket_FullRange = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket_FullRange")

# études de muscle recruitment ball and socket
Results_BallAndSocket_Muscle_Recruitment = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket_MuscleRecruitmentStudy")

# Results_BallAndSocket_NewAMMR = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket_NewAMMR")

# Results_BallAndSocket_FullRange = load_results_from_file(SaveSimulationsDirectory, "Results_BallAndSocket_FullRange")

# %%                                                Chargement autres résultats pour validation

# dataBergmann_2007
dataBergmann_2007 = load_results_from_file(SaveSimulationsDirectory, "dataBergmann_2007")

# dataWickham abduction
dataWickham = load_results_from_file(SaveSimulationsDirectory, "dataWickham_abduction")
# FDK avec data de validation de Wickham
dataWickham_abduction = load_results_from_file(SaveSimulationsDirectory, "dataWickham_abduction")
dataWickham_adduction = load_results_from_file(SaveSimulationsDirectory, "dataWickham_adduction")
dataWickham_abduction_FullRange = load_results_from_file(SaveSimulationsDirectory, "dataWickham_abduction_FullRange")

# data Dal Maso
data_Dal_Maso_sup = load_results_from_file(SaveSimulationsDirectory, "data_Dal_Maso_sup")
data_Dal_Maso_inf = load_results_from_file(SaveSimulationsDirectory, "data_Dal_Maso_inf")

data_Dal_Maso = {"Dal Maso supérieur": data_Dal_Maso_sup, "Dal Maso inférieur": data_Dal_Maso_inf}


# %% Chargement autres variables
# Chargement des dictionnaires de variable
SaveVariablesDirectory = "Saved VariablesDictionary"
FDK_Variables = load_results_from_file(SaveVariablesDirectory, "FDK_Variables")


# FDK Polynomial avec Ball And Socket
Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket = Results_GlenoidLocalAxis_MR_Polynomial.copy()
Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket["Ball And Socket"] = Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"]

# %% Dictionnaire comparaison Dal Maso

CompDalMaso_Results_GlenoidLocalAxis_MR_Polynomial = {key: Results_GlenoidLocalAxis_MR_Polynomial[key].copy() for key in CaseNames_3}
CompDalMaso_Results_GlenoidLocalAxis_MR_Polynomial["Dal Maso supérieur"] = data_Dal_Maso_sup
CompDalMaso_Results_GlenoidLocalAxis_MR_Polynomial["Dal Maso inférieur"] = data_Dal_Maso_inf

# %%                                                Dictionaires comparaison wickham

# Comparaison FDK polynomial recruitment
CompWickham_Results_GlenoidLocalAxis_MR_Polynomial = Results_GlenoidLocalAxis_MR_Polynomial.copy()
CompWickham_Results_GlenoidLocalAxis_MR_Polynomial["Wickham"] = dataWickham_abduction
CompWickham_Results_GlenoidLocalAxis_MR_Polynomial["Ball And Socket"] = Results_BallAndSocket["middle-normal"]


# Comparaison avec Recruitment types Wickham
CompWickham_Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types = Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types.copy()
CompWickham_Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types["Wickham"] = dataWickham_abduction
CompWickham_Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types["Ball And Socket"] = Results_BallAndSocket["middle-normal"]


# Comparaison avec Ball And Socket et Wickham
CompWickham_Results_BallAndSocket = Results_BallAndSocket.copy()
CompWickham_Results_BallAndSocket["Wickham"] = dataWickham_abduction

# Comparaison avec Ball And Socket muscle recruitment et Wickham
CompWickham_Results_BallAndSocket_Muscle_Recruitment = Results_BallAndSocket_Muscle_Recruitment.copy()
CompWickham_Results_BallAndSocket_Muscle_Recruitment["Wickham"] = dataWickham_abduction

"""
Comparaison avec Bergmann
"""
# Comparaison FDK polynomial recruitment
CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial = Results_GlenoidLocalAxis_MR_Polynomial.copy()
CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial["Bergmann_2007"] = dataBergmann_2007
CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial["Ball And Socket"] = Results_BallAndSocket["middle-normal"]


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

Muscles_actifs = ["Deltoideus anterior",
                  "Deltoideus lateral",
                  "Deltoideus posterior",
                  "Lower trapezius",
                  "Middle trapezius",
                  "Upper trapezius",
                  "Rhomboideus",
                  "Supraspinatus",
                  "Serratus anterior",
                  "Subscapularis",
                  "Infraspinatus",
                  "Triceps long head"
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
list_muscles_actifs = ["Deltoideus anterior",
                       "Deltoideus lateral",
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
# 6
list_muscle_variation = ["Deltoideus anterior",
                         "Deltoideus lateral",
                         "Deltoideus posterior",
                         "Subscapularis",
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


# %% COP

# # Par variables tilt et acromion
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13])

# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="center left", figsize=[14, 13])

# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="center left", figsize=[14, 13])

# # Tilt
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_Tilt_5_Acromion_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 6])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_Tilt_5_Acromion_3, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 6])

# # Acromion
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_Acromion_5_Tilt_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 6])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_Acromion_5_Tilt_3, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 6])

# # # CSA
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_9, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[14, 14])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[14, 13])

# %% GHLin
"""
Translation dans repère implant, orientation implant
GHLin ISB
"""
# # Par variables tilt et acromion
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, COP_contour, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[0.8, -2.1], annotation_reference_offset=[0, 7])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, COP_contour, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_3, **CasesVariables_Acromion_3_Tilt_3}, COP_contour, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, COP_contour, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])

# # CSA
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, COP_contour, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])

# # Sans contour
# # Par variables tilt et acromion
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, None, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.8, -2.1], annotation_reference_offset=[0, 5], xlim=[-2.5, 2.5], ylim=[0, 10])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_3, **CasesVariables_Acromion_3_Tilt_3}, None, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="center left", figsize=[24, 13], annotation_offset=[4, -2.1], annotation_reference_offset=[0, 5], xlim=[-2.5, 2.5], ylim=[0, 10])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, None, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="center left", figsize=[20, 16], annotation_offset=[4, -2.1], annotation_reference_offset=[0, 5], xlim=[-2.5, 2.5], ylim=[0, 10])

# # CSA
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, None, figure_title="Déplacement absolu de la tête humérale (GHLin ISB)", variable="GHLin ISB", composantes=["AP", "IS"], legend_position="center left", figsize=[20, 14], annotation_offset=[1.8, -2.1], annotation_reference_offset=[0, 7], xlim=[-2.5, 2.5], ylim=[0, 10])

"""
Translation dans repère implant, orientation implant
GHLin ISB Relative
"""
# # Par variables tilt et acromion
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, COP_contour, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[0.8, -2.1], annotation_reference_offset=[0, 7])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, COP_contour, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])

# # CSA
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, COP_contour, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 14], annotation_offset=[1.1, -2.1], annotation_reference_offset=[0, 7])

# # Sans contour
# # Par variables tilt et acromion
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, None, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[1.8, -2.1], annotation_reference_offset=[0, 5], xlim=[0, 5], ylim=[0, 7])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, None, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[4, -2.1], annotation_reference_offset=[0, 5], xlim=[0, 5], ylim=[0, 7])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_3_Acromion_5, **CasesVariables_Acromion_3_Tilt_5}, None, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_offset=[4, -2.1], annotation_reference_offset=[0, 5], xlim=[0, 5], ylim=[0, 7])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, None, figure_title="Déplacement relatif de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="center left", figsize=[20, 16], annotation_offset=[4, -2.1], annotation_reference_offset=[0, 5], xlim=[0, 5], ylim=[0, 7])

# # CSA
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, None, figure_title="Déplacement absolu de la tête humérale (GHLin ISB Relative)", variable="GHLin ISB Relative", composantes=["AP", "IS"], legend_position="center left", figsize=[20, 14], annotation_offset=[1.8, -2.1], annotation_reference_offset=[0, 7], xlim=[0, 5], ylim=[0, 7])

# %% Forces
"""
Forces
"""
# # forces par variable
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[24, 13], xlim=[0, 120], same_lim=True, grid_x_step=15)
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[24, 13], xlim=[0, 120], same_lim=True, grid_x_step=15)
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[14, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # CSA
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_9, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[14, 14], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[14, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)


# # Forces par variables par composantes
# # 3x3
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # Forces par variables par composantes
# # 5x5
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=CaseNames_3, subplot={"dimension": [1, 3], "number": 1}, subplot_title="Médiolatéral", composante_y=["ML"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=CaseNames_3, subplot={"dimension": [1, 3], "number": 2}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=CaseNames_3, subplot={"dimension": [1, 3], "number": 3}, subplot_title="Antéropostérieur", composante_y=["AP"], xlim=[0, 120], grid_x_step=15, grid_y_step=50, same_lim=True)

# # CSA par composantes
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[14, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[14, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_CSA_6, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[14, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)


# # Comparaison avec Bergmann 2007
# PremadeGraphs.graph_by_variable(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Bergmann, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[14, 13])

# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [1, 2], "number": 1}, figsize=[15, 8], subplot_title="Angle d'abduction", xlim=[0, 120], grid_x_step=15, same_lim=True)
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Elevation", "ForceContact", "Force de contact", cases_on=CaseNames_3, subplot={"dimension": [1, 2], "number": 2}, subplot_title="Angle d'élévation", xlim=[0, 120], grid_x_step=15, same_lim=True)

# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_5, "Bergmann_2007"], subplot={"dimension": [1, 2], "number": 1}, figsize=[15, 8], subplot_title="Angle d'abduction", xlim=[0, 120], grid_x_step=15, same_lim=True)
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Elevation", "ForceContact", "Force de contact", cases_on=CaseNames_5, subplot={"dimension": [1, 2], "number": 2}, subplot_title="Angle d'élévation", xlim=[0, 120], grid_x_step=15, same_lim=True, legend_position="center left")

# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 1}, figsize=[15, 8], subplot_title="Médiolatéral", composante_y=["ML"])
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 2}, subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_3, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 3}, subplot_title="Antéropostérieur", composante_y=["AP"], xlim=[0, 120], grid_x_step=15, same_lim=True)

# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_5, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 1}, subplot_title="Médiolatéral", composante_y=["ML"])
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_5, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 2}, figsize=[15, 8], subplot_title="Inférosupérieur", composante_y=["IS"])
# graph(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "ForceContact", "Force de contact", cases_on=[*CaseNames_5, "Bergmann_2007"], subplot={"dimension": [1, 3], "number": 3}, figsize=[15, 8], subplot_title="Antéropostérieur", composante_y=["AP"], xlim=[0, 120], grid_x_step=15, same_lim=True, legend_position="center left")

# # par variable 3x3
# PremadeGraphs.graph_by_variable(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Bergmann, "Abduction", "ForceContact", "Forces de contact Totale", legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Bergmann, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Bergmann, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Bergmann, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# # par variable 5x5
# PremadeGraphs.graph_by_variable(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5_Bergmann, "Abduction", "ForceContact", "Forces de contact Totale", legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5_Bergmann, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5_Bergmann, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)
# PremadeGraphs.graph_by_variable(CompBergmann_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_5_Bergmann, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13], xlim=[0, 120], grid_x_step=15, same_lim=True)

# %% Muscles Activity

# # Activité 9 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", cases_on=[*CaseNames_3, "Ball And Socket"], composante_y=["Max"], figsize=[24, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", cases_on=[*CaseNames_3, "Ball And Socket"], composante_y=["Max"], figsize=[24, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", cases_on=[*CaseNames_3, "Ball And Socket"], composante_y=["Max"], figsize=[16, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_actifs, [4, 3], "Abduction", "Activity", "Activation maximale des muscles", cases_on=[*CaseNames_3, "Ball And Socket"], composante_y=["Max"], figsize=[24, 20], grid_x_step=15, xlim=[0, 120], same_lim=True)

# # sans same_lim
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", cases_on=[*CaseNames_3, "Ball And Socket"], composante_y=["Max"], figsize=[24, 14], grid_x_step=15, xlim=[0, 120], same_lim=False)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", cases_on=[*CaseNames_3, "Ball And Socket"], composante_y=["Max"], figsize=[24, 14], grid_x_step=15, xlim=[0, 120], same_lim=False)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", cases_on=[*CaseNames_3, "Ball And Socket"], composante_y=["Max"], figsize=[16, 14], grid_x_step=15, xlim=[0, 120], same_lim=False)


# # Activité 25 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", cases_on=CaseNames_5, composante_y=["Max"], grid_x_step=15, xlim=[0, 120])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", cases_on=CaseNames_5, composante_y=["Max"], grid_x_step=15, xlim=[0, 120])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", cases_on=CaseNames_5, composante_y=["Max"], grid_x_step=15, xlim=[0, 120])

# # Activité rassemblé par variables sans les parties des muscles
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3, Muscles_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Activité rassemblé par variables avec les parties des muscles (9 cas)
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3, Muscles_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Activité rassemblé par variables avec les parties des muscles (25 cas)
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_5, Muscles_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # CSA par variables
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_9, Muscles_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], legend_position="center left", figsize=[14, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_6, Muscles_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], legend_position="center left", figsize=[14, 13], grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Muscles par parties individuelles
# # 25 cas
# PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, AllMuscles_List, "Abduction", "Activity", composante_y_muscle_combined=["Max"], cases_on="all", grid_x_step=15, xlim=[0, 120], same_lim=True)
# # 9 cas
# PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, AllMuscles_List, "Abduction", "Activity", composante_y_muscle_combined=["Max"], cases_on=CaseNames_3, grid_x_step=15, xlim=[0, 120], same_lim=True)


# # Comparaison avec la littérature
# PremadeGraphs.muscle_graph_from_list(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, Muscle_Comp_Main, [3, 3], "Abduction", "Activity", "Recrutement Polynomial : Activation maximale des muscles", cases_on=CompWickham_CasesNames_3, composante_y=["Max"], figsize=[24, 16], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, Muscle_Comp_Aux, [2, 3], "Abduction", "Activity", "Recrutement Polynomial : Activation maximale des muscles", cases_on=CompWickham_CasesNames_3, composante_y=["Max"], figsize=[24, 16], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, Muscles_Comp_actifs, [4, 3], "Abduction", "Activity", "Recrutement Polynomial : Activation maximale des muscles", cases_on=[*CompWickham_CasesNames_3, "Ball And Socket"], composante_y=["Max"], figsize=[24, 20], legend_position="center left", grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Comparaison avec Wicham par variables
# PremadeGraphs.muscle_graph_by_variable(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, CasesVariables_3_Wickham, Muscles_Comp_Variation, "Abduction", "Activity", composante_y_muscle_combined=["Max"], muscle_part_on=False, figsize=[16, 10], same_lim=True)

# # Muscles qui varient
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation, [3, 2], "Abduction", "Activity", "Activation influencés par le CSA", composante_y=["Max"], cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[14, 14], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation, [3, 2], "Abduction", "Activity", "Activation influencés par le CSA", composante_y=["Max"], cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[14, 14])

# # Muscles qui varient2
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation_faible, [3, 3], "Abduction", "Activity", "Activation influencés par le CSA", composante_y=["Max"], cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[14, 14], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation_faible, [3, 3], "Abduction", "Activity", "Activation influencés par le CSA", composante_y=["Max"], cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[14, 14])

# %% Muscles Ft

"""
Par catégories
"""
# # Ft 9 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Force musculaire : Muscles actifs (Ft > 10N)", cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[24, 14], xlim=[0, 120], ylim=[0, 200], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Force musculaire : Muscles peu actifs (10 N > Ft > 5N)", cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[24, 14], xlim=[0, 120], ylim=[0, 20], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Force musculaire : Muscles inactifs (Ft < 5N)", cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[16, 14], xlim=[0, 120], ylim=[0, 20], legend_position="center left", grid_x_step=15)

# # sans same_lim
# # Ft 9 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Force musculaire : Muscles actifs (Ft > 10N)", cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Force musculaire : Muscles peu actifs (10 N > Ft > 5N)", cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Force musculaire : Muscles inactifs (Ft < 5N)", cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[16, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15)

# # Ft 25 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Force musculaire : Muscles actifs (Ft > 10N)", cases_on=[*CaseNames_5, "Ball And Socket"], figsize=[24, 14], xlim=[0, 120], ylim=[0, 200], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Force musculaire : Muscles peu actifs (10 N > Ft > 5N)", cases_on=[*CaseNames_5, "Ball And Socket"], figsize=[24, 14], xlim=[0, 120], ylim=[0, 20], legend_position="center left", grid_x_step=15)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Force musculaire : Muscles inactifs (Ft < 5N)", cases_on=[*CaseNames_5, "Ball And Socket"], figsize=[16, 14], xlim=[0, 120], ylim=[0, 20], legend_position="center left", grid_x_step=15)

"""
Muscles qui varient
"""
# # Muscles qui varient
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation, [3, 2], "Abduction", "Ft", "Activation influencés par le CSA", cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[14, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation, [3, 2], "Abduction", "Ft", "Activation influencés par le CSA", cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[14, 14], grid_x_step=15, xlim=[0, 120])

# # Muscles qui varient faiblement
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation, [3, 2], "Abduction", "Ft", "Activation influencés par le CSA", cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[14, 14], grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, list_muscle_variation_faible, [3, 3], "Abduction", "Ft", "Activation influencés par le CSA", cases_on=[*CaseNames_3, "Ball And Socket"], figsize=[14, 14], grid_x_step=15, xlim=[0, 120])


"""
Par variables
"""
# # Ft rassemblé par variables sans les parties des muscles
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3_Ball_And_Socket, list_muscle_variation, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Ft rassemblé par variables avec les parties des muscles (9 cas)
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3, list_muscle_variation, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Ft rassemblé par variables avec les parties des muscles (25 cas)
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_5, list_muscle_variation, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # CSA par variables
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_9, list_muscle_variation, "Abduction", "Ft", legend_position="center left", figsize=[14, 14], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_6, list_muscle_variation, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)


"""Muscles qui varient peu"""
# Ft rassemblé par variables sans les parties des muscles
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3_Ball_And_Socket, list_muscle_variation_faible, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # CSA par variables
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_9, list_muscle_variation_faible, "Abduction", "Ft", legend_position="center left", figsize=[14, 14], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_CSA_6, list_muscle_variation_faible, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=False, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Ft rassemblé par variables avec les parties des muscles (9 cas)
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_3, list_muscle_variation_faible, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

# # Ft rassemblé par variables avec les parties des muscles (25 cas)
# PremadeGraphs.muscle_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, CasesVariables_5, list_muscle_variation_faible, "Abduction", "Ft", legend_position="center left", figsize=[14, 13], muscle_part_on=True, grid_x_step=15, xlim=[0, 120], same_lim=True)

"""
Muscles par parties
"""
# # Muscles par parties individuelles
# # 25 cas
# PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, AllMuscles_List, "Abduction", "Ft", cases_on="all", grid_x_step=15, xlim=[0, 120], legend_position="center left")

# 9 cas
PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, AllMuscles_List, "Abduction", "Ft", cases_on=CaseNames_3, grid_x_step=15, xlim=[0, 120], same_lim=True)

# %% Analyse 180° abduction avec conflit acromion pris en compte

# # forces par variable
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", figure_title="Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", figure_title="Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", figure_title="Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13])


# # COP
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="max_x", annotation_reference_offset=[-3.5, -1], annotation_offset=[-0.4, 2.1])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg, CasesVariables_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="max_x", annotation_reference_offset=[-3.5, -1], annotation_offset=[-0.4, 2.1])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg, CasesVariables_3, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="min_y", annotation_reference_offset=[-5.5, -1], annotation_offset=[-0.4, 2.1])


# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg, CasesVariables_5, "ForceTolError", "Abduction", "ForceTolError", legend_position="center left", figsize=[24, 13])

# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg, CasesVariables_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13])

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

# # forces par variable
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, CasesVariables_5, "Abduction", "ForceContact", "Forces de contact", legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", "Forces de contact AP", composante_y=["AP"], legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", "Forces de contact IS", composante_y=["IS"], legend_position="center left", figsize=[24, 13])
# PremadeGraphs.graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, "Abduction", "ForceContact", "Forces de contact ML", composante_y=["ML"], legend_position="center left", figsize=[24, 13])

# # COP
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="min_y", annotation_reference_offset=[-2.5, -1], annotation_offset=[-0.4, 2.1])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, CasesVariables_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="min_y", annotation_reference_offset=[-2.5, -1], annotation_offset=[-0.4, 2.1])
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_180deg_FullRange, CasesVariables_3, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13], annotation_mode="last", annotation_reference_mode="min_y", annotation_reference_offset=[-2.5, -1], annotation_offset=[-0.4, 2.1])

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

# # Par variables tilt et acromion
# PremadeGraphs.COP_graph_by_variable(Results_GlenoidLocalAxis_MR_Polynomial_no_delt_post_scaling_Elevation, CasesVariables_5, COP_contour, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], legend_position="lower center", figsize=[24, 13])

# %% force des muscles projetées

# for muscle_name in list_muscle_variation:
#     # force muscle projetée origine
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 3], "number": 1}, subplot_title="AP origine", composante_y=["Total_AP"], cases_on=CaseNames_3, legend_position="center left", figsize=[14, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 3], "number": 2}, subplot_title="IS origine", composante_y=["Total_IS"], cases_on=CaseNames_3, legend_position="center left", figsize=[14, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F origin", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 3], "number": 3}, subplot_title="ML origine", composante_y=["Total_ML"], cases_on=CaseNames_3, legend_position="center left", figsize=[14, 13])

#     # force muscle projetée insertion
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 3], "number": 4}, subplot_title="AP insertion", composante_y=["Total_AP"], cases_on=CaseNames_3, legend_position="center left", figsize=[14, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 3], "number": 5}, subplot_title="IS insertion", composante_y=["Total_IS"], cases_on=CaseNames_3, legend_position="center left", figsize=[14, 13])
#     muscle_graph(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, muscle_name, "Abduction", "F insertion", f"{muscle_name} : Forces projetées dans le repère scapula", subplot={"dimension": [2, 3], "number": 6}, subplot_title="ML insertion", composante_y=["Total_ML"], cases_on=CaseNames_3, legend_position="center left", figsize=[14, 13], grid_x_step=15, xlim=[15, 120], same_lim=True)

# %% Moment arm

"""
toutes les fibres
"""
# 25 cas
# PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial, AllMuscles_List, "Abduction", "MomentArm", composante_y_muscle_combined=["Mean"], cases_on="all", grid_x_step=15, xlim=[0, 120], legend_position="center left")
# 9 cas
# PremadeGraphs.graph_all_muscle_fibers(Results_GlenoidLocalAxis_MR_Polynomial, AllMuscles_List, "Abduction", "MomentArm", composante_y_muscle_combined=["Mean"], cases_on=CaseNames_3, grid_x_step=15, xlim=[0, 120], legend_position="center left")

"""
par catégories
"""
# # Moment arm 25 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_actifs, [4, 3], "Abduction", "MomentArm", "Bras de levier : Muscles actifs (Ft > 10N)", composante_y=["Mean"], cases_on=CaseNames_5, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_peu_actif, [1, 3], "Abduction", "MomentArm", "Bras de levier : Muscles peu actifs (10 N > Ft > 5N)", composante_y=["Mean"], cases_on=CaseNames_5, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_inactifs, [3, 3], "Abduction", "MomentArm", "Bras de levier : Muscles inactifs (Ft < 5N)", composante_y=["Mean"], cases_on=CaseNames_5, figsize=[16, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])

# Moment arm 9 cas
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_actifs, [4, 3], "Abduction", "MomentArm", "Bras de levier : Muscles actifs (Ft > 10N)", composante_y=["Mean"], cases_on=CaseNames_3, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_peu_actif, [1, 3], "Abduction", "MomentArm", "Bras de levier : Muscles peu actifs (10 N > Ft > 5N)", composante_y=["Mean"], cases_on=CaseNames_3, figsize=[24, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])
# PremadeGraphs.muscle_graph_from_list(Results_GlenoidLocalAxis_MR_Polynomial, list_muscles_inactifs, [3, 3], "Abduction", "MomentArm", "Bras de levier : Muscles inactifs (Ft < 5N)", composante_y=["Mean"], cases_on=CaseNames_3, figsize=[16, 14], xlim=[0, 120], legend_position="center left", grid_x_step=15, same_lim=True, ylim=[-50, 50])
