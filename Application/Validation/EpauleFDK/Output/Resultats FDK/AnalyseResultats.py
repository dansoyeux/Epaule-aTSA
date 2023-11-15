import Anybody_LoadOutput.Tools as LoadOutputTools
import Anybody_Graph.GraphFunctions as Graph

import Anybody_Graph.PremadeGraphs as PremadeGraphs

# %% Setup des couleurs et légendes

SimulationsLineStyleDictionary = {
    # New Cases Names
    # Glen xdown
    "xdown-xshort": {"color": "lightblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 3},
    "xdown-short": {"color": "deepskyblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "xdown-normal": {"color": "cornflowerblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "xdown-long": {"color": "mediumblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "xdown-xlong": {"color": "midnightblue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 3},

    # Glen down
    "down-xshort": {"color": "violet", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2.5},
    "down-short": {"color": "magenta", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "down-normal": {"color": "mediumorchid", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "down-long": {"color": "blueviolet", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "down-xlong": {"color": "purple", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": 2.5},

    # glen normal
    "middle-xshort": {"color": "lime", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "middle-short": {"color": "greenyellow", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 3},
    "middle-normal": {"color": "mediumseagreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "middle-long": {"color": "darkolivegreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "middle-xlong": {"color": "darkgreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": 3},

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

    "Case 6": {"color": "lime", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "Case 1": {"color": "mediumseagreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "Case 2": {"color": "darkgreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},

    # Glen up
    "Case 5": {"color": "coral", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": None},
    "Case 3": {"color": "red", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": None},

    # Glen down
    "Case 7": {"color": "blue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "Case 4": {"color": "darkviolet", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},


    "FDK": {"color": "tab:blue", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "FDK Full Range": {"color": "tab:red", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "Ball And Socket": {"color": "black", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3},

    "Résultats": {"color": "darkorange"},

    # data de validation
    "Lauranne": {"color": 'hotpink'},
    "Marta": {"color": 'darkturquoise'},

    "Dal Maso supérieur": {"color": "black", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3},
    "Dal Maso inférieur": {"color": "grey", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3},

    "Bergmann": {"color": "black"},
    "Wickham": {"color": "darkorange", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3},


    "equation FDK Lauranne": {"color": 'hotpink'},
    "Bigliani": {"color": 'firebrick'},
    "Bigliani et k0=0.1": {"color": 'darkorange'},
    "Bigliani et k0=1": {"color": 'forestgreen'},
    "F=-10": {"color": 'saddlebrownbrown'},
    "k1-k4 = 0": {"color": "forestgreen"},

    "Résultats Penché": {"color": "steelblue"},
    "Résultats Droit": {"color": "firebrick"},
    "Résultats Droit antero": {"color": "forestgreen"},
    "Résultats Droit Sans Flexion": {"color": "darkviolet"},
    "Résultats Droit en face -21": {"color": "saddlebrown"},
    "Résultats Droit en face -15": {"color": "tab:olive"},

    "Wrapping normal": {"color": "darkorange", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": 3}
}


SimulationDescriptionDictionary = [
    # Nom des cas de simulation


    "xdown-xshort", "CSA = 12° : Glene très basse      -  Acromion très court",
    "xdown-short", "CSA = 16° : Glene très basse      -  Acromion court",
    "xdown-normal", "CSA = 20° : Glene très basse      -  Acromion normal",
    "xdown-long", "CSA = 25° : Glene très basse      -  Acromion long",
    "xdown-xlong", "CSA = 30° : Glene très basse      -  Acromion très long",

    "down-xshort", "CSA = 16° : Glene basse             -  Acromion très court",
    "down-short", "CSA = 20° : Glene basse             -  Acromion court",
    "down-normal", "CSA = 25° : Glene basse             -  Acromion normal",
    "down-long", "CSA = 30° : Glene basse             -  Acromion long",
    "down-xlong", "CSA = 35° : Glene basse             -  Acromion très long",

    "middle-xshort", "CSA = 20° : Glene normale         -  Acromion très court",
    "middle-short", "CSA = 25° : Glene normale         -  Acromion court",
    "middle-normal", "CSA = 30° : Glene normale         -  Acromion normal",
    "middle-long", "CSA = 35° : Glene normale         -  Acromion long",
    "middle-xlong", "CSA = 40° : Glene normale         -  Acromion très long",

    "up-xshort", "CSA = 25° : Glene haute             -  Acromion très court",
    "up-short", "CSA = 30° : Glene haute             -  Acromion court",
    "up-normal", "CSA = 35° : Glene haute             -  Acromion normal",
    "up-long", "CSA = 40° : Glene haute             -  Acromion long",
    "up-xlong", "CSA = 45° : Glene haute             -  Acromion très long",

    "xup-xshort", "CSA = 30° : Glene très haute      -  Acromion très court",
    "xup-short", "CSA = 35° : Glene très haute      -  Acromion court",
    "xup-normal", "CSA = 40° : Glene très haute      -  Acromion normal",
    "xup-long", "CSA = 45° : Glene très haute      -  Acromion long",
    "xup-xlong", "CSA = 50° : Glene très haute      -  Acromion très long",

    "Case 6", "CSA = 20° : Glene normale  -  Acromion court",
    "Case 1", "CSA = 30° : Glene normale  -  Acromion normal",
    "Case 2", "CSA = 40° : Glene normale  -  Acromion long",

    "Case 5", "CSA = 30° : Glene haute      -  Acromion court",
    "Case 3", "CSA = 40° : Glene haute      -  Acromion normal",

    "Case 7", "CSA = 20° : Glene basse      -  Acromion normal",
    "Case 4", "CSA = 30° : Glene basse      -  Acromion long",

    # Nom des composantes
    "AP", "Axe antéropostérieur (Antérieur = +)",
    "IS", "Axe inférosupérieur (Supérieur = +)",
    "ML", "Axe médiolatéral (Latéral = +)",

    # Nom des datas de validation
    "Wickham", "Wickham et al. 2010, n=24",
    "Bergmann", "Bergmann et al. 2007"


]

# Fonctions pour définir les légendes et styles des graphiques en fonction des noms des simulations dans les dictionnaires
Graph.DefineSimulationsLineStyle(SimulationsLineStyleDictionary)
Graph.DefineSimulationDescription(SimulationDescriptionDictionary)

# Fonction pour définir le contour qui sera dessiné par la fonction COPGraph
COPContour = Graph.DefineCOPContour("GleneContour", "pp")


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
                        "CSA Élevé": {"CSA = 40°": CSA_40_Cases, "CSA = 45°": CSA_35_Cases, "CSA = 50°": CSA_50_Cases}}

# Les 6 qui sont dans la range de CSA
CasesVariables_CSA_6 = {"CSA Moyen": {"CSA = 20°": CSA_20_Cases, "CSA = 25°": CSA_25_Cases, "CSA = 30°": CSA_30_Cases},
                        "CSA Élevé": {"CSA = 35°": CSA_35_Cases, "CSA = 40°": CSA_40_Cases, "CSA = 45°": CSA_35_Cases}
                        }

# %%                                                Chargement des résultats FDK

# Chemin d'accès au dossier dans lequel les fichiers ont été sauvegardés
SaveSimulationsDirectory = "Saved Simulations"

Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types")

Results_GlenoidLocalAxis_MR_Polynomial = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial")

Results_GlenoidLocalAxis_MR_Polynomial_180deg = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_180deg")

Results_GlenoidLocalAxis_MR_Polynomial_NewWrapping = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_MR_Polynomial_NewWrapping")

Results_GlenoidLocalAxis_NewWrapping_NewAMMR = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_NewWrapping_NewAMMR")

Results_GlenoidLocalAxis_NewWrapping_FullRange = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_NewWrapping_FullRange")

Results_GlenoidLocalAxis_NewWrapping_NoghProth = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "Results_GlenoidLocalAxis_NewWrapping_NoghProth")

# %%                                                Chargement des résultats BallAndSocket
Results_BallAndSocket = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "Results_BallAndSocket")

# études de muscle recruitment ball and socket
Results_BallAndSocket_Muscle_Recruitment = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "Results_BallAndSocket_MuscleRecruitmentStudy")

Results_BallAndSocket_NewAMMR = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "Results_BallAndSocket_NewAMMR")

Results_BallAndSocket_FullRange = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "Results_BallAndSocket_FullRange")

# %%                                                Chargement autres résultats pour validation

# dataBergmann
dataBergmann = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "dataBergmann")

# dataWickham abduction
dataWickham = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "dataWickham_abduction")
# FDK avec data de validation de Wickham
dataWickham_abduction = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "dataWickham_abduction")
dataWickham_adduction = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "dataWickham_adduction")
dataWickham_abduction_FullRange = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "dataWickham_abduction_FullRange")

# data Dal Maso
data_Dal_Maso_sup = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "data_Dal_Maso_sup")
data_Dal_Maso_inf = LoadOutputTools.LoadVariableFromFile(SaveSimulationsDirectory, "data_Dal_Maso_inf")

data_Dal_Maso = {"Dal Maso supérieur": data_Dal_Maso_sup, "Dal Maso inférieur": data_Dal_Maso_inf}


# %% Chargement autres variables
# Chargement des dictionnaires de variable
SaveVariablesDirectory = "Saved VariablesDictionary"
FDK_Variables = LoadOutputTools.LoadVariableFromFile(SaveVariablesDirectory, "FDK_Variables")


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

# Comp FullRange avec littérature
Comp_FullRange = {"Ball And Socket Full Range": Results_BallAndSocket_FullRange["middle-normal"].copy(), "Ball And Socket Short Range": Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"]}
Comp_FullRange["Wickham"] = dataWickham_abduction_FullRange
Comp_FullRange["FDK Full Range"] = Results_GlenoidLocalAxis_NewWrapping_FullRange["middle-normal"]
Comp_FullRange["FDK"] = Results_GlenoidLocalAxis_MR_Polynomial["middle-normal"]

# Comp FullRange FDK
Comp_FullRange_FDK = {"FDK Full Range": Results_GlenoidLocalAxis_NewWrapping_FullRange["middle-normal"]}
Comp_FullRange_FDK["FDK"] = Results_GlenoidLocalAxis_MR_Polynomial["middle-normal"]

# %% Liste des catégories de muscles

# 9 muscles --> graphique 3x3
Muscles_Main = ["Deltoideus lateral",
                "Deltoideus anterior",
                "Deltoideus posterior",
                "Lower trapezius",
                "Middle trapezius",
                "Upper trapezius",
                "Rhomboideus",
                "Supraspinatus",
                "Serratus anterior"
                ]

# 9 muscles --> graphique 3x3
# {"Nom_Muscle": Composante_y}
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
Muscles_Variation = ["Deltoideus lateral",
                     "Deltoideus anterior",
                     "Deltoideus posterior",
                     "Triceps long head"
                     ]

# Muscles for comparison with Wickham et al. data
# 3x3
Muscle_Comp_Main = ["Deltoideus lateral",
                    "Deltoideus anterior",
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
Muscles_Comp_Variation = ["Deltoideus lateral",
                          "Deltoideus anterior",
                          "Deltoideus posterior"
                          ]

AllMuscles_List = list(FDK_Variables["Muscles"].keys())


# %%                                                GRAPH CODE TEMPLATES

"""Toutes les composantes_y et total activés"""
# Graph.Graph(DATA, "Abduction", "NOM_VARIABLE_Y", "TITRE", Composante_y=["x", "y", "z", "Total"])


"""Composantes_y de GHLin"""
# Graph.Graph(DATA, "Abduction", "GHLin", "TITRE", Composante_y=["AP", "IS", "ML", "Total"])

"""
Tout les graphiques (pas de comparaison)
"""
# # force et COP 2x2
# Graph.COPGraph(DATA, "Résultats", COPContour, CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression", DrawPeakCOPAngleOn=False, DrawCOPPointsOn=False)
# Graph.Graph(DATA, "Abduction", "ForceContact", "Résultats", CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Forces de contact entre les implants")

# # COP
# Graph.COPGraph(DATA, "Position du centre de pression", COPContour, CasesOn=MiddleCases, Subplot={"Dimension": [1, 3], "Number": 1, "Figsize": [15, 6]}, SubplotTitle="Glene normale")
# Graph.COPGraph(DATA, "Position du centre de pression", COPContour, CasesOn=UpCases, Subplot={"Dimension": [1, 3], "Number": 2}, SubplotTitle="Glene haute")
# Graph.COPGraph(DATA, "Position du centre de pression", COPContour, CasesOn=DownCases, Subplot={"Dimension": [1, 3], "Number": 3}, SubplotTitle="Glene basse", LegendPosition='center left')

# forces 1x1
# Graph.Graph(DATA, "Abduction", "ForceContact", "Forces de contact entre les implants", CasesOn="all")


# %% Graphiques avec nouveau wrapping polynomial

"""
COP
"""

# # Par variables tilt et acromion
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Position du centre de pression", CasesVariables_5, Variable="COP", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Position du centre de pression", {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, Variable="COP", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Position du centre de pression", CasesVariables_3, Variable="COP", Composantes=["AP", "IS"], LegendPosition="center left", Figsize=[14, 13])

# # Tilt
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Position du centre de pression", CasesVariables_Tilt_5_Acromion_5, Variable="COP", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 6])
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Position du centre de pression", CasesVariables_Tilt_5_Acromion_3, Variable="COP", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 6])

# # Acromion
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Position du centre de pression", CasesVariables_Acromion_5_Tilt_5, Variable="COP", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 6])
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Position du centre de pression", CasesVariables_Acromion_5_Tilt_3, Variable="COP", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 6])

# # CSA
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Position du centre de pression", CasesVariables_CSA_9, Variable="COP", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[14, 18])
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Position du centre de pression", CasesVariables_CSA_6, Variable="COP", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[14, 13])

"""
Translation dans repère implant, orientation implant
GHLin
"""
# # Par variables tilt et acromion
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Déplacement absolu de la tête humérale (GHLin)", CasesVariables_5, Variable="GHLin", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Déplacement absolu de la tête humérale (GHLin)", {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, Variable="GHLin", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])

# # CSA
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Déplacement absolu de la tête humérale (GHLin)", CasesVariables_CSA_6, Variable="GHLin", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 18])

# # Par variables tilt et acromion
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, None, "Déplacement absolu de la tête humérale (GHLin)", CasesVariables_5, Variable="GHLin", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, None, "Déplacement absolu de la tête humérale (GHLin)", {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, Variable="GHLin", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])

# # CSA
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, None, "Déplacement absolu de la tête humérale (GHLin)", CasesVariables_CSA_6, Variable="GHLin", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[14, 18])

"""
Translation dans repère implant, orientation implant
GHLinRelative
"""
# # Par variables tilt et acromion
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Déplacement relatif de la tête humérale (GHLin Relative)", CasesVariables_5, Variable="GHLin Relative", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Déplacement relatif de la tête humérale (GHLin Relative)", {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, Variable="GHLin Relative", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])

# # CSA
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, COPContour, "Déplacement relatif de la tête humérale (GHLin Relative)", CasesVariables_CSA_6, Variable="GHLin Relative", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])

