import mysql.connector
from scrape_blog import scrape_blog
from preprocess_text import preprocess_content
from generate_embeddings import generate_embeddings
from store_faiss import store_in_faiss

# MySQL config
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'tenalirk',  # Replace with your MySQL password
    'database': 'blog_tool'
}

# Scrape, preprocess, embed, and store
test_url = "https://en.wikipedia.org/wiki/Hindustan_Times"
blog_data = scrape_blog(test_url)
if blog_data:
    print(f"Title: {blog_data['title']}")
    print(f"Total content length: {len(blog_data['content'])} characters")
    
    # Preprocess into chunks
    chunks = preprocess_content(blog_data['content'], chunk_size=500)
    print(f"Created {len(chunks)} chunks")
    
    # Generate embeddings
    embeddings = generate_embeddings(chunks)
    if embeddings is not None:
        print(f"Generated {len(embeddings)} embeddings")
        
        # Store in FAISS and get indices
        index = store_in_faiss(embeddings, 'blog_index.faiss')
        if index:
            print(f"Stored {index.ntotal} embeddings in FAISS")
        
        # Store in MySQL with FAISS index
        chunk_ids = []
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
                chunk_ids.append(chunk_id)
            conn.commit()
            print(f"Stored {len(chunk_ids)} chunks in MySQL")
        except Exception as e:
            print(f"Error storing in MySQL: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()