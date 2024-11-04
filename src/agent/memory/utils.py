import re
from datetime import datetime

def read_markdown_file(file_path: str) -> str:
    with open(file_path, 'r',encoding='utf-8') as f:
        markdown_content = f.read()
    return markdown_content

def extract_llm_response(option_text):
    # Regular expressions to match the different parts of the options
    thought_pattern = re.compile(r"<Thought>(.*?)</Thought>")
    agent_pattern = re.compile(r"<Agent>(.*?)</Agent>")
    request_pattern = re.compile(r"<Request>(.*?)</Request>")
    response_pattern = re.compile(r"<Response>(.*?)</Response>")
    task_pattern = re.compile(r"<Task>(.*?)</Task>")
    result_pattern = re.compile(r"<Result>(.*?)</Result>")
    timestamp_pattern = re.compile(r"<Timestamp>(.*?)</Timestamp>")
    final_answer_pattern = re.compile(r"<Final-Answer>(.*?)</Final-Answer>")
    route_pattern = re.compile(r"<Route>(.*?)</Route>")

    # Extract the thought process or confirmation
    thought = thought_pattern.search(option_text)
    thought = thought.group(1) if thought else None

    # Extract the route to determine which option is being handled
    route = route_pattern.search(option_text)
    route = route.group(1) if route else None

    if route == "Retrieve":
        # This is Option 1: A request for information
        agent = agent_pattern.search(option_text)
        agent = agent.group(1) if agent else None
        
        request = request_pattern.search(option_text)
        request = request.group(1) if request else None

        return {
            "Thought": thought,
            "Agent": agent,
            "Request": request,
            "Route": route
        }
    
    elif route == "Store":
        # This is Option 2: Storing information
        agent = agent_pattern.search(option_text)
        agent = agent.group(1) if agent else None
        
        task = task_pattern.search(option_text)
        task = task.group(1) if task else None
        
        result = result_pattern.search(option_text)
        result = result.group(1) if result else None
        
        return {
            "Thought": thought,
            "Agent": agent,
            "Task": task,
            "Result": result,
            "Route": route
        }
    
    elif route == "Final":
        # This is Option 3: Operation Finished
        final_answer = final_answer_pattern.search(option_text)
        final_answer = final_answer.group(1) if final_answer else None
        
        return {
            "Thought": thought,
            "Final Answer": final_answer,
            "Route": route
        }
    
    else:
        # If no recognized route is found
        return {
            "Error": "Unknown route or malformed option.",
            "Route": route
        }