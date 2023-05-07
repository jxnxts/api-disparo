from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, String, DateTime, BIGINT, BOOLEAN, text, JSON

Base = declarative_base()

class Cidade(Base):
    __tablename__ = "cidade"
    id = Column(INTEGER, primary_key=True)

class Contatos(Base):
    __tablename__ = "contatos"
    id = Column(INTEGER, primary_key=True)
    nome = Column(String(100), nullable=True)
    sobrenome = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    DDD = Column(String(2), nullable=True)
    telefone = Column(String(), nullable=True)
    cidade_id = Column(INTEGER, nullable=True)
    CEP = Column(String(8), nullable=True)
    lat = Column(String(100), nullable=True)
    long = Column(String(100), nullable=True)
    endereco = Column(String(100), nullable=True)
    numero = Column(String(100), nullable=True)
    grupos = Column(JSON, nullable=True)
    instances = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)

class Etiquetas(Base):
    __tablename__ = "etiquetas"
    id = Column(INTEGER, primary_key=True)
    nome = Column(String(100), nullable=True)

class Grupo_Participantes(Base):
    __tablename__ = "grupo_participantes"
    id = Column(INTEGER, primary_key=True)
    contato = Column(INTEGER, nullable=True)
    grupo = Column(INTEGER, nullable=True)

class Grupos(Base):
    __tablename__ = "grupos"
    id = Column(INTEGER, primary_key=True)
    number_group = Column(String(100), nullable=True)
    nome = Column(String(100), nullable=True)
    instance = Column(String(100), nullable=True)
    admin = Column(String(100), nullable=True)
    ativo = Column(BOOLEAN, nullable=True)
    cidade = Column(INTEGER, nullable=True)
    tema = Column(INTEGER, nullable=True)
    invitationLink = Column(String(100), nullable=True)
    creation = Column(DateTime, nullable=True)
    communityId = Column(String(100), nullable=True)
class Instance(Base):
    __tablename__ = "instance"
    id = Column(INTEGER, primary_key=True)
    instanceId = Column(String(100), nullable=True)
    token = Column(String(100), nullable=True)
    nome = Column(String(100), nullable=True)
    tipo_instance = Column(INTEGER, nullable=True)
    numero = Column(String(100), nullable=True)


class Tipo_Instance(Base):
    __tablename__ = "tipo_instance"
    id = Column(INTEGER, primary_key=True)
    nome = Column(String(100), nullable=True)