import requests
from bs4 import BeautifulSoup

def scrape_blog(url):
    try:
        # Fetch the blog page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.find('title').text if soup.find('title') else 'No title found'
        
        # Extract main content (assuming paragraphs)
        content = ' '.join(p.text.strip() for p in soup.find_all('p'))
        if not content:
            content = 'No content found'
        
        return {
            'url': url,
            'title': title,
            'content': content
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Test the function
if __name__ == "__main__":
    test_url = "https://blog.python.org/"  # Replace with a real blog URL for testing
    blog_data = scrape_blog(test_url)
    if blog_data:
        print(f"URL: {blog_data['url']}")
        print(f"Title: {blog_data['title']}")
        print(f"Content: {blog_data['content'][:200]}...")  # Print first 200 chars