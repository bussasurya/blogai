import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import mysql.connector

def retrieve_answer(question, index_file, db_config, top_k=1):
    """
    Retrieve relevant chunks for a question using FAISS and MySQL.
    :param question: User's question (string).
    :param index_file: Path to FAISS index.
    :param db_config: MySQL connection details.
    :param top_k: Number of chunks to retrieve.
    :return: List of relevant chunks with metadata.
    """
    try:
        # Load embedding model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Convert question to embedding
        question_embedding = model.encode([question], convert_to_numpy=True)
        
        # Load FAISS index
        index = faiss.read_index(index_file)
        
        # Search for top_k similar chunks
        distances, indices = index.search(question_embedding, top_k)
        
        # Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Retrieve chunk content from MySQL
        results = []
        for idx in indices[0]:
            cursor.execute(
                """
                SELECT url, title, chunk_id, content
                FROM blogs
                WHERE faiss_index = %s
                """,
                (int(idx),)
            )
            row = cursor.fetchone()
            if row:
                results.append({
                    'url': row[0],
                    'title': row[1],
                    'chunk_id': row[2],
                    'content': row[3]
                })
        
        print(f"Retrieved {len(results)} chunks for question: {question}")
        return results
    except Exception as e:
        print(f"Error retrieving answer: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Test the function with user input
if __name__ == "__main__":
    # MySQL config
    db_config = {
        'host': 'localhost',
        'user': 'root',  # Replace with your MySQL username
        'password': 'tenalirk',  # Replace with your MySQL password
        'database': 'blog_tool'
    }
    
    # Prompt for user input
    index_file = "blog_index.faiss"
    while True:
        question = input("Enter your question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            print("Exiting...")
            break
        
        if not question.strip():
            print("Please enter a valid question.")
            continue
        
        results = retrieve_answer(question, index_file, db_config, top_k=1)
        if results:
            for result in results:
                print(f"URL: {result['url']}")
                print(f"Title: {result['title']}")
                print(f"Chunk ID: {result['chunk_id']}")
                print(f"Content: {result['content'][:200]}...")  # Preview
        print("-" * 50)