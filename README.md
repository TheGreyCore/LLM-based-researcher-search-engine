# LLM-based Researcher Search Engine

Project (E13) created by:
- Dmitri Matetski
- Hendrik Püss
- Georg-Oliver Loorand

## Preface

This project is a search engine for researchers at the University of Tartu, utilizing large language models (LLMs) and embedding vectors to provide accurate and relevant search results.

Our main objective is to create a tool that enables users to find key information quickly -- in this case, searching for researchers and studies from the University of Tartu. In a practical sense, the project can be scaled and transform to other fields with minimal changes in code. For example, hospital workers may find it useful to quickly access critical information that is normally stored in large databases.

## Features

- **Language Translation**: Automatically translates non-English queries to English.
- **Query Validation**: Validates user input to ensure it is a valid search query.
- **Search by Various Criteria**: Allows searching by researcher name, research title, or type of research.
- **Customizable Results**: Determines the number of search results to return, with a default of 5.
- **Formatted Output**: Provides search results in a human-readable format, maintaining the original language of the query.

## Project Structure

- `aiLib.py`: Contains the `AILib` class for interacting with the Azure OpenAI API.
- `backend/service.py`: Contains the `Service` class for processing user prompts and generating search results.
- `backend/app.py`: Flask application for handling HTTP requests and processing prompts.
- `embeddingsVectors.py`: Contains the `EmbeddingVectors` class for interacting with the embedding vectors API.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/TheGreyCore/LLM-based-researcher-search-engine.git
    cd LLM-based-researcher-search-engine
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    ```sh
    export OPENAI_API_KEY=your_openai_api_key
    ```

5. Run Milvus database:
    ```sh
    docker run -d --name milvus_cpu_0.11.0 -p 19530:19530 -p 19121:19121 milvusdb/milvus:0.11.0-cpu-d030521-3ea1b4
    ```

## Usage

1. Run the Flask application:
    ```sh
    python backend/app.py
    ```

2. Access the application at `http://localhost:5000/prompt?prompt=your_query&key=forTesting`.

## Example

To search for researchers, send a GET request to the `/prompt` endpoint with the query and key parameters:
```sh
curl "http://localhost:5000/prompt?prompt=search_query&key=forTesting"
```

## Data collection

In this project, each entry is required to contain the release year, title, authors, keywords, links, and abstract. The largest hurdle in terms of data was collecting the abstracts, as only a small fraction of studies submitted to ETIS (Estonian Research Information System) contain them. Consequently, we used a web scraper to gather more data. This would quickly offer diminishing returns as the scraper had to be adjusted for every domain separately, and every subsequent domain would have given us only 25 or fewer entries. In total, we collected nearly 900 entries that had to be cleaned.
