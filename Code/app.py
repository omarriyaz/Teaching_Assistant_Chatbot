# Necessaryimports

import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# Functions

# Function to extract text from PDFs
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf) # Using the PdfReader class from PyPDF2 library
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter( # Using the CharacterTextSplitter class from langchain library
        separator="\n", # Single line break
        chunk_size=1000, # Chunk size of 1000 characters
        chunk_overlap=200, # Chunk overlap of 200 characters 
        length_function=len # Length
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create vectorstore
def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") # Using the instructor-xl embeddings 
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Function to create conversation chain
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI() # GPT 3.5 Turbo Chat Model
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Function to handle user input
def handle_user_input(user_question):
    response = st.session_state.conversation({'question': user_question}) # Get response from the conversation chain using the question asked by the user
    st.session_state.chat_history = response['chat_history'] # Update the chat history stored in session state with the conversation

    # Display the chat history
    for i, message in enumerate(reversed(st.session_state.chat_history)):
        if i % 2 == 0:
            # If the index is even, it means it's a Chatbot's message
            st.markdown(f'<div style="background-color: #2b313e; color: white; padding: 10px; border-radius: 10px; margin-bottom: 20px;">Chatbot: {message.content}</div>', unsafe_allow_html=True)
        else:
            # If the index is odd, it means it's a User's message
            st.markdown(f'<div style="background-color: #475063; color: white; padding: 10px; border-radius: 10px; margin-bottom: 20px;">You: {message.content}</div>', unsafe_allow_html=True)

def main():
    load_dotenv() # Gives access to API keys
    st.set_page_config(page_title="Teaching Assistant Chatbot") # Page title
    header_placeholder = st.empty()  # Placeholder for dynamic header text
    subheader_placeholder = st.empty() # Placeholder for dynamic header text

    if "pdf_sent_successfully" not in st.session_state: # Check if the pdf has been sent successfully
        st.session_state.pdf_sent_successfully = False # Set the pdf_sent_successfully to False
    
    if st.session_state.pdf_sent_successfully:
        header_placeholder.header("Teaching Assistant Chatbot")
        subheader_placeholder.caption("Document successfully uploaded!")

    else:
        header_placeholder.header("Upload your documents then I will be ready to assist you!")
        subheader_placeholder.caption("To Upload your documents you can open the sidebar and either browse through the files on your computer or simply drag and drop your documents on there.")

    # User input
    user_question = st.text_input("Ask me a question about your documents:")
    if user_question:
            handle_user_input(user_question)

    # Sidebar
    with st.sidebar:
        st.subheader("Upload your Documents Here:")
        st.caption("You can upload multiple PDFs here as long as they are under 200MB per file. Click on 'Browse Files' or drag and drop your files to select them. Once you have uploaded your PDFs, click on the 'Send to Chatbot' button and close the sidebar to start chatting with the Teaching Assistant Chatbot.")
        pdf_docs = st.file_uploader("Choose Files:", accept_multiple_files=True) # File uploader for PDFs
        
        if pdf_docs:
            if st.button("Send to Chatbot"):
                with st.spinner("Sending your documents to the Teaching Assistant Chatbot..."): # Spinner to show that the documents are being sent
                    try:
                        raw_text = get_pdf_text(pdf_docs)
                        text_chunks = get_text_chunks(raw_text)
                        vectorstore = get_vectorstore(text_chunks)
                        st.session_state.conversation = get_conversation_chain(vectorstore)
                        st.session_state.pdf_sent_successfully = True  
                        st.success("You can now chat with your documents.")
                        header_placeholder.header("Teaching Assistant Chatbot")
                        subheader_placeholder.caption("Document successfully uploaded!")
                    
                    # Error handling
                    except Exception as e:
                        st.error(f"Error occurred: {str(e)}")
# Main function
if __name__ == "__main__": 
    main()