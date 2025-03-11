import sqlite3
import os
import string
import secrets
import re

# Get the values from the environment variables
host = os.getenv("HOST", "127.0.0.1")  # Default to 127.0.0.1 if HOST is not found
port = int(os.getenv("PORT", 8000))    # Default to 8000 if PORT is not found

def create_db():
    # First ensure any existing connection is closed
    """Create database and tables."""
    # Cleanup code is still helpful for robustness
    if os.path.exists("mydatabase.db"):
        os.remove("mydatabase.db")
    
    conn = sqlite3.connect("mydatabase.db", check_same_thread=False)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE url_map (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        long_url TEXT,
        short_url TEXT,
        clicks BIGINT
    );
    ''')
    
    cursor.execute('''CREATE INDEX idx_short_url ON url_map(short_url);''')
    cursor.execute('''CREATE INDEX idx_long_url ON url_map(long_url);''')
    
    conn.commit()
    return conn

# Function to check if the URL structure is valid
def is_valid_url(url):
    # Regular expression for URL validation
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ... or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ... or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None

# Function to generate a random string
def generate_random_string():
    return ''.join(secrets.choice(string.ascii_letters) for _ in range(5)).lower()

def db_insert(long_url, db_connection):

    if not is_valid_url(long_url):
        return(f"The URL {long_url} is invalid.")

    cursor = db_connection.cursor()

    # check that the long_url hasn't been mapped (to prevent having multiple short_urls mapped to same long_url)
    cursor.execute("SELECT short_url FROM url_map WHERE long_url = ?", (long_url,))
    result = cursor.fetchone()

    if result:
        return f"http://{host}:{port}/{result[0]}"
    # Generate a random string
    random_string = generate_random_string()

    # Check if the random string already exists in the database
    cursor.execute('SELECT COUNT(*) FROM url_map WHERE short_url = ?', (random_string,))
    count = cursor.fetchone()[0]

    # If the random string exists, generate a new one
    while count > 0:
        random_string = generate_random_string()
        cursor.execute('SELECT COUNT(*) FROM url_map WHERE short_url = ?', (random_string,))
        count = cursor.fetchone()[0]

    # Now insert the new random string, ensuring it's unique
    cursor.execute('''
        INSERT INTO url_map (long_url, short_url, clicks)
        VALUES (?, ?, ?)
    ''', (long_url, random_string, 0))

    # Commit the changes to the database
    db_connection.commit()

    return f"http://{host}:{port}/{random_string}"

def find_long_url(short_url, db_connection):
    cursor = db_connection.cursor()

    try:
        # Query to check if the short_url exists in the table
        cursor.execute("SELECT long_url FROM url_map WHERE short_url = ?", (short_url,))
        result = cursor.fetchone()

        # If result is found, increment clicks and return the long_url
        if result:
            # Extract long_url and clicks count from the result
            long_url = result[0]

            return long_url  # Return the long_url after incrementing clicks
        else:
            return "Short URL not found"  # Or return None 
    
    except sqlite3.Error as e:
        # Handle database errors
        return f"An error occurred: {e}"
    
def increment_clicks(short_url, db_connection):
    cursor = db_connection.cursor()

    try:
        # Query to check if the short_url exists in the table
        cursor.execute("SELECT clicks FROM url_map WHERE short_url = ?", (short_url,))
        result = cursor.fetchone()

        # If result is found, increment clicks
        if result:
            clicks = result[0]
            new_clicks = clicks + 1

            # Update the clicks count in the database
            cursor.execute("UPDATE url_map SET clicks = ? WHERE short_url = ?", (new_clicks, short_url))
            db_connection.commit()  # Commit the changes

        else:
            return "Short URL not found"  # Or return None 

    except sqlite3.Error as e:
        # Handle database errors
        return f"An error occurred: {e}"


    
def get_url_map(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("SELECT long_url, short_url, clicks FROM url_map")
    results = cursor.fetchall()

    # Convert the results to a more readable format
    url_map = []
    for long_url, short_url, clicks in results:
        url_map.append({
            'long_url': long_url,
            'short_url': short_url,
            'clicks': clicks
        })

    return url_map






