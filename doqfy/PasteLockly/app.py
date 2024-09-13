# app.py
from flask import Flask, request, redirect, url_for, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import base64
import binascii

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snippets.db'
db = SQLAlchemy(app)

class Snippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=True)
    content = db.Column(db.LargeBinary, nullable=False)

def generate_key():
    return Fernet.generate_key()

def encrypt_content(content, key):
    fernet = Fernet(key)
    return fernet.encrypt(content.encode())

def decrypt_content(encrypted_content, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_content).decode()

def is_valid_key(key):
    try:
        base64.urlsafe_b64decode(key)
        return True
    except (TypeError, binascii.Error):
        return False

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        content = request.form['content']
        secret_key = request.form.get('secret_key')

        if secret_key:
            if not is_valid_key(secret_key):
                return "Invalid secret key format", 400
            key = secret_key.encode()
        else:
            key = generate_key()

        encrypted_content = encrypt_content(content, key) if key else content.encode()

        snippet = Snippet(content=encrypted_content, key=key.decode() if key else None)
        db.session.add(snippet)
        db.session.commit()

        # Return the snippet ID and key if provided
        return render_template('snippet_created.html', snippet_id=snippet.id, key=key.decode() if key else None)

    return render_template('home.html')

@app.route('/snippet/<int:snippet_id>', methods=['GET', 'POST'])
def view_snippet(snippet_id):
    snippet = Snippet.query.get_or_404(snippet_id)

    if request.method == 'POST':
        secret_key = request.form['secret_key'].encode()

        if snippet.key and secret_key != snippet.key.encode():
            abort(403)  # Forbidden

        try:
            content = decrypt_content(snippet.content, secret_key)
        except Exception as e:
            print(f"Decryption Error: {e}")
            abort(403)  # Forbidden

        return render_template('snippet.html', content=content)

    return render_template('snippet.html', content=None)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
