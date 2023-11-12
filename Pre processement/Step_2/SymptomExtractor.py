import pandas as pd
import json

class SymptomExtractor:

    def __init__(self, input_file):
        self.input_file = input_file
        self.df = pd.read_excel(self.input_file)

    def preprocess_symptoms(self, output_file):
        symptom_columns = [col for col in self.df.columns if 'Symptom_' in col]
    
        user_decisions = {}  # Record user decisions for each symptom

        for col in symptom_columns:
            for idx, symptom in enumerate(self.df[col]):
                if pd.notna(symptom):
                    # Remove trailing spaces automatically
                    symptom = symptom.strip()

                    # If the user has already made a decision about this symptom, apply that decision
                    if symptom in user_decisions:
                        if user_decisions[symptom]:
                            self.df[col] = self.df[col].replace(symptom, symptom.capitalize())
                        continue

                    # If symptom requires capitalization and hasn't been decided on yet, ask the user
                    capitalized_symptom = symptom.capitalize()
                    if symptom != capitalized_symptom:
                        while True:
                            user_input = input(f"Modify symptom '{symptom}' to '{capitalized_symptom}'? (y/n): ")
                            if user_input in ['y', 'n']:
                                break
                            print("Invalid input. Please enter 'y' or 'n'.")

                        if user_input == 'y':
                            self.df[col] = self.df[col].replace(symptom, capitalized_symptom)
                            user_decisions[symptom] = True
                        else:
                            user_decisions[symptom] = False

        # Save the preprocessed dataframe to a new Excel file
        self.df.to_excel(output_file, index=False)

    def extract_symptoms(self):
        symptom_columns = [col for col in self.df.columns if 'Symptom_' in col]
        all_symptoms = self.df[symptom_columns].values.flatten()
        unique_symptoms = list(set(all_symptoms))
        unique_symptoms = [symptom for symptom in unique_symptoms if symptom is not None and symptom == symptom]
        unique_symptoms.sort()
        return unique_symptoms

    def save_to_xlsx(self, symptoms, output_file):
        df = pd.DataFrame(symptoms, columns=['Symptoms'])
        df.to_excel(output_file, index=False)

    def rows_with_gaps(self):
        symptom_columns = [col for col in self.df.columns if 'Symptom_' in col]
        gap_info = []
        for index, row in self.df.iterrows():
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
        symptom_columns = [col for col in self.df.columns if 'Symptom_' in col]
        all_symptoms_series = self.df[symptom_columns].stack()
        frequency = all_symptoms_series.value_counts()
        return frequency

    def append_frequency_to_xlsx(self, symptoms, output_file):
        df = pd.DataFrame(symptoms, columns=['Symptoms'])
        frequencies = self.get_symptom_frequency()
        df['Frequency'] = df['Symptoms'].map(frequencies).fillna(0).astype(int)
        df = df[['Frequency', 'Symptoms']]
        df.to_excel(output_file, index=False)

if __name__ == "__main__":
    extractor = SymptomExtractor("Datasets/step_1/draft.xlsx")

    while True:
        choice = input("Would you like to check the structure of the symptoms? (y/n): ")
        if choice in ['y', 'n']:
            break
        print("Invalid input. Please enter 'y' or 'n'.")

    if choice == 'y':
        extractor.preprocess_symptoms("Datasets/step_1/preprocessed_draft.xlsx")

    symptoms = extractor.extract_symptoms()
    extractor.append_frequency_to_xlsx(symptoms, "Datasets/step_2/output_symptoms_with_frequency.xlsx")

    gap_info = extractor.rows_with_gaps()
    extractor.save_to_json(gap_info, "rows_with_gaps.json")
