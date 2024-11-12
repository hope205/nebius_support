import chromadb,json, os
import streamlit as st
from streamlit_chat import message
from openai import OpenAI
from embed import *
from dotenv import load_dotenv



load_dotenv()


st.set_page_config(page_title="Nebius", page_icon=":robot_face:")

#load your 
client = chromadb.PersistentClient(path="chroma_db")

#net_test


system_message = """

    You are an intelligent customer support assistant with expertise at answering questions about Nebius just like a human would. \
    Your goal is to use the information provided below to answer the questions of the user.\
    If you don't know the answer to any question, tell the user to check out the information from Nebius AI website. \
    Ensure your responses are polite and friendly.  \
    Your accurate responses are crucial to the growth of  Nebius AI. \

"""


human_template = """
    User Query: {query}

    Relevant knowledge base Snippets: {context}
"""

# Generate response to user prompt
def generate_response(prompt):
    # Perform semantic search and retrieves similar documents
    search_results = collection.query(
    query_texts= prompt,
    n_results=3
)

    context = " "
    context += f"Snippet from: {search_results}\n\n"

    # Generate human prompt template and convert to API message format
    query_with_context = human_template.format(query= prompt, context=context)

    # # Convert chat history to a list of messages
    st.session_state['messages'].append({"role": "user", "content": query_with_context})

    client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

    # Run the chat client
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-fast",
        messages= st.session_state['messages'],
        temperature=0.2,
        max_tokens=150,
    )
    r = response.to_json()
    res = json.loads(r)

    # Parse response
    bot_response = res["choices"][0]["message"]["content"] 

    st.session_state['messages'].append({"role": "assistant", "content": bot_response})

    return bot_response




st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Chat", "Knowledge base"])

# Page 1: Upload Document
if page == "Knowledge base":
    st.title("Upload a Text Document")

    # File uploader for text files
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"])

    if uploaded_file is not None:
        # Read the text file 
        file_content = uploaded_file.read().decode("utf-8")

        #this function helps to create chunks of text from the document
        document = load_document_and_chunk(file_content)

        # Each chunk of text is converted to an embedding format
        embedding = generate_embeddings(document)

        st.text_area("Embeddings generated succefully")


    else:
        st.write("Please upload a text file to build your knowledge base")




# Page 2: Chat Page
elif page == "Chat":
    st.title("Nebius Customer Assistant")


    collection = client.get_collection(name="net_test")



    # Initialise session state variables
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "system", "content":  system_message}
        ]
        

    st.sidebar.title("Sidebar")
    clear_button = st.sidebar.button("Clear Conversation", key="clear")

    if clear_button:
        st.session_state['generated'] = []
        st.session_state['past'] = []
        st.session_state['messages'] = [
            {"role": "system", "content": system_message}
        ]

    # container for chat history
    response_container = st.container()
    # container for text box

    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("You:", key='input', height=100)
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = generate_response(user_input)
            
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)
        

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))