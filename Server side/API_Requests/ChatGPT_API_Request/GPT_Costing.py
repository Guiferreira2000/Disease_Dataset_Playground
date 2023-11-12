from langchain.callbacks import get_openai_callback

chain = create_extraction_chain(llm, salary_range) # Example

with get_openai_callback() as cb:
    result = chain.predict_and_parse(text=text)
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Successful Requests: {cb.successful_requests}")
    print(f"Total Cost (USD): ${cb.total_cost}")

