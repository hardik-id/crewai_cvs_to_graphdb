import os
from typing import Any

from crewai_tools import BaseTool
from dotenv import load_dotenv
from neo4j import GraphDatabase
from pydantic import PrivateAttr

# Load environment variables from the .env file
load_dotenv()


class CypherExecutorTool(BaseTool):
    name: str = "Cypher Query Executor Tool"
    description: str = (
        "This tool executes single complete Cypher query in a Neo4j database."
    )

    _neo4j_connection: Any = PrivateAttr()

    model_config = {
        'underscore_attrs_are_private': True,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Get Neo4j credentials from environment variables
        neo4j_uri = os.getenv('NEO4J_URI')
        neo4j_user = os.getenv('NEO4J_USER')
        neo4j_password = os.getenv('NEO4J_PASSWORD')

        # Initialize the Neo4j connection
        if not neo4j_uri or not neo4j_user or not neo4j_password:
            raise ValueError("Neo4j connection information is missing from the environment variables")

        # Set the private attribute
        self._neo4j_connection = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def _run(self, cypher_query: str) -> str:
        # Split queries by semicolon
        queries = cypher_query
        results = []

        # Use the private Neo4j connection attribute
        with self._neo4j_connection.session() as session:
            if cypher_query.strip():  # Skip empty queries
                result = session.run(cypher_query.strip())  # Execute each query
                results.append(result.data())  # Collect the results

        # Combine results for output
        return "\n".join(str(r) for r in results)
