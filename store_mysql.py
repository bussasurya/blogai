import mysql.connector

def store_metadata(blog_data, chunks, db_config):
    """
    Store blog metadata and chunks in MySQL.
    :param blog_data: Dict with url, title, content.
    :param chunks: List of text chunks.
    :param db_config: Dict with MySQL connection details.
    :return: List of stored chunk IDs.
    """
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Insert each chunk with metadata
        chunk_ids = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"{blog_data['url']}_chunk_{i}"
            try:
                cursor.execute(
                    """
                    INSERT INTO blogs (url, title, chunk_id, content)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (blog_data['url'], blog_data['title'], chunk_id, chunk)
                )
                chunk_ids.append(chunk_id)
            except mysql.connector.Error as e:
                print(f"Skipping chunk {chunk_id}: {e}")
                continue
        
        # Commit and close
        conn.commit()
        print(f"Stored {len(chunk_ids)} chunks in MySQL for {blog_data['url']}")
        return chunk_ids
    except Exception as e:
        print(f"Error storing in MySQL: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Test the function
if __name__ == "__main__":
    # Sample blog data and chunks
    sample_blog_data = {
        'url': 'https://en.wikipedia.org/wiki/Hindustan_Times',
        'title': 'Hindustan Times Wiki',
        'content': 'This is sample content.'
    }
    sample_chunks = [
        'This is the first chunk.',
        'This is the second chunk.'
    ]
    
    # MySQL connection config
    db_config = {
        'host': 'localhost',
        'user': 'root',  # Replace with your MySQL username (e.g., 'root')
        'password': 'tenalirk',  # Replace with your MySQL password
        'database': 'blog_tool'
    }
    
    chunk_ids = store_metadata(sample_blog_data, sample_chunks, db_config)
    if chunk_ids:
        print(f"Stored chunk IDs: {chunk_ids}")