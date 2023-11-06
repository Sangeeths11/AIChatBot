# import sys
# sys.path.append('server')

import os
import openai
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
import chromadb
import api.appconfig as config

from api.endpoints.subjects.model import getSubjectById, updateSubject
from api.endpoints.documents.model import getAllDocuments
from api.endpoints.videos.model import getAllVideos

openai.api_key = os.getenv("OPENAI_API_KEY")
import requests
from itertools import zip_longest
import uuid


chromaClient = chromadb.PersistentClient(path=config.VECTORSTORE_PATH)

    
def documentQA(userId, subjectId, prompt):
    if prompt.lower() == "clear":
        clearConversationHistoryResources(userId, subjectId)
        return {"question": prompt, "answer": "Chat history cleared"}


    # Add prompt to history
    extendChatHistoryWithPrompt(userId, subjectId, prompt)
    
    
    questions, answers = getConversationHistoryResources(userId, subjectId)
    chat_history = assembleList(questions, answers)
    
    urlList = getAllDocumentsOnSubject(userId, subjectId)
    documents = splitFiles(urlList)
    
    # IF NECESSARY
    #vectordb = getOrCreateVectorstore(subjectId, documents)
    vectordb = buildVectorstore(documents, userId, subjectId)
    
    # “higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic”
    qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=0.8, model_name="gpt-4"),
        vectordb.as_retriever(search_kwargs={'k': 6}),
        return_source_documents=True,
        verbose=True,
        handle_parsing_errors=True
    )

    result = qa({"question": prompt, "chat_history": chat_history})
    
    # add answer to history
    extendChatHistoryWithAnswer(userId, subjectId, result["answer"])
    
    return {"question": prompt, "answer": result["answer"]}

# Gets all the urls for documents and videos on the subject
def getAllDocumentsOnSubject(userId, subjectId):
    docs = getAllDocuments(userId, subjectId)
    videos = getAllVideos(userId, subjectId)
    docUrls = [doc["url"] for doc in docs]
    videoUrls = [video["transcriptUrl"] for video in videos]
    urlList = docUrls + videoUrls
    return urlList

def splitFiles(urlList):
    documents = []
    for file in urlList:
        if file.endswith(".pdf"):
            loader = PyPDFLoader(file)
            documents.extend(loader.load())
        elif file.endswith('.docx') or file.endswith('.doc'):
            loader = Docx2txtLoader(file)
            documents.extend(loader.load())
        elif file.endswith('.txt'):
            loader = UnstructuredURLLoader([file])
            documents.extend(loader.load())
            
    return documents
    
    
def splitDocuments(documents):
    textSplitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=30)
    documents = textSplitter.split_documents(documents)
    return documents
    
    
def buildVectorstore(documents, userId, subjectId):
    vectordb = Chroma.from_documents(documents, embedding=OpenAIEmbeddings(), persist_directory=f'{config.VECTORSTORE_PATH}{userId}/{subjectId}/')
    vectordb.persist()
    return vectordb 


# def getOrCreateVectorstore(name, documents):
#     collection = chromaClient.get_or_create_collection(name=name)
#     for doc in documents:
#         uuid_name = uuid.uuid1()
#         collection.upsert(ids=[str(uuid_name)], documents=doc.page_content)
#     return collection


def extendChatHistoryWithPrompt(userId, subjectId, prompt):
    questions, answers = getConversationHistoryResources(userId, subjectId)
    questions.append(prompt)
    updateSubject(userId, subjectId, conversationHistoryDocsQuestions=questions)
    

def extendChatHistoryWithAnswer(userId, subjectId, answer):
    questions, answers = getConversationHistoryResources(userId, subjectId)
    answers.append(answer)
    updateSubject(userId, subjectId, conversationHistoryDocsAnswers=answers)


def clearConversationHistoryResources(userId, subjectId):
    updateSubject(userId, subjectId, conversationHistoryDocsAnswers=[], conversationHistoryDocsQuestions=[])

    
def getConversationHistoryResources(userId, subjectId):
    subject = getSubjectById(userId, subjectId)
    if not subject:
        return [], []
    return subject.get("conversationHistoryDocsQuestions", []), subject.get("conversationHistoryDocsAnswers", [])


def assembleList(questions, answers):
    return list(zip_longest(questions, answers, fillvalue=""))


