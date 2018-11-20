from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from .parsers import Academico, DiarioParser

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CORS(app)

@app.route('/diario/<login>/<password>')
def get_diario(login, password):
    diario = DiarioParser(login=login, password=password)
    res = diario.parse()
    # return json.dumps(res, ensure_ascii=False)
    return jsonify(res)

@app.route('/')
def get_root():
    return jsonify({'info': 'Ok!'})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
