from flask import Flask, jsonify, render_template
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    data = r.get('nifty50_data')
    if data:
        data = eval(data.decode('utf-8'))
    return render_template('index.html', data=data)

@app.route('/api/data')
def get_data():
    data = r.get('nifty50_data')
    if data:
        data = eval(data.decode('utf-8'))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
