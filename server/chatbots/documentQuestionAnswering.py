import sys
sys.path.append('server')

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

import appconfig as config

openai.api_key = os.getenv("OPENAI_API_KEY")


# get all the doc urls of subject and build vectorStore
testDocList = [
    "https://storage.googleapis.com/aitutor-e6db8.appspot.com/documents/documents_ML_HypotheseTests_DanielSchafh%C3%A4utle%20(2)%20(2).pdf",
    "https://storage.googleapis.com/aitutor-e6db8.appspot.com/documentsHypothesisTesting_HANDOUT.pdf"
]

    
def documentQA(userId, subjectId, prompt):
    
    chat_history = getChatHistory(userId, subjectId)
    # get User, clear chat history, if he has one on the subject already, evtl in the future, not its a F E A T U R E
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
    
    
    extendChatHistory(prompt, result["answer"])


def getAllDocumentsOnSubject(userId, subjectId):
    return ["url1", "url2", "...."]

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
    return documents
    
    
def splitDocuments(documents):
    textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    documents = textSplitter.split_documents(documents)
    return documents
    
    
def buildVectorstore(documents):
    vectordb = Chroma.from_documents(documents, embedding=OpenAIEmbeddings(), persist_directory=config.VECTORSTORE_PATH)
    vectordb.persist()
    return vectordb



def getChatHistory(userId, subjectId):
    pass


def extendChatHistory(prompt, answer):

    pass



def clearConversationHistory():
    pass