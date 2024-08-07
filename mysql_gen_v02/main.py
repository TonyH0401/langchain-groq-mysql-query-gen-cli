# --------------------------
# Section:
# --------------------------
from utils import read_mysql_db_schemas, convert_schemas_to_json_llm, convert_json_mysql_schemas_to_markdown, generate_mysql_query
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
load_dotenv()

# --------------------------
# Section:
# --------------------------
if __name__ == "__main__":
    try:
        print(">>>>> Hello World Demo")
        # Define file paths
        filepath_1 = "Zookeeper.sql"
        filepath_2 = "./mysql_db_schemas/employee.sql"
        raw_mysql_db_schemas = read_mysql_db_schemas(filepath=filepath_2)
        if raw_mysql_db_schemas is None:
            raise Exception("File read, there is no data!")
        markdown_json_schemas = convert_json_mysql_schemas_to_markdown(json_schemas=convert_schemas_to_json_llm(
            raw_schemas=raw_mysql_db_schemas))
        # print(markdown_json_schemas)
        # Define questions
        question_1 = "How many employees are there?"
        question_2 = "List the top 15 employees (include the employee's name) with the highest salaries"
        mysql_query_gen = generate_mysql_query(markdown_json_schemas, question_2)
        print(mysql_query_gen)
    except Exception as e:
        print(f">>>>> Exception message: {e}")
