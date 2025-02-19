# -*- coding: utf-8 -*-
"""knowledge_graph_implementation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1L9mI0LHO5KdAurfbKnqQ8VeEDXWpCcSA

# **Querying the Graph DB using Python Programming and Langchain**
"""

!pip install --upgrade --quiet  langchain langchain-community langchain-groq neo4j

#Graph DB Configuration
NEO4J_URI="neo4j+s://512a7b64.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="Zbm2aMw6WLcCGw20k0eUO2pSvMzWyW4lxh_tVxpZ03Q"

import os
os.environ["neo4j+s://c6502278.databases.neo4j.io"] = NEO4J_URI
os.environ["neo4j"] = NEO4J_USERNAME
os.environ["uJiRWP3qBSnrC_hPGZ0inPeAMf7PIRToEOCwXuy8a-U"] = NEO4J_PASSWORD

from langchain_community.graphs import Neo4jGraph
graph=Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
)

graph

groq_api_key="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"

from langchain_groq import ChatGroq

llm=ChatGroq(groq_api_key=groq_api_key,model_name="Gemma2-9b-It")
llm

from langchain_core.documents import Document
text="""
The UK Student Visa is designed for individuals aged 16 and over who wish to study at a recognized educational institution in the UK. To be eligible, applicants must have received an unconditional offer from a licensed student sponsor, demonstrate sufficient financial resources to support themselves and pay for their course, and possess adequate English language skills. Parental consent is required for applicants aged 16 or 17.
Among the various UK visa categories, the Student Visa, Graduate Visa, Skilled Worker Visa, Family Visa, and Standard Visitor Visa are some of the most common.
The process of obtaining a Student Visa for the UK typically includes completing an online application, paying the necessary fees, gathering supporting documents like your CAS and financial statements, and attending an appointment to provide your biometric data.
The length of stay on a Student Visa depends on the type of course:
Up to 5 years for degree-level courses.
Up to 2 years for courses below degree level.
Students can arrive in the UK up to one week before their course starts if it lasts six months or less, or up to one month before if it lasts longer.
Students may be able to bring their partner and children as dependents.
"""
documents=[Document(page_content=text)]
documents

!pip install --upgrade --quiet langchain_experimental

from langchain_experimental.graph_transformers import LLMGraphTransformer
llm_transformer=LLMGraphTransformer(llm=llm)

graph_documents=llm_transformer.convert_to_graph_documents(documents)

graph_documents

graph_documents[0].nodes

graph_documents[0].relationships

"""### **RAG Framework**"""

!pip install --upgrade --quiet  apoc

### Load the dataset for uk immigration visa

ukimmigrationandvisa_query = """
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/OnyiobaziA/UK-IMMIGRATION-PROJECT/refs/heads/main/uk_visa_text.csv' AS row

WITH row
WHERE row.Subject IS NOT NULL AND row.Subject <> "" AND row.Detail IS NOT NULL AND row.Detail <> ""

MERGE (source:Entity {name: row.Subject})
SET source.detail = coalesce(source.detail, "") + row.Detail + "\n"

MERGE (target:Entity {name: row.Detail})

WITH source, row, target
WHERE row.Relationship IS NOT NULL AND row.Relationship <> ""

CREATE (source)-[:RELATED_TO {relationshipType: row.Relationship}]->(target)

RETURN "Data Loaded Successfully and Relationships Created";
"""

graph

graph.query(ukimmigrationandvisa_query)

graph.refresh_schema()
print(graph.schema)

from langchain.chains import GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(llm=llm, graph=graph, verbose=True, allow_dangerous_requests=True) # Set allow_dangerous_requests to True
chain

response=chain.invoke({"query":"What documents do I require to apply for a student visa"})

response