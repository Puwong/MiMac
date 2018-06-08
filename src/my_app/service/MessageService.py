from .BaseService import BaseService
from my_app.models import Message, MessageBatch


class MessageService(BaseService):
    model = Message


class MessageBatchServiice(BaseService):
    model = MessageBatch