# # Par variables tilt et acromion
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, None, "Déplacement relatif de la tête humérale (GHLin Relative)", CasesVariables_5, Variable="GHLin Relative", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, None, "Déplacement relatif de la tête humérale (GHLin Relative)", {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, Variable="GHLin Relative", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])

# # CSA
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, None, "Déplacement relatif de la tête humérale (GHLin Relative)", CasesVariables_CSA_6, Variable="GHLin Relative", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[14, 18])


"""
Translation absolue
"""
# # Par variables tilt et acromion
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, None, "Déplacement de la tête humérale", CasesVariables_5, Variable="Translation", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, None, "Déplacement de la tête humérale", {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, Variable="Translation", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[24, 13])

# # CSA
# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, None, "Déplacement de la tête humérale", CasesVariables_CSA_9, Variable="Translation", Composantes=["AP", "IS"], LegendPosition="lower center", Figsize=[14, 18])

"""
Comparaison translations

COMPARER AVEC TRANSLATION GHPROTH_ISB
"""
# Graph.Graph(CompDalMaso_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "Translation", "Déplacement absolu de la tête humérale", Composante_y=["AP"], SubplotTitle="Déplacement Antéropostérieur", CasesOn="all", Subplot={"Dimension": [1, 3], "Number": 1})
# Graph.Graph(CompDalMaso_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "Translation", "Déplacement absolu de la tête humérale", Composante_y=["IS"], SubplotTitle="Déplacement Inférosupérieur", CasesOn="all", Subplot={"Dimension": [1, 3], "Number": 2})
# Graph.Graph(CompDalMaso_Results_GlenoidLocalAxis_MR_Polynomial, "Abduction", "Translation", "Déplacement absolu de la tête humérale", Composante_y=["ML"], SubplotTitle="Déplacement Médiolatéral", CasesOn="all", Subplot={"Dimension": [1, 3], "Number": 3})


