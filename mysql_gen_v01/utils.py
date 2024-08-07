from langfuse.callback import CallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from mysql_gen_v01.mysql_db_schemas import schema
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API = os.getenv("GROQ_API", "")
llm = ChatGroq(api_key=GROQ_API, model="gemma2-9b-it")
parser = StrOutputParser()


def read_mysql_schemas_file(filepath):
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


def convert_schemas_to_json_llm(schemas):
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
    reponse = chain.invoke({"schemas": schemas})
    return reponse


def convert_json_to_markdown(json):
    return f"```sql\n{json}\n```"

