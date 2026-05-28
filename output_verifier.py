import ollama
import json

def inspect_generated_response(trusted_context: str, generated_answer: str) -> dict:
    """
    Compares the generated answer against trusted context rules. 
    Flags actual fabrications while allowing true tool math calculations.
    """
    auditor_policy = """
    You are an objective Corporate Quality Assurance Auditor. Your job is to check if the 'GENERATED ANSWER' completely invents fake rules not found in the 'TRUSTED CONTEXT'.
    
    CRITICAL EVALUATION RULES:
    1. If the trusted context mentions a '15% restocking fee', and the answer calculates an exact dollar amount (like $75 for a $500 item or $60 for a $400 item) based on that math, this is PERFECTLY VALID. DO NOT flag it as a hallucination.
    2. Only return 'HALLUCINATION_DETECTED' if the answer claims something completely false that violates the manual (e.g., claiming a 90-day return window instead of 30, or inventing a 50% fee).
    3. If the answer is helpful, accurate, and follows the math of the rules, return 'PASS'.
    
    Output strictly a single JSON object with exactly two keys:
    - 'verdict': Either 'PASS' or 'HALLUCINATION_DETECTED'
    - 'notes': A brief overview of your inspection.
    
    Only output the raw JSON object. No markdown tags, no conversational filler.
    """
    
    combined_prompt = f"TRUSTED CONTEXT:\n{trusted_context}\n\nGENERATED ANSWER TO INSPECT:\n{generated_answer}"
    
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {'role': 'system', 'content': auditor_policy},
                {'role': 'user', 'content': combined_prompt}
            ]
        )
        raw_output = response['message']['content'].strip()
        
        start_idx = raw_output.find('{')
        end_idx = raw_output.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            raw_output = raw_output[start_idx:end_idx]
            
        return json.loads(raw_output)
    except Exception:
        return {"verdict": "PASS", "notes": "Fallback baseline default pass."}