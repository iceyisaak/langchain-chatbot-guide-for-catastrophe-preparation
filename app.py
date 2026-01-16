import os
from dotenv import load_dotenv

import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings



#############################################

st.title("Catastrophe Preparation Guide")
st.write("The Langchain Chatbot based on BBK.bund.de")


############################################

st.sidebar.title("Keys & Tokens")
groq_api_key=st.sidebar.text_input("Enter your Groq API Key: ",type="password")
hf_token=st.sidebar.text_input("Enter your HuggingFace Token: ",type="password")



############################################ 

prompt_template=ChatPromptTemplate.from_template(
    """
        Du bist ein hilfreicher Assistent für die Notfallvorsorge.
        Beantworte die Frage so präzise wie möglich anhand des bereitgestellten Kontextes.
        Wenn im Kontext Mengenangaben (wie Liter oder Tage) stehen, nenne diese explizit.

        Context: {context}
        Question: {input}
        Answer:
    """
)

############################################ UI


# llm=Ollama(model='gemma:2b')

if groq_api_key:
    llm = ChatGroq(api_key=groq_api_key, model_name="llama-3.1-8b-instant")

    def create_vector_embedding():
        if "vectors" not in st.session_state:
            # st.session_state.embeddings=OllamaEmbeddings(model="mxbai-embed-large")
            st.session_state.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            st.session_state.loader=PyPDFDirectoryLoader("./document")
            st.session_state.docs=st.session_state.loader.load()

            if not st.session_state.docs:
                st.error("No documents found in the ./document folder!")
                return
            
            st.session_state.text_splitter=RecursiveCharacterTextSplitter(
                chunk_size=1200,
                chunk_overlap=600,
                separators=["\n\n", "\n", ".", " ", ""]
            )
            st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs[:])
            st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)
            st.success("Vector Database Ready!")

    if "vectors" not in st.session_state:
        with st.spinner("Loading documents..."):
            create_vector_embedding()


    if "messages" not in st.session_state:

        st.session_state["messages"]=[{
            "role":"assistant",
            "content":"Hallo, ich helfe Ihnen gerne bei der Krisen- und Katastrophenvorsorge. Wie kann ich Ihnen helfen?"
        }]


    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])



    if prompt:=st.chat_input(placeholder="How do I keep myself prepared?"):
        st.session_state.messages.append({
            "role":"user",
            "content":prompt
        })
        st.chat_message("user").write(prompt)

        document_chain=create_stuff_documents_chain(llm,prompt_template)
        retriever=st.session_state.vectors.as_retriever(search_kwargs={"k": 5})
        retrieval_chain=create_retrieval_chain(retriever,document_chain)


        # Das zeigt Ihnen in Streamlit an, was der Bot wirklich "liest"
        # relevant_docs = retriever.invoke(prompt)
        # with st.expander("Gefundene Textstellen im PDF"):
        #     for doc in relevant_docs:
        #         st.write(doc.page_content)



        with st.chat_message("assistant"):
            response=retrieval_chain.invoke({'input':prompt})
            st.write(response['answer'])
            st.session_state.messages.append({
                "role":"assistant",
                "content":response['answer']
            })
