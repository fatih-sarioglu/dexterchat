template_1 = """
    You are a helpful assistant that helps users with their queries.\
    Answer the below user questions considering the chat history.\
    
    Chat History: {chat_history}

    User Message: {user_message}
"""

template_2 = """
    You are a helpful assistant that creates titles for conversations.\
    Give title to a conversation given the start of a conversations.\
    Just write the title as answer, do not add extra information.\
    Do not use quotation marks.\
    
    User Query: {user_query}
    AI Message: {ai_message}
"""