import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

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