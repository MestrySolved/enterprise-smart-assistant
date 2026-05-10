from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from langchain.docstore.document import Document

from langchain_google_genai import GoogleGenerativeAIEmbeddings


def create_vectorstore():

    with open("office_policy.txt", "r") as f:
        text = f.read()

    docs = [Document(page_content=text)]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore