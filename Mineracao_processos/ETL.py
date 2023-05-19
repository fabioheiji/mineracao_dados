import pm4py
from pm4py.objects.conversion.bpmn import converter as bpmn_converter
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
from pm4py.algo.analysis.woflan import algorithm as woflan

from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
import os

def model_metrics(log, petri_net, initial_marking, final_marking, model_name, results = {}):
    prec = pm4py.precision_token_based_replay(log, petri_net, initial_marking, final_marking)
    print("Precision - Token replay: {}".format(prec))

    # prec = pm4py.precision_alignments(log, petri_net, initial_marking, final_marking)
    # print("Precision - Aligments: {}".format(prec))

    gen = generalization_evaluator.apply(log, petri_net, initial_marking, final_marking)
    print("Generalization: {}".format(gen))

    simp = simplicity_evaluator.apply(petri_net)
    print("Simplicity: {}".format(simp))

    # is_sound = woflan.apply(petri_net, initial_marking, final_marking, parameters={woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True,
    #                                                  woflan.Parameters.PRINT_DIAGNOSTICS: False,
    #                                                  woflan.Parameters.RETURN_DIAGNOSTICS: False})
    
    # print("Sound?: {}".format(is_sound))
    results[model_name]={
        'Precisao':prec,
        'Generalizacao':gen,
        'Simplicidade':simp,        
    }        

    return results

def discovery(path_folder_file=None,path_folder_bpmn=None,path_folder_png=None):
    ##########################################################################################
    # Trocar estes paths######################################################################
    # path_folder_file = "/Users/yamada/USP/Materias/7 semestre/Mineracao de dados/Celonis Dataset/BPI Challenge 2020 - Prepaid Travel Costs/"
    # path_folder_bpmn = "/Users/yamada/USP/Materias/7 semestre/Mineracao de dados/Celonis Dataset/BPI Challenge 2020 - Prepaid Travel Costs/"
    # path_folder_png = "./Mineracao_processos"
    ##########################################################################################
    ##########################################################################################

    path_file = os.path.join(path_folder_file,'PrepaidTravelCost.xes')
    log = pm4py.read_xes(path_file)

    results = {}
    
    # Inductive Miner
    # BPMN
    bpmn_model = pm4py.discover_bpmn_inductive(log)
    # pm4py.view_bpmn(bpmn_model)
    path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_inductive.bpmn")
    path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_inductive.png")
    pm4py.save_vis_bpmn(bpmn_model,path3)
    pm4py.write_bpmn(bpmn_model, path2)

    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)
    results = model_metrics(log, petri_net, initial_marking, final_marking, 'Inductive_Miner')

    # Heuristic Miner
    # BPMN
    bpmn_model = pm4py.discover_heuristics_net(log, dependency_threshold=0.99)
    bpmn_model = pm4py.convert_to_bpmn(bpmn_model)
    # pm4py.view_bpmn(bpmn_model)
    path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_heuristic.bpmn")
    path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_heuristic.png")
    pm4py.save_vis_bpmn(bpmn_model,path3)
    pm4py.write_bpmn(bpmn_model, path2)

    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(log)
    results = model_metrics(log, petri_net, initial_marking, final_marking, 'Heuristic_Miner', results)


    # Heuristic Miner
    # BPMN
    bpmn_model = pm4py.discover_heuristics_net(log, dependency_threshold=0.99,and_threshold=.99, loop_two_threshold=.99)
    bpmn_model = pm4py.convert_to_bpmn(bpmn_model)
    # pm4py.view_bpmn(bpmn_model)
    path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_heuristic_99.bpmn")
    path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_heuristic_99.png")
    pm4py.save_vis_bpmn(bpmn_model,path3)
    pm4py.write_bpmn(bpmn_model, path2)

    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(log,dependency_threshold=0.99, and_threshold=.99, loop_two_threshold=.99)
    results = model_metrics(log, petri_net, initial_marking, final_marking, 'Heuristic_Miner_0.99', results)

    # Alpha
    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(log)
    results = model_metrics(log, petri_net, initial_marking, final_marking, 'Alpha', results)

    # Alpha Plus
    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_alpha_plus(log)
    results = model_metrics(log, petri_net, initial_marking, final_marking, 'Alpha_Plus', results)

    return results

if __name__ == "__main__":

    path_folder_file = "/Users/yamada/USP/Materias/7 semestre/Mineracao de dados/Celonis Dataset/BPI Challenge 2020 - Prepaid Travel Costs/"
    path_folder_bpmn = "/Users/yamada/USP/Materias/7 semestre/Mineracao de dados/Celonis Dataset/BPI Challenge 2020 - Prepaid Travel Costs/"
    path_folder_png = "./Mineracao_processos"
    results = discovery(path_folder_file,path_folder_bpmn,path_folder_png)
    print(results)
    # ##########################################################################################
    # # Trocar estes paths######################################################################
    # path_folder_file = "/Users/yamada/USP/Materias/7 semestre/Mineracao de dados/Celonis Dataset/BPI Challenge 2020 - Prepaid Travel Costs/"
    # path_folder_bpmn = "/Users/yamada/USP/Materias/7 semestre/Mineracao de dados/Celonis Dataset/BPI Challenge 2020 - Prepaid Travel Costs/"
    # path_folder_png = "./Mineracao_processos"
    # ##########################################################################################
    # ##########################################################################################

    # path_file = os.path.join(path_folder_file,'PrepaidTravelCost.xes')
    # log = pm4py.read_xes(path_file)

    # # Inductive Miner
    # # bpmn_model = pm4py.discover_bpmn_inductive(log)
    # # pm4py.view_bpmn(bpmn_model)
    # # path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_inductive.bpmn")
    # # path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_inductive.png")
    # # pm4py.save_vis_bpmn(bpmn_model,path3)
    # # pm4py.write_bpmn(bpmn_model, path2)

    # petri_net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)

    # prec, gen, simp = model_metrics(log, petri_net, initial_marking, final_marking)    


    # '''

    # # Heuristic Miner
    # bpmn_model = pm4py.discover_heuristics_net(log, dependency_threshold=0.99)
    # bpmn_model = pm4py.convert_to_bpmn(bpmn_model)
    # # pm4py.view_bpmn(bpmn_model)
    # path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_heuristic.bpmn")
    # path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_heuristic.png")
    # pm4py.save_vis_bpmn(bpmn_model,path3)
    # pm4py.write_bpmn(bpmn_model, path2)
    
    # # Heuristic Miner
    # bpmn_model = pm4py.discover_heuristics_net(log, dependency_threshold=0.99,and_threshold=.99, loop_two_threshold=.99)
    # bpmn_model = pm4py.convert_to_bpmn(bpmn_model)
    # # pm4py.view_bpmn(bpmn_model)
    # path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_heuristic_99.bpmn")
    # path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_heuristic_99.png")
    # pm4py.save_vis_bpmn(bpmn_model,path3)
    # pm4py.write_bpmn(bpmn_model, path2)
    # '''
