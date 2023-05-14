import pm4py
import os
if __name__ == "__main__":
    ##########################################################################################
    # Trocar estes paths######################################################################
    path_folder_file = "/Users/yamada/USP/Materias/7 semestre/Mineracao de dados/Celonis Dataset/BPI Challenge 2020 - Prepaid Travel Costs/"
    path_folder_bpmn = "/Users/yamada/USP/Materias/7 semestre/Mineracao de dados/Celonis Dataset/BPI Challenge 2020 - Prepaid Travel Costs/"
    path_folder_png = "./Mineracao_processos"
    ##########################################################################################
    ##########################################################################################

    path_file = os.path.join(path_folder_file,'PrepaidTravelCost.xes')
    log = pm4py.read_xes(path_file)
    bpmn_model = pm4py.discover_bpmn_inductive(log)
    # pm4py.view_bpmn(bpmn_model)
    path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_inductive.bpmn")
    path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_inductive.png")
    pm4py.save_vis_bpmn(bpmn_model,path3)
    pm4py.write_bpmn(bpmn_model, path2)

    # Heuristic Miner
    bpmn_model = pm4py.discover_heuristics_net(log, dependency_threshold=0.99)
    bpmn_model = pm4py.convert_to_bpmn(bpmn_model)
    # pm4py.view_bpmn(bpmn_model)
    path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_heuristic.bpmn")
    path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_heuristic.png")
    pm4py.save_vis_bpmn(bpmn_model,path3)
    pm4py.write_bpmn(bpmn_model, path2)
    
    # Heuristic Miner
    bpmn_model = pm4py.discover_heuristics_net(log, dependency_threshold=0.99,and_threshold=.99, loop_two_threshold=.99)
    bpmn_model = pm4py.convert_to_bpmn(bpmn_model)
    # pm4py.view_bpmn(bpmn_model)
    path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_heuristic_99.bpmn")
    path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_heuristic_99.png")
    pm4py.save_vis_bpmn(bpmn_model,path3)
    pm4py.write_bpmn(bpmn_model, path2)
