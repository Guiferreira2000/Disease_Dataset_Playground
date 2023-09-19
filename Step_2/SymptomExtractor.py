import pandas as pd
import json

class SymptomExtractor:

    def __init__(self, input_file):
        self.input_file = input_file

    def extract_symptoms(self):
        # Read the dataset
        df = pd.read_excel(self.input_file)

        # Extract all symptoms into a single list
        symptom_columns = [col for col in df.columns if 'Symptom_' in col]
        all_symptoms = df[symptom_columns].values.flatten()

        # Convert to a set to remove duplicates and then back to list
        unique_symptoms = list(set(all_symptoms))

        # Remove None or NaN values
        unique_symptoms = [symptom for symptom in unique_symptoms if symptom is not None and symptom == symptom]

        # Sort the symptoms alphabetically
        unique_symptoms.sort()

        return unique_symptoms

    def save_to_xlsx(self, symptoms, output_file):
        df = pd.DataFrame(symptoms, columns=['Symptoms'])
        df.to_excel(output_file, index=False)

    def rows_with_gaps(self):
        df = pd.read_excel(self.input_file)
        symptom_columns = [col for col in df.columns if 'Symptom_' in col]

        gap_info = []
        for index, row in df.iterrows():
            empty_found = False
            for col in symptom_columns:
                if pd.isna(row[col]):
                    empty_found = True
                elif empty_found:
                    gap_info.append({"row_index": index, "disease": row["Disease"]})
                    break

        return gap_info

    def save_to_json(self, gap_info, output_file):
        with open(output_file, 'w') as json_file:
            json.dump({"Rows with gaps": gap_info}, json_file, indent=4)

    def get_symptom_frequency(self):
        df = pd.read_excel(self.input_file)
        symptom_columns = [col for col in df.columns if 'Symptom_' in col]

        # Flatten all symptom columns into a single series
        all_symptoms_series = df[symptom_columns].stack()

        # Calculate symptom frequency
        frequency = all_symptoms_series.value_counts()

        return frequency

    def append_frequency_to_xlsx(self, symptoms, output_file):
        df = pd.DataFrame(symptoms, columns=['Symptoms'])

        # Get symptom frequencies and add to the dataframe
        frequencies = self.get_symptom_frequency()
        df['Frequency'] = df['Symptoms'].map(frequencies).fillna(0).astype(int)

        # Switch order of columns
        df = df[['Frequency', 'Symptoms']]

        df.to_excel(output_file, index=False)

if __name__ == "__main__":
    extractor = SymptomExtractor("Datasets/step_1/draft.xlsx")
    symptoms = extractor.extract_symptoms()
    extractor.append_frequency_to_xlsx(symptoms, "Datasets/step_2/output_symptoms_with_frequency.xlsx")

    gap_info = extractor.rows_with_gaps()
    extractor.save_to_json(gap_info, "rows_with_gaps.json")
