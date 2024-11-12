import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

#load the environment variables
load_dotenv()

# Initialize ChromaD
client = chromadb.PersistentClient(path="chroma_db", settings=Settings())
collection = client.get_or_create_collection(name="net_test")


#net_test

#load the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2",cache_folder="embedding_tranform" )



# Function to split text into chunks of a specified maximum length
def chunk_text(text, max_length= 100):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_length += len(word) + 1  # Including a space
        if current_length > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = len(word) + 1
        current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

                 

def load_document_and_chunk(text):
    document_chunks = []
    try:
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            document_chunks.append({
                "content": chunk,
                "metadata": {"source": "flie" },
                "chunk_id": str(i)
            })
        return document_chunks
    except Exception as e:
        print(f"Error reading file: {e}")



def generate_embeddings(chunks):
    for chunk in chunks:
        embedding = embedding_model.encode(chunk["content"]).tolist()
        collection.add(
            documents=chunk["content"],
            embeddings= embedding,
            metadatas=chunk["metadata"],
            ids = chunk["chunk_id"]
        )
    print("Chunks embedded and stored in Chroma DB")

    return embedding



 










