import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools.db_tool import query_truck_database
from tools.catia_tool import control_catia_software
from tools.regulation_tool import check_regulations
from agent.prompts import SYSTEM_PROMPT
from langchain.memory import ConversationBufferMemory
load_dotenv()


def get_llm():
    """Initialize LLM pointing to Azure OpenAI"""
    return AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        temperature=1,
        
    )


def create_agent() -> AgentExecutor:
    """Assemble the Agent: LLM + Tools + Prompt"""
    llm = get_llm()

    tools = [
        query_truck_database,
        control_catia_software,
        check_regulations,
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    
    memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )
