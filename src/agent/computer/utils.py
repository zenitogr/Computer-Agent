import re

def read_markdown_file(file_path: str) -> str:
    with open(file_path, 'r',encoding='utf-8') as f:
        markdown_content = f.read()
    return markdown_content

def extract_llm_response(response: str) -> dict:
    """
    Function to handle the responses from Option 1, Option 2, and Option 3
    from the Computer Agent and extract relevant information.
    """
    result = {
        'Thought': None,
        'Agent': None,
        'Response': None,
        'Request': None,
        'Final Answer': None,
        'Route': None
    }
    
    # Regular expressions for different parts of the response
    thought_regex = re.compile(r'<Thought>\s*(.*?)\s*</Thought>', re.DOTALL)
    agent_regex = re.compile(r'<Agent>\s*(.*?)\s*</Agent>', re.DOTALL)
    request_regex = re.compile(r'<Request>\s*(.*?)\s*</Request>', re.DOTALL)
    response_regex = re.compile(r'<Response>\s*(.*?)\s*</Response>', re.DOTALL)
    final_answer_regex = re.compile(r'<Final-Answer>\s*(.*?)\s*</Final-Answer>', re.DOTALL)
    route_regex = re.compile(r'<Route>\s*(.*?)\s*</Route>', re.DOTALL)
    
    # Extract Thought
    thought_match = thought_regex.search(response)
    if thought_match:
        result['Thought'] = thought_match.group(1).strip()
    
    # Extract Agent (Option 1)
    agent_match = agent_regex.search(response)
    if agent_match:
        result['Agent'] = agent_match.group(1).strip()

    # Extract Response (Option 1)
    response_match = response_regex.search(response)
    if response_match:
        result['Response'] = response_match.group(1).strip()

    # Extract Request (Option 2)
    request_match = request_regex.search(response)
    if request_match:
        result['Request'] = request_match.group(1).strip()

    # Extract Final Answer (Option 3)
    final_answer_match = final_answer_regex.search(response)
    if final_answer_match:
        result['Final Answer'] = final_answer_match.group(1).strip()

    # Extract Route
    route_match = route_regex.search(response)
    if route_match:
        result['Route'] = route_match.group(1).strip()

    return result