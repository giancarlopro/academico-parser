from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

from academico.database import Base

MINUTES_BEFORE_UPDATE = 10


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    matricula = Column(String(12), unique=True)
    senha = Column(String(50))

    diarios = relationship("Diario")

    def __init__(self, matricula=None, senha=None):
        self.matricula = matricula
        self.senha = senha
    
    def to_native(self):
        return [d.to_native() for d in self.diarios]

class Diario(Base):
    __tablename__ = 'diario'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    cod = Column(Integer)
    materia = Column(String(50))
    professor = Column(String(50))
    turma = Column(String(50))

    description = relationship("DiarioDescription")

    def __init__(self, user_id=None, cod=None, materia=None, professor=None, turma=None):
        self.user_id = user_id
        self.cod = cod
        self.materia = materia
        self.professor = professor
        self.turma = turma

    def __repr__(self):
        return '<Diario %r>' % (self.cod)

    def to_native(self):
        return {
            'cod': self.cod,
            'materia': self.materia,
            'professor': self.professor,
            'turma': self.turma,
            'description': [dd.to_native() for dd in self.description if self.description]
        }


class DiarioDescription(Base):
    __tablename__ = 'diario_description'

    id = Column(Integer, primary_key=True)
    diario_id = Column(Integer, ForeignKey('diario.id'))
    data = Column(String(50))
    info = Column(String(120))
    tipo = Column(String(120))
    nota = Column(Integer)
    peso = Column(Integer)

    def __init__(self, diario_id=None, data=None, info=None, tipo=None, nota=None, peso=None):
        self.diario_id = diario_id
        self.data = data
        self.info = info
        self.tipo = tipo
        self.nota = nota
        self.peso = peso
 
    def __repr__(self):
        return '<DiarioDescription %r>' % (self.info)
    
    def to_native(self):
        return {
            'data': self.data,
            'info': self.info,
            'tipo': self.tipo,
            'nota': self.nota,
            'peso': self.peso
        }


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    diario_updated_at = Column(DateTime, default=datetime.now() - timedelta(MINUTES_BEFORE_UPDATE))
    boletim_updated_at = Column(DateTime, default=datetime.now())

    def __init__(self, user_id=None):
        self.user_id = user_id
    
    def need_to_update_diario(self):
        offset = datetime.now() - timedelta(minutes=MINUTES_BEFORE_UPDATE)
        if self.diario_updated_at > offset:
            return False
        return True