"""
Forces
"""
# # forces par variable
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, "Forces de contact", "Abduction", "ForceContact", CasesVariables_5, LegendPosition="center left", Figsize=[24, 13])
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, "Forces de contact", "Abduction", "ForceContact", {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, LegendPosition="center left", Figsize=[24, 13])
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, "Forces de contact", "Abduction", "ForceContact", CasesVariables_3, LegendPosition="center left", Figsize=[14, 13])

# # CSA
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, "Forces de contact", "Abduction", "ForceContact", CasesVariables_CSA_9, LegendPosition="center left", Figsize=[14, 18])
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, "Forces de contact", "Abduction", "ForceContact", CasesVariables_CSA_6, LegendPosition="center left", Figsize=[14, 13])


# # Forces par variables par composantes
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, "Forces de contact AP", "Abduction", "ForceContactLocal", {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, Composante_y=["AP"], LegendPosition="center left", Figsize=[24, 13])
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, "Forces de contact IS", "Abduction", "ForceContactLocal", {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, Composante_y=["IS"], LegendPosition="center left", Figsize=[24, 13])
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, "Forces de contact ML", "Abduction", "ForceContactLocal", {**CasesVariables_Tilt_5_Acromion_3, **CasesVariables_Acromion_5_Tilt_3}, Composante_y=["ML"], LegendPosition="center left", Figsize=[24, 13])

