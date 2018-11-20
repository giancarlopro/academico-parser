from datetime import datetime

from academico.database import db_session
from academico.models import Config, Diario, DiarioDescription, User


class UserSerializer:
    def __init__(self, matricula=None, senha=None):
        if matricula and senha:
            self.user = User.query.filter(
                User.matricula == matricula,
                User.senha == senha
            ).one_or_none()
            if not self.user:
                self.user = User(matricula, senha)
                db_session.add(self.user)
                db_session.commit()
        else:
            self.user = None

    def get(self):
        return self.user


class ConfigSerializer:
    def __init__(self, user_id=None):
        if user_id:
            self.config = Config.query.filter(
                Config.user_id == user_id
            ).one_or_none()
            if not self.config:
                self.config = Config(user_id)
                db_session.add(self.config)
                db_session.commit()
        else:
            self.config = None
    
    def get(self):
        return self.config


class DiarioSerializer:

    def __init__(self, user_id=None, cod=None, materia=None, professor=None, turma=None):
        if user_id and cod:
            self.diario = Diario(user_id, cod, materia, professor, turma)

            config = ConfigSerializer(user_id).get()
            config.diario_updated_at = datetime.now()
            
            db_session.add(self.diario)
            db_session.add(config)
            db_session.commit()
        elif user_id:
            self.diario = Diario.query.filter(
                Diario.user_id == user_id
            )
        else:
            self.diario = None
        
    def get(self):
        return self.diario


class DiarioDescriptionSerializer:

    def __init__(self, diario_id=None, data=None, info=None, tipo=None, nota=None, peso=None):
        if diario_id and data:
            self.diario_description = DiarioDescription(
                diario_id,
                data,
                info,
                tipo,
                nota,
                peso
            )
            db_session.add(self.diario_description)
            db_session.commit()
        elif diario_id:
            self.diario_description = DiarioDescription.query.filter(
                DiarioDescription.diario_id == diario_id
            )
        else:
            self.diario_description = None

    def get(self):
        return self.diario_description
