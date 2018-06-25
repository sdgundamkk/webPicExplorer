#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
CSRF_ENABLED = True
SECRET_KEY = '123456'
from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField,SelectMultipleField
from wtforms.validators import DataRequired,Length

dbPath = 'sqlite:///'+ os.path.join(os.path.abspath(os.path.dirname(__file__)),'static','task.db')
task_details = [u'序号', u'任务名称', u'评测人员' , u'样张路径', u'评测维度模板' , u'创建时间', u'结果页面' ]
SUPERADMIN       = 'superadmin'
SUPERADMINPASSWD = 'admin'

USERLIST = [('1','tangpeng'),('2','zhangbo'),('3','anmengla'),('4','zhangmingle')
            ,('5','zengyanli'),('6','wangtao'),('7','dubeng'),('8','wanjuan')]
PICPATH = ["/static/workfor/IMG_0/IMG_0.jpg",
           "/static/workfor/IMG_20150204_204154_0/IMG_20150204_204154_0.jpg",
           "/static/workfor/IMG_20150204_222329_7/IMG_20150204_222329_7.jpg",
           "/static/workfor/IMG_20150207_164553_2/IMG_20150207_164553_2.jpg",
           "/static/workfor/IMG_20150208_211251_1/IMG_20150208_211251_1.jpg",
           "/static/workfor/IMG_20150209_172049_6/IMG_20150209_172049_6.jpg",
           "/static/workfor/IMG_20150209_195345_0/IMG_20150209_195345_0.jpg",
           ]


TEMPLATEVERSION = {'default':[u'图片名称', u'主体准确度',u'背景虚化',u'主体边缘',u'光斑']}

class BaseLogin(Form):
    name=StringField('姓名',validators=[DataRequired(message="请输入用户名")
        ,Length(5,20,message='用户名长度在5-20之间')],render_kw={'placeholder':'用户名'})
    password=PasswordField('password',validators=[DataRequired(message="请输入密码")
        ,Length(5,20,message='密码长度在5-20之间')],render_kw={'placeholder':'密码'})
    
class AddTaskForm(Form):
    taskName = StringField('任务名称',validators=[DataRequired(message="请输入任务名称")
        ,Length(5,20,message='任务名称长度在5-20之间')],render_kw={'placeholder':'任务名称'})
    picList = StringField('图片路径',validators=[DataRequired(message="请输入用户名")
        ,Length(5,20,message='图片路径5-20之间')],render_kw={'placeholder':'图片路径'})
    taskTemplate = StringField('模板名称',validators=[DataRequired(message="请输入用户名")
        ,Length(5,20,message='模板名称5-20之间')],render_kw={'placeholder':'模板名称'})
    users = SelectMultipleField('分派给', choices=USERLIST)
    submit = SubmitField('Submit')