import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader

# sidebar
with st.sidebar:
    st.title('LLM Chatbot')
    st.markdown('''
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM Model
    
    ''')
    add_vertical_space(5)
    st.write('References: [Prompt Engineer](https://youtube.com/@engineerprompt)')

def main():
    st.header("Chat with the Teaching Assistant Chatbot")
    
    # upload a PDF file
    pdf = st.file_uploader("Upload your PDF Here", type="pdf")

    if pdf is not None:
        pdf_reader = PdfReader(pdf)


if __name__ == "__main__":
    main()