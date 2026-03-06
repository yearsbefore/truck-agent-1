import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import AzureChatOpenAI

load_dotenv()

# Initialize database connection
_db_url = os.getenv("DATABASE_URL", "sqlite:///database/trucks.db")
_db = SQLDatabase.from_uri(_db_url)

_llm = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    temperature=1,
)

_sql_agent = create_sql_agent(
    llm=_llm,
    db=_db,
    agent_type="openai-tools",
    verbose=True,
)



@tool
def query_truck_database(query: str) -> str:
    """
    Query the truck database using natural language.
    Automatically generates SQL and returns results.
    Use when: looking up truck models, brands, payload, or dimensions.
    Example input: "Find all trucks with payload over 20 tons" / "What Volvo models are available?"
    """
    try:
        result = _sql_agent.invoke({"input": query})
        return result.get("output", "Query completed but returned no results.")
    except Exception as e:
        return f"Database query error: {str(e)}"
