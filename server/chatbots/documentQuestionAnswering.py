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
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate

import appconfig as config

openai.api_key = os.getenv("OPENAI_API_KEY")

testDocList = [
    "https://storage.googleapis.com/aitutor-e6db8.appspot.com/documents/documents_ML_HypotheseTests_DanielSchafh%C3%A4utle%20(2)%20(2).pdf",
    "https://storage.googleapis.com/aitutor-e6db8.appspot.com/documentsHypothesisTesting_HANDOUT.pdf"
]

# def load_doc(file):
#     loader=PyPDFLoader(file)
#     pages  = loader.load_and_split()
#     #print("pages", pages)
#     return loader.load()
    


# def main():
#     data=load_doc('https://storage.googleapis.com/aitutor-e6db8.appspot.com/documents/documents_ML_HypotheseTests_DanielSchafh%C3%A4utle%20(2)%20(2).pdf')
#     #print(data[1].page_content)
#     print(data[1].metadata)
#     print(f'you have {len(data)} pages in your data')
#     print(f'there are {len(data[1].page_content)} characters in the page')



# if __name__ == "__main__":
#     main()
    
    

documents = []
for file in testDocList:
    if file.endswith(".pdf"):
        #pdf_path = "./docs/" + file
        loader = PyPDFLoader(file)
        documents.extend(loader.load())
    elif file.endswith('.docx') or file.endswith('.doc'):
        doc_path = "./docs/" + file
        loader = Docx2txtLoader(doc_path)
        documents.extend(loader.load())
    elif file.endswith('.txt'):
        text_path = "./docs/" + file
        loader = TextLoader(text_path)
        documents.extend(loader.load())

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
documents = text_splitter.split_documents(documents)

vectordb = Chroma.from_documents(documents, embedding=OpenAIEmbeddings(), persist_directory=config.VECTORSTORE_PATH)
vectordb.persist()

pdf_qa = ConversationalRetrievalChain.from_llm(
    ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo"),
    vectordb.as_retriever(search_kwargs={'k': 6}),
    return_source_documents=True,
    verbose=False
)

yellow = "\033[0;33m"
green = "\033[0;32m"
white = "\033[0;39m"

chat_history = []
print(f"{yellow}---------------------------------------------------------------------------------")
print('Welcome to the DocBot. You are now ready to start interacting with your documents')
print('---------------------------------------------------------------------------------')
while True:
    query = input(f"{green}Prompt: ")
    if query == "exit" or query == "quit" or query == "q" or query == "f":
        print('Exiting')
        sys.exit()
    if query == '':
        continue
    result = pdf_qa(
        {"question": query, "chat_history": chat_history})
    print(f"{white}Answer: " + result["answer"])
    chat_history.append((query, result["answer"]))
    