from flask import g
from .base_service import BaseService
from .user_service import UserService
from my_app.models import Article, TextNode
from my_app.common.tools import get_time_format


class ArticleService(BaseService):
    model = Article

    def get_by_user(self, id_or_ins, ignore_delete=False):
        user = UserService(self.db).get(id_or_ins)
        articles = list()
        for article in user.articles:
            if not article.delete or ignore_delete:
                articles.append(article)
        return articles

    def get_info(self, id_or_ins, with_text=False):
        ins = self.get(id_or_ins)
        info = super(ArticleService, self).get_info(ins)
        info.update({
            'created_at': get_time_format(info['created_at']),
            'modified_at': get_time_format(info['modified_at']),
        })
        if with_text:
            text = u''
            for text_node in ins.text_nodes:
                text += text_node.context
            info.update({
                'text': text,
            })
        return info

    def update(self, id_or_ins, title, text):
        article = self.get(id_or_ins)
        article.title = title
        start = 0
        for text_node in article.text_nodes:
            if start*1000 > len(text):
                self.db.session.delete(text_node)
            else:
                text_node.context = text[start*1000:(start+1)*1000]
            start += 1
        for i in range((len(text)+999)//1000 - start):
            tmp = text[start*1000:(start+1)*1000]
            text_node = TextNode(context=tmp)
            self.db.session.add(text_node)
            article.text_nodes.append(text_node)
            start += 1
        self.db.session.commit()
        return article

    def create(self, title, text):
        article = self.model(title=title)
        self.db.session.add(article)
        for i in range((len(text)+999)//1000):
            tmp = text[i*1000:(i+1)*1000]
            text_node = TextNode(context=tmp)
            self.db.session.add(text_node)
            article.text_nodes.append(text_node)
        user = UserService(self.db).get(g.user_id)
        user.articles.append(article)
        self.db.session.commit()
        return article

    def delete(self, id_or_ins, lazy=True):
        article = self.get(id_or_ins)
        if lazy:
            article.delete = True
        else:
            for text_node in article.text_nodes:
                self.db.session.delete(text_node)
            self.db.session.delete(article)
        self.db.session.commit()


