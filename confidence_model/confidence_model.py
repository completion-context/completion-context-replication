import os

import sys
import argparse

import random

import math

from statistics import *

score_folder=""
prediction_folder=""

target_file="targets.txt"


to_analyze=os.listdir(score_folder)
to_analyze=[f for f in to_analyze if ".txt" in f and "baseline" not in f]

to_analyze=[f.replace("score_", "").replace(".txt", "") for f in to_analyze]


def mix_all_contexts():

    dict_score=dict()
    dict_status=dict()
    dict_prediction=dict()

    file = open(target_file, 'r')
    target = file.readlines()
    target=[l.strip() for l in target]
    file.close()

    for context in to_analyze:

        print("Context: {}".format(context))

        path_baseline=os.path.join(prediction_folder, "baseline/perfect_prediction.txt")
        path_context=os.path.join(prediction_folder, "{}/perfect_prediction.txt".format(context))

        path_score_baseline=os.path.join(score_folder, "score_baseline.txt")
        path_score_context=os.path.join(score_folder, "score_{}.txt".format(context))

        path_prediction_baseline=os.path.join(prediction_folder, "baseline/predictions.txt")
        path_prediction_context=os.path.join(prediction_folder, "{}/predictions.txt".format(context))

        file = open(path_baseline, 'r')
        lines_baseline = file.readlines()
        lines_baseline=[l.strip() for l in lines_baseline]
        file.close()

        file = open(path_context, 'r')
        lines_context = file.readlines()
        lines_context=[l.strip() for l in lines_context]

        file.close()

        file = open(path_score_baseline, 'r')
        lines_score_baseline = file.readlines()
        lines_score_baseline=[l.strip() for l in lines_score_baseline]

        file.close()

        file = open(path_score_context, 'r')
        lines_score_context = file.readlines()
        lines_score_context=[l.strip() for l in lines_score_context]

        file.close()

        file = open(path_prediction_baseline, 'r')
        lines_prediction_baseline = file.readlines()
        lines_prediction_baseline=[l.strip() for l in lines_prediction_baseline]

        file.close()

        file = open(path_prediction_context, 'r')
        lines_prediction_context = file.readlines()
        lines_prediction_context=[l.strip() for l in lines_prediction_context]

        scores_baseline = [float(s) for s in lines_score_baseline]
        scores_context = [float(s) for s in lines_score_context]

        if len(dict_score.keys()) ==0:
            for i, (j,k,w) in enumerate(zip(lines_baseline, scores_baseline, lines_prediction_baseline)):
                score_b=(math.exp(k))
                dict_score[i]=score_b
                dict_status[i]=j
                dict_prediction[i]=w


        for i, (j,k,w) in enumerate(zip(lines_context, scores_context, lines_prediction_context)):
            score_c=(math.exp(k))

            # print(dict_score[i], score_c)

            if score_c>dict_score[i]:
                dict_score[i]=score_c
                dict_status[i]=j
                dict_prediction[i]=w

                # print(score_c, j, w)

 

    mix_path=os.path.join(score_folder, "mix_baseline", "mix_all_contexts.txt")
    # print(mix_path)
    f=open(mix_path, "w+")
    for k in dict_status.keys():
        value=dict_status[k]
        f.writelines("{}\n".format(value))
    f.close()


    mix_path=os.path.join(score_folder, "mix_baseline", "mix_all_contexts_predictions.txt")
    # print(mix_path)
    f=open(mix_path, "w+")
    for k in dict_prediction.keys():
        value=dict_prediction[k]
        f.writelines("{}\n".format(value))    
    f.close()

    perfect_mix=0
    tot=0
    for k in dict_status.keys():
        score=dict_status[k]
        tot+=1
        if score=="True":
            perfect_mix+=1



    print("PERFECT MIX ALL CONTEXTS: {} ( {}% )".format(str(perfect_mix), str(round(round(perfect_mix/tot, 4)*100,2))))

    prediction_mix=list()
    for k in dict_prediction.keys():
        prediction_mix.append(dict_prediction[k])

    # check if we did everything OK
    check_ok=0
    for x,y in zip(prediction_mix, target):

        if x.replace(" ", "").replace("<nl>", "")== y.replace(" ", "").replace("<nl>", ""):
            check_ok+=1

    print(check_ok)


mix_all_contexts()
