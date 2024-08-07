# Generate (optimized) MySQL Query using LangChain and GroqAI on CLI (Version 02)

Welcome MySQL Query Generation using Langchain and GroqAI Project! This project is designed to be a guide, testing and implementation for generating MySQL Query using LangChain and GroqAI.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Virtual Environment](#Virtual-Environment)
  - [Installation](#installation)
  - [Environment Variable](#Environment-Variable)
- [Quick Start](#Quick-Start)
- [Development Documentation](#development-documentation)

## Introduction

This is my implementation of LangChain - An LLM Framework and GroqAI. There are 2 implementations using MySQL (with MySQL there are 2 different versions). Each implementation has notes, synopsis, hints and further research included.

The original tutorial by LangChain that I based on is linked [here](https://python.langchain.com/v0.2/docs/tutorials/sql_qa/). I will also have the tutorial displayed in case the hyperlink is not accessible https://python.langchain.com/v0.2/docs/tutorials/sql_qa/. However, I don't totally follow the tutorial and there are variation within the implementation.

## Getting Started

I recommend running this project on **Python 3.10+**. This project was originally running on **Python 3.9.19**.

### Virtual Environment

A virtual environment should be setup for this project. You can use any of yours preferable virtual environment, I will use Anaconda/Miniconda as the Virtual Environment for this project.

### Installation

To get started, you need to download this project from Github and navigate to the project's folder.

```sh
cd langchain-mysql-gen-cli/
```

Dowloading the project's dependencies from `requirements.txt` file.

```sh
pip install -r requirements.txt
```

I also have a [link](https://chatgpt.com/share/757c50b4-f574-48d0-a04d-c955d100aeab) to support you in this process.

### Environment Variable

This step is **important**! Create an `.env` file to store your API KEY(s). These are the API KEY(s) you will need. Currently, in this project, I am using Google's Gemini API but you can change it to any LLM(s) you prefer.

```sh
GOOGLE_API_KEY=""
```

## Quick Start

Most of the functions are defined in `main.py`. Run the project using the following command(s).

```sh
python main.py
```

## Development Documentation

Order from newest to oldest.

### 06/08/2024

- Problem: Currently, we are using raw schemas to generate queries. I learnt that markdown and json format is best used for LLM (in this
paritcular case), so I want to convert the raw schemas into json then into markdown. I have several method of approach.
    - Original method: Code the json formatter and markdown by yourself. **This I implemented**.
    - Structured Output Parser method: Using LLM + output_parser_structure, the LLM will read the raw schemas and the output parser will return structured result. However, with this method, we need to pre-defined the structure and the properties we want to take out first (not automatically generated). 
        - https://python.langchain.com/v0.2/docs/how_to/structured_output/ (gotta read it all, I stopped at Few-shot)
        - https://python.langchain.com/v0.2/docs/how_to/#output-parsers.
    - Fully LLM method: Another approach is to ask the LLM (fully) to extract the columns inside the raw schemas, basically letting the LLM do  all the work (reading and extracting from raw schemas). This has a high change of hallucination. **This I implemented**, it is pretty accurate but it is pretty slow as well.

### 03/08/2024

- In LangChain, there is a function (and toolkits) for SQL, this function already has a default prompt but you can define your own prompt (I did implement this method in the project).

- LangChain's SQL tutorial:
  - https://python.langchain.com/v0.2/docs/tutorials/sql_qa/.
  - https://api.python.langchain.com/en/latest/chains/langchain.chains.sql_database.query.create_sql_query_chain.html, definition of a function used.
  - https://python.langchain.com/v0.2/docs/how_to/#use-cases, list of use cases for SQL RAG.

- Here is an old result from a deleted implementation:
```mysql
    SELECT
        tt.ticket_type_id,
        tt.ticket_type_name,
        SUM(bd.quantity) AS total_sold
    FROM TicketType AS tt
    JOIN BookingDetail AS bd
    ON tt.ticket_type_id = bd.ticket_type_id
    JOIN Booking AS b
    ON bd.booking_id = b.booking_id
    WHERE
        b.created_at >= DATE_FORMAT(NOW(), '%Y-01-01')
    GROUP BY
        tt.ticket_type_id,
        tt.ticket_type_name
    ORDER BY
        total_sold DESC
    LIMIT 50;
```