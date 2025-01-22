# Computer Agent

## Overview

This project aims to replicate how a person naturally interacts with a computer to solve tasks. The system utilizes multiple agents to handle tasks such as web browsing, terminal operations, GUI interactions, and memory storage for adaptive decision-making. The **Memory Agent** is pivotal in recalling previous actions, which enhances the efficiency and accuracy of solving related tasks in the future.

### Architecture

The following diagram outlines the high-level interactions between the different agents:
![Image of the architecture](diagram.svg)

### Development Status

This project is currently in the **development stage**, but significant progress has been made on its core components:

- **Web Search Agent**: Fully functional and effectively automates web interactions to retrieve data.
- **System Agent**: Almost fully functional, capable of handling GUI tasks. Currently supported only on Windows operating systems.
- **Terminal Agent**: Working at an optimal level for executing advanced or specific terminal commands.
- **Memory Agent**: Still under development. Thinking whether a centralized memory agent or dedicated memory for each agent would provide better efficiency and functionality.

### Important Note

This program runs directly on your machine and leverages a large language model (LLM) to execute commands. **Use this system with caution**, as it can interact with your system files, settings, and applications. Improper use or unintended commands may lead to potential harm to your system. 

## Project Components

The system is structured around the following agents, each with a specialized role:

1. **System Agent**  
   Handles GUI-based tasks such as opening files, manipulating windows, and interacting with desktop elements. Currently supported only on Windows and nearing full functionality.

2. **Web Search Agent**  
   Automates web browsing to gather data or solve tasks using online resources. This agent is fully functional and reliable.

3. **Terminal Agent**  
   Executes terminal commands for advanced operations. This component is fully operational and performs tasks efficiently.

4. **Memory Agent**  
   Stores and recalls past actions to improve decision-making and avoid redundant operations. Still under development, with ongoing discussions about the best architecture for memory management.

## Workflow

1. The **Memory Agent** (or agent-specific memory) stores methodologies and steps used for solving tasks.
2. When a new query is received, the system checks past stored actions to replicate or adapt a similar solution.
3. The system integrates the **System**, **Web Search**, and **Terminal Agent** as needed to solve the task, mimicking a human approach.

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/jeomon/computer-agent.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the agent system:
   ```bash
   python app.py
   Enter your query: <your query goes here>
   ```

## Example Interaction

```plaintext
Enter your query: What it time now in US               
Thought: I need to find the current time in the US. I can use the web agent to search for this information.
Agent Name: Web Agent
Agent Request: What is the current time in the US?
Thought: I need to find the current time in the US. I can use Google to search for this information. I will open a new tab and navigate to google.com.
Action Name: Tab Tool
Action Input: {'mode': 'open'}
Observation: Opened new tab and switched to it
Thought: I have opened a new tab. Now I need to navigate to google.com to perform the search.
Action Name: GoTo Tool
Action Input: {'url': 'https://www.google.com'}
Observation: Navigated to https://www.google.com
Thought: I am on the google homepage. I need to type my query in the search box which is element with index 6 and then click on the google search button which is element with index 10.
Action Name: Type Tool
Action Input: {'index': 6, 'text': 'current time in the US'}
Observation: Typed current time in the US in element 6
Thought: I have typed the query in the search box. Now I will click on the Google Search button which is element with index 21 to perform the search.
Action Name: Click Tool
Action Input: {'index': 21}
Observation: Clicked element 21
Thought: The current time in Washington, D.C., USA is 1:41 pm on Tuesday, 21 January 2025 (GMT-5). I have the answer from the search results. I can now provide the final answer.
Final Answer: The current time in Washington, D.C., USA is 1:41 pm on Tuesday, 21 January 2025 (GMT-5).
Agent Response: The current time in Washington, D.C., USA is 1:41 pm on Tuesday, 21 January 2025 (GMT-5).
Thought: I have found the current time in Washington, D.C., USA. This should be sufficient to answer the user's question about the time in the US.
Final Answer: The current time in Washington, D.C., USA is 1:41 pm on Tuesday, 21 January 2025 (GMT-5).
```

## Future Directions

- Enhance the **System Agent** to handle more advanced and complex GUI tasks.
- Finalize the design and implementation of the **Memory Agent**, determining whether centralized or agent-specific memory is most effective.
- Continue refining the **Web Search Agent** and **Terminal Agent** for robust performance across a wide range of scenarios.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---