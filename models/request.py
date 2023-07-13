from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
import datetime
from db.database import Database
# from sqlalchemy.sql.expression import exists

database = Database()
engine = database.get_db_connection()

# Requests Models Basicas


class CidadeRequest(BaseModel):
    id: Optional[int] = Field(None, title="Cidade ID")


class ContatosRequest(BaseModel):
    # id: Optional[int] = Field(None, title="Contato ID")
    nome: Optional[str] = Field(None, title="Nome", max_length=100)
    sobrenome: Optional[str] = Field(None, title="Sobrenome", max_length=100)
    email: EmailStr = Field(..., title="Email")
    DDD: Optional[str] = Field(None, title="DDD", max_length=2)
    telefone: Optional[str] = Field(None, title="Telefone", max_length=9)
    cidade_id: Optional[int] = Field(None, title="Cidade ID")
    CEP: Optional[str] = Field(None, title="CEP", max_length=8)
    lat: Optional[str] = Field(None, title="Latitude", max_length=100)
    long: Optional[str] = Field(None, title="Longitude", max_length=100)
    endereco: Optional[str] = Field(None, title="Endereço", max_length=100)
    numero: Optional[str] = Field(None, title="Número", max_length=100)
    grupos: Optional[List[int]] = Field(None, title="Grupos")
    instances: Optional[List[int]] = Field(None, title="Instâncias")
    tags: Optional[List[int]] = Field(None, title="Tags")


class ContatosCreateRequest(BaseModel):
    id: Optional[int] = Field(None, title="Contato ID")
    nome: Optional[str] = Field(None, title="Nome", max_length=100)
    sobrenome: Optional[str] = Field(None, title="Sobrenome", max_length=100)
    email: EmailStr = Field(..., title="Email")
    DDD: Optional[str] = Field(None, title="DDD", max_length=2)
    telefone: Optional[str] = Field(None, title="Telefone", max_length=15)
    cidade_id: Optional[int] = Field(None, title="Cidade ID")
    CEP: Optional[str] = Field(None, title="CEP", max_length=8)
    lat: Optional[str] = Field(None, title="Latitude", max_length=100)
    long: Optional[str] = Field(None, title="Longitude", max_length=100)
    endereco: Optional[str] = Field(None, title="Endereço", max_length=100)
    numero: Optional[str] = Field(None, title="Número", max_length=100)
    grupos: Optional[List[int]] = Field(None, title="Grupos")
    instances: Optional[List[int]] = Field(None, title="Instâncias")
    tags: Optional[List[int]] = Field(None, title="Tags")


class EtiquetasRequest(BaseModel):
    id: Optional[int] = Field(None, title="Etiqueta ID")
    nome: Optional[str] = Field(None, title="Nome", max_length=100)


class GrupoParticipantesRequest(BaseModel):
    id: Optional[int] = Field(None, title="Grupo Participante ID")
    contato: Optional[int] = Field(None, title="Contato")
    grupo: Optional[int] = Field(None, title="Grupo")


class GruposRequest(BaseModel):
    id: Optional[int] = Field(None, title="Grupo ID")
    number_group: Optional[str] = Field(
        None, title="Número do Grupo", max_length=100)
    nome: Optional[str] = Field(None, title="Nome", max_length=100)
    instance: Optional[str] = Field(None, title="Instância", max_length=100)
    admin: Optional[str] = Field(None, title="Admin", max_length=100)
    invitationLink: Optional[str] = Field(
        None, title="invitationLink", max_length=100)
    creation: Optional[datetime.datetime] = Field(None, title="creation")
    communityId: Optional[str] = Field(
        None, title="communityId", max_length=100)
    ativo: Optional[bool] = Field(None, title="Ativo")
    cidade: Optional[int] = Field(None, title="Cidade")
    tema: Optional[int] = Field(None, title="Tema")


class InstanceRequest(BaseModel):
    id: Optional[int] = Field(None, title="Instância ID")
    instanceId: Optional[str] = Field(None, title="Chave", max_length=100)
    token: Optional[str] = Field(None, title="Nome", max_length=100)
    nome: Optional[str] = Field(None, title="Número", max_length=100)
    numero: Optional[str] = Field(None, title="Número", max_length=100)
    tipo_instance: Optional[int] = Field(None, title="Tipo")


class TipoInstanceRequest(BaseModel):
    id: Optional[int] = Field(None, title="Tipo Instância ID")
    nome: Optional[str] = Field(None, title="Nome", max_length=100)


class CreateGroup(BaseModel):
    groupName: Optional[str] = Field(None, title="Nome", max_length=100)
    phones: List[str]


# Request Models de Update acessorias
class InstanceUpdateRequest(BaseModel):
    instance_id: int

    # Adcionar @validator


class TagUpdateRequest(BaseModel):
    tags: List[str]

    # Adcionar @validator


class GroupUpdateRequest(BaseModel):
    groups: List[str]

    # Adcionar @validator


class MensagemImagemRequest(BaseModel):
    phone: str
    image: str
    caption: Optional[str]
    delayMessage: Optional[int]

class MensagemTextRequest(BaseModel):
    message: str
    phone: str
    delayMessage: Optional[int]

class MensagemLinkRequest(BaseModel):
    phone: str
    message: str
    image: Optional[str]
    linkUrl: Optional[str]
    title: Optional[str]
    linkDescription: Optional[str]
    delayMessage: Optional[int]
    linkType: Optional[str]

# {
#   "phone": "5511999998888",
#   "message": "Aqui você coloca um texto sobre o site, atenção esse texto preciso ter o link que será enviado no final da mensagem! Assim: https://z-api.io",
#   "image": "https://firebasestorage.googleapis.com/v0/b/zaap-messenger-web.appspot.com/o/logo.png?alt=media",
#   "linkUrl": "https://z-api.io",
#   "title": "Z-API",
#   "linkDescription": "Integração com o whatsapp"
# }

class MensagemVideoRequest(BaseModel):
    phone: str
    video: str
    caption: Optional[str]
    delayMessage: Optional[int]


class MensagemAudioRequest(BaseModel):
    phone: str
    audio: str
    delayMessage: Optional[int]
    delayTyping: Optional[int]


class MensagemImagemRequestGrupo(BaseModel):
    imagem: str
    caption: Optional[str]


class MensagemAudioRequestGrupo(BaseModel):
    audio: str
    delayTyping: Optional[int]


class MensagemVideoRequestGrupo(BaseModel):
    video: str
    caption: Optional[str]

class MensagemTextRequestGrupo(BaseModel):
    message: str
