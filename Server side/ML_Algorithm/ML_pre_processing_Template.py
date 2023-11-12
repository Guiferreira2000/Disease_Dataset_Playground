import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer

# Load the Dataset
df = pd.read_excel('Labeled_Diseases_Dataset.xlsx', sheet_name='Diseases & Symptoms')

# Extract Features and Target
symptoms = df.iloc[:, 2:].values  # Extract symptom columns as features
diseases = df['Disease'].values  # Extract disease column as target

# Preprocess the Target Variable
label_encoder = LabelEncoder()
diseases_encoded = label_encoder.fit_transform(diseases)


X_train, X_test, y_train, y_test = train_test_split(symptoms, diseases_encoded, test_size=0.2, random_state=42)

