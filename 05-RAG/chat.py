from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
load_dotenv()
#Take user query
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
     url="http://localhost:6333",
    collection_name = "learning_vectors",
    embedding=embedding_model
)

query = input(">")

#vector similarity search in db

search_result = vector_db.similarity_search(
    query=query
)

print("Search Result", search_result)

context = "\n\n".join([f"Page Content : {result.get("metadata").get("page_content")}\nPage Number: f{result.metadata.page_label}\nFile Location: {result.get("metadata").get("source")}" for result in search_result])

SYSTEM_PROMPT = f"""You are helpful AI assistant who answer query based on available content 
recieved from pdf file along with page_contents and page number.

You should only answer the user based on the following context and navigate the user
to open the right page number to know more.

Context:
{context}
"""

print(SYSTEM_PROMPT)