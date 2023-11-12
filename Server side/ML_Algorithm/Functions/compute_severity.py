# Loading the severity scores
with open("/home/guilherme/Documents/GitHub/Tese/MDCompass/ML_Algorithm/json_files/severity_scores.json", "r") as f:
    severity_mapping = json.load(f)

def get_severity_scores(symptom_list):
  """
      Load severity scores from a given JSON file and assign them to each symptom in the DataFrame.

  """

    # Normalizar os valores com base numa distribuição Gaussiana

  return [severity_mapping.get(symptom, 0) for symptom in symptom_list]