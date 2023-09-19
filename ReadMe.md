https://platform.openai.com/docs/api-reference/completions/create?lang=python

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

    SymptomExtractor.py -> Puts all symptoms in the same format and extract all symptoms to an excell sheet so it can later processed.
    
    symptom_to_label.py -> 

    symptom_data_updater.py ->

<h3> Requirements: </h3>
    - Symptoms cannot be duplicate
    - Symptoms must be associated with ICD 11 labels










<h2>Extra documentation</h2>
<h3>Dataset</h3>
    - Disease_Dataset_Verified.xlsx -> Final output dataset of step 1

    - Disease_Dataset_with_new_symptoms.xlsx -> Dataset create by Dataset_security_check.py 

    - Draft.xlxs - small scale dataset to test code

    - diseases_with_mismatched_symptoms.json -> Dataset symptoms mismathes in a json format