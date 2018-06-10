from flask import g
from sqlalchemy import or_

from .base_service import BaseService
from my_app.models import Message, MessageBatch
from my_app.common.constant import MessageType
from my_app.common.tools import get_time_format


class MessageService(BaseService):
    model = Message

    def create(self, context, type=MessageType.NORMAL, reply_message_id=None):
        message = self.model(context=context, type=type, from_user_id=g.user_id, reply_message_id=reply_message_id)
        self.db.session.add(message)
        self.db.session.commit()
        return message

    def get_info(self, id_or_ins):
        info = super(MessageService, self).get_info(id_or_ins)
        info.update({
            'created_at': get_time_format(float(info['created_at']))
        })
        return info


class MessageBatchServiice(BaseService):
    model = MessageBatch

    filter_fields = ['by_uid']

    @classmethod
    def filter_my_batches(cls, filter_uid=None, **kwargs):
        # TODO: judge the efficiency of or_ method, could change to "1 filter twice. 2 unique. 3 return id in ids."
        return [or_[cls.model.from_user_id == (filter_uid if filter_uid else g.user_id),
                    cls.model.to_user_id == (filter_uid if filter_uid else g.user_id)]]

    def create(self, title, to_uid, type, context):
        message_batch = self.model(title=title, from_user_id=g.user_id, to_user_id=to_uid)
        self.db.session.add(message_batch)
        message = MessageService(self.db).create(context=context, type=type)
        message_batch.messages.append(message)
        self.db.session.commit()
        return message_batch

    def get_info(self, id_or_ins):
        ins = self.get(id_or_ins)
        info = super(MessageBatchServiice, self).get_info(ins)
        info.update({
            'messages': sorted([MessageService(self.db).get_info(message) for message in ins.messages],
                               key=lambda x: x['id'])
        })
        return info