# # CSA par composantes
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, "Forces de contact AP", "Abduction", "ForceContactLocal", CasesVariables_CSA_6, Composante_y=["AP"], LegendPosition="center left", Figsize=[14, 13])
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, "Forces de contact IS", "Abduction", "ForceContactLocal", CasesVariables_CSA_6, Composante_y=["IS"], LegendPosition="center left", Figsize=[14, 13])
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial, "Forces de contact ML", "Abduction", "ForceContactLocal", CasesVariables_CSA_6, Composante_y=["ML"], LegendPosition="center left", Figsize=[14, 13])

"""
Muscles
"""
# # Activité 9 cas
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", CasesOn=CaseNames_3, Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", CasesOn=CaseNames_3, Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", CasesOn=CaseNames_3, Composante_y=["Max"])

# # Activité 25 cas
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", CasesOn=CaseNames_5, Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", CasesOn=CaseNames_5, Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", CasesOn=CaseNames_5, Composante_y=["Max"])


# # Fm
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Main, [3, 3], "Abduction", "Fm", "Muscles principaux : Forces musculaires", CasesOn=CaseNames_3)
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Aux, [3, 3], "Abduction", "Fm", "Muscles auxiliaires : Forces musculaires", CasesOn=CaseNames_3)
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Extra, [2, 3], "Abduction", "Fm", "Muscles extras : Forces musculaires", CasesOn=CaseNames_3)


