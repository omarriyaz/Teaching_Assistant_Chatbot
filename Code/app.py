import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf) # using the PdfReader class from PyPDF2 library
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter( # using the CharacterTextSplitter class from langchain library
        separator="\n", # single line break
        chunk_size=1000, # chunk size of 1000 characters
        chunk_overlap=200, # chunk overlap of 200 characters 
        length_function=len # length
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") # instructor-xl embeddings
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    
    llm = ChatOpenAI() # gpt chat model

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    # Define CSS styles
    css_styles = '''
    <style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.bot {
        background-color: #475063;
    }
    .chat-message .avatar {
        width: 8%;  /* Adjust the width of the avatar */
    }
    .chat-message.user .avatar {
        width: 8%;  /* Adjust the width of the avatar for user's messages */
    }
    .chat-message .avatar img {
        max-width: 50px;  /* Adjust the maximum width of the avatar image */
        max-height: 50px;  /* Adjust the maximum height of the avatar image */
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message.user .message {
        width: 90%;  /* Adjust the width of the message container */
        padding: 0 5rem;  /* Padding for user's messages */
        color: #fff;
    }

    .chat-message.bot .message {
        width: 90%;  /* Adjust the width of the message container */
        padding: 0 5rem;  /* Padding for bot's messages */
        color: #fff;
    }
    </style>
    '''

    bot_template = '''
    <div class="chat-message bot">
        <div class="avatar">
            <img src="https://t3.ftcdn.net/jpg/03/22/38/32/360_F_322383277_xcXz1I9vOFtdk7plhsRQyjODj08iNSwB.jpg">
        </div>
        <div class="message" style="padding: 0 5rem; width: 90%;">{{MSG}}</div>
    </div>
    '''

    user_template = '''
    <div class="chat-message user">
        <div class="avatar">
            <img src="https://openclipart.org/image/2000px/247320">
        </div>    
        <div class="message" style="padding: 0 5rem; width: 90%;">{{MSG}}</div>
    </div>
    ''' 

    # Inject CSS styles
    st.write(css_styles, unsafe_allow_html=True)

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            # Display user's message
            st.write(
                f'<div class="chat-message user">{user_template.replace("{{MSG}}", message.content)}</div>',
                unsafe_allow_html=True
            )
        else:
            # Display bot's message
            st.write(
                f'<div class="chat-message bot">{bot_template.replace("{{MSG}}", message.content)}</div>',
                unsafe_allow_html=True
            )


def main():
    st.set_page_config(page_title="Teaching Assistant Chatbot") 

    header_placeholder = st.empty()  # Placeholder for dynamic header text
    subheader_placeholder = st.empty()

    if "pdf_sent_successfully" not in st.session_state:
        st.session_state.pdf_sent_successfully = False
    
    if st.session_state.pdf_sent_successfully:
        header_placeholder.header("Chat with the Teaching Assistant Chatbot")
        subheader_placeholder.caption("")
    else:
        header_placeholder.header("Upload your documents then I will be ready to assist you!")
        subheader_placeholder.caption("To Upload your documents you can open the sidebar and either browse through the files on your computer or simply drag and drop your documents on there.")
    
    user_question = st.text_input("Ask me a question about your documents:")  # Show text input field
    if user_question:
            handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on the 'Send to Chatbot' ", accept_multiple_files=True)
        
        if pdf_docs:
            if st.button("Send to Chatbot"):
                with st.spinner("Processing"):
                    try:
                        raw_text = get_pdf_text(pdf_docs)
                        text_chunks = get_text_chunks(raw_text)
                        vectorstore = get_vectorstore(text_chunks)
                        st.session_state.conversation = get_conversation_chain(vectorstore)
                        st.session_state.pdf_sent_successfully = True  
                        st.success("Success! You can now chat with your documents.")
                        header_placeholder.header("Chat with the Teaching Assistant Chatbot")
                        subheader_placeholder.caption("")
                        show_text_input = True
                    except Exception as e:
                        st.error(f"Error occurred: {str(e)}")
        
if __name__ == "__main__":
    main()