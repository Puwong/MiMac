# -*- coding: utf-8 -*-
from flask import g
from sqlalchemy import or_

from .base_service import BaseService
from my_app.models import Message, MessageBatch
from my_app.common.constant import MessageType
from my_app.common.tools import get_time_format


class MessageService(BaseService):
    model = Message

    def reply_context(self, id_or_ins, yes):
        message = self.get(id_or_ins)
        if message.type == MessageType.YES_OR_NO:
            return u'我觉得你说的没错。' if yes else u'我觉得你说的不对。'
        else:
            return ''

    def create(self, context, type=MessageType.NORMAL, reply_message_id=None):
        message = self.model(context=context, type=type, from_user_id=g.user_id, reply_message_id=reply_message_id)
        self.db.session.add(message)
        self.db.session.commit()
        return message

    def read(self, id_or_ins):
        message = self.get(id_or_ins)
        if message.from_user_id == g.user_id:
            return
        message.readed = True
        self.db.session.commit()

    def get_info(self, id_or_ins, with_reply=False):
        message = self.get(id_or_ins)
        if message.type == MessageType.NORMAL and not message.readed:
            self.read(message)
        info = super(MessageService, self).get_info(message)
        info.update({
            'created_at': get_time_format(float(message.created_at))
        })
        if with_reply:
            info.update({
                'reply_context': self.get(message.reply_message_id).context[0:64] if message.reply_message_id else ""
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

    def the_other_person(self, id_or_ins):
        message_batch = self.get(id_or_ins)
        return message_batch.to_user_id if message_batch.from_user_id == g.user_id else message_batch.from_user_id

    def create(self, title, to_uid, type, context):
        message_batch = self.model(title=title, from_user_id=g.user_id, to_user_id=to_uid)
        self.db.session.add(message_batch)
        message = MessageService(self.db).create(context=context, type=type)
        message_batch.messages.append(message)
        self.db.session.commit()
        return message_batch

    def reply(self, id_or_ins, reply_message_id, message_type, context):
        message_service = MessageService(self.db)
        if reply_message_id and type(reply_message_id) is int:
            replied_msg = message_service.get(reply_message_id)
            message_service.read(replied_msg)
        message = message_service.create(context, message_type, reply_message_id)
        message_batch = self.get(id_or_ins)
        message_batch.messages.append(message)
        self.db.session.commit()
        return message_batch

    def get_info(self, id_or_ins, with_message=False, with_reply=False):
        message_batch = self.get(id_or_ins)
        info = super(MessageBatchServiice, self).get_info(message_batch)
        if with_message:
            info.update({
                'messages': sorted([MessageService(self.db).get_info(message, with_reply)
                                    for message in message_batch.messages], key=lambda x: x['id'])
            })
        return info