# Activité rassemblé par variables sans les parties des muscles
# PremadeGraphs.MuscleGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Variation, "Abduction", "Activity", CasesVariables_3, LegendPosition="center left", Figsize=[14, 13], Composante_y=["Max"], MusclePartOn=False)

# # Activité rassemblé par variables avec les parties des muscles (9 cas)
# PremadeGraphs.MuscleGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Variation, "Abduction", "Activity", CasesVariables_3, LegendPosition="center left", Figsize=[14, 13], Composante_y=["Max"], MusclePartOn=True)

# # Activité rassemblé par variables avec les parties des muscles (25 cas)
# PremadeGraphs.MuscleGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Variation, "Abduction", "Activity", CasesVariables_5, LegendPosition="center left", Figsize=[14, 13], Composante_y=["Max"], MusclePartOn=True)

# # CSA par variables
# PremadeGraphs.MuscleGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Variation, "Abduction", "Activity", CasesVariables_CSA_9, LegendPosition="center left", Figsize=[14, 14], Composante_y=["Max"], MusclePartOn=False)
# PremadeGraphs.MuscleGraphByVariable(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, Muscles_Variation, "Abduction", "Activity", CasesVariables_CSA_6, LegendPosition="center left", Figsize=[14, 13], Composante_y=["Max"], MusclePartOn=False)


# # Muscles par parties individuelles
# # 25 cas
# PremadeGraphs.GraphAllMuscleFibers(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, AllMuscles_List, "Abduction", "Activity", Composante_y=["Max"], CasesOn="all")
# # 9 cas
# PremadeGraphs.GraphAllMuscleFibers(Results_GlenoidLocalAxis_MR_Polynomial_BallAndSocket, AllMuscles_List, "Abduction", "Activity", Composante_y=["Max"], CasesOn=CaseNames_3)

# # Comparaison avec la littérature
# PremadeGraphs.MuscleGraphFromList(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, Muscle_Comp_Main, [3, 3], "Abduction", "Activity", "Recrutement Polynomial : Activation maximale des muscles", CasesOn=CompWickham_CasesNames_3, Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, Muscle_Comp_Aux, [2, 3], "Abduction", "Activity", "Recrutement Polynomial : Activation maximale des muscles", CasesOn=CompWickham_CasesNames_3, Composante_y=["Max"])

"""
Pouvoir ajouter Wickham et ball and socket aux graphs de muscles par variables
"""
# NOT WORKING FOR NOW
# PremadeGraphs.MuscleGraphByVariable(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, Muscles_Comp_Variation, "Abduction", "Activity", Composante_y=["Max"], MusclePartOn=False)

# %% Graphiques avec nouveau wrapping Quadratique

# # force et COP 2x2
# Graph.COPGraph(Results_GlenoidLocalAxis_NewWrapping, "Résultats", COPContour, CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression", DrawPeakCOPAngleOn=False, DrawCOPPointsOn=False)
# Graph.Graph(Results_GlenoidLocalAxis_NewWrapping, "Abduction", "ForceContact", "Résultats", CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Forces de contact entre les implants")

# # COP
# Graph.COPGraph(Results_GlenoidLocalAxis_NewWrapping, "Position du centre de pression", COPContour, CasesOn=MiddleCases, Subplot={"Dimension": [1, 3], "Number": 1, "Figsize": [15, 6]}, SubplotTitle="Glene normale")
# Graph.COPGraph(Results_GlenoidLocalAxis_NewWrapping, "Position du centre de pression", COPContour, CasesOn=UpCases, Subplot={"Dimension": [1, 3], "Number": 2}, SubplotTitle="Glene haute")
# Graph.COPGraph(Results_GlenoidLocalAxis_NewWrapping, "Position du centre de pression", COPContour, CasesOn=DownCases, Subplot={"Dimension": [1, 3], "Number": 3}, SubplotTitle="Glene basse")

# PremadeGraphs.COPGraphByVariable(Results_GlenoidLocalAxis_NewWrapping, COPContour)

# # Activité
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_NewWrapping, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_NewWrapping, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_NewWrapping, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])

