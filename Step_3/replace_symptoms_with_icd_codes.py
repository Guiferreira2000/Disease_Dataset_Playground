import pandas as pd

def main():
    # File paths
    draft_path = "Datasets/step_1/draft.xlsx"
    symptoms_icd_path = "Datasets/step_2/symptoms_updated_ICD.xlsx"
    output_path = "Datasets/step_3/diseases_with_ICD_labels.xlsx"

    # Read the files into pandas DataFrames
    draft_df = pd.read_excel(draft_path)
    symptoms_icd_df = pd.read_excel(symptoms_icd_path)
    
    # Convert the symptoms to a dictionary: {symptom: ICD 11}
    symptoms_to_icd = dict(zip(symptoms_icd_df['Symptom'], symptoms_icd_df['ICD 11']))

    # Iterate through symptom columns and replace the symptoms with ICD 11 labels
    symptom_cols = [col for col in draft_df.columns if "Symptom_" in col]
    for col in symptom_cols:
        # Check for symptoms without an ICD match and warn the user
        unmatched_symptoms = draft_df[~draft_df[col].isin(symptoms_to_icd.keys())][col].dropna().unique()
        for symptom in unmatched_symptoms:
            print(f"Warning: No ICD code match found for symptom: {symptom}")
        
        draft_df[col] = draft_df[col].map(symptoms_to_icd)

    # Remove exact duplicate ICD codes in each row and shift ICD codes to the left to fill gaps
    rows_with_duplicates = 0
    for index, row in draft_df.iterrows():
        icd_codes = row[symptom_cols].dropna().tolist()
        
        exact_duplicates = [icd for icd in icd_codes if icd_codes.count(icd) > 1]
        
        if exact_duplicates:
            rows_with_duplicates += 1
            print(f"Warning: Disease '{row['Disease']}' had exact duplicated ICD codes: {', '.join(set(exact_duplicates))}")

        unique_icd_codes = []
        [unique_icd_codes.append(x) for x in icd_codes if x not in unique_icd_codes]  # Removes exact duplicates while preserving order

        # Fill the ICD codes back into the row, ensuring no gaps
        for i, col in enumerate(symptom_cols):
            draft_df.at[index, col] = unique_icd_codes[i] if i < len(unique_icd_codes) else None  # Fill with None if out of ICD codes

    print(f"\nTotal number of rows with exact duplicates: {rows_with_duplicates}")

    # Write the resulting DataFrame back to Excel
    draft_df.to_excel(output_path, index=False)
    print(f"File saved to {output_path}")

if __name__ == "__main__":
    main()
