# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 09:47:45 2023
Functions to load output data from EpauleFDK .h5 and AnyFileOut and create a dictionnary containing variables and the simulations informations
@author: Dan
"""


# Libraries needed
import numpy as np
import anypytools.h5py_wrapper as h5py2
from anypytools.datautils import read_anyoutputfile

class DefineSimulationOutput:
    """    
    Avant de charger des simulations, utiliser cette fonction
    Permet de créer plusieurs listes de variables à charger selon la simulation
    
    Permet d'initialiser :
            SimulationVariables : Quelles sont les variables à charger des fichiers h5, leur noms...
            SimulationConstants : Les constantes à charger
            MusclesArray : Les muscles à charger
            MusclesVariables : Les variables musculaires à charger contenues dans un fichier texte

    Le résultat sera dans les variables d'entrée des fonctions LoadResultsh5, LoadSimulationCases et LoadSimulations

        MusclesArray =  np.array['MuscleFolderPath','AnybodyMuscleName','PartString',nPart,'MuscleName']

        Ex: to load the deltoideus lateral (Called deltoideus_lateral_part_n in anybody) that has 4 parts and give it the name Deltoideus Lateral
            and the supraspinatus (Called supraspinatus_n) that has 6 parts and give it the name Supraspinatus:
            MusclesArray = np.array([["deltoideus_lateral","_part_",4,"deltoideus lateral"],["supraspinatus","_",6,"Supraspinatus"]])
            MusclesArray has a dimension of nMuscles x 1

    Exemple :
        SimulationOutput_1 = DefineSimulationOutput(SimulationVariables, SimulationConstants, MusclesArray, MusclesVariables)

        Results_1 = LoadResultsh5(SaveDatadir, 'Simulation1', SimulationOutput)

        Pour une simulation avec les mêmes variables à charger
        Results_2 = LoadResultsh5(SaveDatadir, 'Simulation_2', SimulationOutput_1)

        Pour une simulation avec d'autres variables à charger
        SimulationOutput_2 = DefineSimulationOutput(SimulationVariables2, SimulationConstants2, MusclesArray2, MusclesVariables2)

        Results_3 = LoadResultsh5(SaveDatadir, 'Simulation_3', SimulationOutput_2)
    """

    def __init__(self, SimulationVariables=None, SimulationConstants=None, MusclesArray=None, MusclesVariables=None):
        self.SimulationVariables = SimulationVariables
        self.SimulationConstants = SimulationConstants
        self.MusclesArray = MusclesArray
        self.MusclesVariables = MusclesVariables

            

# %% Math Functions


def TransformVector(Vector, RotMatrix, TranslationVect, InverseTransform=False):
    """
    Transforme un vecteur avec une matrice de rotation et le bouge d'un certain vecteur pour chaque pas de temps

    RotMatrix est la matrice de rotation à chaque pas de temps (nstep,3,3)

    TranslationVect : Vecteur de translation colonne à chaque pas de temps (nstep,1)

    Le vecteur à transformer à chaque pas de temps est une matrice (nstep,3)

    InverseTransform : False : Transformation directe : RotMat * Vector + TranslationVector
                       True : si on veut faire une transformation inverse (Vector = Vector * (RotMat - TranslationVector))

    """

    nstep = Vector.shape[0]

    TransformedVector = np.zeros([nstep, 3])

    # Transformation directe
    if InverseTransform is False:
        for step in range(nstep):
            TransformedVector[step, :] = np.dot(
                RotMatrix[step, :, :], Vector[step, :]) + TranslationVect[step, :]

    # Transformation inverse
    if InverseTransform:
        for step in range(nstep):
            TransformedVector[step, :] = np.dot(
                RotMatrix[step, :, :].T, Vector[step, :] - TranslationVect[step, :])

    return TransformedVector


# %% Mise en forme des dictionnaires de variables
def ArrayToDictionnary(Array, VariableDescription='', SequenceComposantes='', MultiplyFactor=1):
    """
    Met en forme un array 2D (nstep,ndim) sous la forme d'un dictionnaire :
        "Description" : Description qui sera utilisée par les graphiques

        SequenceComposantes : sépare ensuite les composantes dans un dictionnaire selon la séquence précisée (forme de liste ["composante 1","Composante 2"...])
        Par défaut : La séquence par défaut est ['x','y','z']
                   : WARNING : par défaut, les vecteurs sont séparés en 3 composantes maximum

        "Total" : Calcule la valeur totale de la variable à chaque step de simulation
                : Cette valeur n'est pas calculée si la séquence de composante contient la valeur "Total"
    """

    VariableOutput = {}
    VariableOutput["Description"] = VariableDescription

    # If the output is a vector, puts the output in total and no components are created
    if Array.ndim == 1:
        VariableOutput["Total"] = Array * MultiplyFactor

        # Stores the variable component sequence
        VariableOutput["SequenceComposantes"] = ["Total"]

    # If the output is multidimensional
    else:
        # Si la séquence n'est pas spécifiée, met xyz en séquence par défaut en s'adaptant au nombre de composantes
        DefaultSequence = ['x', 'y', 'z']
        if SequenceComposantes == '':
            SequenceComposantes = DefaultSequence[0:Array.shape[1]]

        # Parcours le nom des composantes dans l'ordre spécifié
        for col, Composante in enumerate(SequenceComposantes):
            VariableOutput[Composante] = Array[:, col] * MultiplyFactor

        # Calculates the total of the component at each timestep if the total is not already calculated
        if "Total" not in SequenceComposantes:
            VariableOutput["Total"] = np.linalg.norm(
                Array, axis=1) * MultiplyFactor

        # Stores the variable component sequence
        VariableOutput["SequenceComposantes"] = SequenceComposantes

    return VariableOutput


# %% Load AnyFileOut File Variable

def LoadAnyFileOutVariable(FileOutPath, FileType, VariablePath=str, LoadConstantsOnly=False):
    """
    Loads a specific variable from an AnyFileOut file
    Or can load only the constants
    """

    data, dataheader, constantsdata = read_anyoutputfile(
        FileOutPath + "." + FileType)

    if LoadConstantsOnly is False:
        # Constructs a dictionary with all the variables and constants
        DataDictionary = {}
        for index, Variable in enumerate(dataheader):

            # Deletes the anybody path of the variable name to only keep the variable name
            Variable = Variable.replace("Main.Study.FileOut.", "")

            DataDictionary[Variable] = data[:, index]

        # adds the variable to DataDictionary
        for index, Variable in enumerate(constantsdata):

            DataDictionary[Variable] = constantsdata[Variable]

        # Loads every variable and constants
        if VariablePath == "all":
            Output = DataDictionary
        else:
            # Loads a specific variable
            Output = DataDictionary[VariablePath]

    # Loads only the constanst
    if LoadConstantsOnly:
        Output = constantsdata

    return Output


# %% Load AnyFileOut File
def LoadAnyFileOut(FileOutPath, FileType="txt", LoadConstantsOnly=False):
    """
    Load an AnyFileOut and creates a dictionnary
    FileType : says if the FileOut is a .txt,.csv...
    LoadConstantsOnly : True if output must only be the constants to complete these missing informations while loading a .h5 file
    Ex : FileOut.txt :
         FileOutPath = File Path and Name
         FileType = txt
    """

    # Constantes à charger
    Parametres_FDK = ["k0", "k1", "k2", "k3", "k4", "kz", "kd",
                      "ForceTol", "UseAdaptiveForceTolOnOff", "MaxIteration", "Perturbation", "PerturbationSymmetricOnOff", "LocalSearchOnOff", "MaxNewtonStep"]
    Positions_initiales = ["px", "py", "pz"]
    Implants_Parameters = ["HumerusName", "GlenoidName", "Case", "GleneImplantTiltAngle", "RotationAxis",
                           "GlenImplantRotation", "GlenImplantPosition", "GlenImplantCenter", "HumImplantPosition", "HumImplantRotation", "AcromionOffset"]
    Simulation_Parameters = ["Movement", "Case", "GHReactions", "nstep"]
    Mannequin = ["GlenohumeralFlexion",
                 "GlenohumeralAbduction", "GlenohumeralExternalRotation"]
    MyMuscleWrapping = ["WrappingSurfaceShape", "LateralWrapping_RadiusX",
                        "LateralWrapping_Radius", "LateralWrapping_RadiusHeight"]

    """
    Add the variable to load from the text file here
    """
    # The variables are loaded only if LoadConstantsOnly is False
    # if LoadConstantsOnly == False:

    # If only the constants need to be loaded
    if LoadConstantsOnly:
        FileOut = {}

    # Loads the constants
    constantsdata = LoadAnyFileOutVariable(
        FileOutPath, FileType, LoadConstantsOnly=True)

    # All the constants names in the .txt file
    constantsNames = list(dict.keys(constantsdata))

    # Goes through all constants names
    # Adds constants to the ouptut data and puts it in seperated dictionary keys depending on their names
    for Variable in constantsNames:
        VariableName = Variable.replace("Main.Study.FileOut.", "")

        if any(i == VariableName for i in Parametres_FDK):

            # creates the dictionnary if it doesn't exist yet
            if "Paramètres FDK" not in FileOut:
                FileOut["Paramètres FDK"] = {}

            FileOut["Paramètres FDK"][VariableName] = constantsdata[Variable]

        if any(i == VariableName for i in Positions_initiales):

            # creates the dictionnary if it doesn't exist yet
            if "Positions initiales" not in FileOut:
                FileOut["Positions initiales"] = {}

            FileOut["Positions initiales"][VariableName] = constantsdata[Variable]

        if any(i == VariableName for i in Implants_Parameters):

            # creates the dictionnary if it doesn't exist yet
            if "Paramètres implants" not in FileOut:
                FileOut["Paramètres implants"] = {}

            FileOut["Paramètres implants"][VariableName] = constantsdata[Variable]

        if any(i == VariableName for i in Simulation_Parameters):

            # creates the dictionnary if it doesn't exist yet
            if "Paramètres de simulation" not in FileOut:
                FileOut["Paramètres de simulation"] = {}

            FileOut["Paramètres de simulation"][VariableName] = constantsdata[Variable]

        if any(i == VariableName for i in Mannequin):

            # creates the dictionnary if it doesn't exist yet
            if "Mannequin" not in FileOut:
                FileOut["Mannequin"] = {}

            FileOut["Mannequin"][VariableName] = constantsdata[Variable]

        if any(i == VariableName for i in MyMuscleWrapping):

            # creates the dictionnary if it doesn't exist yet
            if "MyMuscleWrapping" not in FileOut:
                FileOut["MyMuscleWrapping"] = {}

            FileOut["MyMuscleWrapping"][VariableName] = constantsdata[Variable]

    return FileOut
# %% Load h5 variable


def LoadAnyVariable(Path, VariablePath, Failed, VariableDescription="", SequenceComposantes='', MultiplyFactor=1, OutputDictionnary=True):
    """
    Uses the Anypytool function to load a model variable from an .anydata.h5 file by using the anybody variable path in the study with . instead of /

    Warning : Only non constants values are stored in h5

    Creates a dictionnary containing : The variable description that will be used for graphs
                                       If the variable is multidinensional : The variable total is calculated and the components are output
                                       If the variable is a vector : The variable is put in "Total" and no components are created

    Path is the path of the file to load (it must begin with "Output." since it's the output data that is stored in an h5 file)
    Failed : removes the values in the results in case the simulation failed after a certain time
    Failed : is the first step number that failed (if the step number go from 0 to nstep)
    VariableDescription : Description of the variable that is going to be used in the axis label on the graph
    SequenceComposantes : Indicates which colomns corresponds to which component (x,y or z)
                          The sequence is xyz by defaukt. So the first column will be x, then y then z
    MultiplyFactor : If multiplying every value by a factor is needed (to convert m to mm for example)

    OutputDictionnary : Can be put on False to be able to have Variable in an array and not in a dictionnary that seperates it's components
                      : False must be used if you want to make calculations or if Variable is not in 2D but more (examples rotation matrices)

    Ex: to load the variable  : Seg.Scapula.ghProth.Axes
        VariablePath = "Output.Seg.Scapula.ghProth.Axes"

    h5File has to be a global variable defined as the h5 file loaded with anypytools.h5py_wrapper:

        global h5File
        with h5py2.File(Path + '.anydata.h5', "r") as h5File:
    """

    # # Charge le fichier h5 en ajoutant l'extension au nom du fichier
    # h5Path += '.anydata.h5'

    # # Avec cette fonction on peut utiliser les mêmes chemins d'accès aux variables que anybody
    # with h5py2.File(h5Path, "r") as f:

    # Ne cherche la variable que si elle existe dans le fichier
    if VariablePath in h5File:
        Output = np.array(h5File[VariablePath])

    # Si la variable n'existe pas, ne la cherche pas, met un message d'erreur et remplit la variable avec des 0
    else:
        print("La variable : " + VariablePath + " n'existe pas dans le fichier h5 : " + Path + '.anydata.h5')
        Output = np.zeros(len(h5File["Output.Abscissa.t"]))

    # If Failed is the number of the first step that failed, deletes these failed steps
    if type(Failed) is int:

        # Shape of the Output
        shapeOutput = np.shape(Output)

        # Shape of the part without fails
        shapeClean = np.copy(shapeOutput)
        shapeClean[0] = Failed

        # Shape of the part with failes
        shapeFailed = np.copy(shapeOutput)
        shapeFailed[0] = shapeOutput[0] - Failed

        # Creates arrays full of True to select non-failed steps
        Clean = np.full(tuple(shapeClean), True)
        # Creates arrays full of False to select failed steps
        Failed = np.full(tuple(shapeFailed), False)

        # Creates a mask of the same size of the output
        mask = np.append(Clean, Failed, axis=0)

        # Select the data from output without fails
        CleanOutput = Output[mask]

        # shape the output back to it's original shape
        CleanOutput = np.reshape(CleanOutput, shapeClean)

    # When none of the steps failed
    else:
        CleanOutput = Output

    # Mise en forme du dictionnaire output si activé
    if OutputDictionnary:

        # Converts the array to a dictionnary
        VariableOutput = ArrayToDictionnary(
            CleanOutput, VariableDescription, SequenceComposantes, MultiplyFactor)

    # Variable output est un array si OutputDictionnary est False
    else:
        VariableOutput = CleanOutput * MultiplyFactor

    return VariableOutput


# %% Load Muscles
def LoadMuscle(FilePath, MuscleFolderPath, AnybodyMuscleName, MuscleName, PartString, nParts=1, Failed=False, FileType="h5"):
    """
    Load the variables of a muscle from a .anydata.h5 file or from a AnyFileOut file (when the type is h5 but another extension)
    Failed : removes the 0 in the results in case the simulation failed after a certain time
    It can handle muscles that are seperated in multiple parts (deltoideys lateral has 5 muscles in anybody)

    Also calculates the total of each variable along the multiple parts.
    For the activity or corrected activity, the Total is the mean activity of all parts at each timestep
    If the variable is an activity or a force, also calculates its maximum at each timestep and names this component "Max"

    nParts : number of parts the muscle has
    PartString : String to add after the name to have the name of the muscle part in anybody
    Ex : deltoideus goes from deltoideus_lateral_part_1 to deltoideus_lateral_part_5
         nParts = 5
         PartString = "_part_"

    """

    MuscleOutput = {}

    # The names in Anybody of the muscle variables to load for each muscles
    AnybodyVariableNames = ["Ft", "Fm", "CorrectedActivity"]

    # Names to give in the dictionnary (renames Corrected Activity to activity)
    VariableNames = ["Ft", "Fm", "Activity"]

    # Multiply factors to apply
    # The activity is multilpied by 100 to be in %
    MultiplyFactors = [1, 1, 100]

    VariableDescriptions = [
        "Force musculaire totale [Newton]", "Force musculaire [Newton]", "Activité du muscle [%]"]

    # If the muscle is in one part
    if nParts == 1:

        # Loads the muscle variables from a h5 file
        if FileType == "h5":

            # Parcours les variables à load et les met dans le dictionnaire du muscle
            for index, VariableName in enumerate(VariableNames):
                MusclePath = MuscleFolderPath + "." + AnybodyMuscleName + "." + AnybodyVariableNames[index]

                MuscleOutput[VariableName] = LoadAnyVariable(
                    FilePath, MusclePath, Failed, VariableDescription=VariableDescriptions[index], MultiplyFactor=MultiplyFactors[index])

        # Loads the muscle variables from a AnyFileOut file
        else:
            for VariableName in VariableNames:
                MusclePath = MuscleFolderPath + "." + AnybodyMuscleName + "." + AnybodyVariableNames[index]
                MuscleOutput[VariableName] = LoadAnyFileOutVariable(
                    FilePath, FileType, MusclePath)

    # if the muscle is divided in multiple parts
    else:

        # Parcours les numéros des muscleparts pour ensuite load les part une à une
        for Part in range(1, nParts + 1):

            # Creates the name of the muscle part in anybody
            AnybodyMusclePart = AnybodyMuscleName + PartString + str(Part)

            # Creates the name of the muscle part given in the Output dictionnary
            MusclePart = MuscleName + " " + str(Part)

            # Puts every musclepart values in a different dictionnary key
            MuscleOutput[MusclePart] = {}

            # Loads the muscle variables from a h5 file
            if FileType == "h5":

                # For every variable, loads the data of every part of the muscle
                for index, VariableName in enumerate(VariableNames):

                    MusclePath = MuscleFolderPath + "." + AnybodyMusclePart + "." + AnybodyVariableNames[index]

                    # Loads the muscle part variables
                    MuscleOutput[MusclePart][VariableName] = LoadAnyVariable(
                        FilePath, MusclePath, Failed, VariableDescription=VariableDescriptions[index], MultiplyFactor=MultiplyFactors[index])

            # Loads the muscle variables from a AnyFileOut file
            else:
                # For every variable, loads the data of every part of the muscle
                for VariableName in VariableNames:

                    MusclePath = MuscleFolderPath + "." + AnybodyMusclePart + "." + AnybodyVariableNames[index]

                    # Loads the muscle part variables
                    MuscleOutput[MusclePart][VariableName] = LoadAnyFileOutVariable(
                        FilePath, FileType, MusclePath)

        # Computes the total variable of every part and stores it under a dictionnary named MuscleName
        MuscleParts = list(dict.keys(MuscleOutput))

        # Initializes the dictionnary that will store the total muscle variables
        MuscleOutput[MuscleName] = {}

        # Goes through every variable and sums every variable
        for Variabeindex, VariableName in enumerate(VariableNames):
            # Creates the array that will store the total of each variable
            MuscleTotal = np.zeros(
                [len(MuscleOutput[MusclePart][VariableName]["Total"]), nParts])

            # Goes through every muscle part and makes a sum
            for Partindex, Part in enumerate(MuscleParts):

                # Construit une matrice avec les valeurs de toutes les parties
                MuscleTotal[:, Partindex] = MuscleOutput[Part][VariableName]["Total"]

            # For forces and activities, calculates the total and the maximum of the variable along every muscelpart for each timestep
            if "F" == VariableName[0]:
                MuscleTotalVariable = np.zeros([len(MuscleOutput[MusclePart][VariableName]["Total"]), 2])

                MuscleTotalVariable[:, 0] = np.sum(MuscleTotal, axis=1)
                MuscleTotalVariable[:, 1] = np.max(MuscleTotal, axis=1)
                SequenceComposantes = ["Total", "Max"]

            # If the variable is the activity, the total is the mean activity
            elif "Activity" in VariableName:
                MuscleTotalVariable[:, 0] = np.mean(MuscleTotal, axis=1)
                MuscleTotalVariable[:, 1] = np.max(MuscleTotal, axis=1)
                SequenceComposantes = ["Total", "Max"]

            # Only calculates the total along every musclepart for each timestep
            else:
                MuscleTotalVariable = np.sum(MuscleTotal, axis=1)
                SequenceComposantes = ""

            # Puts the total muscle variable in the dictionnary using the standard dictionnary shape ("Total","Description")
            MuscleOutput[MuscleName][VariableName] = ArrayToDictionnary(
                MuscleTotalVariable, VariableDescription=VariableDescriptions[Variabeindex], SequenceComposantes=SequenceComposantes)

    return MuscleOutput


def LoadMuscleList(FilePath, MusclesArray, Failed=False, FileType=str):
    """
    Loads the muscles variables stored in a .anydata.h5 file or a AnyFileOut file
    The muscles to load, the number of parts to load, the part string and the name of the muscle to put in the dictionnaryare stored in the array :
    MusclesArray =  np.array['MuscleFolderPath','AnybodyMuscleName','PartString',nPart,'MuscleName']

    FileType : h5 or AnyFileOut

    Ex: to load the deltoideus lateral (Called deltoideus_lateral_part_n in anybody) that has 4 parts and give it the name Deltoideus Lateral
        and the supraspinatus (Called supraspinatus_n) that has 6 parts and give it the name Supraspinatus:
        MusclesArray = np.array([["deltoideus_lateral","_part_",4,"deltoideus lateral"],["supraspinatus","_",6,"Supraspinatus"]])
        MusclesArray has a dimension of nMuscles x 1
    """

    Muscles = {}
    # Parcours les noms de muscles dans MusclesArray (première colonne)
    for Muscle_number, AnybodyMuscleName in enumerate(MusclesArray[:, 1]):
        # Sélectionne le nombre de parties
        Muscle_nPart = int(MusclesArray[Muscle_number, 3])

        # Sélectionne la chaine de charactère avant le numéro de partie
        PartString = MusclesArray[Muscle_number, 2]
        # Sélectionne le nom complet du dossier dans lequel le muscle est situé sur Anybody
        MuscleFolderPath = MusclesArray[Muscle_number, 0]

        # Name to give to the muscle in the dictionnary
        MuscleName = MusclesArray[Muscle_number, 4]

        # Met le muscle dans un dossier en fonction du nom choisi
        Muscles[MuscleName] = LoadMuscle(
            FilePath, MuscleFolderPath, AnybodyMuscleName, MuscleName, PartString, Muscle_nPart, Failed, FileType)

    return Muscles


def LoadGHReactions(GHReactionsShape, Path, Failed, RotG, PosG):
    """
    Loads the GHReactions informations :
    The EdgeMuscles and the CavityNodes Position in the local glenoid implant reference frame

    GHReactions can be "Circle" or "Edge" depending on the type of the GHReactions used
    """
    CavityEdgeNode = {}
    # Initialise Muscle array as a (0,5) np.array
    EdgeMusclesArray = np.empty((0, 5), int)

    if GHReactionsShape == "Circle":
        EdgeMuscleDir = 'Output.Seg.Scapula.GlenImplantPos.GHReactionCenterNode.CavityEdgeNode'
    elif GHReactionsShape == "Edge":
        EdgeMuscleDir = 'Output.Seg.Scapula.GlenImplantPos.CavityEdgeNode'

    # Total number of edge muscles
    NumberEdgeMuscles = 8
    # Creates a MuscleArray to load the EdgeMuscles
    EdgeMusclesArray = np.array(
        [["Output.Jnt.MyGHReactions", "EdgeMuscle", "", NumberEdgeMuscles, "Edge muscle"]])

    # Goes through every edgemuscles
    for EdgeMuscleNumber in range(1, NumberEdgeMuscles + 1):
        # Gets the position of the EdgeMuscles insertion points in mm
        Pos = LoadAnyVariable(Path, EdgeMuscleDir + str(EdgeMuscleNumber) + '.r', Failed, MultiplyFactor=1000, OutputDictionnary=False)

        # Transforms the global position to the local coordinate system of the glenoid implant
        # Only takes the position at the first step because it is a constant

        PosLocal = TransformVector(Pos, RotG, PosG, InverseTransform=True)

        CavityEdgeNode["Cavity EdgeNode " + str(EdgeMuscleNumber)] = PosLocal[0, :]

    # Loads the Muscles variables
    GHReactions = LoadMuscleList(Path, EdgeMusclesArray, Failed, FileType="h5")
    # Adds the shape of the GHReaction
    GHReactions["Shape"] = GHReactionsShape
    # Adds the position of the edgenodes
    GHReactions["Cavity Nodes Position"] = CavityEdgeNode

    Constants = LoadAnyFileOutVariable(Path, 'txt', LoadConstantsOnly=True)
    # Loads the Strength of the EdgeMuscles only if it's in the FileOut file
    if "Main.Study.FileOut.EdgeMuscleStrength" in Constants:
        GHReactions["Muscles Strength"] = Constants["Main.Study.FileOut.EdgeMuscleStrength"]

    return GHReactions


# %% Load h5 data

def LoadResultsh5(FileDirectory, FileName, AddConstants=False, Failed=False, GHReactions=False, MyMuscleWrapping=False):
    """
    Reads variables from an anydata.h5 file

    Charge plusieurs h5 et les mets dans le même dictionnaire sous forme de cas de simulation

    FileDirectory : Type : string
                  : Chemin d'accès au dossier où le fichiers h5 sont situés

    FileName : Nom des fichiers à charger
             : Noms des fichier (sans extension)
             : pour un fichier Resultats.anydata.h5 FileName = "Resultats"

    AddConstants : Mettre à True si un fichier texte existe au même nom et au même endroit pour charger les constantes de simulations définies dans LoadResultsh5

    Sums the total variable for a muscle in multiple parts
    AddConstants : adds the constants that are not stored in the h5 file by reading them in the FileOut file
    Failed : removes the failed steps in case the simulation failed after a certain step
    GHReactions : If the new MyGHReactions.any was activated, load these muscles and load the position of the
    MyMuscleWrapping : list of the names of the muscles that were redefined with new wrapping (lateral, posterior or anterior)

    Template to load a variable :
        Results["nom_de_variable"] = LoadAnyVariable(Path, "Output.Chemin.accès.variable.dans.Anybody.depuis.l'output",Failed,MultiplyFactor = , VariableDescription = "Description de la variable [unité de la variable]")
    """

    # Chemin d'accès au fichier (sans l'extension)
    Path = FileDirectory + FileName

    global h5File
    # Avec cette fonction on peut utiliser les mêmes chemins d'accès aux variables que anybody
    with h5py2.File(Path + '.anydata.h5', "r") as h5File:

        Results = {}
        # List of muscles to load and number of parts
        MusclesArray = np.array([
            ["Output.Mus", "deltoideus_lateral", "_part_", 4, "deltoideus lateral"],
            ["Output.Mus", "deltoideus_anterior", "_part_", 4, "deltoideus anterior"],
            ["Output.Mus", "deltoideus_posterior", "_part_", 4, "deltoideus posterior"],
            ["Output.Mus", "supraspinatus", "_", 6, "supraspinatus"]
        ])

        # if some deltoideus muscles have been redefined to change de muscle wrapping
        if type(MyMuscleWrapping) is list:

            # Change le nom du muscle vers My_ + nom du muscle si ce muscle a été redéfini pour permettre de changer le wrapping
            if "lateral" in MyMuscleWrapping:
                MusclesArray[0][1] = "My_" + MusclesArray[0][1]

            if "anterior" in MyMuscleWrapping:
                MusclesArray[1][1] = "My_" + MusclesArray[1][1]

            if "posterior" in MyMuscleWrapping:
                MusclesArray[2][1] = "My_" + MusclesArray[2][1]

        Results["Angle"] = LoadAnyVariable(
            Path, 'Output.rotD', Failed, VariableDescription="Angle d'abduction [°]")

        # Loads Epsilon in mm
        Results["Eps"] = LoadAnyVariable(Path, 'Output.Jnt.SpringForce.Eps', Failed,
                                         MultiplyFactor=1000, VariableDescription="Déplacement relatif de l'humérus [mm]", SequenceComposantes=["AP", "IS", "ML"])

        Results["SpringForce"] = LoadAnyVariable(
            Path, 'Output.Jnt.SpringForce.F', Failed, VariableDescription="Force de ressort [Newton]")

        Results["ForceContact"] = LoadAnyVariable(
            Path, 'Output.Jnt.ProtheseContact.Fmaster', Failed, VariableDescription="Force de contact [Newton]")

        Results["ForceTolError"] = LoadAnyVariable(
            Path, 'Output.ForceDepKinError.Val', Failed, VariableDescription="FDK Residual Force Error [N]")

        # Loads GHLin in mm
        Results["GHLin"] = LoadAnyVariable(Path, 'Output.Jnt.GHLin.Pos', Failed,
                                           MultiplyFactor=1000, VariableDescription="Déplacement Linéaire de l'humérus [mm]", SequenceComposantes=["AP", "IS", "ML"])

        """Glenoid implant position and rotation in the global body reference frame
        In an array to be used to convert the COP in the local reference frame of the scapula
        """
        # Rotation of the glenoid implant
        RotG = LoadAnyVariable(
            Path, 'Output.Seg.Scapula.GlenImplantPos.Axes', Failed, OutputDictionnary=False)

        # Position of the glenoid converted in mm
        PosG = LoadAnyVariable(Path, 'Output.Seg.Scapula.GlenImplantPos.r',
                               Failed, OutputDictionnary=False, MultiplyFactor=1000)

        # COP in mm in an array to be converted in local reference frame
        COPGlobal = LoadAnyVariable(
            Path, 'Output.Jnt.ProtheseContact.COP', Failed, MultiplyFactor=1000, OutputDictionnary=False)

        # COP in mm calculated with an inverse transform to be converted to the local glenoid implant reference frame
        COPlocalImplant = TransformVector(
            COPGlobal, RotG, PosG, InverseTransform=True)

        Results["COP"] = ArrayToDictionnary(
            COPlocalImplant, VariableDescription="Position du centre de pression [mm]")

        # Maximal COPy position
        Results["COP"]["Max y Angle"] = {}
        Results["COP"]["Max y Angle"]["y"] = np.amax(COPlocalImplant[:, 1])

        # x positon when COPy is maximal
        Results["COP"]["Max y Angle"]["x"] = COPlocalImplant[:,
                                                             0][np.argmax(COPlocalImplant[:, 1])]

        # Angle when COPy is maximal
        Results["COP"]["Max y Angle"]["Angle"] = round(
            Results["Angle"]["Total"][np.argmax(COPlocalImplant[:, 1])], 1)

        # Minimal COPy position
        Results["COP"]["Min y Angle"] = {}
        Results["COP"]["Min y Angle"]["y"] = np.amin(COPlocalImplant[:, 1])

        # x positon when COPy is maximal
        Results["COP"]["Min y Angle"]["x"] = COPlocalImplant[:,
                                                             0][np.argmin(COPlocalImplant[:, 1])]

        # Angle when COPy is maximal
        Results["COP"]["Min y Angle"]["Angle"] = round(
            Results["Angle"]["Total"][np.argmin(COPlocalImplant[:, 1])], 1)

        """
        Checks the type of GHReactions, if it's a string it means that it was activated
        If the reaction forces were activated, creates a new entry in Results where the muscles and the nodes positions of GHReactions are stored
        """
        if type(GHReactions) is str:
            Results["GHReactions"] = LoadGHReactions(
                GHReactions, Path, Failed, RotG, PosG)

        # Gets the muscles variables
        Muscles = LoadMuscleList(Path, MusclesArray, Failed, FileType="h5")

        Results["Muscles"] = Muscles

        if AddConstants:
            Constants = LoadAnyFileOut(Path, LoadConstantsOnly=True)

            Results["Model informations"] = Constants

    # Ferme le fichier h5
    h5File.close()

    return Results


def LoadResultsLauranne(Path, Failed=False):

    global h5File

    # Avec cette fonction on peut utiliser les mêmes chemins d'accès aux variables que anybody
    with h5py2.File(Path + '.anydata.h5', "r") as h5File:

        Results = {}

        Results["Angle"] = LoadAnyVariable(
            Path, 'Output.rotD', Failed, VariableDescription="Angle d'abduction [°]")

        # Loads Epsilon in mm
        Results["Eps"] = LoadAnyVariable(Path, 'Output.Jnt.SpringForce.Eps', Failed,
                                         MultiplyFactor=1000, VariableDescription="Déplacement relatif de l'humérus [mm]")

        Results["SpringForce"] = LoadAnyVariable(
            Path, 'Output.Jnt.SpringForce.F', Failed, VariableDescription="Force de ressort [Newton]")

        Results["ForceContact"] = LoadAnyVariable(
            Path, 'Output.Jnt.ProtheseContact.Fmaster', Failed, VariableDescription="Force de contact [Newton]")

        # Loads GHLin in mm
        Results["GHLin"] = LoadAnyVariable(Path, 'Output.Jnt.GHLin.Pos', Failed,
                                           MultiplyFactor=1000, VariableDescription="Déplacement Linéaire de l'humérus [mm]")

        """Glenoid implant position and rotation in the global body reference frame
        In an array to be used to convert the COP in the local reference frame of the scapula
        """
        RotG = LoadAnyVariable(
            Path, 'Output.Seg.Scapula.GlenImplantPos.Axes', Failed, OutputDictionnary=False)

        # Position converted in mm
        PosG = LoadAnyVariable(Path, 'Output.Seg.Scapula.GlenImplantPos.r',
                               Failed, OutputDictionnary=False, MultiplyFactor=1000)

        # COP in mm in an array to be converted in local reference frame
        COPGlobal = LoadAnyVariable(
            Path, 'Output.Jnt.ProtheseContact.COP', Failed, MultiplyFactor=1000, OutputDictionnary=False)

        # COP in mm calculated with an inverse transform to be converted to the local glenoid implant reference frame
        COPlocalImplant = TransformVector(
            COPGlobal, RotG, PosG, InverseTransform=True)

        Results["COP"] = ArrayToDictionnary(
            COPlocalImplant, "Position du centre de pression [mm]")

        # Maximal COPy position
        Results["COP"]["Max y Angle"] = {}
        Results["COP"]["Max y Angle"]["y"] = np.amax(COPlocalImplant[:, 1])

        # x positon when COPy is maximal
        Results["COP"]["Max y Angle"]["x"] = COPlocalImplant[:, 0][np.argmax(COPlocalImplant[:, 1])]

        # Angle when COPy is maximal
        Results["COP"]["Max y Angle"]["Angle"] = round(
            Results["Angle"]["Total"][np.argmax(COPlocalImplant[:, 1])], 1)

    return Results


def LoadGraphLauranne():

    AngleGraph = np.array([14.94949494949495, 19.7979797979798, 24.646464646464647, 29.696969696969695, 34.74747474747475, 41.01010101010101, 47.27272727272727, 53.535353535353536, 60.4040404040404, 66.06060606060606, 72.12121212121212, 77.97979797979798, 80.60606060606061, 84.44444444444444, 87.27272727272727, 90.3030303030303, 92.92929292929293,
                          95.95959595959596, 98.78787878787878, 103.43434343434343, 105.85858585858585, 108.88888888888889, 111.51515151515152, 112.32323232323232, 112.92929292929293, 114.34343434343434, 114.54545454545455, 115.15151515151516, 116.56565656565657, 118.18181818181817, 118.78787878787878, 118.78787878787878, 118.78787878787878, 118.78787878787878, 120]).T
    ForceGraph = np.array([119.17808219178083, 147.94520547945206, 184.9315068493151, 217.80821917808223, 252.7397260273973, 304.10958904109594, 347.26027397260276, 394.5205479452055, 439.72602739726034, 486.98630136986304, 534.2465753424658, 577.3972602739726, 602.0547945205481, 663.6986301369864, 713.013698630137, 766.4383561643837, 823.9726027397261,
                          879.4520547945207, 918.4931506849316, 936.9863013698631, 957.5342465753425, 1000.6849315068495, 1017.123287671233, 1050, 1070.5479452054797, 1080.8219178082193, 1111.6438356164385, 1140.4109589041097, 1115.7534246575344, 1128.082191780822, 1080.8219178082193, 1041.7808219178082, 1013.0136986301371, 984.2465753424658, 984.2465753424658]).T

    COPxGraph = np.array([-3.4211374407582933, -5.03081081081081,
                         4.105550239234449, -3.6108837209302322, -0.7566666666666666]).T
    COPyGraph = np.array([0.06222222222222223, 5.378048780487806,
                         4.7882736156351795, 3.276971608832808, 0.36408668730650157]).T

    COP = np.array([COPxGraph, COPyGraph]).T

    Results = {}
    Results["Angle"] = ArrayToDictionnary(
        AngleGraph, VariableDescription="Angle d'abduction [°]")
    Results["ForceContact"] = ArrayToDictionnary(
        ForceGraph, VariableDescription="Force de contact [Newton]")
    Results["COP"] = ArrayToDictionnary(
        COP, VariableDescription="Position du centre de pression [mm]")
    Results["COP"]["Max y Angle"] = {
        "Angle": 60, "x": COPxGraph[2], "y": COPyGraph[2]}

    # Results = {"Angle":AngleGraph, "ForceContact":{"ForceTotale":ForceGraph},"COP":{"x":COPxGraph,"y":COPyGraph,"Max y Angle":{"Angle":60,"x":COPxGraph[2],"y":COPyGraph[2]}}}

    return Results

# %% Load des simulations ou des cas de simulation


def LoadSimulationCases(FileDirectory, CasesFileNamesList, SimulationCases, AddConstants=False, Failed=False):
    """
    Charge plusieurs h5 et les mets dans le même dictionnaire sous forme de cas de simulation

    FileDirectory : Type : string
                  : Chemin d'accès au dossier où les fichiers h5 sont situés
                  : Les fichiers doivent être dans le même dossier

    CasesFileNamesList : Liste des noms des fichiers à charger
             : Noms des fichier (sans extension)
             : pour un fichier Resultats.anydata.h5 FileName = "Resultats"


    SimulationCases : type liste
                    : Nom des cas de simulation à mettre comme clé de dictionnaire

    AddConstants : Mettre à True si un fichier texte existe au même nom et au même endroit pour charger les constantes de simulations définies dans LoadResultsh5

    Failed : List containing the first Failed step of each simulation, or False if the simulation didn't failed

    Exemple 1 : FileNamesList = ['nom__cas1','nom_cas2','nom__cas3']
              : SimulationCases = ['Cas 1','Cas 2','Cas 3']

    Exemple 2 : Les cas de simulations vont de 1 à 3 mais cette simulation n'a que les cas 1 et 2
              : On met donc le second nom de fichier à '' pour signifier que cette simulation n'a pas de cas 2
              : CasesFileNamesList = ['nom__cas1','','nom__cas3']
              : SimulationCases = ['Cas 1','Cas 2','Cas 3']

    Exemple 3 : On remplit les cas de simulation au fur et à mesure. Il y a 3 cas mais le cas 3 n'a pas encore été simulé :
              : SimulationCases = ['Cas 1','Cas 2','Cas 3']
              : CasesFileNamesList = ['nom__cas1','nom__cas2',''] ou ['nom__cas1','nom__cas2']
    """

    # Si aucun cas n'a fail, crée une liste remplie de Failed = False
    if Failed is False:
        Failed = [False] * len(CasesFileNamesList)

    Results = {}
    # Parcours le nom des cas de simulation et charge les fichiers h5 correspondants
    for index in range(len(CasesFileNamesList)):

        # Crée un cas de simulation seulement si un fichier existe pour ce cas
        if not CasesFileNamesList[index] == '':
            Results[SimulationCases[index]] = LoadResultsh5(
                FileDirectory, CasesFileNamesList[index], AddConstants, Failed[index])

    return Results


def LoadSimulations(FileDirectory, FileNamesList, SimulationNamesList, AddConstants=False, SimulationCases=False):
    """
    Charge plusieurs h5 et les mets dans le même dictionnaire sous forme de simulation avec des noms différents qui pourront être comparés avec Compare = True dans les graphiques

    FileDirectory : Type : string
                  : Chemin d'accès au dossier où les fichiers h5 sont situés
                  : Les fichiers doivent être dans le même dossier

    FileNamesList : Liste des noms des fichiers à charger
                  : Liste contenant le nom des simulations à mettre dans le dictionnaire


    FileNamesList : type : liste
                  : taille : [nbe simulations]
                  : pour un fichier Resultats.anydata.h5 FileName = "Resultats"
                                 : s'il y a des cas, chaque ligne est une liste de la taille [nombre de cas total] avec le nom de chaque cas
                                 : Cette liste en ligne doit avoir la même taille que la liste SimulationCases
                        : Un '' dans le nom de fichier pour un cas signifie que le cas n'est pas simulé pour cette simulation
                        :

    SimulationCases : type : liste
                    :
                    : Par défaut : False : S'il n'y a pas de cas de simulation
                    : liste des cas de simulation s'il y en a


    AddConstants : Mettre à True si un fichier texte existe au même nom et au même endroit pour charger les constantes de simulations définies dans LoadResultsh5

    Exemple :
                SimulationCases = Liste des noms de cas de simulation ['Cas 1','Cas 2','Cas 3']
                SimulationNamesList = liste des h5 à charger sous la forme :
                    [['nom_simulation1_cas1','nom_simulation1_cas2','nom_simulation1_cas3'],
                     ['nom_simulation2_cas1','','nom_simulation2_cas3']]

                Les simulations peuvent ne pas avoir tous les cas de simulation.
                Ici il y a 3 cas mais la simulation 2 n'a pas de cas 2. Donc '' est mis comme nom de fichier

    """

    """
    to check : check la taille de SimulationNamesList et voir si les lignes sont bien des listes avec SimulationCases = True
    check si autant de ligne dans simulationnameslist que dans filesnameslist
    """

    Results = {}

    # S'il y a des cas de simulation
    if type(SimulationCases) is list:

        # Parcours les simulations et ajoute les cas de simulation
        for index, Simulation in enumerate(SimulationNamesList):
            Results[Simulation] = LoadSimulationCases(
                FileDirectory, FileNamesList[index], SimulationCases, AddConstants)

    else:
        for index, Simulation in enumerate(SimulationNamesList):
            Results[Simulation] = LoadResultsh5(
                FileDirectory, FileNamesList[index], AddConstants)
    return Results
