# Deep Learning-based Code Completion: On the Impact on Performance of Additional Contextual Information

In this work we present a large-scale study exploring the role of contextual information (i.e., additional information that can be provided to the model) in improving the capabilities of the state-of-the-art Transformer-based models when completing entire lines of code.

## T5 model

### Preliminary step
The training of the model is done on a TPU instance of **Colab**.
A GCS Bucket is mandatory.
To Set up a new GCS Bucket for training and fine-tuning a T5 Model, please follow the guide provided by Google [here](https://cloud.google.com/storage/docs/quickstart-console).


### Pipeline
* ##### Datasets

    You can find the datasets used for pretraining and fine-tuning the models [here](https://zenodo.org/record/7643970) inside `datasets` folder. 
    We shared all the 20 finetuning datasets (one for each context we experimented with, including the limited context presented in the validity section).

* ##### Tokenizer
    
    You can find the dataset used for training the tokenizer (featuring 1M random instances for pretraining dataset and around 700k instances from C4 corpus [here](https://zenodo.org/record/7643970) inside `tokenizers` folder.
    You can train the SentencePiece tokenizer in this way
    ```
    ./spm_train --input=tokenizer_training.txt  --model_prefix=SP --vocab_size=32000 --bos_id=-1  --eos_id=1 --unk_id=2 --pad_id=0 --shuffle_input_sentence=true --character_coverage=1.0)
    ```
    The trained tokenizer can be found in the `Pretraining` folder
      
* ##### Pretraining
    
    For pretraining the model you can find the notebook **pretraining.ipynb** in the `Pretraining` folder. 
    You can also find the gin file for config in the `configuration_file` subfolder and the trained tokenizer in the `tokenizer_model` subfolder.
    The pretrained model is available [here](https://zenodo.org/record/7643970) inside the `pretrained_model` folder
    
* ##### Hyper Parameter tuning

    We did hyper parameter tuning to find the best model for the finetuning.
    We tested 4 configuration and trained the model for 25k steps.
    The configurations are the following:
    - constant learning rate (lr = 0.001)
    - Inverse Square Root (warmup_steps = 10000)
    - slanted (cut_fraction=0.1, ratio=32, max_learning_rate=0.01, start_step=0)
    - polynomial learning rate (starter_learning_rate=0.01, end_learning_rate=1e-6, decay_step=10000, power=0.5)
    
    You can find the notebooks in `HP_Tuning/notebooks`.
    The configuration files for each HP tuning are in `HP_Tuning/configuration_files`.
    You can find the script to evaluate the performances in the `HP_Tuning/evaluation` folder that can be run in the following way:
    ```
    python3 perfect_predictions.py --folder <folder_with_predictions> 
    ```
    In the **--folder** you have to save all the files generated during the evaluation by tensorflow (input file, target file, and prediction file with the specific configuration).
    You can find [here](https://zenodo.org/record/7643970) the HP tuning models and the files for the predictions inside the `hp_tuning` folder.
    
    Then we evaluated the performance; the best model was **constant**.
    Here the **percentage of perfect predictions** for each configuration:
    | DATASET           | CONSTANT | SLANTED | ISR   | POLYNOMIAL |
    |-------------------|----------|---------|-------|------------|
    | finetuning    |    31.27 |   29.19 | 30.67 |      2.53 |
    
* ##### Finetuning

    To **evaluate the performance** of each model we used a beam size of 1.
    We finetuned each model for 160k steps.
    You can find all the file in `Finetuning` folder.
  
    You can finetune and evaluate the models by running the **finetuning.ipynb** and **evaluation.ipynb** notebooks (check the comments in the notebook).
    We evaluated the prediction for the eval set for all the checkpoint stored in order to find the best checkpoint for each contextual model.
        
    You can evaluate the **number of perfect predictions** running:
    ```
    python3 perfect_predictions_eval_set.py --target_file <path_to_target_file> --prediction_folder <path_to_prediction_file>
    ```
    Where
    - target_path contains the file with the correct value that the model should predict
    - prediction_folder contains the file T5 predictions for each checkpoint

    We reported the percentage of correct prediction for all checkpoints in the **results_eval_set.md** file.
    
    Once that we have found the best checkpoint for each configuration, we can generate the predictions for each dataset (**finetuning_test_set.py**) and evaluate the performance on the test set (**perfect_predictions_test_set.py**).
    
    The results are reported in the paper are also present in the **results_test_set.md** file.
   
    You can find the models and the predictions [here](https://zenodo.org/record/7643970) inside the `finetuning` folder.
  
* ##### TSDAE   
  
  We shared all material used for finding the most similar issue, using the Transformers and Sequential Denoising Auto-Encoder (TSDAE).
  The dataset used for training the TSDAE, featuring all the linked issues, can be found in the `TSDAE/tsdae_dataset` folder.
  We trained 6 different configurations:
    | Scheduler    | Learning Rate | MRR  |
    |--------------|---------------|------|
    | constant     | 3e-5          | 0.36 |
    | constant     | 1e-5          | 0.34 |
    | warmupcosine | 3e-5          | 0.34 |
    | warmupcosine | 1e-5          | 0.29 |
    | warmuplinear | 3e-5          | 0.34 |
    | warmuplinear | 1e-5          | 0.28 |
  
  The trained model for best configuration found (constant scheduler with 3e-5 learning rate) is stored in `TSDAE/tsdae_best_configuration` folder.
  The notebook we used for training the 6 models can be found in `TSDAE/trained_configurations`
  Once chosen the best configuration, we used that configuration to find the most similar issue for each dataset instance. The notebook can be found in `TSDAE/dataset_building`
  
* ##### Confidence of the model    

    We leverage the confidence of the models to further improve the achieved performance.
    We stored the scores for each model and the predictions of the confidence model [here](https://zenodo.org/record/7643970) inside the `Confidence_model` folder.
    The script to generate the predictions for the score model, that keeps into account the confidence of each model, can be found in `confidence_model` folder.
    
* ##### Statistical analysis    

    We performed a statistical analysis to check the significance of our results using the McNemar's test and Odds Ratio effect size.
    You can find the script, the data and the results for all the models in the `statistical_analysis` folder.
    


   
    