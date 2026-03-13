from flask import Flask, request, render_template_string
from searcher import Searcher
import time

app = Flask(__name__)
searcher = Searcher()
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Search</title>
    <style>
    body {
            text-align: center;
            margin-top: 50px
        }
        .results {
            text-align: center;
            margin: 20px auto;
    </style>
    
</head>
<body>
    <h1>Zotgle</h1>
    <form action="/search" method="GET">
        <input type="Text" name="q" placeholder="Enter search query" value="{{ query }}">
        <button type="submit">Search</button>
    </form>
    {% if results is not none %}
        <div class="results">
        <p> Here are the top 5 results in {{time}} secs</p>
        {% for url,score in results %}
            <p> {{loop.index}}. <a href="{{ url }}">{{ url }}</a> (score: {{ score }})</p>
        {% endfor %}
        {% if not results %}
            <p> Found NO results</p>
        {% endif %}
        </div>
    {% endif %}
    
    </body>
    </html>
        
        
        
        
        
        
    """
@app.route("/")
def index():
    return render_template_string(HTML,query="", results=None, time=0)
@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return render_template_string(HTML)
    start = time.time()
    results = searcher.search(q)
    elapsed = f"{time.time() - start}"
    return render_template_string(HTML,query="", results=results, time=elapsed)
if __name__ == "__main__":
    app.run(debug=True)
#TO RUN THIS RUN THIS FILE AND IN YOUR BROWSER PASTE THIS
# http://127.0.0.1:5000