import pandas as pd
import pm4py
from pm4py.objects.conversion.bpmn import converter as bpmn_converter
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
from pm4py.algo.analysis.woflan import algorithm as woflan

from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
import os

def model_metrics(log, petri_net, initial_marking, final_marking):
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
    results={
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
    results['Inductive_Miner'] = model_metrics(log, petri_net, initial_marking, final_marking)

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
    results['Heuristic_Miner'] = model_metrics(log, petri_net, initial_marking, final_marking)


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
    results['Heuristic_Miner_0.99'] = model_metrics(log, petri_net, initial_marking, final_marking)

    # Alpha
    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(log)
    results['Alpha'] = model_metrics(log, petri_net, initial_marking, final_marking)

    # Alpha Plus
    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_alpha_plus(log)
    results['Alpha_Plus'] = model_metrics(log, petri_net, initial_marking, final_marking)

    return results

def discovery_log_dataframe(path_folder_bpmn=None,path_folder_png=None,train_log=None,test_log=None):
    ##########################################################################################
    # Trocar estes paths######################################################################
    # path_folder_file = "/Users/yamada/USP/Materias/7 semestre/Mineracao de dados/Celonis Dataset/BPI Challenge 2020 - Prepaid Travel Costs/"
    # path_folder_bpmn = "/Users/yamada/USP/Materias/7 semestre/Mineracao de dados/Celonis Dataset/BPI Challenge 2020 - Prepaid Travel Costs/"
    # path_folder_png = "./Mineracao_processos"
    ##########################################################################################
    ##########################################################################################

    log = test_log

    results = {}
    replayed_traces = {}
    
    # Inductive Miner
    # BPMN
    bpmn_model = pm4py.discover_bpmn_inductive(train_log)
    # pm4py.view_bpmn(bpmn_model)
    path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_inductive.bpmn")
    path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_inductive.png")
    pm4py.save_vis_bpmn(bpmn_model,path3)
    pm4py.write_bpmn(bpmn_model, path2)

    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(train_log)
    results['Inductive_Miner'] = model_metrics(log, petri_net, initial_marking, final_marking)
    replayed_traces['Inductive_Miner'] = pm4py.conformance_diagnostics_token_based_replay(log, petri_net, initial_marking, final_marking)

    # Heuristic Miner
    # BPMN
    bpmn_model = pm4py.discover_heuristics_net(train_log, dependency_threshold=0.99)
    bpmn_model = pm4py.convert_to_bpmn(bpmn_model)
    # pm4py.view_bpmn(bpmn_model)
    path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_heuristic.bpmn")
    path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_heuristic.png")
    pm4py.save_vis_bpmn(bpmn_model,path3)
    pm4py.write_bpmn(bpmn_model, path2)

    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(train_log)
    results['Heuristic_Miner'] = model_metrics(log, petri_net, initial_marking, final_marking)
    replayed_traces['Heuristic_Miner'] = pm4py.conformance_diagnostics_token_based_replay(log, petri_net, initial_marking, final_marking)


    # Heuristic Miner
    # BPMN
    bpmn_model = pm4py.discover_heuristics_net(train_log, dependency_threshold=0.99,and_threshold=.99, loop_two_threshold=.99)
    bpmn_model = pm4py.convert_to_bpmn(bpmn_model)
    # pm4py.view_bpmn(bpmn_model)
    path2 = os.path.join(path_folder_bpmn,"BPI_Challenge_2020_heuristic_99.bpmn")
    path3 = os.path.join(path_folder_png,"BPI_Challenge_2020_heuristic_99.png")
    pm4py.save_vis_bpmn(bpmn_model,path3)
    pm4py.write_bpmn(bpmn_model, path2)

    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(train_log,dependency_threshold=0.99, and_threshold=.99, loop_two_threshold=.99)
    results['Heuristic_Miner_0.99'] = model_metrics(log, petri_net, initial_marking, final_marking)
    replayed_traces['Heuristic_Miner_0.99'] = pm4py.conformance_diagnostics_token_based_replay(log, petri_net, initial_marking, final_marking)

    # Alpha
    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(train_log)
    results['Alpha'] = model_metrics(log, petri_net, initial_marking, final_marking)
    replayed_traces['Alpha'] = pm4py.conformance_diagnostics_token_based_replay(log, petri_net, initial_marking, final_marking)

    # Alpha Plus
    # Petri Net
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_alpha_plus(train_log)
    results['Alpha_Plus'] = model_metrics(log, petri_net, initial_marking, final_marking)
    replayed_traces['Alpha_Plus'] = pm4py.conformance_diagnostics_token_based_replay(log, petri_net, initial_marking, final_marking)

    return results, replayed_traces


if __name__ == "__main__":
    path_folder_file = "/Users/yamada/USP/Materias/7 semestre/Mineracao de dados/Celonis Dataset/BPI Challenge 2020 - Prepaid Travel Costs/"
    path_file = os.path.join(path_folder_file,'PrepaidTravelCost.xes')
    log = pm4py.read_xes(path_file)

    end_datetime = pd.to_datetime('2018-01-01').tz_localize('UTC')
    log_until_2017 = log[log['time:timestamp'] < end_datetime].copy()
    log_after_2017 = log[log['time:timestamp'] >= end_datetime].copy()


    path_folder_bpmn = "./Mineracao_processos/Concept_drift_until_2017"
    path_folder_png = "./Mineracao_processos/Concept_drift_until_2017"
    results_until_2017 = discovery_log_dataframe(
        path_folder_file=path_folder_file,
        path_folder_bpmn=path_folder_bpmn,
        path_folder_png=path_folder_png,
        train_log=log_until_2017
        )

    path_folder_bpmn = "./Mineracao_processos/Concept_drift_after_2017"
    path_folder_png = "./Mineracao_processos/Concept_drift_after_2017"
    results_after_2017 = discovery_log_dataframe(
        path_folder_file=path_folder_file,
        path_folder_bpmn=path_folder_bpmn,
        path_folder_png=path_folder_png,
        train_log=log_after_2017
        )   

    print(results_until_2017)
    print(results_after_2017)
