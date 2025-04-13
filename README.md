
# Blog Q&A System

A web-based Q&A system that allows users to input a URL (e.g., a Wikipedia page) and ask questions about its content. The system scrapes the webpage, processes the text, stores it in a MySQL database and FAISS index, and uses a DistilBERT LLM (Large Language Model) for question-answering. Built with Flask for the UI, Python for backend processing, and MySQL for storage.

## Features
- **Dynamic URL Processing**: Enter any URL (e.g., `https://en.wikipedia.org/wiki/Wikimedia_Foundation`), and the system scrapes and indexes its content.
- **Question Answering**: Ask questions (e.g., "When was Wikipedia formed?"), and get precise answers using the DistilBERT LLM.
- **Database Storage**: Content is chunked and stored in a MySQL database with metadata (URL, title, chunk ID).
- **Vector Search**: Uses FAISS for efficient retrieval of relevant content based on question embeddings.
- **Flask UI**: Simple web interface to input URLs and questions, displaying answers and retrieved chunks.

## Project Structure
blogai/
├── venv/                    # Virtual environment
├── templates/
│   └── index.html           # Flask UI template
├── app.py                   # Main Flask application with LLM integration
├── scrape_blog.py           # Web scraping logic
├── preprocess_text.py       # Text chunking logic
├── generate_embeddings.py   # Embedding generation with SentenceTransformer
├── store_faiss.py           # FAISS index storage
├── test_full_pipeline.py    # Pipeline for testing scraping to storage
├── blog_index.faiss         # FAISS index (generated)
└── README.md                # This file

## Prerequisites
- Python 3.8+
- MySQL Server (e.g., MySQL Community Server)
- Git
- A web browser (e.g., Chrome, Firefox)

## Setup Instructions

### 1. Clone the Repository:
git clone https://github.com/<your-username>/blogai.git
cd blogai

### 2. Create and Activate a Virtual Environment:
python -m venv venv
.
env\Scripts ctivate  # Windows
# source venv/bin/activate  # Linux/Mac

### 3. Install Dependencies:
pip install flask sentence-transformers faiss-cpu mysql-connector-python transformers

### 4. Set Up MySQL Database:
Install MySQL if not already installed. Then log in to MySQL:
mysql -u root -p

Create a database:
CREATE DATABASE blog_tool;

### 5. Update `app.py` with Your MySQL Credentials:
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'blog_tool'
}
