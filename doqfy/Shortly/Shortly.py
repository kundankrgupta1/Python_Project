from flask import Flask, request, redirect, render_template
import hashlib

app = Flask(__name__)
url_db = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = hashlib.md5(original_url.encode()).hexdigest()[:6]
        url_db[short_url] = original_url
        return f"Short URL: {request.host}/{short_url}"
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    original_url = url_db.get(short_url)
    return redirect(original_url) if original_url else "URL not found"

if __name__ == '__main__':
    app.run(debug=True)
