import faiss
import numpy as np

def store_in_faiss(embeddings, index_file='blog_index.faiss'):
    """
    Store embeddings in a FAISS index.
    :param embeddings: Numpy array of embeddings.
    :param index_file: File to save the FAISS index.
    :return: FAISS index object.
    """
    try:
        # Get embedding dimension
        dimension = embeddings.shape[1]
        
        # Create a FAISS index (L2 distance)
        index = faiss.IndexFlatL2(dimension)
        
        # Add embeddings to the index
        index.add(embeddings)
        
        # Save the index to disk
        faiss.write_index(index, index_file)
        print(f"Saved FAISS index with {index.ntotal} embeddings to {index_file}")
        
        return index
    except Exception as e:
        print(f"Error storing in FAISS: {e}")
        return None

# Test the function
if __name__ == "__main__":
    # Sample embeddings (replace with real embeddings later)
    sample_embeddings = np.array([
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
        [0.7, 0.8, 0.9]
    ], dtype=np.float32)
    
    index = store_in_faiss(sample_embeddings, 'test_index.faiss')
    if index:
        print(f"FAISS index contains {index.ntotal} embeddings")