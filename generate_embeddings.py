from sentence_transformers import SentenceTransformer
import numpy as np

def generate_embeddings(chunks):
    """
    Convert text chunks into vector embeddings.
    :param chunks: List of text chunks.
    :return: Numpy array of embeddings.
    """
    try:
        # Load a lightweight embedding model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Generate embeddings
        embeddings = model.encode(chunks, convert_to_numpy=True)
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None

# Test the function
if __name__ == "__main__":
    # Sample chunks (replace with real chunks later)
    sample_chunks = [
        "This is a sample chunk about Python programming.",
        "Python is great for data science and automation.",
        "Learn Python with simple syntax and powerful libraries."
    ]
    
    embeddings = generate_embeddings(sample_chunks)
    if embeddings is not None:
        print(f"Generated {len(embeddings)} embeddings:")
        print(f"Embedding shape: {embeddings.shape}")
        print(f"First embedding (first 5 values): {embeddings[0][:5]}")