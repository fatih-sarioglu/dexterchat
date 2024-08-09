import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from prompts import template_1

from pymongo import MongoClient

from dotenv import load_dotenv
import os


# load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGO_URI")

# set page config
st.set_page_config(page_title="DexterChat", page_icon="🤖")
st.title("DexterChat")

# custom styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

client = MongoClient(mongo_uri)

def get_chat_headers():
    chat_headers = client.chat_history.chat_headers.find()

    return chat_headers


def load_page(chat_id):
    chat_history = client.chat_history.chat_bodies.find_one({"id": chat_id})

    if chat_history is not None:
        st.session_state.chat_history = chat_history["messages"]
        for idx, message in enumerate(st.session_state.chat_history):
            if idx % 2 == 0:
                with st.chat_message("You"):
                    st.markdown(message)
            else:
                with st.chat_message("assistant"):
                    st.markdown(message)


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
    st.title("DexterChat")
    st.write("DexterChat is a chatbot that helps users with their queries.")
    st.button("New Chat", type='primary')

    st.divider()
    st.header("Recent Conversations")

    for header in get_chat_headers():
        st.button(label=header["title"],
                  key=header["id"],
                  on_click=load_page,
                  args=(header["id"],))

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# chat input
user_message = st.chat_input("Ask something")
if user_message is not None and user_message != "":

    with st.chat_message("You"):
        st.markdown(user_message)
    st.session_state.chat_history.append(user_message)

    with st.chat_message("assistant"):
        ai_message = st.write_stream(get_response(user_message, st.session_state.chat_history))
    st.session_state.chat_history.append(ai_message)