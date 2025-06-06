from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# print("Docs[0]", docs[5])

#chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

split_docs=text_splitter.split_documents(documents=docs)

#Vector emb

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)
## using embedding model create embedding of split docs

vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name = "learning_vectors",
    embedding=embedding_model
)

print("Indexing done")