# # Fm
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_NewWrapping, Muscles_Main, [3, 3], "Abduction", "Fm", "Muscles principaux : Forces musculaires", CasesOn="all")
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_NewWrapping, Muscles_Aux, [3, 3], "Abduction", "Fm", "Muscles auxiliaires : Forces musculaires", CasesOn="all")
# PremadeGraphs.MuscleGraphFromList(Results_GlenoidLocalAxis_NewWrapping, Muscles_Extra, [2, 3], "Abduction", "Fm", "Muscles extras : Forces musculaires", CasesOn="all")


# # forces 1x1
# Graph.Graph(Results_GlenoidLocalAxis_NewWrapping, "Abduction", "ForceContact", "Forces de contact entre les implants", CasesOn="all")

# # forces 3x3 par variable
# PremadeGraphs.GraphByVariable(Results_GlenoidLocalAxis_NewWrapping, "Forces de contact", "Abduction", "ForceContact")

# # Graphiques avec nouveau wrapping des muscles parties de muscles qui varient séparés par variables
# PremadeGraphs.MuscleGraphByVariable(Results_GlenoidLocalAxis_NewWrapping, Muscles_Variation, "Abduction", "Activity", Composante_y=["Max"])

# # Muscles par parties individuelles
# PremadeGraphs.GraphAllMuscleFibers(Results_GlenoidLocalAxis_NewWrapping, AllMuscles_List, "Abduction", "Activity", Composante_y=["Max"], CasesOn="all")

# # Avec Ball and Socket
# PremadeGraphs.GraphAllMuscleFibers(Results_GlenoidLocalAxis_NewWrapping_BallAndSocket, AllMuscles_List, "Abduction", "Activity", Composante_y=["Max"], CasesOn="all")
# %% Comparaison BallAndSocket/FDK "middle"

# comp_AcromionLength = {"FDK": Results_GlenoidLocalAxis, "Ball And Socket": Results_BallAndSocket}
# CasesList = list(Results_BallAndSocket.keys())

# for Case in CasesList:
#     # Activité
#     PremadeGraphs.MuscleGraphFromList(comp_AcromionLength, Muscles_Main, [3, 3], "Abduction", "Activity", f"{Case} : Muscles principaux : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])
#     PremadeGraphs.MuscleGraphFromList(comp_AcromionLength, Muscles_Aux, [3, 3], "Abduction", "Activity", f"{Case} : Muscles auxiliaires : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])
#     PremadeGraphs.MuscleGraphFromList(comp_AcromionLength, Muscles_Extra, [2, 3], "Abduction", "Activity", f"{Case} : Muscles extras : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])

#     # Fm
#     PremadeGraphs.MuscleGraphFromList(comp_AcromionLength, Muscles_Main, [3, 3], "Abduction", "Fm", f"{Case} : Muscles principaux : Forces musculaires", Compare=True, CasesOn=[Case])
#     PremadeGraphs.MuscleGraphFromList(comp_AcromionLength, Muscles_Aux, [3, 3], "Abduction", "Fm", f"{Case} : Muscles auxiliaires : Forces musculaires", Compare=True, CasesOn=[Case])
#     PremadeGraphs.MuscleGraphFromList(comp_AcromionLength, Muscles_Extra, [2, 3], "Abduction", "Fm", f"{Case} : Muscles extras : Forces musculaires", Compare=True, CasesOn=[Case])

# %% BallAndSocket seul sans scaling acromion

# # Activité
# PremadeGraphs.MuscleGraphFromList(Results_BallAndSocket, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", CasesOn=["middle-normal"], Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(Results_BallAndSocket, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", CasesOn=["middle-normal"], Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(Results_BallAndSocket, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", CasesOn=["middle-normal"], Composante_y=["Max"])

# # Fm
# PremadeGraphs.MuscleGraphFromList(Results_BallAndSocket, Muscles_Main, [3, 3], "Abduction", "Fm", "Muscles principaux : Forces musculaires", CasesOn=["middle-normal"])
# PremadeGraphs.MuscleGraphFromList(Results_BallAndSocket, Muscles_Aux, [3, 3], "Abduction", "Fm", "Muscles auxiliaires : Forces musculaires", CasesOn=["middle-normal"])
# PremadeGraphs.MuscleGraphFromList(Results_BallAndSocket, Muscles_Extra, [2, 3], "Abduction", "Fm", "Muscles extras : Forces musculaires", CasesOn=["middle-normal"])

# # Muscles par parties individuelles Ball And Socket sans scaling
# PremadeGraphs.GraphAllMuscleFibers(Results_BallAndSocket, AllMuscles_List, "Abduction", "Activity", Composante_y=["Max"], CasesOn=["middle-normal"])

# %% étude muscle recruitment type

# # BallAndSocket
# PremadeGraphs.GraphAllMuscleFibers(Results_BallAndSocket_Muscle_Recruitment, AllMuscles_List, "Abduction", "Activity", Composante_y=["Max"], CasesOn=["MR_Polynomial", "MR_MinMaxStrict", "MR_MinMaxAux", "MR_Quadratic", "MR_QuadraticAux"])


