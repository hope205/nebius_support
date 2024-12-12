import chromadb,os,json
from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb.config import Settings
from openai import OpenAI
from dotenv import load_dotenv

#load the environment variables
load_dotenv()



#Custom embedding function
class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings: 
        # Initialize the OpenAI client with Nebius AI Studio's API endpoint and API key
        client = OpenAI(
        base_url="https://api.studio.nebius.ai/v1/",
        # Retrieve API key securely from environment variables
        api_key=os.getenv("NEBIUS_API_KEY") 
        )
        
        # Generate embeddings by calling the specified Nebius AI model
        embedding_response = client.embeddings.create(
            model="intfloat/e5-mistral-7b-instruct",
            input= input  # Pass the input documents to be embedded   
        )
        
        # Convert the response to JSON format
        embed_res = embedding_response.to_json()
        
         # Parse the JSON response to a Python dictionary
        r = json.loads(embed_res)
        
        embeddings = r['data'][0]['embedding']
        
        # Return the extracted embeddings
        return embeddings

# Create an instance of the custom embedding function
custom_embeddings= MyEmbeddingFunction()




# Initialize ChromaD
client = chromadb.PersistentClient(path="chroma_db", settings=Settings())
collection = client.get_or_create_collection(name="neb_data", embedding_function= custom_embeddings)




# Function to split text into chunks of a specified maximum length
def chunk_text(text, max_length= 512):    
    # Split the input text into a list of words
    words = text.split()
    # Initialize an empty list to store the resulting chunks
    chunks = []
    # Initialize an empty list to collect words for the current chunk
    current_chunk = []
    # Initialize a counter to track the length of the current chunk
    current_length = 0

    # Iterate over each word in the list of words
    for word in words:
        # Add the length of the word plus 1 to the current length
        current_length += len(word) + 1  # Including a space
        # If the current length exceeds the maximum allowed length
        if current_length > max_length:
            # Join the words in the current chunk into a string and add it to the list of chunks
            chunks.append(" ".join(current_chunk))
            
            # Reset the current chunk to start collecting new words
            current_chunk = []
            
            # Reset the current length to the length of the current word plus 1 (for the space)
            current_length = len(word) + 1
    
        # Add the current word to the current chunk
        current_chunk.append(word)
        

    # After the loop, if there are any remaining words in the current chunk, add them to the list of chunks
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks



# function to load a document and split it into manageable chunks
def load_document_and_chunk(text):
    # Initialize an empty list to store the document chunks
    document_chunks = []
    try:
        # Call the chunk_text function to split the input text into smaller chunks
        chunks = chunk_text(text)
        
        # Iterate through the chunks and create a dictionary for each chunk
        for i, chunk in enumerate(chunks):
            document_chunks.append({
                "content": chunk,            # Store the text content of the chunk
                "metadata": {"source": "file"},  # Add metadata indicating the source of the chunk
                "chunk_id": str(i)               # Assign a unique chunk ID (as a string) based on the index
            })
        
        # Return the list of document chunks
        return document_chunks

    # Handle any exceptions that occur during the chunking process
    except Exception as e:
	    #Print an error message if an exception occurs
        print(f"Error reading file: {e}") 
        


# This Function generates and store embeddings in a ChromaDB collection
def generate_embeddings(chunks):
    # Iterate over each chunk of data to process and store embeddings
    for chunk in chunks:
        collection.add(
            documents=chunk["content"],     # Adds the chunk's text content to the collection
            metadatas=chunk["metadata"],    # Attach metadata to the chunk (e.g., source info, tags)
            ids=chunk["chunk_id"]            # Assign a unique identifier to each chunk
        )
        print("Chunks embedded")             # Print confirmation for each chunk added

    # Print confirmation once all chunks have been stored in the collection
    print("Chunks stored in Chroma DB")