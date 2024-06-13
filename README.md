# PDF & GitHub Query Assistant with Reranker

## Overview

The PDF & GitHub Query Assistant with Reranker is a Streamlit application that allows users to upload PDF files or provide GitHub repository links to extract and query information. The app ranks document chunks based on their relevance to user queries using a cross-encoder model and generates responses using OpenAI's GPT-4 model.

## Features

- **Upload PDF Files**: Upload and process PDF files to extract text (upto 200mb).
- **GitHub Repository Support**: Provide GitHub repository links to fetch and process text from code and documentation files.
- **Relevance Ranking**: Rank document chunks based on their relevance to user queries using the `cross-encoder/ms-marco-MiniLM-L-6-v2` model.
- **Query Responses**: Generate answers to user queries using OpenAI's GPT-4 model.

## Directory Structure

my_app/
│
├── app.py
├── github_utils.py
├── pdf_utils.py
└── query_utils.py


- **app.py**: Handles the Streamlit interface and user interactions.
- **github_utils.py**: Manages fetching and processing data from GitHub repositories.
- **pdf_utils.py**: Manages extracting and processing text from PDF files.
- **query_utils.py**: Manages ranking documents and generating answers using OpenAI's API.

## Usage

1. **Run the Streamlit app**:
   ```sh
   streamlit run app.py
   
2. **Upload a PDF file or enter a GitHub repository URL**
3. **Enter your OpenAI API Key**
4. **Submit a query to get answers based on the content of the uploaded PDF or the provided GitHub repository**

## Future
This is only the first draft. I am planning to use open source models to eliminate the need of an OpenAI API Key