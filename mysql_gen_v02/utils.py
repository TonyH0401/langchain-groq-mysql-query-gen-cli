from langfuse.callback import CallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "")
langfuse_handler = CallbackHandler(
    secret_key=LANGFUSE_SECRET_KEY,
    public_key=LANGFUSE_PUBLIC_KEY,
    host=LANGFUSE_HOST,
)

GROQ_API = os.getenv("GROQ_API", "")
llm = ChatGroq(api_key=GROQ_API, model="gemma2-9b-it")
# llm = ChatGroq(api_key=GROQ_API, model="llama3-70b-8192")
parser = StrOutputParser()


def read_mysql_db_schemas(filepath):
    raw_mysql_schemas = None
    try:
        file_exist = os.path.isfile(filepath)
        if file_exist is False:
            print("> File does not exist!")
            return None
        fd = open(filepath, 'r')
        sqlFile = fd.read()
        raw_mysql_schemas = sqlFile
        fd.close()
    except Exception as e:
        print(f"> Exception message: {e}")
    return raw_mysql_schemas


def convert_schemas_to_json_llm(raw_schemas):
    template = """
        You are an information extracting expert.
        Your goal is to extract column information from the provided schemas and convert them into JSON format.
        
        Schemas: {schemas}

        You strictly follow these goals and rules below. No yapping and do not make up information. DO NOT skip this step.
        DO:
            - The schema table name is the JSON object name.
            - Each column is a property in the JSON object.
            - The value of each property is the datatype of each column.
            - Include property for "PRIMARY KEY" and "CONSTRAINT".
            - Extract the column information from the schemas and return the extracted data in JSON format.
            - Return ONLY the JSON format.
        DO NOT:
            - Add "Here is the extracted data in JSON format:" or any similar lines.
    """
    prompt = PromptTemplate.from_template(template=template)
    chain = prompt | llm | parser
    response = chain.invoke({"schemas": raw_schemas})
    return response


def convert_json_mysql_schemas_to_markdown(json_schemas):
    return f"""```mysql\n {json_schemas} \n```"""


def generate_mysql_query(schemas, specifications):
    template = """
        You are a MySQL expert.
        Your goal is to create syntactically correct MySQL query ONLY.

        The answer format: 
            ```sql 
                Answer 
            ```. 

        Given the MySQL database schemas: {schemas}.
        Generate MySQL "SELECT" query based on the following user specifications: {specifications}.

        You strictly follow these goals and rules below. No yapping and do not make up information. DO NOT skip this step:
        MUST DO LIST:
        - ONLY displays minimum 3 and maximum 5 properties in the schema.
        - The schema's primary key(s) must ALWAYS be used in "SELECT" query.
        - ONLY use relevant tables to the user specifications or columns that are needed to answer user question.
        - ALWAYS look at the tables in the database to see what you can query and use ONLY the column names you can see in the tables below.
        - Pay attention to which column is in which table.
        - Order the results to return the most informative data in the database.
        - Use "JOIN" when joining multiple tables.
        - Use 'LIMIT' to limit the output to 10 rows.
        MUST NOT DO LIST:
        - DO NOT use "*" when generating "SELECT" query.
        - DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
        - DO NOT use "DISTINCT" as much as possible.
        - DO NOT query for columns that do not exist.
        - DO NOT add any explanations.
        DO NOT skip this step.
    """
    prompt = PromptTemplate.from_template(template=template)
    chain = prompt | llm | parser
    response = chain.invoke(
        {"schemas": schemas, "specifications": specifications}, config={"callbacks": [langfuse_handler]})
    return response
