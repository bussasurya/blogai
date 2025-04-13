from scrape_blog import scrape_blog
from preprocess_text import preprocess_content

# Scrape a blog
test_url = "https://blog.python.org/"  # Replace with your preferred blog URL
blog_data = scrape_blog(test_url)

if blog_data:
    print(f"Title: {blog_data['title']}")
    print(f"Total content length: {len(blog_data['content'])} characters")
    
    # Preprocess the content
    chunks = preprocess_content(blog_data['content'], chunk_size=500)
    print(f"Created {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}: {chunk[:100]}... ({len(chunk.split())} words)")