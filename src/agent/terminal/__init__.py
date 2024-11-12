from src.agent.terminal.utils import extract_llm_response,read_markdown_file
from src.message import AIMessage,HumanMessage,SystemMessage
from langgraph.graph import StateGraph,START,END
from src.agent.terminal.state import AgentState
from src.agent.memory import MemoryAgent
from src.inference import BaseInference
from src.agent import BaseAgent
from termcolor import colored
from subprocess import run
from platform import platform
from getpass import getuser
from os import getcwd

class TerminalAgent(BaseAgent):
    def __init__(self,llm:BaseInference=None,verbose:bool=False,max_iteration:int=10):
        self.name='Terminal Agent'
        self.description=''
        self.llm=llm
        self.verbose=verbose
        self.max_iteration=max_iteration
        self.iteration=0
        self.memory=MemoryAgent(llm,verbose)
        self.system_prompt=read_markdown_file('./src/agent/terminal/prompt.md')
        self.graph=self.create_graph()

    def reason(self,state:AgentState):
        llm_response=self.llm.invoke(state.get('messages'))
        # print(llm_response.content)
        agent_data=extract_llm_response(llm_response.content)
        # print(dumps(agent_data,indent=2))
        if self.verbose:
            thought=agent_data.get('Thought')
            print(colored(f'Thought: {thought}',color='light_magenta',attrs=['bold']))
        return {**state,'agent_data': agent_data}

    def action(self,state:AgentState):
        agent_data=state.get('agent_data')
        thought=agent_data.get('Thought')
        command=agent_data.get('Command')
        route=agent_data.get('Route')
        if self.verbose:
            print(colored(f'Command: {command}',color='blue',attrs=['bold']))
        try:
            result=run(command.split(),capture_output=True,text=True)
            if result.returncode==0:
                observation=result.stdout.strip()
            else:
                observation=result.stderr.strip()
        except Exception as e:
            observation=str(e)
        if self.verbose:
            print(colored(f'Observation: {observation}',color='green',attrs=['bold']))
        ai_prompt=f'<Thought>{thought}</Thought>\n<Command>{command}</Command>\n\n<Route>{route}</Route>'
        user_prompt=f'<Observation>{observation}</Observation>'
        messages=[AIMessage(ai_prompt),HumanMessage(user_prompt)]
        return {**state,'agent_data':agent_data,'messages':messages}
    
    def retrieve(self,state:AgentState):
        state['messages'].pop()
        agent_data=state.get('agent_data')
        thought=agent_data.get('Thought')
        agent_name=agent_data.get('Agent')
        request=agent_data.get('Request')
        route=agent_data.get('Route')
        agent_response=self.memory.invoke(f'<Agent>{agent_name}</Agent>\n<Request>{request}</Request>')
        ai_message=AIMessage(f'<Thought>{thought}</Thought>\n<Agent>{agent_name}</Agent>\n<Request>{request}</Request>\n<Route>{route}</Route>')
        human_message=HumanMessage(f'<Response>{agent_response}</Response>')
        messages=[ai_message,human_message]
        return {**state,'messages':messages}

    def final(self,state:AgentState):
        agent_data=state.get('agent_data')
        final_answer=agent_data.get('Final Answer')
        if self.verbose:
            print(colored(f'Final Answer: {final_answer}',color='cyan',attrs=['bold']))
        plan=agent_data.get('Plan')
        return {**state,'output':final_answer,'Plan':plan}

    def main_controller(self,state:AgentState):
        agent_data=state.get('agent_data')
        route=agent_data.get('Route').lower()
        return route
        

    def create_graph(self):
        graph=StateGraph(AgentState)
        graph.add_node('reason',self.reason)
        graph.add_node('action',self.action)
        graph.add_node('retrieve',self.retrieve)
        graph.add_node('final',self.final)

        graph.add_edge(START,'reason')
        graph.add_conditional_edges('reason',self.main_controller)
        graph.add_edge('action','retrieve')
        graph.add_edge('action','reason')
        graph.add_edge('final',END)

        return graph.compile(debug=False)

    def invoke(self,input:str):
        parameters={
            'os':platform(),
            'cwd':getcwd(),
            'user':getuser()
        }
        system_prompt=self.system_prompt.format(**parameters)
        user_prompt=f'Query: {input}'
        state={
            'input':input,
            'messages':[SystemMessage(system_prompt),HumanMessage(user_prompt)],
            'agent_data':None,
            'output':None
        }
        graph_response=self.graph.invoke(state)
        return graph_response

    def stream(self,input:str):
        pass
        