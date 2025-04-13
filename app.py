from flask import Flask, request, render_template
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import mysql.connector
from transformers import pipeline
from scrape_blog import scrape_blog
from preprocess_text import preprocess_content
from generate_embeddings import generate_embeddings
from store_faiss import store_in_faiss
import os

app = Flask(__name__)

# MySQL config
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'tenalirk',  # Replace with your MySQL password
    'database': 'blog_tool'
}
index_file = "blog_index.faiss"

def clear_data():
    """Clear MySQL table and FAISS index."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE blogs")
        conn.commit()
    except Exception as e:
        print(f"Error clearing MySQL: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    if os.path.exists(index_file):
        os.remove(index_file)

def process_url(url):
    """Scrape, preprocess, embed, and store data for a URL."""
    try:
        blog_data = scrape_blog(url)
        if not blog_data:
            return False
        chunks = preprocess_content(blog_data['content'], chunk_size=500)
        embeddings = generate_embeddings(chunks)
        if embeddings is None:
            return False
        index = store_in_faiss(embeddings, index_file)
        if not index:
            return False
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            for i, chunk in enumerate(chunks):
                chunk_id = f"{blog_data['url']}_chunk_{i}"
                cursor.execute(
                    """
                    INSERT INTO blogs (url, title, chunk_id, content, faiss_index)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (blog_data['url'], blog_data['title'], chunk_id, chunk, i)
                )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error storing in MySQL: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    except Exception as e:
        print(f"Error processing URL: {e}")
        return False

def retrieve_answer(question, index_file, db_config, top_k=2):
    """Retrieve relevant chunks for a question."""
    conn = None
    cursor = None
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
    """Generate an answer using the QA model."""
    try:
        qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')
        combined_context = " ".join(contexts)[:512]
        result = qa_pipeline(question=question, context=combined_context)
        return result['answer']
    except Exception as e:
        print(f"Error generating LLM answer: {e}")
        return "Sorry, I couldn't generate an answer."

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    chunks = None
    question = None
    url = None
    error = None
    if request.method == 'POST':
        question = request.form.get('question')
        url = request.form.get('url')
        if url:
            clear_data()
            if not process_url(url):
                error = "Failed to process the provided URL."
        if question and not error:
            if os.path.exists(index_file):
                results = retrieve_answer(question, index_file, db_config, top_k=2)
                if results:
                    contexts = [result['content'] for result in results]
                    chunks = [context[:200] + "..." for context in contexts]
                    answer = generate_llm_answer(question, contexts)
                else:
                    answer = "No relevant information found."
            else:
                answer = "No data available. Please provide a URL to process."
    return render_template('index.html', question=question, answer=answer, chunks=chunks, url=url, error=error)

if __name__ == '__main__':
    app.run(debug=True)