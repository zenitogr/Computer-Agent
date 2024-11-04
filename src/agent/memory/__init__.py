from src.agent.memory.utils import read_markdown_file, extract_llm_response
from src.message import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from src.agent.memory.state import AgentState
from src.inference import BaseInference
from src.agent import BaseAgent
from termcolor import colored
from uuid import uuid4
import time
import json
import os

class MemoryAgent(BaseAgent):
    def __init__(self, llm:BaseInference=None, verbose: bool = False, memory_file: str = 'memory.json'):
        self.name = 'Memory Agent'
        self.description = ''
        self.system_prompt = read_markdown_file('./src/agent/memory/prompt.md')
        self.llm = llm
        self.verbose = verbose
        self.graph = self.create_graph()
        self.memory_file_path = f'./memory/{memory_file}'
        if not os.path.exists('memory'):
            os.mkdir('memory')
        if not os.path.exists(self.memory_file_path):
            with open(self.memory_file_path, 'w') as f:
                json.dump([], f)

    def reason(self, state: AgentState):
        ai_message = self.llm.invoke(state.get('messages'))
        agent_data = extract_llm_response(ai_message.content)
        if self.verbose:
            thought = agent_data.get('Thought')
            print(colored(f'Thought: {thought}', color='light_magenta', attrs=['bold']))
        return {**state, 'agent_data': agent_data,'messages':[ai_message]}

    def retrieve(self, state: AgentState):
        agent_data = state.get('agent_data')
        thought = agent_data.get('Thought')
        agent_name = agent_data.get('Agent')
        request = agent_data.get('Request')
        route = agent_data.get('Route')
        if self.verbose:
            print(colored(f'Agent: {agent_name}', color='green', attrs=['bold']))
            print(colored(f'Request: {request}', color='blue', attrs=['bold']))
        results = []
        with open(self.memory_file_path, 'r') as f:
            memories = json.load(f)
            for memory in memories:
                if memory['agent_name'].lower() == agent_name.lower():
                    results.append(memory)
        if self.verbose:
            print(colored(f'Fetched Memories: {results}', color='yellow', attrs=['bold']))
        state['messages'].pop()
        ai_messsage=AIMessage(f'<Thought>{thought}</Thought>\n<Agent>{agent_name}</Agent>\n<Request>{request}</Request>\n<Route>{route}</Route>')
        human_message = HumanMessage(f'<Response>Fetched Memories: {results}</Response>')
        return {**state, 'messages': [ai_messsage,human_message]}

    def store(self, state: AgentState):
        agent_data = state.get('agent_data')
        thought = agent_data.get('Thought')
        agent_name = agent_data.get('Agent')
        task = agent_data.get('Task')
        result = agent_data.get('Result')
        timestamp = int(time.time())
        route = agent_data.get('Route')
        if self.verbose:
            print(colored(f'Agent: {agent_name}', color='green', attrs=['bold']))
            print(colored(f'Task: {task}', color='blue', attrs=['bold']))
            print(colored(f'Result: {result}', color='cyan', attrs=['bold']))
        memory_entry = {
            'id': str(uuid4()),
            'agent_name': agent_name,
            'task': task,
            'result': result,
            'timestamp': timestamp
        }
        with open(self.memory_file_path, 'r+') as f:
            memories = json.load(f)
            memories.append(memory_entry)
            f.seek(0)
            json.dump(memories, f, indent=4)
        if self.verbose:
            print(colored(f'Stored Memory: {memory_entry}', color='green', attrs=['bold']))
        state['messages'].pop()
        ai_message = AIMessage(f'<Thought>{thought}</Thought>\n<Agent>{agent_name}</Agent>\n<Task>{task}</Task>\n<Result>{result}</Result>\n<Timestamp>{timestamp}</Timestamp>\n<Route>{route}</Route>')
        human_message = HumanMessage(f'<Response>Stored Memory from {agent_name}: {memory_entry}</Response>')
        return {**state, 'messages': [ai_message, human_message]}

    def controller(self, state: AgentState):
        agent_data = state.get('agent_data')
        return agent_data.get('Route').lower()

    def final(self, state: AgentState):
        agent_data = state.get('agent_data')
        final_answer = agent_data.get('Final Answer')
        if self.verbose:
            print(colored(f'Final Answer: {final_answer}', color='cyan', attrs=['bold']))
        return {**state, 'output': final_answer}

    def create_graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node('reason', self.reason)
        workflow.add_node('retrieve', self.retrieve)
        workflow.add_node('store', self.store)
        workflow.add_node('final', self.final)

        workflow.add_edge(START, 'reason')
        workflow.add_conditional_edges('reason', self.controller)
        workflow.add_edge('retrieve', 'reason')
        workflow.add_edge('store', 'reason')
        workflow.add_edge('final', END)

        return workflow.compile(debug=False)

    def invoke(self, input: str):
        state = {
            'input': input,
            'messages': [SystemMessage(self.system_prompt), HumanMessage(input)],
            'agent_data': {},
            'output': '',
        }
        graph_response=self.graph.invoke(state)
        return graph_response['output']

    def stream(self, input: str):
        pass
