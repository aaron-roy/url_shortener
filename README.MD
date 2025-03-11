Http Server that allows the Client to send a URL to be shortened.
```
url_shortener/
├── main.py
├── utils.py
├── test.py
```

### Overview of Files
- main.py: Initializes the FastAPI application and defines the API endpoints to shorten a url, obtain the url a short url is mapped to, and get all which retreives all the links and their click counter
- utils.py: Helper methods which are called in main.py. Most methods connect to SQLite3 db instance and are inserting and retrieving valeus from the DB.
- test.py: A file to run to easily shorten URLs and see click counter live

### Installation and Set Up 
1. **Clone the repository:**
   ```bash
   git clone git@github.com:aaron-roy/url_shortener.git
   cd url_shortener
   ```
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
### Running the Code 
1. **Start up FastAPI server DB with Uvicorn and SQLite3:**
   ```bash
   python3 main.py
   ```
### Testing the Code 
1. **Run Test Script:**
   ```bash
   python3 test.py
   ```
