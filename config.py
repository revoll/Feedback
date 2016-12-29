# encoding: utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))


def read_admin_list():
    with open(os.path.join(basedir, 'admin.txt')) as f:
        id_list = f.readlines()
        for i in range(0, len(id_list)):
            id_list[i] = id_list[i].strip()
    return id_list


class Config:
    SECRET_KEY = 'JXGA-FEEDBACK'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = u'sqlite:///' + os.path.join(basedir, u'data.sqlite')
    FLASKY_SLOW_DB_QUERY_TIME=0.5
    FLASKY_FEEDBACKS_PER_PAGE = 10
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = set([u'jpg', u'jpeg', u'png', u'bmp'])
    FEEDBACK_SUBJECTS = u'大数据平台,智能云搜,超级档案,关系人分析,人员轨迹分析,车辆轨迹分析,高危人员分析,' \
                        u'情报主题研判,嫌疑指数分析,通讯信息分析,侦查摸排助手,反恐综合应用,警情态势分析'.split(u',')
    FEEDBACK_ADMIN_LIST = read_admin_list()

    @staticmethod
    def init_app(app):
        pass
