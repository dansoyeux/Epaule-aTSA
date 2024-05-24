# -*- coding: utf-8 -*-
"""
Created on Thu May 23 11:32:41 2024

@author: Dan
"""

from Anybody_Package.Anybody_Graph.PremadeGraphs import muscle_graph_from_list
from Anybody_Package.Anybody_Graph.PremadeGraphs import muscle_graph_by_case_categories
from Anybody_Package.Anybody_Graph.PremadeGraphs import COP_graph_by_case_categories
from Anybody_Package.Anybody_Graph.PremadeGraphs import graph_by_case_categories

from Anybody_Package.Anybody_Graph.GraphFunctions import graph
from Anybody_Package.Anybody_Graph.GraphFunctions import COP_graph
from Anybody_Package.Anybody_Graph.GraphFunctions import muscle_graph

from Anybody_Package.Anybody_Graph.Tools import save_all_active_figures

from Anybody_Package.Anybody_Graph.GraphFunctions import define_simulations_line_style


def figures_article(Results, COP_contour, SimulationsLineStyleDictionary, list_muscles_actifs, CaseNames_36x, save_figure=False):
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
    }
    
    define_simulations_line_style(SimulationsLineStyleDictionary_article)

    Categories_Article = {"line": {"Downward inclination": ["xdown-xshort", "xdown-normal", "xdown-xlong"],
                                   "Neutral inclination": ["neutral-xshort", "neutral-normal", "neutral-xlong"],
                                   "Upward inclination": ["up-xshort", "up-normal", "up-xlong"]
                                   }}

    NeutralCases_3 = ["neutral-xshort", "neutral-normal", "neutral-xlong"]

    # Muscle Kinematics
    muscle_graph(Results, "Deltoid lateral", "Abduction", "Force Angle", subplot={"dimension": [1, 3], "number": 1}, cases_on=NeutralCases_3, subplot_title="Deltoid lateral force angle", grid_x_step=15, xlim=[15, 120], grid_y_step=10, ylim=[-80, 20], composante_y=["Origin"])
    muscle_graph(Results, "Deltoid lateral", "Abduction", "MomentArm", subplot={"dimension": [1, 3], "number": 2}, composante_y=["Mean"], cases_on=NeutralCases_3, subplot_title="Deltoid lateral moment arm", grid_x_step=15, xlim=[15, 120], grid_y_step=5, ylim=[0, 40])
    muscle_graph(Results, "Deltoid lateral", "Abduction", "Ft", subplot={"dimension": [1, 3], "number": 3}, composante_y=["Total"], cases_on=NeutralCases_3, subplot_title="Deltoid lateral force", grid_x_step=15, xlim=[15, 120], grid_y_step=25, ylim=[0, 200])

    # COP
    COP_graph_by_case_categories(Results, Categories_Article, COP_contour, composantes=["AP", "IS"], graph_annotation_on=False, draw_COP_points_on=False, COP_first_point_size=10, COP_first_point_mew=2, xlim=[-17, 17], ylim=[-19, 22], grid_x_step=5, legend_position="lower center", hide_center_axis_labels=True)

    # Contact forces for neutral inclination
    graph(Results, "Abduction", "ContactForce glenoid", figure_title="Contact Forces on the glenoid implant, neutral inclination", subplot_title="Posterior-anterior shear", composante_y=["AP"], cases_on=["neutral-xshort", "neutral-normal", "neutral-xlong"], subplot={"dimension": [1, 3], "number": 1})
    graph(Results, "Abduction", "ContactForce glenoid", figure_title="Contact Forces on the glenoid implant, neutral inclination", subplot_title="Inferior-superior shear", composante_y=["IS"], cases_on=["neutral-xshort", "neutral-normal", "neutral-xlong"], subplot={"dimension": [1, 3], "number": 2})
    graph(Results, "Abduction", "ContactForce glenoid", figure_title="Contact Forces on the glenoid implant, neutral inclination", subplot_title="Compression force", composante_y=["ML"], cases_on=["neutral-xshort", "neutral-normal", "neutral-xlong"], subplot={"dimension": [1, 3], "number": 3}, same_lim=True, grid_x_step=15, xlim=[15, 120], grid_y_step=50, ylim=[-100, 400], hide_center_axis_labels=True)

    # instability ratio
    graph_by_case_categories(Results, Categories_Article, "Abduction", "Instability Ratio", figure_title="Instability ratio", grid_x_step=15, xlim=[15, 120], same_lim=True, legend_on=True, hide_center_axis_labels=True, ylim=[0, 0.7])

    # Forces des muscles actifs
    define_simulations_line_style(SimulationsLineStyleDictionary)
    muscle_graph_from_list(Results, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Muscle forces", cases_on=CaseNames_36x, grid_x_step=15, xlim=[15, 120], ylim=[0, 200], hide_center_axis_labels=True, figsize=[24, 14], grid_y_step=50)

    # ajouter save graphiques si activé
    if save_figure:
        save_all_active_figures("Graphiques", "Article", "article", "png")



def all_variables_graphs(data, data_Ball_And_Socket, literature_data, save_folder_path="", save_folder_name="Saved_graphs", save_graph=False, save_format="png", composante_on=False, **graph_parameters):
    """For now, save_folder_path is a relative path (that's why we add "./" at the beginning )"""
    import os

    import matplotlib.pyplot as plt
    folder_full_path = f"./{save_folder_path}/{save_folder_name}"
    muscle_dir_path = f"{folder_full_path}/Muscles"
    Ft_dir_path = f"{muscle_dir_path}/Ft"
    MA_dir_path = f"{muscle_dir_path}/MomentArm"

    if save_graph:
        if os.path.exists(folder_full_path):

            raise ValueError(f"The folder :\n'{os.path.abspath(folder_full_path)}'\n already exists. Enter a folder that doesn't exist")

        # Creates the folder in which the files are going to be saved
        os.mkdir(folder_full_path)
        os.mkdir(f"{muscle_dir_path}")
        os.mkdir(f"{muscle_dir_path}/Ft")
        os.mkdir(f"{muscle_dir_path}/MomentArm")

        # Closes all figures
        plt.close("all")

    def my_muscle_categories_graph(data, data_Ball_And_Socket, folder_path, save_graph=False, save_format="png", list_muscles_actifs=[], list_muscles_peu_actif=[], list_muscles_inactifs=[], CaseNames_3="", CaseNames_5="", composante_on=False, **graph_parameters):

        subfolder_name = "Muscle Categories"
        graph_files_name = "Muscle_category"
        subfolder_path = f"{folder_path}/{subfolder_name}"

        figsize = [24, 14]

        data["Ball And Socket"] = data_Ball_And_Socket

        CaseNames_3_categories_F = [*CaseNames_3, "Ball And Socket"]
        CaseNames_5_categories_F = [*CaseNames_5, "Ball And Socket"]

        # Ft 9 cas
        muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Muscle Force (Ft > 10N)", cases_on=CaseNames_3_categories_F, figsize=figsize, ylim=[0, 200], **graph_parameters)
        muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Muscle Force (10 N > Ft > 5N)", cases_on=CaseNames_3_categories_F, figsize=figsize, ylim=[0, 20], **graph_parameters)
        muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Muscle Force (Ft < 5N)", cases_on=CaseNames_3_categories_F, figsize=figsize, ylim=[0, 20], **graph_parameters)

        # sans same_lim
        # Ft 9 cas
        muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Muscle Force (Ft > 10N)", cases_on=CaseNames_3_categories_F, figsize=figsize, **graph_parameters)
        muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Muscle Force (10 N > Ft > 5N)", cases_on=CaseNames_3_categories_F, figsize=figsize, **graph_parameters)
        muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Muscle Force (Ft < 5N)", cases_on=CaseNames_3_categories_F, figsize=figsize, **graph_parameters)

        # Ft 25 cas
        muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "Ft", "Muscle Force (Ft > 10N)", cases_on=CaseNames_5_categories_F, figsize=figsize, ylim=[0, 200], **graph_parameters)
        muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "Ft", "Muscle Force (10 N > Ft > 5N)", cases_on=CaseNames_5_categories_F, figsize=figsize, ylim=[0, 20], **graph_parameters)
        muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "Ft", "Muscle Force (Ft < 5N)", cases_on=CaseNames_5_categories_F, figsize=figsize, ylim=[0, 20], **graph_parameters)

        # Saves the figures in a sub folder
        if save_graph:
            save_all_active_figures(folder_path, subfolder_name, graph_files_name, save_format)

        if composante_on:
            figsize = [24, 18]
            # insertion
            composante = "Total"
            muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)

            composante = "Total_AP"
            muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)

            composante = "Total_IS"
            muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)

            composante = "Total_ML"
            muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "F insertion", f"Projected muscle force insertion {composante} (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)

            # Saves the figures in a sub folder insertion
            if save_graph:
                save_all_active_figures(subfolder_path, "Insertion", graph_files_name, save_format)

            # origin
            composante = "Total"
            muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)

            composante = "Total_AP"
            muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)

            composante = "Total_IS"
            muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)

            composante = "Total_ML"
            muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (Ft > 10N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (10 N > Ft > 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)
            muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "F origin", f"Projected muscle force origin {composante} (Ft < 5N)", composante_y=[composante], cases_on=CaseNames_3_categories_F, **graph_parameters, same_lim=True, figsize=figsize)

            # Saves the figures in a sub folder origine
            if save_graph:
                save_all_active_figures(subfolder_path, "Origine", graph_files_name, save_format)

        if save_graph:
            print("Muscle Force categories figures saved \n")

    def my_muscle_force_by_categories_graph(data, data_Ball_And_Socket, folder_path, save_graph=False, save_format="png", CasesCategories_3=None, CasesCategories_5=None, composante_on=False, muscle_list_by_categories=[], **graph_parameters):

        figsize_3 = [14, 13]
        figsize_5 = [24, 14]

        subfolder_name = "By Categories"
        graph_files_name = "By_Category"
        subfolder_path = f"{folder_path}/{subfolder_name}"

        data["Ball And Socket"] = data_Ball_And_Socket

        CasesCategories_3_F = {}
        CasesCategories_5_F = {}

        # adds Ball And Socket to the case categories
        for line_name, line in CasesCategories_3.items():
            CasesCategories_3_F[line_name] = {}
            for column_name, column in line.items():
                CasesCategories_3_F[line_name][column_name] = [*column, "Ball And Socket"]

        # adds Ball And Socket to the case categories
        for line_name, line in CasesCategories_5.items():
            CasesCategories_5_F[line_name] = {}
            for column_name, column in line.items():
                CasesCategories_5_F[line_name][column_name] = [*column, "Ball And Socket"]

        # Seulement le total
        muscle_graph_by_case_categories(data, CasesCategories_5_F, muscle_list_by_categories, "Abduction", "Ft", composante_y_muscle_combined=["Total"], figsize=figsize_5, muscle_part_on=False, same_lim=True, **graph_parameters)
        muscle_graph_by_case_categories(data, CasesCategories_3_F, muscle_list_by_categories, "Abduction", "Ft", composante_y_muscle_combined=["Total"], figsize=figsize_3, muscle_part_on=False, same_lim=True, **graph_parameters)

        # Saves the figures in a sub folder By Categories
        if save_graph:
            save_all_active_figures(folder_path, subfolder_name, graph_files_name, save_format)

        if composante_on:

            # F insertion
            # 25 cas
            muscle_graph_by_case_categories(data, CasesCategories_5_F, muscle_list_by_categories, "Abduction", "F insertion", composante_y_muscle_combined=["Total"], figsize=figsize_5, muscle_part_on=False, same_lim=True, **graph_parameters)
            muscle_graph_by_case_categories(data, CasesCategories_5_F, muscle_list_by_categories, "Abduction", "F insertion", composante_y_muscle_combined=["Total_AP"], figsize=figsize_5, muscle_part_on=False, same_lim=True, **graph_parameters)
            muscle_graph_by_case_categories(data, CasesCategories_5_F, muscle_list_by_categories, "Abduction", "F insertion", composante_y_muscle_combined=["Total_IS"], figsize=figsize_5, muscle_part_on=False, same_lim=True, **graph_parameters)
            muscle_graph_by_case_categories(data, CasesCategories_5_F, muscle_list_by_categories, "Abduction", "F insertion", composante_y_muscle_combined=["Total_ML"], figsize=figsize_5, muscle_part_on=False, same_lim=True, **graph_parameters)

            # # F insertion
            # # 9 cas
            # muscle_graph_by_case_categories(data, CasesCategories_3_F, muscle_list_by_categories, "Abduction", "F insertion", composante_y_muscle_combined=["Total"], figsize=figsize_3, muscle_part_on=False, same_lim=True, **graph_parameters)
            # muscle_graph_by_case_categories(data, CasesCategories_3_F, muscle_list_by_categories, "Abduction", "F insertion", composante_y_muscle_combined=["Total_AP"], figsize=figsize_3, muscle_part_on=False, same_lim=True, **graph_parameters)
            # muscle_graph_by_case_categories(data, CasesCategories_3_F, muscle_list_by_categories, "Abduction", "F insertion", composante_y_muscle_combined=["Total_IS"], figsize=figsize_3, muscle_part_on=False, same_lim=True, **graph_parameters)
            # muscle_graph_by_case_categories(data, CasesCategories_3_F, muscle_list_by_categories, "Abduction", "F insertion", composante_y_muscle_combined=["Total_ML"], figsize=figsize_3, muscle_part_on=False, same_lim=True, **graph_parameters)

            # Saves the figures in a sub folder insertion
            if save_graph:
                save_all_active_figures(subfolder_path, "Insertion", graph_files_name, save_format)

            # 25 cas
            # F origin
            muscle_graph_by_case_categories(data, CasesCategories_5_F, muscle_list_by_categories, "Abduction", "F origin", composante_y_muscle_combined=["Total"], figsize=figsize_5, muscle_part_on=False, same_lim=True, **graph_parameters)
            muscle_graph_by_case_categories(data, CasesCategories_5_F, muscle_list_by_categories, "Abduction", "F origin", composante_y_muscle_combined=["Total_AP"], figsize=figsize_5, muscle_part_on=False, same_lim=True, **graph_parameters)
            muscle_graph_by_case_categories(data, CasesCategories_5_F, muscle_list_by_categories, "Abduction", "F origin", composante_y_muscle_combined=["Total_IS"], figsize=figsize_5, muscle_part_on=False, same_lim=True, **graph_parameters)
            muscle_graph_by_case_categories(data, CasesCategories_5_F, muscle_list_by_categories, "Abduction", "F origin", composante_y_muscle_combined=["Total_ML"], figsize=figsize_5, muscle_part_on=False, same_lim=True, **graph_parameters)

            # # F origin
            # # 9 cas
            # muscle_graph_by_case_categories(data, CasesCategories_3_F, muscle_list_by_categories, "Abduction", "F origin", composante_y_muscle_combined=["Total"], figsize=figsize_3, muscle_part_on=False, same_lim=True, **graph_parameters)
            # muscle_graph_by_case_categories(data, CasesCategories_3_F, muscle_list_by_categories, "Abduction", "F origin", composante_y_muscle_combined=["Total_AP"], figsize=figsize_3, muscle_part_on=False, same_lim=True, **graph_parameters)
            # muscle_graph_by_case_categories(data, CasesCategories_3_F, muscle_list_by_categories, "Abduction", "F origin", composante_y_muscle_combined=["Total_IS"], figsize=figsize_3, muscle_part_on=False, same_lim=True, **graph_parameters)
            # muscle_graph_by_case_categories(data, CasesCategories_3_F, muscle_list_by_categories, "Abduction", "F origin", composante_y_muscle_combined=["Total_ML"], figsize=figsize_3, muscle_part_on=False, same_lim=True, **graph_parameters)

            # Saves the figures in a sub folder insertion
            if save_graph:
                save_all_active_figures(subfolder_path, "Origine", graph_files_name, save_format)

        if save_graph:
            print("Muscles by Muscle Categories figures saved\n")

    def my_muscle_moment_arm_graph(data, folder_path, save_graph=False, save_format="png", CaseNames_3=[], CaseNames_5=[], CasesCategories_3=None, CasesCategories_5=None, muscle_list_by_categories=[], list_muscles_actifs=[], list_muscles_peu_actif=[], list_muscles_inactifs=[], **graph_parameters):

        figsize_3 = [14, 13]
        figsize_5 = [24, 14]

        graph_files_name = "Moment_arm"

        figsize = [24, 14]

        # Ft 9 cas
        muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "MomentArm", "Moment Arm (Ft > 10N)", composante_y=["Mean"], cases_on=CaseNames_3, figsize=figsize, same_lim=True, **graph_parameters)
        muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "MomentArm", "Moment Arm (10 N > Ft > 5N)", composante_y=["Mean"], cases_on=CaseNames_3, figsize=figsize, same_lim=True, **graph_parameters)
        muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "MomentArm", "Moment Arm (Ft < 5N)", composante_y=["Mean"], cases_on=CaseNames_3, figsize=figsize, same_lim=True, **graph_parameters)

        # Ft 25 cas
        muscle_graph_from_list(data, list_muscles_actifs, [4, 3], "Abduction", "MomentArm", "Moment Arm (Ft > 10N)", composante_y=["Mean"], cases_on=CaseNames_5, figsize=figsize, same_lim=True, **graph_parameters)
        muscle_graph_from_list(data, list_muscles_peu_actif, [1, 3], "Abduction", "MomentArm", "Moment Arm (10 N > Ft > 5N)", composante_y=["Mean"], cases_on=CaseNames_5, figsize=figsize, same_lim=True, **graph_parameters)
        muscle_graph_from_list(data, list_muscles_inactifs, [3, 3], "Abduction", "MomentArm", "Moment Arm (Ft < 5N)", composante_y=["Mean"], cases_on=CaseNames_5, figsize=figsize, same_lim=True, **graph_parameters)

        if save_graph:
            save_all_active_figures(folder_path, "Muscle Categories", graph_files_name, save_format)

        # Seulement le total
        muscle_graph_by_case_categories(data, CasesCategories_3, muscle_list_by_categories, "Abduction", "MomentArm", composante_y_muscle_combined=["Mean"], figsize=figsize_5, muscle_part_on=False, same_lim=True, **graph_parameters)

        if save_graph:
            save_all_active_figures(folder_path, "By Categories", graph_files_name, save_format)
            print("Moment Arms figures saved\n")

    def my_COP_graph(data, folder_path, save_graph=False, save_format="png", CasesCategories_3=None, CasesCategories_5=None, **graph_parameters):

        subfolder_name = "COP"
        graph_files_name = "COP"
        # subfolder_path = f"{folder_path}/{subfolder_name}"

        COP_graph_parameters = graph_parameters.copy()
        COP_graph_parameters["xlim"] = [-15, 15]
        COP_graph_parameters["ylim"] = [-20, 20]
        COP_graph_parameters["grid_x_step"] = 5
        COP_graph_parameters["grid_y_step"] = 5

        figsize_3 = [14, 13]
        figsize_5 = [24, 14]

        COP_graph_parameters["annotation_offset"] = [0.8, -2.1]
        COP_graph_parameters["annotation_reference_offset"] = [1, 3]

        COP_graph_by_case_categories(data, CasesCategories_5, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], figsize=figsize_5, **COP_graph_parameters)
        COP_graph_by_case_categories(data, CasesCategories_3, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], figsize=figsize_3, **COP_graph_parameters)

        COP_graph_by_case_categories(data, CasesCategories_5, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], figsize=figsize_5, **COP_graph_parameters, graph_annotation_on=False)
        COP_graph_by_case_categories(data, CasesCategories_3, figure_title="Position du centre de pression", variable="COP", composantes=["AP", "IS"], figsize=figsize_3, **COP_graph_parameters, graph_annotation_on=False)

        graph_by_case_categories(data, CasesCategories_5, "Abduction", "COP", "COP en AP", composante_y=["AP"], figsize=figsize_5, same_lim=True, **graph_parameters)
        graph_by_case_categories(data, CasesCategories_5, "Abduction", "COP", "COP en IS", composante_y=["IS"], figsize=figsize_5, same_lim=True, **graph_parameters)

        graph_by_case_categories(data, CasesCategories_3, "Abduction", "COP", "COP en AP", composante_y=["AP"], figsize=figsize_3, same_lim=True, **graph_parameters)
        graph_by_case_categories(data, CasesCategories_3, "Abduction", "COP", "COP en IS", composante_y=["IS"], figsize=figsize_3, same_lim=True, **graph_parameters)

        if save_graph:
            save_all_active_figures(folder_path, subfolder_name, graph_files_name, save_format)
            print("COP figures saved\n")

    def my_ContactForce_graph(data, literature_data, folder_path, save_graph=False, save_format="png", CaseNames_3=None, CaseNames_5=None, CasesCategories_3=None, CasesCategories_5=None, **graph_parameters):

        subfolder_name = "ContactForce"
        graph_files_name = "ContactForce"
        subfolder_path = f"{folder_path}/{subfolder_name}"

        figsize_3 = [14, 13]
        figsize_5 = [24, 14]

        data_Bergmann = data.copy()
        data_Bergmann["Bergmann 2007"] = literature_data["ContactForce humerus"]["Bergmann 2007"]
        CaseNames_3_Bergmann = [*CaseNames_3, "Bergmann 2007"]

        CasesCategories_3_Bergmann = {}
        CasesCategories_5_Bergmann = {}

        # adds Bergmann to the case categories
        for line_name, line in CasesCategories_3.items():
            CasesCategories_3_Bergmann[line_name] = {}
            for column_name, column in line.items():
                CasesCategories_3_Bergmann[line_name][column_name] = [*column, "Bergmann 2007"]

        # adds Bergmann to the case categories
        for line_name, line in CasesCategories_5.items():
            CasesCategories_5_Bergmann[line_name] = {}
            for column_name, column in line.items():
                CasesCategories_5_Bergmann[line_name][column_name] = [*column, "Bergmann 2007"]

        # Comparé à bergmann
        # Graph simple
        graph(data_Bergmann, "Abduction", "ContactForce humerus", "Contact force on the humeral implant", cases_on=CaseNames_3_Bergmann, subplot={"dimension": [2, 2], "number": 1}, subplot_title="Total", composante_y=["Total"], **graph_parameters)
        graph(data_Bergmann, "Abduction", "ContactForce humerus", "Contact force on the humeral implant", cases_on=CaseNames_3_Bergmann, subplot={"dimension": [2, 2], "number": 2}, subplot_title="AP", composante_y=["AP"], **graph_parameters)
        graph(data_Bergmann, "Abduction", "ContactForce humerus", "Contact force on the humeral implant", cases_on=CaseNames_3_Bergmann, subplot={"dimension": [2, 2], "number": 3}, subplot_title="IS", composante_y=["IS"], **graph_parameters)
        graph(data_Bergmann, "Abduction", "ContactForce humerus", "Contact force on the humeral implant", cases_on=CaseNames_3_Bergmann, subplot={"dimension": [2, 2], "number": 4}, subplot_title="ML", composante_y=["ML"], **graph_parameters)

        graph_by_case_categories(data_Bergmann, CasesCategories_3_Bergmann, "Abduction", "ContactForce humerus", "Contact force on the humeral implant Total", composante_y=["Total"], figsize=figsize_3, same_lim=True, **graph_parameters)
        graph_by_case_categories(data_Bergmann, CasesCategories_3_Bergmann, "Abduction", "ContactForce humerus", "Contact force on the humeral implant AP", composante_y=["AP"], figsize=figsize_3, same_lim=True, **graph_parameters)
        graph_by_case_categories(data_Bergmann, CasesCategories_3_Bergmann, "Abduction", "ContactForce humerus", "Contact force on the humeral implant IS", composante_y=["IS"], figsize=figsize_3, same_lim=True, **graph_parameters)
        graph_by_case_categories(data_Bergmann, CasesCategories_3_Bergmann, "Abduction", "ContactForce humerus", "Contact force on the humeral implant ML", composante_y=["ML"], figsize=figsize_3, same_lim=True, **graph_parameters)

        if save_graph:
            os.mkdir(subfolder_path)
            save_all_active_figures(subfolder_path, "Comparaison Bergmann", graph_files_name, save_format)

        # Repère glene
        # Graph simple
        graph(data_Bergmann, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant", cases_on=CaseNames_3, subplot={"dimension": [2, 2], "number": 1}, subplot_title="Total", composante_y=["Total"], **graph_parameters)
        graph(data_Bergmann, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant", cases_on=CaseNames_3, subplot={"dimension": [2, 2], "number": 2}, subplot_title="AP", composante_y=["AP"], **graph_parameters)
        graph(data_Bergmann, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant", cases_on=CaseNames_3, subplot={"dimension": [2, 2], "number": 3}, subplot_title="IS", composante_y=["IS"], **graph_parameters)
        graph(data_Bergmann, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant", cases_on=CaseNames_3, subplot={"dimension": [2, 2], "number": 4}, subplot_title="ML", composante_y=["ML"], **graph_parameters)

        graph_by_case_categories(data, CasesCategories_3, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant Total", composante_y=["Total"], figsize=figsize_3, same_lim=True, **graph_parameters)
        graph_by_case_categories(data, CasesCategories_3, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant AP", composante_y=["AP"], figsize=figsize_3, same_lim=True, **graph_parameters)
        graph_by_case_categories(data, CasesCategories_3, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant IS", composante_y=["IS"], figsize=figsize_3, same_lim=True, **graph_parameters)
        graph_by_case_categories(data, CasesCategories_3, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant ML", composante_y=["ML"], figsize=figsize_3, same_lim=True, **graph_parameters)

        graph_by_case_categories(data, CasesCategories_5, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant Total", composante_y=["Total"], figsize=figsize_5, same_lim=True, **graph_parameters)
        graph_by_case_categories(data, CasesCategories_5, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant AP", composante_y=["AP"], figsize=figsize_5, same_lim=True, **graph_parameters)
        graph_by_case_categories(data, CasesCategories_5, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant IS", composante_y=["IS"], figsize=figsize_5, same_lim=True, **graph_parameters)
        graph_by_case_categories(data, CasesCategories_5, "Abduction", "ContactForce glenoid", "Contact force on the glenoid implant ML", composante_y=["ML"], figsize=figsize_5, same_lim=True, **graph_parameters)

        if save_graph:
            save_all_active_figures(subfolder_path, "Repère glene", graph_files_name, save_format)
            print("ContactForce figures saved\n")

    def my_FDKForceError(data, folder_path, save_graph=False, save_format="png", CasesCategories_3=None, CasesCategories_5=None, **graph_parameters):
        subfolder_name = "ForceDepKinError"
        graph_files_name = "ForceDepKinError"
        # subfolder_path = f"{folder_path}/{subfolder_name}"

        # figsize_3 = [14, 13]
        # figsize_5 = [24, 14]

        graph(data, "Abduction", "ForceDepKinError", "FDK Force Tolerence error", cases_on="all", composante_y=["Total"], **graph_parameters)

        if save_graph:
            save_all_active_figures(folder_path, subfolder_name, graph_files_name, save_format)
            print("FDK ForceTolerance figures saved\n")

    # Categories de muscles
    my_muscle_categories_graph(data, data_Ball_And_Socket, Ft_dir_path, save_graph, composante_on=composante_on, **graph_parameters)

    # Forces par variables
    my_muscle_force_by_categories_graph(data, data_Ball_And_Socket, Ft_dir_path, save_graph, composante_on=composante_on, save_format="png", **graph_parameters)

    # Moment arm
    my_muscle_moment_arm_graph(data, MA_dir_path, save_graph, save_format="png", **graph_parameters)

    # COP
    my_COP_graph(data, folder_full_path, save_graph, save_format="png", **graph_parameters)

    # ContactForce
    my_ContactForce_graph(data, literature_data, folder_full_path, save_graph, save_format="png", **graph_parameters)

    my_FDKForceError(data, folder_full_path, save_graph, save_format="png", **graph_parameters)

    if save_graph:
        abs_path = os.path.abspath(folder_full_path)
        print(f"All graph were succesfully saved in:\n{abs_path}\n")