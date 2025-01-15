from src.agent.computer.utils import extract_llm_response,read_markdown_file
from src.message import AIMessage,HumanMessage,SystemMessage
from langgraph.graph import StateGraph,START,END
from src.agent.computer.state import AgentState
from src.agent.terminal import TerminalAgent
from src.agent.web import WebAgent
from src.agent.system import SystemAgent
from src.agent.memory import MemoryAgent
from src.llm_switcher import LLMSwitcher
from src.inference import BaseInference
from src.agent import BaseAgent
from termcolor import colored
import platform

class ComputerAgent(BaseAgent):
    def __init__(self,llm:BaseInference|LLMSwitcher=None,max_iteration:int=10,verbose:bool=False):
        self.name='Computer Agent'
        self.description=''
        self.verbose=verbose
        self.system_prompt=read_markdown_file('src/agent/computer/prompt.md')
        self.max_iteration=max_iteration
        self.iteration=0
        self.llm=llm
        self.graph=self.create_graph()
        self.memory_agent=MemoryAgent(llm=self.llm,verbose=self.verbose)

    def reason(self,state:AgentState):    
        message=self.llm.invoke(state.get('messages'))
        # print(llm_response.content)
        agent_data=extract_llm_response(message.content)
        # print(message.content)
        # print(dumps(agent_data,indent=2))
        if self.verbose:
            thought=agent_data.get('Thought')
            print(colored(f'Thought: {thought}',color='light_magenta',attrs=['bold']))
        return {**state,'agent_data': agent_data,'messages':[message],'current_agent':'Computer Agent'}
    
    def web(self,state:AgentState):
        agent_data=state.get('agent_data')
        request=agent_data.get('Request')
        agent_name=agent_data.get('Agent')
        route=agent_data.get('Route')
        thought=agent_data.get('Thought')
        agent=WebAgent(llm=self.llm,verbose=self.verbose,browser='edge',headless=False)
        agent_response=agent.invoke(request)
        response=agent_response.get('output')
        if self.verbose:
            print(colored(f'Response: {response}',color='blue',attrs=['bold'])) 
        state['messages'].pop()
        ai_message=f'<Thought>{thought}</Thought>\n<Agent>{agent_name}</Agent>\n<Request>{request}</Request>\n<Route>{route}</Route>'
        user_message=f'<Response>{response}</Response>'
        messages=[AIMessage(ai_message),HumanMessage(user_message)] 
        return {**state, 'messages':messages,'agent_response':agent_response,'current_agent':agent_name}

    def terminal(self,state:AgentState):
        agent_data=state.get('agent_data')
        request=agent_data.get('Request')
        agent_name=agent_data.get('Agent')
        route=agent_data.get('Route')
        thought=agent_data.get('Thought')
        agent=TerminalAgent(llm=self.llm,verbose=self.verbose)
        agent_response=agent.invoke(request)
        response=agent_response.get('output')
        if self.verbose:
            print(colored(f'Response: {response}',color='blue',attrs=['bold'])) 
        state['messages'].pop()
        ai_message=f'<Thought>{thought}</Thought>\n<Agent>{agent_name}</Agent>\n<Request>{request}</Request>\n<Route>{route}</Route>'
        user_message=f'<Response>{response}</Response>'
        messages=[AIMessage(ai_message),HumanMessage(user_message)] 
        return {**state, 'messages':messages,'agent_response':agent_response,'current_agent':agent_name}


    def system(self,state:AgentState):
        agent_data=state.get('agent_data')
        request=agent_data.get('Request')
        agent_name=agent_data.get('Agent')
        route=agent_data.get('Route')
        thought=agent_data.get('Thought')
        agent=SystemAgent(llm=self.llm,screenshot=False,strategy='ally_tree',verbose=self.verbose)
        agent_response=agent.invoke(request)
        response=agent_response.get('output')
        if self.verbose:
            print(colored(f'Response: {response}',color='blue',attrs=['bold']))    
        state['messages'].pop()
        ai_message=f'<Thought>{thought}</Thought>\n<Agent>{agent_name}</Agent>\n<Request>{request}</Request>\n<Route>{route}</Route>'
        user_message=f'<Response>{response}</Response>'
        messages=[AIMessage(ai_message),HumanMessage(user_message)] 
        return {**state, 'messages':messages,'agent_response':agent_response,'current_agent':agent_name}
    
    def agent(self,state:AgentState):
        agent_data=state.get('agent_data')
        current_agent=agent_data.get('Agent')
        request=agent_data.get('Request')
        if self.verbose:
            print(colored(f'Agent: {current_agent}',color='green',attrs=['bold']))
            print(colored(f'Request: {request}',color='cyan',attrs=['bold']))
        if current_agent=='Web Agent':
            return self.web(state)
        elif current_agent=='Terminal Agent':
            return self.terminal(state)
        elif current_agent=='System Agent':
            return self.system(state)
        else:
            raise Exception('Invalid agent')

    def memory(self,state:AgentState):
        agent_data=state.get('agent_data')
        route=agent_data.get('Route').lower()
        agent_response=state.get('agent_response')
        request=agent_data.get('Request')
        if route=='agent':
            current_agent=agent_data.get('Agent')
            plan=agent_response.get('Plan','')
            response=agent_response.get('output')
            agent_response=self.memory_agent.invoke(f'Store the folowing information to the memory\nAgent Name: {current_agent}\nTask: {request}\nPlan: {plan}\nResult: {response}')
            message=HumanMessage(f'{agent_response}')
            # if self.verbose:
            #     print(colored(f'Memory Stored: {agent_response}',color='yellow',attrs=['bold']))
        elif route=='memory':
            if self.verbose:
                print(colored(f'Request: {request}',color='cyan',attrs=['bold']))
            agent_response=self.memory_agent.invoke(f'Retrive the folowing information from the memory\nAgent Name: {current_agent}\nRequest: {request}')
            # if self.verbose:
            #     print(colored(f'Memory Response: {agent_response}',color='yellow',attrs=['bold']))
            message=HumanMessage(f'{agent_response}')
        else:
            raise Exception('Invalid route')
        
        return {**state,'messages':[message]}

    def final(self,state:AgentState):
        agent_data=state.get('agent_data')
        final_answer=agent_data.get('Final Answer')
        if self.verbose:
            print(colored(f'Final Answer: {final_answer}',color='cyan',attrs=['bold']))
        return {**state,'output':final_answer}

    def controller(self,state:AgentState):
        agent_data=state.get('agent_data')
        return agent_data.get('Route').lower()

    def create_graph(self):
        workflow=StateGraph(AgentState)
        workflow.add_node('reason',self.reason)
        workflow.add_node('agent',self.agent)
        workflow.add_node('memory',self.memory)
        workflow.add_node('final',self.final)

        workflow.add_edge(START,'reason')
        workflow.add_conditional_edges('reason',self.controller)
        workflow.add_edge('agent','memory')
        workflow.add_edge('memory','reason')
        workflow.add_edge('final',END)

        return workflow.compile(debug=False)

    def invoke(self,input:str):
        parameters={
            'os':platform.platform()
        }
        system_prompt=self.system_prompt.format(**parameters)
        user_prompt=f'Query: {input}'
        state={
            'input':input,
            'messages':[SystemMessage(system_prompt),HumanMessage(user_prompt)],
            'agent_data':{},
            'current_agent':'',
            'agent_response':'',
            'output':'',
        }
        graph_response=self.graph.invoke(state)
        return graph_response['output']

    def stream(self,input:str):
        pass