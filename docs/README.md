# Computer Agent Project

## Overview

This project is inspired by how a person naturally interacts with a computer to solve problems. The system mimics human workflows, using different agents to navigate the operating system, browse the web, interact with the terminal, and recall previous actions to make decisions about new tasks.

Just as a person remembers past actions on a computer to guide future decisions, this agentic system uses a **Memory Agent** to store and recall knowledge from prior tasks. These stored interactions help the system to solve new, often related, problems based on past experiences.

### Architecture
![Image of the architecture](diagram.svg)

### Development Status

This project is still in the **development stage**, with ongoing work being done on the following components:
- **Web Search Agent**: Working well, successfully automates web interactions.
- **Terminal Agent**: Performing terminal tasks correctly.
- **System Agent**: Still under development, requires further refinement to handle GUI tasks effectively.
- **Memory Agent**: Needs improvement to better recall past actions and automate future tasks.

We are showcasing the progress made so far, and the system is not fully complete.

### Important Note

This project utilizes a large language model (LLM) to control and manipulate the operating system's state. As a result, the system may execute commands, open specific files or directories in your file explorer, or even remove files. Please be aware of these actions when running the project, as they directly interact with your system environment.

## Project Components

The system revolves around several agents, each designed to handle different aspects of computer use:

1. **System Agent**: Responsible for GUI-based tasks, including opening files, manipulating windows, and interacting with desktop elements. This agent is still under development but aims to use both the Accessibility Tree and visual analysis (screenshots) to make decisions.
   
2. **Web Search Agent**: Automates web browsing tasks to gather data or solve problems via online resources. This agent is fully functional.
   
3. **Terminal Agent**: Executes terminal commands when needed for more advanced or specific tasks. This agent is nearly complete.
   
4. **Memory Agent**: Stores past actions and methodologies to optimize future task-solving. This component is still being developed but will play a crucial role in reducing redundant actions and improving decision-making.

## Workflow

- The **Memory Agent** stores the methodology and steps used to solve previous problems.
- When a new task arrives, the system checks the **Memory Agent** for relevant past actions to either replicate or adapt a previous solution.
- The system combines different agents (System, Web Search, Terminal) to accomplish tasks in a way that mirrors how a human might use a computer.

## Diagrams

The following diagram outlines the high-level interactions between the different agents:

![Project Diagram](diagram.svg)

More diagrams explaining specific components or workflows can be added here.

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/computer-agent-project.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the agent system:
   ```bash
   python main.py
   ```

## Future Directions

- Improve the **System Agent** to handle more complex GUI tasks and applications.
- Enhance the **Memory Agent** to better store and recall information for more efficient task automation.
- Continue refining the **Web Search Agent** and **Terminal Agent** for greater robustness in handling a wide range of scenarios.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This version emphasizes the development status, the use of LLM for system manipulation, and includes a placeholder for the diagrams. Let me know if you'd like any further modifications!