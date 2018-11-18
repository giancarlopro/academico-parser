from flask import Flask, request, jsonify
import json

from parsers import Academico

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/diario/<login>/<password>')
def get_diario(login, password):
    acad = Academico(login=login, password=password)
    res = acad.parse_diario()
    # return json.dumps(res, ensure_ascii=False)
    return jsonify(res)

@app.route('/')
def get_root():
    return jsonify({'info': 'Ok!'})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
