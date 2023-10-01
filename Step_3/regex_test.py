import re

test_string = '''
Thought: I need to look at the entries in the dataset
Action: Look at each dictionary
Action Input: The data in the dataset
Observation: The entries for AAAA10 and AAAA13 both have symptoms related to elevated blood urea nitrogen
Thought: I need to compare the two codes to determine which is more closely associated
Action: Compare the two codes
Action Input: AAAA10 and AAAA13
Observation: AAAA10 is more closely associated with elevated blood urea nitrogen
Thought: I now know the final answer
Final Answer: Given your answer AAAA1075 It might b "A100.1Z" and AAAA10
'''

# Find the "Final Answer: " section
final_answer = re.search(r"Final Answer: (.+)", test_string)

if final_answer:
    answer_text = final_answer.group(1)
    print(f"Extracted answer_text: {answer_text}")
    
    # Find the ICD code using the updated pattern
    pattern = r"(?:[A-Z]{4}\d{1,}|[A-Z0-9]{4})(?:\.[A-Z0-9]+)?"
    icd_code = re.search(pattern, answer_text)
    
    if icd_code:
        print(f"The extracted ICD 11 Code is: {icd_code.group(0)}")
    else:
        print("No ICD codes found in the extracted answer_text!")
        # Let's test the regex directly to see if it's the pattern that's faulty
        test_code = "AAAA10"
        if re.match(pattern, test_code):
            print("The pattern matches the test code!")
        else:
            print("The pattern doesn't match the test code!")
else:
    print("Final Answer section not found!")
