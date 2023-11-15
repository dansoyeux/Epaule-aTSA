# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 09:53:59 2023
Functions to make graph from EpauleFDK .h5 and AnyFileOut
Makes Variable graps, muscle graphs and COPGraph
@author: Dan
"""

import math
import numpy as np

import matplotlib.pyplot as plt


# %% VARIABLES TO INITIALIZE WHEN USING THESE FUNCTIONS

"""
Reads the .pp file that contains the coordinates of the contour of the glenoid implant
Example : here it is reading GleneContour.pp
"""
# GleneContour = EpauleFDK_Graph.DefineGleneContour("GleneContour")


# %% Plot Variables setup

"""Case style map"""
global SimulationsLineStyle

SimulationsLineStyle = {
    # New Cases Names
    # glen normal
    # glen normal + shorten = greenyellow
    "middle_short": {"color": "lime", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "middle_normal": {"color": "mediumseagreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "middle_long": {"color": "darkgreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},

    # Glen up
    "up_short": {"color": "coral", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": None},
    "up_normal": {"color": "red", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": None},

    # Glen down
    "down_normal": {"color": "blue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "down_long": {"color": "darkviolet", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},

    "Case 6": {"color": "lime", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "Case 1": {"color": "mediumseagreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},
    "Case 2": {"color": "darkgreen", "marker": "", "markersize": 1, "linestyle": "-", "linewidth": None},

    # Glen up
    "Case 5": {"color": "coral", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": None},
    "Case 3": {"color": "red", "marker": "", "markersize": 1, "linestyle": "--", "linewidth": None},

    # Glen down
    "Case 7": {"color": "blue", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},
    "Case 4": {"color": "darkviolet", "marker": "", "markersize": 1, "linestyle": "-.", "linewidth": None},




    "Lauranne": {"color": 'hotpink'},
    "Marta": {"color": 'darkturquoise'},
    "Résultats": {"color": "darkorange"},
    "Bergmann": {"color": "black"},


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
    "Résultats Droit en face -15": {"color": "tab:olive"}
}


"""
Case descriptions in graph
"""

global SimulationDescription

# # Matrice de correspondance entre numéro case et légende
# SimulationDescription = ["Case 1", "Case 1 : CSA = 30° : Glene normale - Acromion normal",
#                      "Case 2", "Case 2 : CSA = 40° : Glene normale - Acromion extended (17mm)",
#                      "Case 3", "Case 3 : CSA = 40° : Glene uptilt - Acromion normal",
#                      "Case 4", "Case 4 : CSA = 30° : Glene downtilt - Acromion extended (17mm)",
#                      "Case 5", "Case 5 : CSA = 30° : Glene uptilt - Acromion shorten (-12mm)"

#                      ]

# Matrice de correspondance entre numéro case et légende
SimulationDescription = [
    # New Cases Names
    "middle_short", "CSA = 20° : Glene normale  -  Acromion court",
    "middle_normal", "CSA = 30° : Glene normale  -  Acromion normal",
    "middle_long", "CSA = 40° : Glene normale  -  Acromion long",

    "up_short", "CSA = 30° : Glene haute      -  Acromion court",
    "up_normal", "CSA = 40° : Glene haute      -  Acromion normal",

    "down_normal", "CSA = 20° : Glene basse      -  Acromion normal",
    "down_long", "CSA = 30° : Glene basse      -  Acromion long",

    "Case 6", "CSA = 20° : Glene normale  -  Acromion court",
    "Case 1", "CSA = 30° : Glene normale  -  Acromion normal",
    "Case 2", "CSA = 40° : Glene normale  -  Acromion long",

    "Case 5", "CSA = 30° : Glene haute      -  Acromion court",
    "Case 3", "CSA = 40° : Glene haute      -  Acromion normal",

    "Case 7", "CSA = 20° : Glene basse      -  Acromion normal",
    "Case 4", "CSA = 30° : Glene basse      -  Acromion long"

]


# %% Plot Setup Functions


def PlotGraph(data, x, y, GraphType, DrawPeakCOPAngleOn=True, label=None, customlabel=None, color=None, DrawGHReactionsNodes=False):
    """
    Function ploting the datas
    The style depends on the GraphType : "Graph", "MuscleGraph" "COPGraph"
    """

    # if a custom label has been declared, it will overwrite the label given by the graph function
    if customlabel is not None:
        graphlabel = customlabel
    else:
        graphlabel = label

    # defines the color and the style of the line depending on the label name
    color, marker, markersize, linestyle, linewidth = DefineGraphLineStyle(graphlabel)

    if GraphType == "Graph":
        plt.plot(x, y, label=graphlabel, color=color, marker=marker, linestyle=linestyle, markersize=markersize, linewidth=linewidth)

    if GraphType == "MuscleGraph":
        plt.plot(x, y, label=graphlabel, color=color, marker=marker, linestyle=linestyle, markersize=markersize, linewidth=linewidth)

    # Draws the glenoid contour, the COP, the max angle, a cross at the first COP
    # Can draw the GHReactions nodes on the glenoid if activated
    if GraphType == "COPGraph":
        plt.plot(x, y, label=graphlabel, color=color, marker=marker, linestyle=linestyle, markersize=markersize, linewidth=linewidth)

        # Draws the first COP
        DrawCOPPoints(data, x, y, AngleStep=15)

        # Draws the max and min COPy values
        DrawPeakCOPAngle(data, x, y, DrawPeakCOPAngleOn)

        # If reactions nodes drawing is activated and if this in this case, there are GHReactions nodes in the current data
        if DrawGHReactionsNodes and ("GHReactions" in list(data.keys())):
            CavityEdgeNodes = list(
                data["GHReactions"]["Cavity Nodes Position"].keys())
            NodePosx = np.array([])
            NodePosy = np.array([])

            # Gets the position of the CavityEdgenodes
            for Node in CavityEdgeNodes:
                NodePosx = np.append(
                    NodePosx, data["GHReactions"]["Cavity Nodes Position"][Node][0])
                NodePosy = np.append(
                    NodePosy, data["GHReactions"]["Cavity Nodes Position"][Node][1])

            # Draws the Cavity nodes on the COP graph
            plt.scatter(NodePosx, NodePosy, color=plt.gca(
            ).lines[-1].get_color(), marker='o', s=40)


def SubplotSetup(Subplot, AddGraph=False):
    """
    Setup a subplot of dimension :
        Subplot["Dimension"] = [nrows,ncols]
    And defines the active axis as the Subplot["Number"]=number of the plot

    Example : Dimension = [2,2]
              the grah numbers are 1 2
                                   3 4

              Number = 3 corresponds to subplot [1,0]

            : To plot on a graph with 2 line and 3 columns on the graph in the center
            Subplot = {"Dimension":[3,3],"Number":5}
    """
    global ax
    global fig

    # If it's a single subplot
    if Subplot is None:

        # Only creates a new subplot if it's the number is one and if we are not drawing twice on the first subplot
        if AddGraph is False:
            plt.figure()
            fig, ax = plt.subplots()

    else:
        # If it's the first subplot then it initializes the graph
        if Subplot["Number"] == 1 and not AddGraph:
            plt.figure()

            fig, ax = plt.subplots(
                Subplot["Dimension"][0], Subplot["Dimension"][1], figsize=(13, 8))

        # If subplot on only one dimension
        if len(ax.shape) == 1:
            plt.figure(fig)
            # Sets the current active subplot
            plt.axes(ax[Subplot["Number"] - 1])

            # Clears the current subplot if AddGraph is False
            if AddGraph is False:
                plt.cla()

        # If the subplot is 2 dimensional
        else:
            plt.figure(fig)

            # quantity of subplots in the figure
            MaxPlotNumber = Subplot["Dimension"][0] * Subplot["Dimension"][1]

            # Creates a 2d matrix that contains the graph number and transforms the number into the axis coordinate in 2d
            # Creates a vector with all the plot numbers
            MatPlotNumber = np.linspace(1, MaxPlotNumber, 4, dtype=int)
            # Reshapes the vector to have a 2d matrix that has the same dimension than the subplot
            MatPlotNumber = np.reshape(
                MatPlotNumber, (-1, Subplot["Dimension"][1]))

            # Finds the coordinate of the wanted subplot to draw
            SubplotCoordinate = np.where(MatPlotNumber == Subplot["Number"])

            # Sets the current active subplot
            plt.axes(ax[SubplotCoordinate[0][0], SubplotCoordinate[1]][0])

            # Clears the current subplot if AddGraph is False
            if AddGraph is False:
                plt.cla()


def DefineSimulationDescription(labels):
    """
    Defines the labels in a legend
    Put the name of the Simulation case or the simulation is in SimulationDescription list if you want a more detailed legend than only their name

    SimulationDescription must be a global variable declared at the begining of a script.

    SimulationDescription = ["Case or Simulation Name","Legend text","Case or Simulation Name","Legend text"]


    depending on the case name from the SimulationDescription list ["Case_name","color","Case_name","color"]
    Uses the function : "GetCaseDescription" to change the case name to it's description'
    """

    Caselabels = []
    for label in labels:
        if any(i == label for i in SimulationDescription):
            Caselabels.append(GetCaseDescription(label))
        else:
            Caselabels.append(label)

    return Caselabels


def ClearLegendDuplicates(lines, labels):
    """
    Searches the list of all labels in a figure and deletes duplicates in the label list and in the lines list
    """
    labels_noduplicate = list(dict.fromkeys(labels))

    # Stores the indexes of the duplicate elements to delete from the list of labels
    duplicate_indexes = []

    # Traverses all the labels without duplicate
    for label in labels_noduplicate:
        # Finds the first occurence of label in the labelslist
        index2 = labels.index(label)

        # While label is in the list after the present index (index2) except at the end
        while label in labels[index2 + 1:-1] and not (index2 + 1 == len(labels)):

            # Searches the next index where label is in the list and stores it in index 2
            index2 = labels.index(label, index2 + 1)

            # Stores the position of the detected duplicate
            duplicate_indexes.append(index2)

        # If a duplicate is in the last position (first occurence of label is not in last position AND an occurence on last position)
        if not (labels.index(label) == len(labels) - 1) and (labels[-1] == label):
            index2 = len(labels) - 1
            duplicate_indexes.append(index2)

    duplicate_indexes = sorted(duplicate_indexes)

    # Going through the duplicateindex in reverse order to erase them without changin the position of the items
    for duplicate_index in sorted(duplicate_indexes, reverse=True):

        labels.pop(duplicate_index)
        lines.pop(duplicate_index)

    return lines, labels


def LegendSetup(Subplot):
    """
    Setups the legend of a figure, depending on if a subplot is activated or not
    If a subplot is activated, puts only one legend with every labels on it
    Sets the color of the lines depending on the name of the case

    Sets the legend with multiple columns depending on the number of labels
    """

    # if a legend already exists in the figure, deletes it to update it
    if fig.legends:
        fig.legends.clear()

    # maximumNumber of labels per columns in the legend
    LabelsPerColumn = 7

    if Subplot is None:
        # Gets all labels of the figure
        lines, labels = ax.get_legend_handles_labels()

        # Only draws the legend if there are multiple labels in the figure
        if len(labels) > 1:

            # Number of columns in the legend to not exceed the max number of labels per column
            ncol = int(np.ceil((len(labels)) / LabelsPerColumn))

            # Changes the names of the case to their description
            Simulationlabels = DefineSimulationDescription(labels)

            # Draws the legend under the graph and with multiple columns
            fig.legend(lines, Simulationlabels, bbox_to_anchor=(
                0.5, -0.4), loc='lower center', ncol=ncol)

    else:

        # Collects all the labels and lines of the figure
        lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
        lines, labels = [sum(i, []) for i in zip(*lines_labels)]

        # removes duplicates labels
        lines, labels = ClearLegendDuplicates(lines, labels)
        # Only draws the legend if there are multiple labels in the figure
        if len(labels) > 1:

            # Number of columns in the legend to not exceed the max number of labels per column
            ncol = int(np.ceil((len(labels)) / LabelsPerColumn))

            # Changes the names of the case to their description
            Simulationlabels = DefineSimulationDescription(labels)

            # Places one legend for the whole subplot
            fig.legend(lines, Simulationlabels, bbox_to_anchor=(
                0.5, -0.20), loc='lower center', ncol=ncol)


def GraphGridSetup(Variable_x, Variable_y):
    """
    Setups the axis ticks and grid depending on the VarName
    If the VarName doesn't have a custom grid, the default grid is ploted
    """
    axe = plt.gca()
    lines = axe.lines

    x = np.array([])
    y = np.array([])

    # Collects all x data in the current subplot
    for nline in range(len(lines)):
        x = np.append(x, lines[nline].get_xdata())
        y = np.append(y, lines[nline].get_ydata())

    # Met des pas de 15° si la variable en x est Angle de 0 au max de l'angle
    if Variable_x == "Angle":
        axe.set_xticks(np.arange(0, math.ceil(max(x)), 15), minor=False)

    # Pour contact force, sauts en y de 50N si l'écart entre le max et le min est assez grand
    if Variable_y == "ForceContact" and abs(max(y) - min(y)) > 200:

        # Major Ticks every 100 N and minor ticks every 50N
        axe.set_yticks(np.arange(0, int(math.ceil(max(y) / 100)) * 100 + 100, 100), minor=False)
        axe.set_yticks(np.arange(0, int(math.ceil(max(y) / 100)) * 100, 50), minor=True)

        # Sets the grid lines boldness
        axe.grid(which='major', alpha=1)
        axe.grid(which='minor', alpha=0.5)

    # Maximum à 100%, sauts de 20%
    elif Variable_y == "Activity" and abs(max(y) - min(y)) > 40:
        axe.set_yticks(np.arange(0, 110, 20), minor=False)
        axe.set_yticks(np.arange(0, 120, 10), minor=True)

        # Sets the grid lines boldness
        axe.grid(which='major', alpha=1)
        axe.grid(which='minor', alpha=0.5)

    elif Variable_y == "Activity" and abs(max(y) - min(y)) <= 40:
        axe.set_yticks(np.arange(0, 50, 10), minor=False)
        axe.set_yticks(np.arange(0, 50, 5), minor=True)

        # Sets the grid lines boldness
        axe.grid(which='major', alpha=1)
        axe.grid(which='minor', alpha=0.5)

    # Pour force des muscles, sauts en y de 50N et en x de 15° si un assez grand écart entre le min et le max de la force
    elif Variable_y == "Fm" and abs(max(y) - min(y)) > 200:

        # Major Ticks every 100 N and minor ticks every 50N
        axe.set_yticks(np.arange(0, int(math.ceil(max(y) / 100)) * 100 + 100, 100), minor=False)
        axe.set_yticks(np.arange(0, int(math.ceil(max(y) / 100)) * 100, 50), minor=True)

        # Sets the grid lines boldness
        axe.grid(which='major', alpha=1)
        axe.grid(which='minor', alpha=0.5)

    else:
        plt.grid(visible=True)


def GetCaseDescription(Case):
    """
    Transforms the case name into it's description (From the SimulationDescription global list)
    SimulationLegend must be a global list declared at the beginning of the code :
        global SimulationLegend
        SimulationLegend = ["Simulation1 Name","Simulation1 description",
                            "Simulation2 Name","Simulation2 description"...]
    """
    CaseDescription = SimulationDescription[SimulationDescription.index(Case) + 1]
    return CaseDescription


def DefineGraphLineStyle(label):
    """
    Defines the style of the line data in a graph depending on it's name
    These line style are defined in a global dictionnary :
        global SimulationsLineStyle
        SimulationsLineStyle = {"Case 1": {"color": "COLORNAME", "marker": "MARKERNAME", "markersize": NUMBER, "linestyle": "LINESTYLE", "linewidth": NUMBER},
                                "Case 2": {"color": "COLORNAME", "marker": "MARKERNAME", "markersize": NUMBER, "linestyle": "LINESTYLE", "linewidth": NUMBER}
                                }
        If one of the settings isn't declared, it will be set to the default value (None)

    """
    # Default values
    marker = None
    markersize = None
    linestyle = None
    linewidth = None
    color = None

    # Only select a custom color if there is a label
    if label is not None:
        # Selects the color from the colormap if the graphlabel is in SimulationColors
        if label in SimulationsLineStyle:

            color = SimulationsLineStyle[label].get("color", None)
            marker = SimulationsLineStyle[label].get("marker", None)
            markersize = SimulationsLineStyle[label].get("markersize", None)
            linestyle = SimulationsLineStyle[label].get("linestyle", None)
            linewidth = SimulationsLineStyle[label].get("linewidth", None)

    return color, marker, markersize, linestyle, linewidth


# %% Graph function


def Graph(data, Variable_x, Variable_y, FigureTitle, CasesOn=False, Compare=False, Composante_x="Total", Composante_y=["Total"], Subplot=None, SubplotTitle=False, **kwargs):
    """
    Fonction générale qui gère les graphiques


    data : le dictionnaire contenant les data à tracer
         : Par défaut : Un dictionnaire ne contenant qu'une seule simulation
         : Soit un jeu de plusieurs datas (Compare = True)

    Variable_x : Le nom de la variable placée en x sur le graphique
    Variable_u : le nom de la variable placée en y sur le graphique

    Composante_y :
                  : type : liste de chaines de charactère
                  : Liste contenant les nom des composantes de la variable à tracer
                  : Par défaut : On trace la composante "Total" donc Composante_y = ["Total"]

                : Activer plusieurs composantes :
                Exemple : Composante_y = ["composante 1","composante 2","composante 3","Total"....]
                          Si on veut activer x et y entrer : Composante_y = ["x","y"]

                : Activer une seule composante :
                Exemple : Si on veut activer y entrer : Composante_y = ["y"]


                CAS PARTICULIER COMPOSANTES: Si on compare, on ne peut activer qu'une seule composante
                                           : Si on active plusieurs composantes, on doit comparer la même donnée (un seul cas de simulation)

    Composantes_x : Le nom de la composante de la variable en abscisse
                  : Composante_x est une chaîne de charactère contenant le nom de la composante de la variable
                  : Par défaut : "Total"
                  : Si on veut activer y entrer : Composantes_x = "y"

    Compare : = True si on veut comparer plusieurs données
              Ne rien mettre (Compare = False par défaut) : on veut tracer qu'une seule donnée

    **kwargs : contient d'autres paramètres comme
             label : si jamais on veut ajouter un label à une donnée d'un graphique qui n'en aurait ou qui en aurait un autre
             AddGraph = True : Si jamais on veut ajouter un autre graphique sur le dernier graphique tracé
                               : False par défaut, les nouvelles données seront tracées en effaçant les anciennes sur le subplot en cours
    """

    # get the customlabel if a label arguent is declared, puts None otherwise as a default value
    customlabel = kwargs.get("label", None)

    # Get AddGraph function. Puts it to false by default if it's not declared in the kwargs
    AddGraph = kwargs.get("AddGraph", False)

    # Verifications for when simulationCases are used
    if CasesOn:
        # If "all", all cases are selected to be drawn
        if CasesOn == "all":
            CasesOn = list(data.keys())

        elif type(CasesOn) is str:
            raise ValueError(
                "CasesOn doit être une liste si 'all' n'est pas utilisé")
            return

        # Vérifie qu'on n'active pas plusieurs cas tout en comparant
        if len(CasesOn) > 1 and Compare:
            raise ValueError(
                "On ne peut pas comparer plusieurs simulations et plusieurs cas en même temps")
            return

        # Vérifie qu'on ne dessine pas plusieurs variables tout en dessinant plusieurs cas
        if len(CasesOn) > 1 and len(Composante_y) > 1:
            raise ValueError(
                "On ne peut pas dessiner plusieurs cas et plusieurs variables en même temps")
            return

        # Vérification que les variables x et y existent
        # ListeVariables =

    # Vérification qu'on ne dessine pas plusieurs variables tout en comparant
    if Compare and len(Composante_y) > 1:
        raise ValueError(
            "On ne peut pas comparer plusieurs simulations et dessiner plusieurs variables")
        return

    GraphType = "Graph"

    SubplotSetup(Subplot, AddGraph)

    # S'il n'y a qu'une composante à tracer
    if len(Composante_y) == 1:

        # Prend la valeur de la composante comme elle est seule
        Composante_y = Composante_y[0]

        if Compare is False:

            if CasesOn is False:
                label = None
                PlotGraph(data, data[Variable_x][Composante_x],
                          data[Variable_y][Composante_y], GraphType, label=label, customlabel=customlabel)

            # If the graph used is CasesGraph
            else:
                for Case in CasesOn:
                    label = Case

                    PlotGraph(data[Case], data[Case][Variable_x][Composante_x], data[Case]
                              [Variable_y][Composante_y], GraphType, label=label, customlabel=customlabel)

        elif Compare:

            ListSimulations = list(data.keys())

            for Simulation in ListSimulations:
                # Definds the color of this simulation depending on its name
                label = Simulation

                if CasesOn is False:
                    PlotGraph(data[Simulation], data[Simulation][Variable_x][Composante_x], data[Simulation]
                              [Variable_y][Composante_y], GraphType, label=label, customlabel=customlabel)

                # When we compare, we compare only one case between several simulations
                elif len(CasesOn) == 1:
                    PlotGraph(data[Simulation][CasesOn[0]], data[Simulation][CasesOn[0]][Variable_x][Composante_x],
                              data[Simulation][CasesOn[0]][Variable_y][Composante_y], GraphType, label=label, customlabel=customlabel)

    # Si plusieurs composantes sont activées
    else:

        # On ne peut comparer que si on active la même donnée, donc seulement une seule composante
        if Compare is False:
            for Composante in Composante_y:
                label = Composante

                if CasesOn is False:
                    PlotGraph(data, data[Variable_x][Composante_x], data[Variable_y]
                              [Composante], GraphType, label=label, customlabel=customlabel)

                # On peut tracer plusieurs composantes seulement si un seul cas de simulation est activé
                elif len(CasesOn) == 1:
                    PlotGraph(data, data[CasesOn[0]][Variable_x][Composante_x], data[CasesOn[0]]
                              [Variable_y][Composante], GraphType, label=label, customlabel=customlabel)

    # Setups the grid and the axes ticks of the graph
    GraphGridSetup(Variable_x, Variable_y)

    # Axis Labels from the variable description
    if Compare:
        if CasesOn is False:
            plt.xlabel(data[ListSimulations[0]][Variable_x]["Description"])
            plt.ylabel(data[ListSimulations[0]][Variable_y]["Description"])
        else:
            plt.xlabel(data[ListSimulations[0]][CasesOn[0]]
                       [Variable_x]["Description"])
            plt.ylabel(data[ListSimulations[0]][CasesOn[0]]
                       [Variable_y]["Description"])
    elif Compare is False:
        if CasesOn is False:
            plt.xlabel(data[Variable_x]["Description"])
            plt.ylabel(data[Variable_y]["Description"])
        else:
            plt.xlabel(data[CasesOn[0]][Variable_x]["Description"])
            plt.ylabel(data[CasesOn[0]][Variable_y]["Description"])

    if Subplot is None:
        plt.title(FigureTitle)
        LegendSetup(Subplot)

    # Dans le cas d'un subplot
    else:

        # If a subplot title is entered, draws it (SubplotTitle isn't a bool)
        if not type(SubplotTitle) is bool:
            plt.title(SubplotTitle)

        # Ne trace la légende que si le dernier graphique du subplot est vide
        # Trace le titre du graphique que lorsqu'on trace le dernier graphique du subplot
        # test pour un subplot 1D ou 2D
        if (len(ax.shape) == 1 and ax[-1].lines) or (not len(ax.shape) == 1 and ax[-1, -1].lines):

            LegendSetup(Subplot)

            # Trace le titre de la figure
            plt.suptitle(FigureTitle)

            # Ajuste les distances entre les subplots quand ils sont tous tracés
            plt.tight_layout()


# %% Muscles Graph
def MusclePartGraph(data, MuscleName, MusclePart, Variable_x, Variable_y, FigureTitle, Composante_x="Total", Composante_y=["Total"], Compare=False, Subplot=None, SubplotTitle=False, CasesOn=False, MusclePartInformation=False, **kwargs):
    """
    Fonction qui gère trace la variable d'une seule fibre musculaire

    lastPart = statement pour dire qu'on dessine la dernière musclepart pour ne tracer la légende qu'à ce moment là


    data : le dictionnaire contenant les data à tracer
         : Par défaut : Un dictionnaire ne contenant qu'une seule simulation
         : Soit un jeu de plusieurs datas (Compare = True)

    Variable_x : Le nom de la variable placée en x sur le graphique
    Variable_u : le nom de la variable placée en y sur le graphique

    Composante_y :
                  : type : liste de chaines de charactère
                  : Liste contenant les nom des composantes de la variable à tracer
                  : Par défaut : On trace la composante "Total" donc Composante_y = ["Total"]

                : Activer plusieurs composantes :
                Exemple : Composante_y = ["composante 1","composante 2","composante 3","Total"....]
                          Si on veut activer x et y entrer : Composante_y = ["x","y"]

                : Activer une seule composante :
                Exemple : Si on veut activer y entrer : Composante_y = ["y"]

                CAS PARTICULIER COMPOSANTES: Si on compare, on ne peut activer qu'une seule composante
                                           : Si on active plusieurs composantes, on doit comparer la même donnée (un seul cas de simulation)

    Composantes_x : Le nom de la composante de la variable en abscisse
                  : Composante_x est une chaîne de charactère contenant le nom de la composante de la variable
                  : Par défaut : "Total"
                  : Si on veut activer y entrer : Composantes_x = "y"

    MusclePartOn  : Liste contenant les numéros des parties à tracer
                  : active ou non de graph la variable totale du muscle ou la variable d'une des parties du muscle
                  : "allparts" toutes les parties on sans le total
                  : "all" toutes les parties avec le total

                  : Défault = False : trace la variable totale du muscle entier
                  : MusclePartOn = liste des numéros de la partie du muscle à tracer


    Compare : = True si on veut comparer plusieurs données
              Ne rien mettre (Compare = False par défaut) : on veut tracer qu'une seule donnée

    **kwargs : contient d'autres paramètres comme
             label : si jamais on veut ajouter un label à une donnée d'un graphique qui n'en aurait ou qui en aurait un autre
             AddGraph = True : Si jamais on veut ajouter un autre graphique sur le dernier graphique tracé
                               : False par défaut, les nouvelles données seront tracées en effaçant les anciennes sur le subplot en cours
    """

    # get the customlabel if a label arguent is declared, puts None otherwise as a default value
    customlabel = kwargs.get("label", None)

    # Get AddGraph function. Puts it to false by default if it's not declared in the kwargs
    AddGraph = kwargs.get("AddGraph", False)

    GraphType = "MuscleGraph"

    # Name of the dictionnary key where the muscles are stored
    # By default it's muscles but in case of an edge muscle it is stored in GHReactions
    if "Edge muscle" in MuscleName:
        MuscleFolder = "GHReactions"
    else:
        MuscleFolder = "Muscles"

    # Initialise les informations sur les muscles parts si elle n'a pas été spécifiée (c'est à dire qu'il n'y a qu'une seule musclePart à dessiner)
    if MusclePartInformation is False:
        MusclePartInformation = {"LastPart": True,
                                 "Total Number Muscle Parts": 1}

    # Parcours toutes les parties de muscles à tracer

    # S'il n'y a qu'une composante à tracer
    if len(Composante_y) == 1:

        # Prend la valeur de la composante comme elle est seule
        Composante_y = Composante_y[0]

        if Compare is False:

            if CasesOn is False:

                # Si plus d'une muscle part est tracée, on met une legende avec le nom de la musclepart
                if MusclePartInformation["Total Number Muscle Parts"] > 1:
                    label = MusclePart

                # Si seulement une muscle part est activée et qu'on ne compare pas, on ne met pas de légende
                else:
                    label = None

                PlotGraph(data, data[Variable_x][Composante_x], data[MuscleFolder][MuscleName]
                          [MusclePart][Variable_y][Composante_y], GraphType, label=label, customlabel=customlabel)

            else:
                # On ne peut tracer qu'une seule donnée, donc on doit avoir soit un seul Case de sélectionné et n>=1 muscle parts
                # Ou on peut avoir plusieurs Case de sélectionnés mais une seule muscle part à tracer
                if len(CasesOn) == 1 or MusclePartInformation["Total Number Muscle Parts"] == 1:

                    for Case in CasesOn:

                        # La légende est le nom du case si il n'y a qu'une seule muscle part à tracer et plus d'un Case sélectionné
                        if len(CasesOn) > 1 and MusclePartInformation["Total Number Muscle Parts"] == 1:
                            label = Case

                        # La légende est le nom de la muscle part s'il n'y a qu'un seul case et plusieurs Muscle part à tracer
                        elif len(CasesOn) == 1 and MusclePartInformation["Total Number Muscle Parts"] > 1:
                            label = MusclePart

                        # Si les deux sont 1, on ne met pas de légende
                        else:
                            label = None

                        PlotGraph(data[Case], data[Case][Variable_x][Composante_x], data[Case][MuscleFolder][MuscleName]
                                  [MusclePart][Variable_y][Composante_y], GraphType, label=label, customlabel=customlabel)

        elif Compare:

            # Si on a plusieurs simulations, on ne peut afficher qu'une seule donnée sur le graphique, donc qu'une seule muscle part
            if MusclePartInformation["Total Number Muscle Parts"] == 1:
                ListSimulations = list(data.keys())

                for Simulation in ListSimulations:
                    label = Simulation

                    if CasesOn is False:
                        PlotGraph(data[Simulation], data[Simulation][Variable_x][Composante_x], data[Simulation][MuscleFolder]
                                  [MuscleName][MusclePart][Variable_y][Composante_y], GraphType, label=label, customlabel=customlabel)

                    # When we compare, we compare only one case between several simulations
                    elif len(CasesOn) == 1:
                        PlotGraph(data[Simulation][CasesOn[0]], data[Simulation][CasesOn[0]][Variable_x][Composante_x], data[Simulation][CasesOn[0]]
                                  [MuscleFolder][MuscleName][MusclePart][Variable_y][Composante_y], GraphType, label=label, customlabel=customlabel)

    # Si plusieurs composantes sont activées
    else:

        # Si on a plusieurs composantes, on ne peut afficher qu'une seule donnée sur le graphique, donc qu'une seule muscle part
        if MusclePartInformation["Total Number Muscle Parts"] == 1:

            # On ne peut comparer plusieurs simulations que si on active la même donnée, on ne peut pas afficher plusieurs composantes avec plusieurs simulations
            if Compare is False:

                for Composante in Composante_y:
                    label = Composante

                    if CasesOn is False:
                        PlotGraph(data, data[Variable_x][Composante_x], data[MuscleFolder][MuscleName]
                                  [MusclePart][Variable_y][Composante], GraphType, label=label, customlabel=customlabel)

                    # On peut tracer plusieurs composantes seulement si un seul cas de simulation est activé
                    elif len(CasesOn) == 1:
                        PlotGraph(data, data[CasesOn[0]][Variable_x][Composante_x], data[CasesOn[0]][MuscleFolder]
                                  [MuscleName][MusclePart][Variable_y][Composante], GraphType, label=label, customlabel=customlabel)

    # Si on trace la dernière muscle part, trace les axes, la légende, les titres etc...
    if MusclePartInformation["LastPart"]:

        # Setups the grid and the axes ticks of the graph
        GraphGridSetup(Variable_x, Variable_y)

        # Axis Labels from the variable description
        if Compare:
            if CasesOn is False:
                plt.xlabel(data[ListSimulations[0]][Variable_x]["Description"])
                plt.ylabel(data[ListSimulations[0]][MuscleFolder]
                           [MuscleName][MusclePart][Variable_y]["Description"])
            else:
                plt.xlabel(data[ListSimulations[0]][CasesOn[0]]
                           [Variable_x]["Description"])
                plt.ylabel(data[ListSimulations[0]][CasesOn[0]][MuscleFolder]
                           [MuscleName][MusclePart][Variable_y]["Description"])
        elif Compare is False:
            if CasesOn is False:
                plt.xlabel(data[Variable_x]["Description"])
                plt.ylabel(data[MuscleFolder][MuscleName]
                           [MusclePart][Variable_y]["Description"])
            else:
                plt.xlabel(data[CasesOn[0]][Variable_x]["Description"])
                plt.ylabel(data[CasesOn[0]][MuscleFolder][MuscleName]
                           [MusclePart][Variable_y]["Description"])

        if Subplot is None:
            plt.title(FigureTitle)
            LegendSetup(Subplot)

        # Dans le cas d'un subplot
        else:

            # If a subplot title is entered, draws it (SubplotTitle isn't a bool)
            if not type(SubplotTitle) is bool:
                plt.title(SubplotTitle)

            # Ne trace la légende que si le dernier graphique du subplot est vide
            # Trace le titre du graphique que lorsqu'on trace le dernier graphique du subplot
            if (len(ax.shape) == 1 and ax[-1].lines) or (not len(ax.shape) == 1 and ax[-1, -1].lines):

                LegendSetup(Subplot)

                # Trace le titre de la figure
                plt.suptitle(FigureTitle)

                # Ajuste les distances entre les subplots quand ils sont tous tracés
                plt.tight_layout()


def MuscleGraph(data, MuscleName, Variable_x, Variable_y, FigureTitle, CasesOn=False, Compare=False, Composante_x="Total", Composante_y=["Total"], MusclePartOn=False, Subplot=None, SubplotTitle=False, **kwargs):
    """
    Draws all the parts of a Muscle that were selected


    data : le dictionnaire contenant les data à tracer
         : Par défaut : Un dictionnaire ne contenant qu'une seule simulation
         : Soit un jeu de plusieurs datas (Compare = True)

    Variable_x : Le nom de la variable placée en x sur le graphique
    Variable_u : le nom de la variable placée en y sur le graphique

    Composante_y :
                  : type : liste de chaines de charactère
                  : Liste contenant les nom des composantes de la variable à tracer
                  : Par défaut : On trace la composante "Total" donc Composante_y = ["Total"]

                : Activer plusieurs composantes :
                Exemple : Composante_y = ["composante 1","composante 2","composante 3","Total"....]
                          Si on veut activer x et y entrer : Composante_y = ["x","y"]

                : Activer une seule composante :
                Exemple : Si on veut activer y entrer : Composante_y = ["y"]


                CAS PARTICULIER COMPOSANTES: Si on compare, on ne peut activer qu'une seule composante
                                           : Si on active plusieurs composantes, on doit comparer la même donnée (un seul cas de simulation)

    Composantes_x : Le nom de la composante de la variable en abscisse
                  : Composante_x est une chaîne de charactère contenant le nom de la composante de la variable
                  : Par défaut : "Total"
                  : Si on veut activer y entrer : Composantes_x = "y"

    MusclePartOn  : Liste contenant les numéros des parties à tracer
                  : active ou non de graph la variable totale du muscle ou la variable d'une des parties du muscle
                  : "allparts" toutes les parties on sans le total
                  : "all" toutes les parties avec le total

                  : Défault = False : trace la variable totale du muscle entier
                  : MusclePartOn = numéro de la partie du muscle à tracer


    Compare : = True si on veut comparer plusieurs données
              Ne rien mettre (Compare = False par défaut) : on veut tracer qu'une seule donnée

    **kwargs : contient d'autres paramètres comme
             label : si jamais on veut ajouter un label à une donnée d'un graphique qui n'en aurait ou qui en aurait un autre
             AddGraph = True : Si jamais on veut ajouter un autre graphique sur le dernier graphique tracé
                               : False par défaut, les nouvelles données seront tracées en effaçant les anciennes sur le subplot en cours
    """

    # Get AddGraph function. Puts it to false by default if it's not declared in the kwargs
    AddGraph = kwargs.get("AddGraph", False)

    # Verifications for when simulationCases are used
    if CasesOn:
        # Active tous les cas présents dans data
        if CasesOn == "all":
            CasesOn = list(data.keys())

        # Vérifie que Cases est toujours une liste si 'all' n'est pas utilisé
        elif not type(CasesOn) is list:
            raise ValueError(
                "CasesOn doit être une liste si 'all' n'est pas utilisé")
            return

        # Vérifie qu'on n'active pas plusieurs cas tout en comparant
        if len(CasesOn) > 1 and Compare:
            raise ValueError(
                "On ne peut pas comparer plusieurs simulations et plusieurs cas en même temps")
            return

        # Vérifie qu'on ne dessine pas plusieurs variables tout en dessinant plusieurs cas
        if len(CasesOn) > 1 and len(Composante_y) > 1:
            raise ValueError(
                "On ne peut pas dessiner plusieurs cas et plusieurs variables en même temps")
            return

    # Name of the dictionnary key where the muscles are stored
    # By default it's muscles but in case of an edge muscle it is stored in GHReactions
    if "Edge Muscle" in MuscleName:
        MuscleFolder = "GHReactions"
    else:
        MuscleFolder = "Muscles"

    # Construit la liste des parties de muscle à tracer

    # Sans cas de simulation selon le cas (avec/sans des cas, avec/sans comparaison)
    if CasesOn is False:
        if Compare is False:
            MuscleParts = list(data[MuscleFolder][MuscleName].keys())
        else:
            ListSimulations = list(data.keys())
            MuscleParts = list(data[ListSimulations[0]]
                               [MuscleFolder][MuscleName].keys())

    # Dans les cas où on a des cas de simulation
    else:
        if Compare is False:
            MuscleParts = list(
                data[CasesOn[0]][MuscleFolder][MuscleName].keys())
        else:
            ListSimulations = list(data.keys())
            MuscleParts = list(data[ListSimulations[0]]
                               [CasesOn[0]][MuscleFolder][MuscleName].keys())

    # Si toutes les parties sont activées, fais une liste avec le nom de toutes les parties sauf le muscle total
    # n'enlève pas la partie totale si le muscle n'a pas de partie
    if MusclePartOn == "allparts" and (not len(MuscleParts) == 1):

        # Enlève le muscle total de la liste
        MuscleParts.remove(MuscleName)

    # Dans le cas où on a entré une liste des numéros des parties
    elif type(MusclePartOn) is list:
        ListMuscleParts = []

        # Parcours les numéros de parties à tracer
        for MusclePartNumber in MusclePartOn:
            # Temporary List of muscleparts to draw
            for MusclePart in MuscleParts:
                # Si le numéro ne se trouve dans le nom de la partie du muscle, enlève cette partie de muscle
                if str(MusclePartNumber) in MusclePart:
                    ListMuscleParts.append(MusclePart)

        # Stores the new value of muscleparts to draw
        MuscleParts = ListMuscleParts

    # Si on ne veut tracer qu'un seul muscle
    elif MusclePartOn is False:
        MuscleParts = [MuscleName]

    # Vérification qu'on ne dessine pas plusieurs parties de muscles tout en comparant
    if Compare and len(MuscleParts) > 1:
        raise ValueError(
            "On ne peut pas comparer plusieurs simulations et dessiner plusieurs parties de muscles en même temps")
        return

    # Vérification qu'on ne dessine pas plusieurs parties de muscles tout en dessinant plusieurs composantes
    if Compare and len(Composante_y) > 1:
        raise ValueError(
            "On ne peut pas dessiner plusieurs composantes et dessiner plusieurs parties de muscles en même temps")
        return
    # Vérifie qu'on ne dessine pas plusieurs parties de muscles tout comparant plusieurs cas de simulation
    if type(CasesOn) is list:
        if len(CasesOn) > 1 and len(MuscleParts) > 1:
            raise ValueError(
                "On ne peut pas dessiner plusieurs cas de simulation et dessiner plusieurs parties de muscles en même temps")
            return

    # Subplot is setup here to be able to draw every part of a muscle on the same figure
    SubplotSetup(Subplot, AddGraph)

    # Initialisation du dictionnaire contenant les informations sur le nombre de muscles parts qui seront tracées
    MusclePartInformation = {}

    # Nombre de muscle parts qui seront tracées sur le même graphique
    MusclePartInformation["Total Number Muscle Parts"] = len(MuscleParts)

    # Parcours les parties de muscles à tracer
    for MusclePart in MuscleParts:

        # Si on trace la dernière partie de muscle pour ne tracer la légende et les axes qu'à ce moment là
        if MusclePart == MuscleParts[-1]:
            MusclePartInformation["LastPart"] = True
        else:
            MusclePartInformation["LastPart"] = False

        MusclePartGraph(data, MuscleName, MusclePart, Variable_x, Variable_y, FigureTitle, Composante_x,
                        Composante_y, Compare, Subplot, SubplotTitle, CasesOn, MusclePartInformation, **kwargs)


# %% COPGraph setup

# Reads a picked points file (.pp)
def ReadPickedPoints(dataPath):
    """
    Reads a .pp file and converts it to an array of points
    """
    # Module that can read .pp files can be found here : https://pypi.org/project/meshlab-pickedpoints/
    import meshlab_pickedpoints
    import numpy as np

    data = meshlab_pickedpoints.load(dataPath)

    mat = np.zeros([len(data), 3])

    for i in range(len(data)):

        for j in range(3):
            mat[i, j] = data[i]['point'][j]

    return mat


def DefineGleneContour(PickedPointFileName):
    """
    Reads the .pp file that contains the coordinates of the contour of the glenoid implant
    PickedPointFileName : Name of the .pp file (without the extension)
    """

    GleneContour = ReadPickedPoints(PickedPointFileName + ".pp")

    return GleneContour


def DrawPeakCOPAngle(data, x, y, DrawPeakCOPAngleOn):
    """
    Draws the angle where COPy reached a maximum or a minimum on a COPGraph
    """

    from scipy.signal import find_peaks

    if DrawPeakCOPAngleOn:
        MaxIndexes = find_peaks(y)[0]

        # Multiply by -1 to get the minimums
        MinIndexes = find_peaks(-1 * y)[0]

        # Gets the color of the last ploted graph
        color = plt.gca().lines[-1].get_color()

        # List of all peaks indexes
        PeakIndexes = [*MaxIndexes, *MinIndexes]

        # Gets the x and y position of the peaks and the peak angle
        Maxx = x[PeakIndexes]
        Maxy = y[PeakIndexes]
        MaxAngle = data["Angle"]["Total"][PeakIndexes]

        for index in range(len(PeakIndexes)):
            plt.plot(Maxx[index], Maxy[index], '.', color=color, markersize=10, mew=2.5)

            plt.annotate(str(round(MaxAngle[index])) + "°",
                         xy=(Maxx[index], Maxy[index]), xycoords='data',
                         xytext=(5, 15), textcoords='offset points',
                         bbox=dict(boxstyle="round", fc=color, alpha=0.6),
                         arrowprops=dict(
                arrowstyle="-", connectionstyle="arc3", color="black"),
                color="black")


def DrawCOPPoints(data, x, y, AngleStep):
    """
    Shows where is the COP at t=0s
    And draws a point where the COP is during the movement
    AngleStep spécifie tous les combien de degré d'abduction un point doit être tracé
        Type = int

    Exemple : AngleStep = 15 : Le COP sera tracé tous les 15° [15, 30, 45, 60....] environ en trouvant les données correspondant aux angles les plus proches
    Le script détect l'angle de début et de fin

    """

    CaseColor = plt.gca().lines[-1].get_color()

    # Liste des angles d'abduction
    AngleList = data["Angle"]["Total"]

    def FindClosestNumber(Array, Number):
        """
        Fonction pour trouver la position et la valeur de l'élément ayant la valeur la plus proche d'un nombre spécifié dans une liste de nombres

        Exemple : Array = [1, 2, 3, 4]
        Number = 3.2

        ClosestNumber = 3
        NumberIndex = 2

        """
        ClosestNumber = Array[min(range(len(Array)), key=lambda i: abs(Array[i] - Number))]
        NumberIndex = np.where(Array == ClosestNumber)[0][0]

        return ClosestNumber, NumberIndex

    # Initialisation des angles
    ClosestAngles = []
    Indexes = []

    # Parcours les valeurs d'angles de la valeur minimale à maximale, avec un pas spécifié
    # Ne sélectionne pas la valeur minimale ni la valeur maximale
    for Angle in range(int(min(AngleList)) + AngleStep, int(max(AngleList)), AngleStep):

        # Trouve la valeur dans la liste d'angle qui est la plus proche de l'angle voulu et sa position dans la liste
        ClosestNumber, NumberIndex = FindClosestNumber(AngleList, Angle)

        ClosestAngles = [*ClosestAngles, ClosestNumber]
        Indexes = [*Indexes, NumberIndex]

    # Sélectionne les valeurs x et y du COP à tracer
    xSelection = x[Indexes]
    ySelection = y[Indexes]

    plt.plot(x[0], y[0], '+', color=CaseColor, markersize=10, mew=2.5)
    plt.plot(xSelection, ySelection, ".", color=CaseColor, markersize=10)


# %% COPGraph


def COPGraph(data, FigureTitle, GleneContour, CasesOn=False, Subplot=None, Compare=False, SubplotTitle=False, DrawPeakCOPAngleOn=True, DrawGHReactionsNodes=False, **kwargs):
    """
    Fonction qui trace le COP (en x et y)de l'implant et le contour de la glène


    data : le dictionnaire contenant les data à tracer
         : Par défaut : Un dictionnaire ne contenant qu'une seule simulation
         : Soit un jeu de plusieurs datas (Compare = True)


    Compare : = True si on veut comparer plusieurs données
              Ne rien mettre (Compare = False par défaut) : on veut tracer qu'une seule donnée

    **kwargs : contient d'autres paramètres comme
             label : si jamais on veut ajouter un label à une donnée d'un graphique qui n'en aurait ou qui en aurait un autre
             AddGraph = True : Si jamais on veut ajouter un autre graphique sur le dernier graphique tracé
                               : False par défaut, les nouvelles données seront tracées en effaçant les anciennes sur le subplot en cours

    """

    # get the customlabel if a label arguent is declared, puts None otherwise as a default value
    customlabel = kwargs.get("label", None)

    # Get AddGraph function. Puts it to false by default if it's not declared in the kwargs
    AddGraph = kwargs.get("AddGraph", False)

    GraphType = "COPGraph"

    # Verigications for when simulationCases are used
    if CasesOn:
        # Active tous les cas présents dans data
        if CasesOn == "all":
            CasesOn = list(data.keys())

        # Vérifie que Cases est toujours une liste si 'all' n'est pas utilisé
        elif not type(CasesOn) is list:
            raise ValueError(
                "CasesOn doit être une liste si 'all' n'est pas utilisé")
            return

        # Vérifie qu'on n'active pas plusieurs cas tout en comparant
        if len(CasesOn) > 1 and Compare:
            raise ValueError(
                "On ne peut pas comparer plusieurs simulations et plusieurs cas en même temps")
            return

    SubplotSetup(Subplot, AddGraph)
    plt.plot(GleneContour[:, 0], GleneContour[:, 1], color='tab:blue')

    # Sets the aspect ratio between x and y axis to be equal
    plt.gca().set_aspect('equal')

    Composante_x = "x"
    Composante_y = "y"
    Variable_x = "COP"
    Variable_y = "COP"

    if Compare is False:

        if CasesOn is False:
            label = None
            PlotGraph(data, data[Variable_x][Composante_x], data[Variable_y][Composante_y],
                      GraphType, DrawPeakCOPAngleOn=DrawPeakCOPAngleOn, DrawGHReactionsNodes=DrawGHReactionsNodes, label=label, customlabel=customlabel)

        # If the graph used is CasesGraph
        else:
            for Case in CasesOn:
                label = Case
                PlotGraph(data[Case], data[Case][Variable_x][Composante_x], data[Case][Variable_y][Composante_y], GraphType,
                          label=label, customlabel=customlabel, DrawPeakCOPAngleOn=DrawPeakCOPAngleOn, DrawGHReactionsNodes=DrawGHReactionsNodes)

    elif Compare:

        ListSimulations = list(data.keys())

        for Simulation in ListSimulations:
            label = Simulation

            if CasesOn is False:
                PlotGraph(data[Simulation], data[Simulation][Variable_x][Composante_x], data[Simulation][Variable_y][Composante_y],
                          GraphType, label=label, customlabel=customlabel, DrawPeakCOPAngleOn=DrawPeakCOPAngleOn, DrawGHReactionsNodes=DrawGHReactionsNodes)

            # When we compare, we compare only one case between several simulations
            elif len(CasesOn) == 1:
                PlotGraph(data[Simulation][CasesOn[0]], data[Simulation][CasesOn[0]][Variable_x][Composante_x], data[Simulation][CasesOn[0]][Variable_y]
                          [Composante_y], GraphType, label=label, customlabel=customlabel, DrawPeakCOPAngleOn=DrawPeakCOPAngleOn, DrawGHReactionsNodes=DrawGHReactionsNodes)

    # Setups the grid and the axes ticks of the graph
    GraphGridSetup("COP", "COP")

    plt.xlabel("<----- Postérieur            Antérieur ----->")
    plt.ylabel("<----- Inférieur            Supérieur ----->")

    if Subplot is None:
        plt.title(FigureTitle)
        LegendSetup(Subplot)

    # Dans le cas d'un subplot
    else:

        # If a subplot title is entered, draws it (SubplotTitle isn't a bool)
        if not type(SubplotTitle) is bool:
            plt.title(SubplotTitle)

        # Ne trace la légende que si le dernier graphique du subplot est vide
        # Trace le titre du graphique que lorsqu'on trace le dernier graphique du subplot
        if (len(ax.shape) == 1 and ax[-1].lines) or (not len(ax.shape) == 1 and ax[-1, -1].lines):

            LegendSetup(Subplot)

            # Trace le titre de la figure
            plt.suptitle(FigureTitle)

            # Ajuste les distances entre les subplots quand ils sont tous tracés
            plt.tight_layout()


# %% test

# import Anybody_LoadOutput as LoadOutput

# GleneContour = DefineGleneContour("GleneContour")

# # Imports the module to import .h5 and AnyFileOut

# SaveDatadir = 'SaveData/Variation_CSA/'

# SimulationCases = ["Case 1", "Case 2", "Case 3", "Case 4", "Case 5"]

# CasesFilesList1 = ['Results-31-07-case1-droit-GlenoidAxisTilt-EnFace-CustomForce',
#                     'Results-31-07-case2-droit-GlenoidAxisTilt-EnFace-CustomForce',
#                     'Results-31-07-case3-droit-GlenoidAxisTilt-EnFace-CustomForce',
#                     'Results-31-07-case4-droit-GlenoidAxisTilt-EnFace-CustomForce',
#                     'Results-31-07-case5-droit-GlenoidAxisTilt-EnFace-CustomForce']


# CasesFilesList2 = [
#     'Results-17-07-case1-antero-Droit-EnFace21',
#     'Results-17-07-case2-antero-Droit-EnFace21',
#     'Results-17-07-case3-antero-Droit-EnFace21',
#     '',
#     'Results-17-07-case5-antero-EnFace21'
# ]


# CasesOffCompareOff = LoadOutput.LoadResultsh5(SaveDatadir, 'Results-31-07-case5-droit-GlenoidAxisTilt-EnFace-CustomForce', AddConstants=True)

# CasesOnCompareOff = LoadOutput.LoadSimulationCases(SaveDatadir, CasesFilesList1, SimulationCases, AddConstants=True)

# CasesOnCompareOn = LoadOutput.LoadSimulations(SaveDatadir, [CasesFilesList1, CasesFilesList2], ["simulation 1", "simulation 2"], AddConstants=True, SimulationCases=SimulationCases)

# CasesOffCompareOn = LoadOutput.LoadSimulations(SaveDatadir, CasesFilesList1, ["simulation 1", "simulation 2", "simulation 3", "simulation 4", "simulation 5"], AddConstants=True)


# %%                                 TEST GRAPH
# %% pas de cas de simulation

# # Compare = False
# Graph(CasesOffCompareOff, "Angle", "ForceContact", "Force contact CasesOn = False Compare = False")
# Graph(CasesOffCompareOff, "Angle", "ForceContact", "Force contact CasesOn = False Compare = False en x", Composante_y=["x"])
# Graph(CasesOffCompareOff, "Angle", "ForceContact", "Force contact CasesOn = False Compare = False plusieurs composantes", Composante_y=["x", "y", "z", "Total"])


# # Compare = True

# Graph(CasesOffCompareOn, "Angle", "ForceContact", "Force contact CasesOn = False Compare = True", Compare=True)
# Graph(CasesOffCompareOn, "Angle", "ForceContact", "Force contact CasesOn = False Compare = True en x", Composante_y=["x"], Compare=True)

# # Message d'erreur fait
# Graph(CasesOffCompareOn, "Angle", "ForceContact", "Force contact CasesOn = False Compare = True plusieurs composantes", Composante_y=["x", "y", "z", "Total"], Compare=True)

# %% Cas de simulation

# # Compare = False

# # 1 Case
# Graph(CasesOnCompareOff, "Angle", "ForceContact", "Force contact CasesOn = True Compare = False Un case", CasesOn=["Case 1"])
# Graph(CasesOnCompareOff, "Angle", "ForceContact", "Force contact CasesOn = True Compare = False en x Un case", Composante_y=["x"], CasesOn=["Case 1"])
# Graph(CasesOnCompareOff, "Angle", "ForceContact", "Force contact CasesOn = True Compare = False plusieurs composantes Un case", Composante_y=["x", "y", "z", "Total"], CasesOn=["Case 1"])

# # Plusieurs cases mais une seule variable_y
# Graph(CasesOnCompareOff, "Angle", "ForceContact", "Force contact CasesOn = True Compare = False plusieurs cases", CasesOn=["Case 1", "Case 2"])
# Graph(CasesOnCompareOff, "Angle", "ForceContact", "Force contact CasesOn = True Compare = False en x plusieurs cases", Composante_y=["x"], CasesOn=["Case 1", "Case 2"])

# # Message d'erreur fait
# Graph(CasesOnCompareOff, "Angle", "ForceContact", "Force contact CasesOn = True Compare = False plusieurs composantes plusieurs cases", Composante_y=["x", "y", "z", "Total"], CasesOn=["Case 1", "Case 2"])


# # All cases mais une seule variable_y
# Graph(CasesOnCompareOff, "Angle", "ForceContact", "Force contact CasesOn = True Compare = False cases all", CasesOn='all')
# Graph(CasesOnCompareOff, "Angle", "ForceContact", "Force contact CasesOn = True Compare = False en x cases all", Composante_y=["x"], CasesOn='all')

# # Message d'erreur fait
# Graph(CasesOnCompareOff, "Angle", "ForceContact", "Force contact CasesOn = True Compare = False plusieurs composantes cases all", Composante_y=["x", "y", "z", "Total"], CasesOn='all')


# # Compare = True

# # 1 Case
# Graph(CasesOnCompareOn, "Angle", "ForceContact", "Force contact CasesOn = True Compare = True Un case", CasesOn=["Case 1"], Compare=True)
# Graph(CasesOnCompareOn, "Angle", "ForceContact", "Force contact CasesOn = True Compare = True en x Un case", Composante_y=["x"], CasesOn=["Case 1"], Compare=True)

# # Message d'erreur fait
# Graph(CasesOnCompareOn, "Angle", "ForceContact", "Force contact CasesOn = True Compare = True plusieurs composantes Un case", Composante_y=["x", "y", "z", "Total"], CasesOn=["Case 1"], Compare=True)


# # Plusieurs cases mais une seule variable_y
# # Message d'erreut fait
# Graph(CasesOnCompareOn, "Angle", "ForceContact", "Force contact CasesOn = True Compare = True plusieurs cases", CasesOn=["Case 1", "Case 2"], Compare=True)
# Graph(CasesOnCompareOn, "Angle", "ForceContact", "Force contact CasesOn = True Compare = True en x plusieurs cases", Composante_y=["x"], CasesOn=["Case 1", "Case 2"], Compare=True)
# Graph(CasesOnCompareOn, "Angle", "ForceContact", "Force contact CasesOn = True Compare = True plusieurs composantes plusieurs cases", Composante_y=["x", "y", "z", "Total"], CasesOn=["Case 1", "Case 2"], Compare=True)


# # All cases mais une seule variable_y
# # Message d'erreut fait
# Graph(CasesOnCompareOn, "Angle", "ForceContact", "Force contact CasesOn = True Compare = True cases all", CasesOn='all', Compare=True)
# Graph(CasesOnCompareOn, "Angle", "ForceContact", "Force contact CasesOn = True Compare = True en x cases all", Composante_y=["x"], CasesOn='all', Compare=True)
# Graph(CasesOnCompareOn, "Angle", "ForceContact", "Force contact CasesOn = True Compare = True plusieurs composantes cases all", Composante_y=["x", "y", "z", "Total"], CasesOn='all', Compare=True)


# %%                                 TEST MUSCLEGRAPH
# %% pas de cas de simulation

# # Juste une partie ou le total
# MuscleGraph(CasesOffCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = False Compare = False")
# MuscleGraph(CasesOffCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = False Compare = False", MusclePartOn=[2])

# # Plusieurs part
# MuscleGraph(CasesOffCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = False Compare = False", MusclePartOn=[1, 2])
# MuscleGraph(CasesOffCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = False Compare = False", MusclePartOn="all")
# MuscleGraph(CasesOffCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = False Compare = False", MusclePartOn="allparts")


# # Compare True
# # Juste une partie ou le total
# MuscleGraph(CasesOffCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = False Compare = True", Compare=True)
# MuscleGraph(CasesOffCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = False Compare = False", MusclePartOn=[2], Compare=True)

# # Plusieurs part
# # Message d'erreur fait
# MuscleGraph(CasesOffCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = False Compare = True", MusclePartOn=[1, 2], Compare=True)
# MuscleGraph(CasesOffCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = False Compare = True", MusclePartOn="all", Compare=True)
# MuscleGraph(CasesOffCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = False Compare = True", MusclePartOn="allparts", Compare=True)


# %% Cas de simulation


# # Compare = False

# # 1 Case
# # Juste une partie ou le total
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", CasesOn=["Case 1"])
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", MusclePartOn=[2], CasesOn=["Case 1"])

# # Plusieurs part 1 case
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", MusclePartOn=[1, 2], CasesOn=["Case 1"])
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", MusclePartOn="all", CasesOn=["Case 1"])
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", MusclePartOn="allparts", CasesOn=["Case 1"])


# # plusieurs Cases
# # Juste une partie ou le total
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", CasesOn=["Case 1", "Case 2"])
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", MusclePartOn=[2], CasesOn=["Case 1", "Case 2"])
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", CasesOn="all")
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", MusclePartOn=[2], CasesOn="all")


# # Plusieurs part, plusieurs case
# # Message d'erreur fait
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", MusclePartOn=[1, 2], CasesOn="all")
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", MusclePartOn="all", CasesOn="all")
# MuscleGraph(CasesOnCompareOff, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = False", MusclePartOn="allparts", CasesOn="all")


# # Compare True
# # 1 Case
# # Juste une partie ou le total
# MuscleGraph(CasesOnCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = True", Compare=True, CasesOn=["Case 1"])
# MuscleGraph(CasesOnCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = True", MusclePartOn=[2], Compare=True, CasesOn=["Case 1"])

# # Plusieurs part
# # Message d'erreur fait
# MuscleGraph(CasesOnCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = True", MusclePartOn=[1, 2], Compare=True, CasesOn=["Case 1"])
# MuscleGraph(CasesOnCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = True", MusclePartOn="all", Compare=True, CasesOn=["Case 1"])
# MuscleGraph(CasesOnCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = True", MusclePartOn="allparts", Compare=True, CasesOn=["Case 1"])


# # Plusieurs Case
# # Juste une partie ou le total
# # Message d'erreut fait
# MuscleGraph(CasesOnCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = True", Compare=True, CasesOn=["Case 1", "Case 2"])
# MuscleGraph(CasesOnCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = True", MusclePartOn=[2], Compare=True, CasesOn=["Case 1", "Case 2"])

# # Plusieurs part un cas
# # Message d'erreur fait
# MuscleGraph(CasesOnCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = True", MusclePartOn=[1, 2], Compare=True, CasesOn=["Case 1", "Case 2"])
# MuscleGraph(CasesOnCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = True", MusclePartOn="all", Compare=True, CasesOn=["Case 1", "Case 2"])
# MuscleGraph(CasesOnCompareOn, "deltoideus lateral", "Angle", "Fm", "Force muscle CasesOn = True Compare = True", MusclePartOn="allparts", Compare=True, CasesOn=["Case 1", "Case 2"])

# %%                                 TEST COPGRAPH
# # Pas de cas de simulation

# # Compare = False
# COPGraph(CasesOffCompareOff, "COPGraph Cases False Compare False", GleneContour)
# COPGraph(CasesOffCompareOn, "COPGraph Cases False Compare True", GleneContour, Compare=True)

# # Cas de simulation
# COPGraph(CasesOnCompareOff, "COPGraph Cases False Compare False", GleneContour, CasesOn="all")

# # Message d'erreur fait
# COPGraph(CasesOnCompareOn, "COPGraph Cases False Compare True", GleneContour, Compare=True, CasesOn="all")
# COPGraph(CasesOnCompareOn, "COPGraph Cases False Compare True", GleneContour, Compare=True, CasesOn="Case 1")
