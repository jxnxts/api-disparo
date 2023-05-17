from pydantic import BaseModel
from typing import List, Optional


class ReturnEnvio(BaseModel):
    zaapId: str
    messageId: str
    id: str


class ReturnEnvioImagem(BaseModel):
    zaapId: str
    messageId: str
    id: str


class CreateGroupReturn(BaseModel):

    phone: str
    invitationLink: str


class Device(BaseModel):

    sessionName: str
    device_model: str


class DeviceReturn(BaseModel):
    phone: Optional[str]
    imgUrl: Optional[str]
    name: str
    device: Device
    sessionId: Optional[str]
    isBusiness: Optional[bool]


class CallRejectReturn(BaseModel):
    value: bool


class RestartReturn(BaseModel):
    value: Optional[bool]


class DisconectReturn(BaseModel):
    value: Optional[bool]


class QrCodeReturn(BaseModel):
    value: Optional[str]
    connected: Optional[bool]


class InstanceStatus(BaseModel):
    connected: bool
    session: bool
    created: int
    error: str
    smartphoneConnected: bool


class Message(BaseModel):
    pinned: bool
    messagesUnread: int
    unread: int
    lastMessageTime: int
    archived: bool
    phone: str
    name: str = ""
    isGroup: bool = False  # Add default value
    isMuted: bool = False  # Add default value
    isMarkedSpam: bool = False  # Add default value


class MessageList(BaseModel):
    messages: List[Message]


class Participant(BaseModel):
    phone: Optional[str]
    isAdmin: Optional[bool]
    isSuperAdmin: Optional[bool]


class GroupMetadata(BaseModel):
    phone: Optional[str]
    description: Optional[str]
    owner: Optional[str]
    subject: Optional[str]
    creation: Optional[int]
    invitationLink: Optional[str]
    communityId: Optional[str]
    isGroupAnnouncement: Optional[bool]
    participants: Optional[List[Participant]]
    subjectTime: Optional[int]
    subjectOwner: Optional[str]
