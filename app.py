import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from prompts import template_1
import os

# load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# set page config
st.set_page_config(page_title="DexterChat", page_icon="🤖")
st.title("DexterChat")

# custom styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")


# get response from the GPT
def get_response(query, chat_history):
    chat_prompt = PromptTemplate.from_template(template_1)

    llm = ChatOpenAI(
        temperature=0.2,
        model="gpt-4o-mini"
    )

    chain = chat_prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "user_message": query
    })

# sidebar
with st.sidebar:
    st.write("DexterChat is a chatbot that helps users with their queries.")
    st.button("New Chat", type='primary')

    st.divider()
    st.header("Recent Conversations")
    st.button(label="Read a PDF", key="1")
    st.button(label="U.S. President in 1901", key="2")
    st.button(label="Daily Tasks", key="3")
    st.button(label="Save Walter White", key="4")
    st.button(label="Read a PDF", key="5")
    st.button(label="U.S. President in 1901", key="6")
    st.button(label="Daily Tasks", key="7")
    st.button(label="Save Walter White", key="8")
    st.button(label="Read a PDF", key="9")
    st.button(label="U.S. President inasdasd as as asd asd 1901", key="10")
    st.button(label="Daily Tasks", key="11")
    st.button(label="Save Walter White", key="12")
    st.button(label="Read a PDF", key="13")
    st.button(label="U.S. President in 1901", key="14")
    st.button(label="Daily Tasks", key="15")
    st.button(label="Save Walter White", key="16")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# display chat history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("You"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# chat input
user_message = st.chat_input("Ask something")
if user_message is not None and user_message != "":
    st.session_state.chat_history.append(HumanMessage(user_message))

    with st.chat_message("You"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        ai_message = st.write_stream(get_response(user_message, st.session_state.chat_history))
        st.session_state.chat_history.append(AIMessage(ai_message))