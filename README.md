## Introduction

---

The Teaching Assistant Chatbot is developed by combining front-end and back-end design as-
pects. The UI puts a focus on ease of use, making it simple for users to upload PDF files and
start the embedding creation and response production processes. With Streamlit functioning
as the GUI and OpenAI’s GPT powering response generation, the design covers both front-
end and back-end development. Using the LLMs and embeddings, back-end processes include
data processing, embedding construction, and response production. The main design and im-
plementation takes heavy inspiration from Alejandro’s PDF chatbot project [Alejandro, 2023]
and Prajwal Krishnas Langchain chatbot project [Krishna, 2023].

## How It Works

---

The application follows these steps to provide responses to your questions:

1. PDF Loading: The app reads multiple PDF documents and extracts their text content.

2. Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.

3. Language Model: The application utilizes a language model to generate vector representations (embeddings) of the text chunks.

4. Similarity Matching: When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones.

5. Response Generation: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.

## Dependencies and Installation

---

To install the Teaching Assistant Chatbot, please follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

3. Obtain an API key from OpenAI and add it to the `.env` file in the project directory.

```commandline
OPENAI_API_KEY=your_secrit_api_key
```

## Usage

---

To use the Teaching Assistant Chatbot, follow these steps:

1. Ensure that you have installed the required dependencies and added the OpenAI API key to the `.env` file.

2. Run the `main.py` file using the Streamlit CLI. Execute the following command:

   ```
   streamlit run app.py
   ```

3. The application will launch in your default web browser, displaying the user interface.

4. Load multiple PDF documents into the app by following the provided instructions.

5. Ask questions in natural language about the loaded PDFs using the chat interface.
