import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from prompts import template_1, template_2

from pymongo import MongoClient
from pymongo.cursor import Cursor

from dotenv import load_dotenv
import os

def read_cache() -> bool:
    """
    Read the cache file and return the value"""
    with open("app_cache.txt", "r") as f:
        return f.read() == "1"

def write_cache(value: bool):
    """
    Write the value to the cache file"""
    with open("app_cache.txt", "w") as f:
        f.write("1" if value else "0")

# load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGO_URI")

# set page config
st.set_page_config(page_title="DexterChat", page_icon="🤖", initial_sidebar_state="expanded")


# custom styling
def local_css(file_name: str) -> None:
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# connect to database
client = MongoClient(mongo_uri)

def get_chat_headers() -> Cursor:
    chat_headers = client.chat_history.chat_headers.find()

    return chat_headers

def create_new_chat(title: str) -> None:
    # can be removed
    try:
        st.session_state.current_chat_id = client.chat_history.chat_headers.find().sort('id', -1).limit(1)[0]['id'] + 1
    except Exception as e:
        st.session_state.current_chat_id = 0

    client.chat_history.chat_headers.insert_one({
        "id": st.session_state.current_chat_id,
        "title": title
    })

    client.chat_history.chat_bodies.insert_one({
        "id": st.session_state.current_chat_id,
        "messages": []
    })

def save_chat_history(chat_id: int, messages: list) -> None:
    client.chat_history.chat_bodies.update_one(
    {
        "id": chat_id
    },
    {
        "$set": {
            "messages": messages
        }
    })

def delete_chat(chat_id: int) -> None:
    client.chat_history.chat_headers.delete_one({"id": chat_id})
    client.chat_history.chat_bodies.delete_one({"id": chat_id})


def load_recent_chats(chat_id: int) -> None:
    st.session_state.current_chat_id = chat_id
    chat_history = client.chat_history.chat_bodies.find_one({"id": st.session_state.current_chat_id})
    if chat_history is not None:
        st.session_state.chat_history = chat_history["messages"]
        
        for idx, message in enumerate(st.session_state.chat_history):
            if idx % 2 == 0:
                with st.chat_message("You"):
                    st.markdown(message)
            else:
                with st.chat_message("assistant"):
                    st.markdown(message)

def new_chat_button() -> None:
    st.session_state.chat_history = []  
    try:
        st.session_state.current_chat_id = client.chat_history.chat_headers.find().sort('id', -1).limit(1)[0]['id'] + 1
    except Exception as e:
        print(e)

def delete_chat_button() -> None:
    delete_chat(st.session_state.current_chat_id)
    st.session_state.chat_history = []
    try:
        st.session_state.current_chat_id = client.chat_history.chat_headers.find().sort('id', -1).limit(1)[0]['id'] + 1
    except Exception as e:
        print(e)
        

# get response from the GPT
def get_response(query, chat_history) -> str:
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

def generate_chat_header(conversation: list) -> str:
    chat_prompt = PromptTemplate.from_template(template_2)

    llm = ChatOpenAI(
        temperature=0.8,
        model="gpt-4o-mini"
    )

    chain = chat_prompt | llm | StrOutputParser()

    return chain.invoke({
        "user_query": conversation[0],
        "ai_message": conversation[1]
    })


# sidebar
with st.sidebar:
    st.title("DexterChat")
    st.write("DexterChat is a chatbot that helps users with their queries.")
    st.button("New Chat", type='primary', on_click=new_chat_button)
    st.button("Delete Chat", type='secondary', on_click=delete_chat_button)

    st.divider()
    st.header("Recent Conversations")

    for header in get_chat_headers().sort('id', -1):
        st.button(label=header["title"],
                  key=header["id"],
                  on_click=load_recent_chats,
                  args=(header["id"],))

def set_session_state_after_new_chat() -> None:
    if read_cache():
        st.session_state.current_chat_id = client.chat_history.chat_headers.find().sort('id', -1).limit(1)[0]['id']
        load_recent_chats(st.session_state.current_chat_id)
        write_cache(False)
        
set_session_state_after_new_chat()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_chat_id" not in st.session_state:
    try:
        st.session_state.current_chat_id = client.chat_history.chat_headers.find().sort('id', -1).limit(1)[0]['id'] + 1
    except Exception as e:
        print(e)

# chat input
user_message = st.chat_input("Ask something")
if user_message is not None and user_message != "":
    load_recent_chats(st.session_state.current_chat_id)
    print("before", st.session_state.chat_history)
    with st.chat_message("You"):
        st.session_state.user_message_wrapper = st.markdown(user_message)
    st.session_state.chat_history.append(user_message)

    with st.chat_message("assistant"):
        st.session_state.ai_message = st.write_stream(get_response(user_message, st.session_state.chat_history))
    st.session_state.chat_history.append(st.session_state.ai_message)

    print("after", st.session_state.chat_history)

    # create new chat header
    if len(st.session_state.chat_history) == 2:
        create_new_chat(generate_chat_header(st.session_state.chat_history))
        save_chat_history(st.session_state.current_chat_id, st.session_state.chat_history)
        write_cache(True)
        st.rerun(scope="app")
    else:
        # save chat history
        save_chat_history(st.session_state.current_chat_id, st.session_state.chat_history)