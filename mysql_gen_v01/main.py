# --------------------------
# Section: Library
# --------------------------
from langfuse.callback import CallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from mysql_db_schemas import SCHEMAS
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

# --------------------------
# Section: Langfuse
# --------------------------
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
langfuse_handler = CallbackHandler(
    secret_key=LANGFUSE_SECRET_KEY,
    public_key=LANGFUSE_PUBLIC_KEY,
    host=LANGFUSE_HOST,
)

# --------------------------
# Section: GroqAI Model
# --------------------------
GROQ_API = os.getenv("GROQ_API", "")
llm = ChatGroq(api_key=GROQ_API, model="llama3-70b-8192")
# llm = ChatGroq(api_key=GROQ_API, model="gemma2-9b-it")

# --------------------------
# Section: Output Parser
# --------------------------
parser = StrOutputParser()

# Define prompts
generate_prompt = PromptTemplate.from_template("""
    You are a MySQL Expert (with extensive experience in creating syntactically correct and optimized MySQL queries).
    Your goal is to generate syntactically correct MySQL queries based on the provided MySQL schemas and user specifications while adhering to strict guidelines.

    The answer format: 
        ```sql 
            Answer 
        ```. 

    MySQL Schemas: {schemas}. 
    User Specifications: {specifications}.

    Generate a MySQL "SELECT" query based on the user specifications while strictly adhering to the following rules below. No yapping and do not make up information. DO NOT skip this step:
    MUST DO LIST: 
    - Display from minimum 3 to maximum 5 significant columns (unless the user specifies which specific columns to obtain).
    - Use ONLY the columns existing in the tables. Pay attention to which columns is in which tables.
    - Use ONLY the needed columns to answer the user specifications.
    - ALWAYS use 'LIMIT' to limit the output to 5 rows.
    - Use function to get the current date, if the question involves "today".
    - ALWAYS use 'JOIN' to join multiple tables.
    - Order the results to return the most informative data in the database.
    - ALWAYS check if there are enough columns when using "GROUP BY".
    - Return ONLY MySQL query.
    Do NOT skip this step.
    MUST NOT DO LIST:
    - DO NOT use "SELECT *".
    - DO NOT use subquery.
    - DO NOT change the table names or the column names.
    - DO NOT query for tables or columns that do not exist.
    - DO NOT use "DISTINCT" as much as possible.
    - DO NOT add or return any explanations about MySQL query.
    Do NOT skip this step.
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


# Define chains
# extract_chain = {
#     "generated_sql": generate_chain} | extract_prompt | llm | parser


# Invoke the (final) chain
# output = extract_chain.invoke({
#     "schema": schema,
#     "question": question
# }, config={"callbacks": [langfuse_handler]})
# print(output)

if __name__ == "__main__":
    try:
        print(">>>>> Hello World Demo")
        # User questions/specifications (must be precise)
        question_1 = "List popular Electronics products"
        # Generate MySQL chain
        generate_chain = generate_prompt | llm | parser
        response = generate_chain.invoke({"schemas": SCHEMAS, "specifications": question_1})
        print(response)
    except Exception as e:
        print(f">>>>> Exception message: {e}")
