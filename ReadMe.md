https://platform.openai.com/docs/api-reference/completions/create?lang=python

ICD Implementation in the website:
https://icd.who.int/docs/icd-api/icd11ect-1.3/


<h1> Disease Symptoms Augmentation with GPT </h1>

This repository serves as a playground lab for augmenting and improving a dataset of diseases and their symptoms using OpenAI's GPT model. The dataset is stored in an Excel file, and the goal is to add additional symptoms for diseases that have less than 10 symptoms. The new symptoms are generated by the GPT model based on the existing symptoms and the nature of the disease.
Code Explanation

The main script of the project is a Python script that reads the Excel file, iterates over the diseases in the dataset, and uses the GPT model to generate additional symptoms for diseases that have less than 10 symptoms. The new symptoms are then added to the dataset, and the modified dataset is saved to a new Excel file.

The script uses the openai.ChatCompletion.create function to generate the new symptoms. This function takes a series of messages as input and returns a generated message as output. The input messages include a system message that defines the assistant's role and the task it needs to perform, and a user message that provides the disease name and existing symptoms and asks the assistant to provide additional symptoms.

The generated symptoms are processed to ensure they are in the correct format. This includes replacing newlines with commas, removing numbering and content within parentheses, and removing any additional sentences or explanations. The processed symptoms are then added to the dataset.
Folder Structure

    prompt_types: This folder contains templates for different types of prompts that can be used with the GPT model. Each prompt type is designed for a specific task or use case. These templates serve as a starting point for defining the role of the chatGPT in diverse scenarios. You can choose the appropriate prompt type based on the task you want the model to perform.

    fine_tunings_models: This folder contains fine-tuned models that have been trained on specific tasks or datasets. Fine-tuning a model can improve its performance on a specific task or make it better at understanding a specific type of data. You can use these models if they are suitable for your task.

<h2> Correct structure logic: </h2>
<h2>Step 1: Dataset criation and enhancement</h2>

    Dataset_augmentation_model.py -> Dataset_security_check.py -> symptom_verification_removal.py

    Dataset_augmentation_model.py - Populates the disease database thanks to the gpt api parameters

    Dataset_security_check.py - Checks the accuracy and truetiness of the data

    symptom_verification_removal.py - Remove the mismacthed symptoms identified by Dataset_security_check.py

    check_disease_length.py - Check each disease number of symptoms through histograms and json files

<h3> Requirements: </h3>
    - Each disease must be labelled through the ICD 11 documentation
    - Each disease must have a least 12 symptoms



<h2>Step 2: Symptoms preprocessing </h2>

    Disease_dataset_dd_mm_AAAA.xlsx -> draft.xlsx (Protective measure. Never work with original data! Always have a backup!!!)

    SymptomExtractor.py -> Puts all symptoms in the same format and extract all symptoms to an excell sheet so it can later processed. draft.xlsx -> preprocessed_draft.xlsx -> output_symptoms_with_frequency.xlsx

    symptom_data_updater.py -> (Optional) It passes past information of older version of preprocessed symptoms into the new output_symptoms_with_frequency.xlsx file

    symptom_to_label.py -> Fetchs the ICD 11 code associated with each disease and fill in the symptoms_updated_ICD.xlsx through the ICD API call. The remaining unlabelled symptoms must ne filled manually

<h3> Requirements: </h3>
    - Symptoms cannot be duplicate
    - Symptoms must be associated with ICD 11 labels



<h2>Step 3:Processing and organizing the labels </h2>

    ICD_11_Processor.py -> It clusters symptoms accordingly to their ICD 11 code

    LLM_json_loader.py -> Implementation of chatgpt inside the icd_11_GPT_formated_data.json File

    replace_symptoms_with_icd_codes.py -> Replace symptoms by their ICD codes accordingly to symptoms_updated_ICD.xlsx

    symptom_converter.py -> Symptoms that have a '/', it'll be split into two separate symptoms and If a symptom contains '&', everything after the '&' including itself will be removed.

    Dataset_augmentation.py -> Data augmentation technique to generate more data samples by removing one symptom at a time

<h3> Requirements: </h3>
    - Chatgpt access to symptoms label process through LLM tools such as Langchain
    - Symptoms of the dataset replaced to ICD 11 codes
    - Dataset augmentation


<h2>Step 4: Extra dataset features </h2>

    check_duplicates.py -> Check duplicate diseases

    incidence_rate.py -> A simple script that gathers information about the diseases incidence rate from chatgpt

    symptom_severity.py -> Script that gathers information about the diseases severity according to chatgpt parameters. Need normalization!


<h3> Requirements: </h3>
    - Each disease must be associated with an incidence rate across the europe region
    - ICD code structure relatedness so the model understand that certain codes and their subcodes are more related than others.




<h2>Step 5: Speech-to-text assistent </h2>




<h3> Requirements: </h3>




<h2>Extra documentation</h2>
<h3>Dataset</h3>
    - Disease_Dataset_Verified.xlsx -> Final output dataset of step 1

    - Disease_Dataset_with_new_symptoms.xlsx -> Dataset create by Dataset_security_check.py 

    - Draft.xlxs - small scale dataset to test code

    - diseases_with_mismatched_symptoms.json -> Dataset symptoms mismathes in a json format


<h3>Data insight</h3>

    - check_disease_length.py - Check each disease number of symptoms through histograms and json files
