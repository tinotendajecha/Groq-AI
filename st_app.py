import streamlit as st
import os
import time
from groq import Groq
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')



# Typical data = { } | If empty will generate random questions then if not empty will generate questions based on the data
def generate_example_questions():

    default_questions = [
        {
        'prompt_id': 1,
        'prompt_response' : '''You are a machine learning expert data annotator analyzing news articles. Provide the following to build a knowledge graph:\n\n1. Entities: Max List entities or 'No'.\n2. INTELLECTUAL CONCEPTS\n3. BIG THEMES\n\nINSTRUCTIONS\n\n- Express each INTELLECTUAL CONCEPTS in 1 to 2 words max\n- Express each BIG THEME in 3 to 4 words max\n\nPresent output as a numbered list'''
        },
        {
        'prompt_id': 2,
        'prompt_response' : '''
            What additional items can be added to this
                OR
            For each of the above categories, What additional items can be added to them.
        '''
        },
        {
        'prompt_id': 3,
        'prompt_response' : '''
            These entities were identified in an article.  Provide best categorization in the format \n
            1. entity, classification, define
        '''
        }
    ]
    return default_questions
    
    # if data != []:
    #     # Take the data pass it into an llm then have it generate 3 seggestion questions frrom the context
    #     # client = Groq()

    #     # response = client.chat.completions.create(
    #     #             messages=[
    #     #         {
    #     #             "role": "system",
    #     #         "content": """you are a helpful assistant who generates three suggestions of questions based on the context of the conversation in a simple JSON format/n
    #     #             /n{
    #     #                 /n "questions": ["qsn1", "qsn2", "qsn3"]
    #     #             /n}
    #     #         """
    #     #         },
    #     #         {
    #     #             "role": "user",
    #     #             "content": f"{data}",
    #     #         }
    #     #     ],
    #     #     model="mixtral-8x7b-32768",
    #     #     max_tokens=1024,
    #     #     response_format= {"type": "json_object"}
    #     # )

    #     # return response
    #     return []


def main():

    client = Groq()

    # Add customization options to the sidebar
    st.sidebar.title('Customization')
        

    model_to_use = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768', 'llama2-70b-4096']
    )
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value = 5)

    list_of_qsns = []

    example_questions = generate_example_questions()

    for question in example_questions:
        list_of_qsns.append(question['prompt_response'])
    
    presaved_prompt = st.sidebar.selectbox(
        'Exisiting prompts',
        list_of_qsns,
        placeholder='Select a question to use as a prompt',
        index=None
    )

    # Creat a text input field
    user_question = st.chat_input('Prompt to use')

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
        model_name=model_to_use,
    )

    # Hook up the converstion chain
    conversation = ConversationChain(
        llm=groq_chat,
        memory=memory
    )

    # print(example_questions)

    # and user_question != ''
    if user_question:

        if presaved_prompt != None:
            user_question = presaved_prompt + ' ' + user_question
        
        print(user_question)
        time.sleep(20)

        response = conversation.invoke(user_question)

        # create a message to append to chat history
        message = {'human': user_question, 'AI' : response['response']}

        # Append the message to the chat history
        st.session_state.chat_history.append(message)

        # Will append the code here for example questions

        # response_text = response['response']
        
        st.markdown(':green[Groq]')
        # st.write(response_text)

        for message in st.session_state['chat_history']:
            with st.chat_message("user"):
                st.markdown(message['human'])
            
            with st.chat_message("assistant"):
                st.markdown(message['AI'])

    
    
    # example_questions = generate_example_questions(st.session_state.chat_history)
    
    # questions = st.selectbox(
    #     'Exisiting prompts',
    #     ['qsn 1', 'qsn2']
    # )



        

        



if __name__ == '__main__':
    main()