# # FDK
# # force et COP 2x2
# Graph.COPGraph(Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types, "middle-normal", COPContour, CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression", DrawPeakCOPAngleOn=False, DrawCOPPointsOn=True)
# Graph.Graph(Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types, "Abduction", "ForceContact", "middle-normal", CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Forces de contact entre les implants")

# # AllMuscleParts
# PremadeGraphs.GraphAllMuscleFibers(Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types, AllMuscles_List, "Abduction", "Activity", Composante_y=["Max"], CasesOn="all")

# %% comparaison des activations musculaires avec littérature

# # Activité FDK avec recrutement quadratique
# PremadeGraphs.MuscleGraphFromList(CompWickham_GlenoidLocalAxis, Muscle_Comp_Main, [3, 3], "Abduction", "Activity", "Recrutement Quadratic Aux : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(CompWickham_GlenoidLocalAxis, Muscle_Comp_Aux, [2, 3], "Abduction", "Activity", "Recrutement Quadratic Aux : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])

# # Activité FDK avec recrutement polynomial
# PremadeGraphs.MuscleGraphFromList(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, Muscle_Comp_Main, [3, 3], "Abduction", "Activity", "Recrutement Polynomial : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(CompWickham_Results_GlenoidLocalAxis_MR_Polynomial, Muscle_Comp_Aux, [2, 3], "Abduction", "Activity", "Recrutement Polynomial : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])

# # Activité FDK avec différents recrutements
# PremadeGraphs.MuscleGraphFromList(CompWickham_Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types, Muscle_Comp_Main, [3, 3], "Abduction", "Activity", "middle-normal : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(CompWickham_Results_GlenoidLocalAxis_New_Wrapping_Rectruitment_types, Muscle_Comp_Aux, [2, 3], "Abduction", "Activity", "middle-normal: Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])

# # Activité BallAndSocket avec recrutement polynomial
# PremadeGraphs.MuscleGraphFromList(CompWickham_Results_BallAndSocket_Muscle_Recruitment, Muscle_Comp_Main, [3, 3], "Abduction", "Activity", "Ball And Socket: Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(CompWickham_Results_BallAndSocket_Muscle_Recruitment, Muscle_Comp_Aux, [2, 3], "Abduction", "Activity", "Ball And Socket : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])


# %% Comparaison version AMMR

# # Ball And Socket
# CompAMMR = {"Old AMMR": {"middle-normal": Results_BallAndSocket_Muscle_Recruitment["MR_Polynomial"]}, "New AMMR": Results_BallAndSocket_NewAMMR}

# # Muscles par parties individuelles
# PremadeGraphs.GraphAllMuscleFibers(CompAMMR, AllMuscles_List, "Abduction", "Activity", Composante_y=["Max"], CasesOn=["middle-normal"], Compare=True)


# FDK
# CompAMMR2 = {"Old AMMR": Results_GlenoidLocalAxis_NewWrapping_NewAMMR, "New AMMR": Results_GlenoidLocalAxis_MR_Polynomial}


# for Case in ["middle-normal"]:
#     # force et COP 2x2
#     Graph.COPGraph(CompAMMR2, f"{Case}", COPContour, CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression", DrawPeakCOPAngleOn=True, DrawCOPPointsOn=True)
#     Graph.Graph(CompAMMR2, "Abduction", "ForceContact", f"{Case}", CasesOn=[Case], Compare=True, Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Forces de contact entre les implants")

#     Graph.COPGraph(Results_GlenoidLocalAxis_NewWrapping_NewAMMR, f"{Case}", COPContour, CasesOn=[Case], Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="New", DrawPeakCOPAngleOn=True, DrawCOPPointsOn=True)
#     Graph.COPGraph(Results_GlenoidLocalAxis_MR_Polynomial, f"{Case}", COPContour, CasesOn=[Case], Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Old", DrawPeakCOPAngleOn=True, DrawCOPPointsOn=True)

#     # Activité
#     PremadeGraphs.MuscleGraphFromList(CompAMMR2, Muscles_Main, [3, 3], "Abduction", "Activity", f"{Case} : Muscles principaux : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])
#     PremadeGraphs.MuscleGraphFromList(CompAMMR2, Muscles_Aux, [3, 3], "Abduction", "Activity", f"{Case} : Muscles auxiliaires : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])
#     PremadeGraphs.MuscleGraphFromList(CompAMMR2, Muscles_Extra, [2, 3], "Abduction", "Activity", f"{Case} : Muscles extras : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])

#     # Fm
#     PremadeGraphs.MuscleGraphFromList(CompAMMR2, Muscles_Main, [3, 3], "Abduction", "Fm", f"{Case} : Muscles principaux : Forces musculaires", Compare=True, CasesOn=[Case])
#     PremadeGraphs.MuscleGraphFromList(CompAMMR2, Muscles_Aux, [3, 3], "Abduction", "Fm", f"{Case} : Muscles auxiliaires : Forces musculaires", Compare=True, CasesOn=[Case])
#     PremadeGraphs.MuscleGraphFromList(CompAMMR2, Muscles_Extra, [2, 3], "Abduction", "Fm", f"{Case} : Muscles extras : Forces musculaires", Compare=True, CasesOn=[Case])

