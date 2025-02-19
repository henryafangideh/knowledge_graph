import streamlit as st
import os
from langchain_community.graphs import Neo4jGraph
from langchain_groq import ChatGroq
from langchain.chains import GraphCypherQAChain

# Set API Keys (Replace with your actual keys)
os.environ["NEO4J_URI"] = "neo4j+s://512a7b64.databases.neo4j.io"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "Zbm2aMw6WLcCGw20k0eU2pSvMzWyW4lxh_tVxpZ03Q"
groq_api_key = "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"

# Initialize Graph Connection
graph = Neo4jGraph(
    url=os.environ["NEO4J_URI"],
    username=os.environ["NEO4J_USERNAME"],
    password=os.environ["NEO4J_PASSWORD"],
)

# Initialize Language Model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")

# Initialize Query Chain
chain = GraphCypherQAChain.from_llm(
    llm=llm, graph=graph, verbose=True, allow_dangerous_requests=True
)

# Streamlit UI
st.title("Knowledge Graph Querying with LangChain & Neo4j")

# User Query Input
user_query = st.text_input("Enter your question:")

if user_query:
    response = chain.invoke({"query": user_query})
    st.subheader("Response:")
    st.write(response)
