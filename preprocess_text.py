def preprocess_content(content, chunk_size=500):
    """
    Clean and split content into chunks.
    :param content: Raw text from blog.
    :param chunk_size: Approx. number of words per chunk.
    :return: List of text chunks.
    """
    # Remove extra whitespace and newlines
    content = ' '.join(content.split())
    
    # Split into words
    words = content.split()
    
    # Create chunks of roughly chunk_size words
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

# Test the function
if __name__ == "__main__":
    # Sample content (replace with real blog content later)
    sample_content = """
    This is a sample blog post about Python programming. Python is a versatile language
    used for web development, data science, and automation. It has a simple syntax
    that makes it easy to learn. In this post, we will explore Python's features and
    benefits for beginners and experts alike.
    """ * 10  # Make it longer for testing
    
    chunks = preprocess_content(sample_content)
    print(f"Created {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}: {chunk[:100]}... ({len(chunk.split())} words)")