# # Compare fibre par fibre
# PremadeGraphs.GraphAllMuscleFibers(CompAMMR2, AllMuscles_List, "Abduction", "Activity", Composante_y=["Max"], CasesOn=["middle-normal"], Compare=True)
# %% Comparaison Full Range

# # Muscles comparés à littérature
# PremadeGraphs.MuscleGraphFromList(Comp_FullRange, Muscle_Comp_Main, [3, 3], "Abduction", "Activity", "Ball And Socket: Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(Comp_FullRange, Muscle_Comp_Aux, [2, 3], "Abduction", "Activity", "Ball And Socket : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])

# Comparaison FDK

# # force et COP 2x2
# Graph.COPGraph(Comp_FullRange_FDK, "Résultats", COPContour, CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 1}, SubplotTitle="Position du centre de pression", DrawPeakCOPAngleOn=False, DrawCOPPointsOn=False)
# Graph.Graph(Comp_FullRange_FDK, "Abduction", "ForceContact", "Résultats", CasesOn="all", Subplot={"Dimension": [1, 2], "Number": 2}, SubplotTitle="Forces de contact entre les implants")

# # forces 1x1
# Graph.Graph(Comp_FullRange_FDK, "Abduction", "ForceContact", "Forces de contact entre les implants", CasesOn="all")


# # Activité
# PremadeGraphs.MuscleGraphFromList(Comp_FullRange_FDK, Muscles_Main, [3, 3], "Abduction", "Activity", "Muscles principaux : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(Comp_FullRange_FDK, Muscles_Aux, [3, 3], "Abduction", "Activity", "Muscles auxiliaires : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(Comp_FullRange_FDK, Muscles_Extra, [2, 3], "Abduction", "Activity", "Muscles extras : Activation maximale des muscles", CasesOn="all", Composante_y=["Max"])

# # Fm
# PremadeGraphs.MuscleGraphFromList(Comp_FullRange_FDK, Muscles_Main, [3, 3], "Abduction", "Fm", "Muscles principaux : Forces musculaires", CasesOn="all")
# PremadeGraphs.MuscleGraphFromList(Comp_FullRange_FDK, Muscles_Aux, [3, 3], "Abduction", "Fm", "Muscles auxiliaires : Forces musculaires", CasesOn="all")
# PremadeGraphs.MuscleGraphFromList(Comp_FullRange_FDK, Muscles_Extra, [2, 3], "Abduction", "Fm", "Muscles extras : Forces musculaires", CasesOn="all")

# %% Comparaison wrapping

# CompWrapping = {"My_Wrapping ghProth": Results_GlenoidLocalAxis_MR_Polynomial, "MyWrapping gh": Results_GlenoidLocalAxis_NewWrapping_NoghProth}

# Graph.COPGraph(CompWrapping, "Comparaison des wrapping", COPContour, CasesOn=["middle-xshort"], Compare=True)
# Case = "middle-xshort"

# PremadeGraphs.MuscleGraphFromList(CompWrapping, Muscles_Main, [3, 3], "Abduction", "Activity", f"{Case} : Muscles principaux : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(CompWrapping, Muscles_Aux, [3, 3], "Abduction", "Activity", f"{Case} : Muscles auxiliaires : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])
# PremadeGraphs.MuscleGraphFromList(CompWrapping, Muscles_Extra, [2, 3], "Abduction", "Activity", f"{Case} : Muscles extras : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])

# CompWrapping2 = {"Nouveau wrapping": Results_GlenoidLocalAxis_MR_Polynomial_NewWrapping, "Wrapping Normal": Results_GlenoidLocalAxis_MR_Polynomial}

# # # COP
# # for Case in xShortCases_5:
# #     Graph.COPGraph(CompWrapping2, f"{Case} : Comparaison des wrapping du deltoïde", COPContour, CasesOn=[Case], Compare=True)

# # Muscles
# for Case in xShortCases_5:

#     PremadeGraphs.MuscleGraphFromList(CompWrapping2, Muscles_Main, [3, 3], "Abduction", "Activity", f"{Case} : Muscles principaux : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])
#     PremadeGraphs.MuscleGraphFromList(CompWrapping2, Muscles_Aux, [3, 3], "Abduction", "Activity", f"{Case} : Muscles auxiliaires : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])
#     PremadeGraphs.MuscleGraphFromList(CompWrapping2, Muscles_Extra, [2, 3], "Abduction", "Activity", f"{Case} : Muscles extras : Activation maximale des muscles", Compare=True, CasesOn=[Case], Composante_y=["Max"])
