# Generate (optimized) MySQL Query using LangChain and GroqAI on CLI (Version 02)

Welcome to MySQL Query Generation Project using LangChain and GroqAI! This project is designed to be a guide, testing and implementation for generating MySQL Query using LangChain and GroqAI.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Virtual Environment](#Virtual-Environment)
  - [Installation](#installation)
  - [Environment Variable](#Environment-Variable)
- [Quick Start](#Quick-Start)
- [Development Documentation](#development-documentation)

## Introduction

This is my implementation of LangChain - An LLM Framework and GroqAI. There are 2 different implementations of LangChain and GroqAI, the first one is with a `SCHEMAS`constant, the second one is with reading schemas from files (I prefer the 2nd one). 

There is also an implementation of Langfuse which is a tracer and debugger be LLM applications.

The tutorial by LangChain that I based on is linked [here](https://python.langchain.com/v0.2/docs/tutorials/sql_qa/). I will also have the tutorial displayed in case the hyperlink is not accessible https://python.langchain.com/v0.2/docs/tutorials/sql_qa/.

## Getting Started

I recommend running this project on **Python 3.10+**. This project was originally running on **Python 3.10.14**.

### Virtual Environment

A virtual environment should be setup for this project. You can use any of yours preferable virtual environment, I will use Anaconda/Miniconda as the Virtual Environment for this project.

### Installation

To get started, you need to download this project from Github and navigate to the project's folder.

```sh
cd langchain-groq-mysql-query-gen-cli/
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
LANGFUSE_SECRET_KEY=""
LANGFUSE_PUBLIC_KEY=""
LANGFUSE_HOST=""
```

## Quick Start

There are 2 different folders representing 2 different implementations, each of the folder contains a `main.py` file to run its respective project. Run the project using the following command(s).

```sh
# Run main.py in version 01
python .\mysql_gen_v01\main.py
# Run main.py in version 02
python .\mysql_gen_v02\main.py
```

## Development Documentation

Order from newest to oldest.

### 07/08/2024

- Create `mysql_gen_v02`.
- Change prompts, add MySQL files.

### 06/08/2024

- Push old prompts, link can be found [here](https://github.com/TonyH0401/langchain-groq-mysql-query-gen-cli/tree/5cfaf064e1bd35802900da10ff3997c22b2af424).
