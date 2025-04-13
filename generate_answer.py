import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import mysql.connector
from transformers import pipeline

def retrieve_answer(question, index_file, db_config, top_k=2):
    """
    Retrieve relevant chunks for a question using FAISS and MySQL.
    """
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        question_embedding = model.encode([question], convert_to_numpy=True)
        index = faiss.read_index(index_file)
        distances, indices = index.search(question_embedding, top_k)
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
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

def generate_llm_answer(question, contexts):
    """
    Generate a concise answer using a QA model based on retrieved contexts.
    :param question: User's question.
    :param contexts: List of retrieved chunk texts.
    :return: Generated answer string.
    """
    try:
        # Load QA model
        qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')
        
        # Combine contexts (truncate to avoid token limit)
        combined_context = " ".join(contexts)[:512]
        
        # Run QA
        result = qa_pipeline(question=question, context=combined_context)
        answer = result['answer']
        
        return answer
    except Exception as e:
        print(f"Error generating LLM answer: {e}")
        return "Sorry, I couldn't generate an answer."

# Test the functions with user input
if __name__ == "__main__":
    # MySQL config
    db_config = {
        'host': 'localhost',
        'user': 'root',  # Replace with your MySQL username
        'password': 'tenalirk',  # Replace with your MySQL password
        'database': 'blog_tool'
    }
    
    # FAISS index file
    index_file = "blog_index.faiss"
    
    while True:
        question = input("Enter your question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            print("Exiting...")
            break
        
        if not question.strip():
            print("Please enter a valid question.")
            continue
        
        # Retrieve relevant chunks
        results = retrieve_answer(question, index_file, db_config, top_k=2)
        if results:
            # Collect all contexts
            contexts = [result['content'] for result in results]
            print(f"Retrieved Chunks:")
            for i, context in enumerate(contexts):
                print(f"Chunk {i}: {context[:200]}...")
            
            # Generate LLM answer
            answer = generate_llm_answer(question, contexts)
            print(f"Question: {question}")
            print(f"Answer: {answer}")
        else:
            print("No relevant chunks found.")
        print("-" * 50)