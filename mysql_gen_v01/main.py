
from langfuse.callback import CallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from mysql_gen_v01.mysql_db_schemas import schema
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

# Env variables
GROQ_API = os.getenv("GROQ_API", "")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "")
LANGFUSE_SEC = os.getenv("LANGFUSE_SEC", "")
LANGFUSE_PUB = os.getenv("LANGFUSE_PUB", "")

# Define Langfuse (LLM tracing)
langfuse_handler = CallbackHandler(
    secret_key=LANGFUSE_SEC,
    public_key=LANGFUSE_PUB,
    host=LANGFUSE_HOST,
)

# Define model
llm = ChatGroq(api_key=GROQ_API, model="llama3-70b-8192")

# Define prompts
generate_prompt = PromptTemplate.from_template("""
    You are a database query specialist with extensive experience in creating precise and efficient SQL queries. 
    Your expertise ensures that every query you generate adheres to the highest standards and rules set by the database schema.
    Your goal is to generate SQL queries based on user input while adhering to strict guidelines.
                                      
    Schema: {schema}. 
    userQuestion: {question}.
    Generate an SQL query based on the userQuestion and pastResult while strictly adhering to the following rules:
    DO:
    - Use the exact name of tables and properties, they MUST be exactly the same in the query as in the schema.
    - ALWAYS look at the tables and tables' properties in the database schema to see what you can query.
    - Use only the column names you can see existing in the tables. 
    - Pay attention to which column is in which table.
    - Naming table must be unique.
    - ALWAYS use 'LIMIT' function to limit the out to 20 rows.
    - Use function to get the current date, if the question involves "today".
    - If there are tables need to be joined, you always use 'JOIN' function to join tables.
    - Query only the columns that are needed to answer the user question.
    - Unless the user specifies in the question specific columns to obtain, display for at most 5 significant columns. 
    - The order of the results to return the most informative data in the database. The schema's primary key(s) must always be used in SELECT query.
    - When 'GROUP BY', specifically check if enough essential columns
    - Return SQL query ONLY.
    Do NOT skip this step.
    Do NOT:
    - Query for columns or properties that do not exist.
    - Make or generate any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
    - Use SQL subquery.
    - Change the table's name.
    - Use columns that not belong to table
    - Use SELECT *.
    - Use 'TOP 1'.
    - Duplicate table names.
    - Return any values beside the SQL query.
    Do NOT skip this step.
                                      
    An optimal and syntactically correct SQL query to retrieve relevant information from the database schema based on the content of the user input.
    Only the SQL query is returned. Nothing other than the SQL query is returned.
""")
extract_prompt = PromptTemplate.from_template("""
    You are an SQL queries extractor expert and specialist.
    You are responsible for extracting ONLY SQL queries code block from a passage or text.
    You must extract SQL queries and place it in this format ```sql ```.
    Your goal is to extract only SQL query code block from a passage or text while adhering to strict guidelines.

    Strictly adhering to the following rules:
    - Receive the output from {generated_sql} and extract ONLY the SQL queries code block.
    - Place the SQL queries code block inside this format ```sql ```.
    - Below the ```sql ``` is the explaination for the SQL queries code block.
    Do NOT skip this step.
                                              
    SQL queries code block generated by {generated_sql} is in this ```sql ``` format.
    With SQL queries code block exaplaination.
""")

# Define output parser
parser = StrOutputParser()

# Define chains
generate_chain = generate_prompt | llm | parser
extract_chain = {
    "generated_sql": generate_chain} | extract_prompt | llm | parser


# Invoke the (final) chain
# output = extract_chain.invoke({
#     "schema": schema,
#     "question": question
# }, config={"callbacks": [langfuse_handler]})
# print(output)

if __name__ == "__main__":
    try:
        print(">>>>> Hello World Demo")
        # Define user question, must be precise
        question_1 = "List popular Electronics products"
    except Exception as e:
        print(f">>>>> Exception message: {e}")