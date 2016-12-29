# encoding: utf-8
from datetime import datetime
from . import db


class FeedType:
    DEFAULT = 0x00
    ZNYS = 0x01
    CJDA = 0x02
    GXRY = 0x02
    RYGJ = 0x03
    CLGJ = 0x04
    GWRY = 0x05
    QBZT = 0x06
    XYZS = 0x07
    TXXX = 0x08
    ZCMP = 0x09
    FKZH = 0x0a
    JQTS = 0x0b


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Integer, default=FeedType.DEFAULT)
    read_flag = db.Column(db.Boolean, default=False, index=True)
    content = db.Column(db.Text)
    appends = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    author_name = db.Column(db.String(46), default='AnonymousUser')
    author_id = db.Column(db.String(18))
    author_dept = db.Column(db.String(64))
    author_contact = db.Column(db.String(64))
