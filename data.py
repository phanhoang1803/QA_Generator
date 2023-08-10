from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
# from langchain.document_loaders import PyPDFLoader
import pickle
import models

def embed(courseID):
    # loader = PyPDFLoader("/content/data/course1/VietAI_system_research.pdf")
    # docs = loader.load_and_split()

    # Load data from directory
    loader = DirectoryLoader('data/course' + str(courseID), glob="**/*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()

    # Splitting data into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 20)
    all_splits = text_splitter.split_documents(docs)

    # Embedding
    vectorstore = FAISS.from_documents(documents=all_splits, embedding=models.Embeddings.load_embeddings())

    # Storing
    with open(f"vectorstores/course{str(courseID)}.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

def load_vectorstore(courseID):
    # Load vectorstore from disk
    with open(f"vectorstores/course{str(courseID)}.pkl", "rb") as f:
        vectorstore = pickle.load(f)

    return vectorstore
    
def embed_and_get_vectorstore(courseID, pdf_path = None):
    # Load data from directory
    if pdf_path == None:
        loader = PyPDFLoader(file_path=pdf_path)
    else:
        loader = DirectoryLoader('data/course' + str(courseID), glob="**/*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    
    # Splitting data into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 20)
    all_splits = text_splitter.split_documents(docs)
    
    # Embedding
    vectorstore = FAISS.from_documents(documents=all_splits, embedding=models.Embeddings.load_embeddings())
    
    return vectorstore