from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import json

from academico.parsers import DiarioParser
from academico.database import db_session
from academico.models import User, Diario, DiarioDescription
from academico.serializers import UserSerializer, DiarioSerializer, DiarioDescriptionSerializer, ConfigSerializer

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CORS(app)

@app.route('/diario/<matricula>/<senha>')
def get_diario(matricula, senha):
    user = UserSerializer(matricula, senha).get()
    config = ConfigSerializer(user.id).get()

    if config.need_to_update_diario():
        parser = DiarioParser(matricula=matricula, senha=senha)
        result = parser.parse()

        for diario in result:
            description = diario.pop('description', [])
            tmp_diario = DiarioSerializer(user.id, **diario).get()

            _ = [DiarioDescriptionSerializer(tmp_diario.id, **d).get() for d in description]

    return jsonify(user.to_native())

@app.route('/')
def get_root():
    return jsonify({'info': 'Ok!'})

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
