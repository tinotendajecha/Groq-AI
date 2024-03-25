import streamlit as st
import os
import time
from groq import Groq
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from dotenv import load_dotenv




def main():
    load_dotenv()

    api_key = os.getenv('GROQ_API_KEY')

    client = Groq()

    # Display the Groq logo
    spacer, col = st.columns([5, 1])  
    with col:  
        st.image('groqcloud_darkmode.png')
    

    st.title('Chat with Groq')
    st.write('Hey, I am your groq assistant. I am here to help you with your queries. Please type your query in the box below and I will try to help you out.')

    # Add customization options to the sidebar
    st.sidebar.title('Customization')

    # Set additional text in state
    if 'additional_text_input' not in st.session_state:
        st.session_state.additional_text_input = ''

    additional_text_input = st.sidebar.text_input('Enter any large text input you might have here', value=st.session_state['additional_text_input'])
        
    st.session_state['additional_text_input'] = additional_text_input

    model_to_use = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768', 'llama2-70b-4096']
    )
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value = 5)

    # Creat a text input field
    user_question = st.text_input('Ask your question')


    memory = ConversationBufferWindowMemory(k=conversational_memory_length) # Set the memory length    

    # Setup up chat history object
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history=[]
    else:
        for message in st.session_state.chat_history:
            memory.save_context({'input':message['human']},{'output':message['AI']})

    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
        groq_api_key=api_key, 
        model_name=model_to_use
    )

    # Hook up the converstion chain
    conversation = ConversationChain(
        llm=groq_chat,
        memory=memory
    )

    if user_question:
        user_query =  user_question + ' ' + additional_text_input
        # print(user_query)
        # print(len(user_query))

        response = conversation.invoke(user_query)

        # create a message to append to chat history
        message = {'human': user_query, 'AI' : response['response']}

        # Append the message to the chat history
        st.session_state.chat_history.append(message)

        response_text = response['response']
        
        st.markdown(':green[Groq]')
        st.write(response_text)

        st.session_state['additional_text_input'] = " "
        # print(st.session_state['additional_text_input'])

        












if __name__ == '__main__':
    main()