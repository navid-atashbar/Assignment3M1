from flask import Flask, request, render_template_string
from searcher import Searcher
import time

app = Flask(__name__)
searcher = Searcher()
HTML = """
<!DOCTYPE html>
<html lang="en">
<head><title>Search</title></head>
<body>
    <h1>Search</h1>
    <form action="/search" method="GET">
        <input type="Text" value="Search">"""