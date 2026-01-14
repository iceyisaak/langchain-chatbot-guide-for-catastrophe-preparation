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



#############################################

st.title("Catastrophe Preparation Guide")
st.write("The Langchain Chatbot based on BBK.bund.de")



############################################ 

prompt_template=ChatPromptTemplate.from_template(
    """
        Sie sind Experte für Notfallvorsorge.

        Nutzen Sie den folgenden Kontext, um die Frage des Nutzers zu beantworten.

        Sollte die Antwort nicht im Kontext enthalten sein, teilen Sie ihm mit, dass Sie es anhand der Dokumente nicht wissen, und erfinden Sie nichts.

        Context: {context}
        Question: {input}
        Answer:
   
    """
)

############################################ UI


llm=Ollama(model='gemma:2b')

def create_vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings=OllamaEmbeddings()
        st.session_state.loader=PyPDFDirectoryLoader("./document")
        st.session_state.docs=st.session_state.loader.load()

        if not st.session_state.docs:
            st.error("No documents found in the ./document folder!")
            return
        
        st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
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
    retriever=st.session_state.vectors.as_retriever(search_kwargs={"k": 7})
    retrieval_chain=create_retrieval_chain(retriever,document_chain)

    with st.chat_message("assistant"):
        response=retrieval_chain.invoke({'input':prompt})
        st.write(response['answer'])
        st.session_state.messages.append({
            "role":"assistant",
            "content":response['answer']
        })
