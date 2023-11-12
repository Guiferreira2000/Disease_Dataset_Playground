import pandas as pd
import numpy as np

def compute_relatedness(code1, code2):
    """
    Computes relatedness between two ICD-11 codes.
    """

    # Check if either code is NaN or not a string
    if not isinstance(code1, str) or not isinstance(code2, str):
        return 0



    # Check if codes are exactly the same
    if code1 == code2:
        return 1.0

    # Handle custom codes
    custom_prefixes = ["AAAA", "BBBB", "CCCC"]
    if code1[:4] in custom_prefixes or code2[:4] in custom_prefixes:
        if code1[:4] == code2[:4]:
            return 0.5
        else:
            return 0

    # Check prefix relatedness for genuine ICD-11 codes
    common_prefix_length = 0
    min_length = min(len(code1), len(code2))

    for i in range(min_length):
        if code1[i] == code2[i]:
            common_prefix_length += 1
        else:
            break
    
    # Add additional weight if first four characters are same
    if code1[:4] == code2[:4]:
        common_prefix_length += 1
        denominator = max(len(code1), len(code2)) + 1
    else:
        denominator = max(len(code1), len(code2))

    return common_prefix_length / denominator


def compute_relatedness_matrix(symptoms_list):
    matrix = []
    for symptom1 in symptoms_list:
        row = []
        for symptom2 in symptoms_list:
            row.append(compute_relatedness(symptom1, symptom2))
        matrix.append(row)
    return np.array(matrix)



# Test
code1 = "ME66.26"
code2 = "ME66.26"
print(compute_relatedness(code1, code2))

# code1 = "AAAA01"
# code2 = "AAAA02"
# print(compute_relatedness(code1, code2))

# code1 = "AAAA01"
# code2 = "ME66.6Z"
# print(compute_relatedness(code1, code2))
