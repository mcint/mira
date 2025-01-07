from flask import Flask, send_from_directory, request
import os
import logging

app = Flask(__name__, static_url_path='/static', static_folder='./static')
DATA_FILE = './data/mira.txt'

def ensure_data_exists():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            f.write('[]')

@app.route('/')
def home():
    try:
        return send_from_directory('static', 'index.html')
    except Exception as e:
        logging.error(f"Error serving index: {e}")
        return "error reading index"

@app.route('/data', methods=['GET'])
def get_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading data: {e}")
        return "error reading file", 500

@app.route('/data', methods=['POST'])
def post_data():
    try:
        with open(DATA_FILE, 'w') as f:
            f.write(request.get_data(as_text=True))
        return '', 200
    except Exception as e:
        logging.error(f"Error writing data: {e}")
        return "error writing file", 500

def start(**kwargs):
    ensure_data_exists()
    logging.basicConfig(level=logging.INFO)
    defaults = dict(
        host="127.0.0.1",
        port=8998,
        debug=False
    )
    app.run(**{**defaults, **kwargs})

if __name__ == '__main__':
    import fire
    fire.Fire(start)
