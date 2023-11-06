# import sys
# sys.path.append('server')

import os
import openai
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate

import api.appconfig as config

from api.endpoints.subjects.model import getSubjectById, updateSubject
from api.endpoints.documents.model import getAllDocuments
from api.endpoints.videos.model import getAllVideos

openai.api_key = os.getenv("OPENAI_API_KEY")

    
def documentQA(userId, subjectId, prompt):

    # Add prompt to history
    extendChatHistoryWithPrompt(userId, subjectId, prompt)
    
    
    chat_history = getConversationHistoryResources(userId, subjectId)
    urlList = getAllDocumentsOnSubject(userId, subjectId)
    documents = splitFiles(urlList)
    
    # IF NECESSARY
    vectordb = buildVectorstore(documents)
    
    # “higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic”
    pdf_qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo"),
        vectordb.as_retriever(search_kwargs={'k': 6}),
        return_source_documents=True,
        verbose=False
    )

    result = pdf_qa(
        {"question": prompt, "chat_history": chat_history})
    print(f"Answer: " + result["answer"])
    
    # add answer to history
    extendChatHistoryWithAnswer(prompt, result["answer"])

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
            loader = TextLoader(file)
            documents.extend(loader.load())
            
        #for mathematical pdfs, maybe try to convert to latex, then upload as latex, for better undestanding
    return documents
    
    
def splitDocuments(documents):
    textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    documents = textSplitter.split_documents(documents)
    return documents
    
    
def buildVectorstore(documents):
    vectordb = Chroma.from_documents(documents, embedding=OpenAIEmbeddings(), persist_directory=config.VECTORSTORE_PATH)
    vectordb.persist()
    return vectordb



def extendChatHistoryWithPrompt(userId, subjectId, prompt):
    hist = getConversationHistoryResources(userId, subjectId)
    hist.append([prompt, ""])
    updateSubject(userId, subjectId, conversationHistoryDocs=hist)
    

def extendChatHistoryWithAnswer(userId, subjectId, answer):
    hist = getConversationHistoryResources(userId, subjectId)
    hist[-1][1] = answer
    updateSubject(userId, subjectId, conversationHistoryDocs=hist)


def clearConversationHistoryResources(userId, subjectId):
    updateSubject(userId, subjectId, conversationHistoryDocs=[])

def clearConversationHistoryGeneral(userId, subjectId):
    updateSubject(userId, subjectId, conversationHistoryGeneral=[])
    
def getConversationHistoryResources(userId, subjectId):
    subject = getSubjectById(userId, subjectId)
    if not subject:
        return []
    return subject["conversationHistoryDocs"]

def getConversationHistoryGeneral(userId, subjectId):
    subject = getSubjectById(userId, subjectId)
    if not subject:
        return []
    return subject["conversationHistoryGeneral"]