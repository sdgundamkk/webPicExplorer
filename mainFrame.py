#!/usr/bin/python
# -*- coding:UTF-8 -*-

from __future__ import with_statement  
# from flask_wtf import Form

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash  
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required, logout_user
from config import BaseLogin,AddTaskForm
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from time import sleep
# from model import User
import os.path
import datetime
import config
import re
# global foo
# foo = []

# configuration
app = Flask(__name__)
app.config.from_object('config')  
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = config.dbPath
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
app.foo = {}
db = SQLAlchemy(app)

login_manager = LoginManager()  
login_manager.init_app(app)
login_manager.login_view = 'login' 

class Task(db.Model):
    __tablename__ = 'tasks'
    id                 = db.Column(db.Integer, primary_key=True)
    task_name          = db.Column(db.String(120))
    user_id            = db.Column(db.String(1200))
    pic_path           = db.Column(db.String(1200))
    version_temp       = db.Column(db.String(120))
    create_time        = db.Column(db.DateTime, default =datetime.datetime.now())
    task_result        = db.Column(db.String(1200))
      
    def __init__(self, task_name,pic_path,version_temp,user_id):
        self.task_name      = task_name
        self.user_id        = user_id
        self.pic_path       = pic_path
        self.version_temp   = version_temp
        self.create_time    = datetime.datetime.now()
        
    def __repr__(self):
        return '%s'%str([self.task_name,self.user_id ,self.pic_path ,self.version_temp,self.create_time])
    
    def get(self):
        return [self.id, self.task_name,self.user_id ,self.pic_path ,self.version_temp,self.create_time]
    
class Users(db.Model):
    __tablename__ = 'User'
    id                 = db.Column(db.Integer, primary_key=True)
    user_name          = db.Column(db.String(120))
    task_id            = db.Column(db.String(120))
    finish_r           = db.Column(db.String(1200))
      
    def __init__(self, user_name):
        self.user_name = user_name
        self.task_id   = ''
        self.finish_r  = ''

    def __repr__(self):
        return '%s' % str(self.user_name)
    
    def get(self):
        return [self.id, self.user_name, self.task_id, self.finish_r]

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = self.get_id()
        
    def verify_password(self, password):
        if password == 'admin':
            return True
        return False
    
    def get_id(self):
        user = db.session.query(Users).filter(Users.user_name==self.username).first()
        if user:
            return user.get()[0]
        return '1'
    
    @staticmethod
    def get(user_id):
        user = db.session.query(Users).filter(Users.id==user_id).first()
        if user:
            return User(user.get()[1])
        return User('admin')
    
    
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.before_request  
def before_request():
    db.create_all()
    g.user = current_user
    if hasattr(g.user, "username"):
        if g.user.username in session['username']:  
            pass
#             print g.user.username
#             print session['username']

def initUser(userName):
    user = db.session.query(Users).filter(Users.user_name==userName).first()
    if not user:
        u = Users(user_name=userName)
        db.session.add(u)
        db.session.commit()

def getTemplate(version):
    return config.TEMPLATEVERSION.get(version, config.TEMPLATEVERSION['default'])

def getAllPath(path):
    result = config.PICPATH
    return result

def getTaskInfo(taskId):
    result = {'id': [], 'tasks': [], 'details': [], 'picpath': []}
    task = db.session.query(Task).filter(Task.id == taskId).first()
    if task:
        infoList = task.get()
        detailsFromTemp = getTemplate(infoList[3])
        picpath = getAllPath(infoList[4])
        return {'id': infoList[0], 'tasks': infoList[1], 'details': detailsFromTemp, 'picpath': picpath}
    return result

def getUserTask(taskid = None):
    current_User = session['username'] if 'username' in session else 'admin' 
    result = {'userName':current_User, 'details':[], 'tasks':[], 'taskName':[], 'details':[], 'picpath':[], 'userObj':None}
    if current_User == 'superadmin':
        return result

    user = db.session.query(Users).filter(Users.user_name==current_User).first()
    if user == 0:
        abort(403)

    result['tasks'] = user.get()[2]
    taskids = result['tasks'].split('|')[1:]
    if len(taskids) == 0:
        return result
    
    for tid in taskids:
        info = getTaskInfo(tid)
        result['taskName'].append(info['tasks'])
    if (not taskid) or (str(taskid) not in taskids):
        taskid = taskids[0]
        
    info = getTaskInfo(taskid)
    result['details'] = info['details']# 模板的转化
    result['picpath'] = info['picpath']# 照片路径的转化
    result['userObj'] = user
    return result

def deleteUserTask(TaskName):
    current_User = session['username'] if 'username' in session else 'admin' 
    user = db.session.query(Users).filter(Users.user_name==current_User).first()
    task = db.session.query(Task).filter(Task.task_name==TaskName).first()
    if user and task:
        tid = '|%s' %task.id
        uid = user.task_id
        index = uid.find(tid)
        user.task_id = uid[:index] + uid[index+len(tid):]
        db.session.commit()
        
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not ('username' in session and session['username'] == config.SUPERADMIN):
            abort(403)
        return func(*args, **kwargs)
    return decorated_view
     

@app.route('/', methods=('POST', 'GET'))
def login():
    g.user = current_user
    if hasattr(g.user, "username"):
        if g.user.username in session['username']:
            return '<h1>已经登陆</h1><p><a href=''/logout''>退出登录</a></p>'

    form=BaseLogin()
    if form.validate_on_submit():
        user = User(form.name.data)
        if user.verify_password(form.password.data):
            login_user(user)
            session['username'] = form.name.data
            initUser(form.name.data)
            result = getUserTask()
            result['details'] = result['details'][1:]
            if result['userName'] not in app.foo:
                app.foo[result['userName']] = {}
            return redirect(url_for('task'))
            
        elif form.name.data == config.SUPERADMIN and form.password.data == config.SUPERADMINPASSWD:
            login_user(user)
            session['username'] = form.name.data
            return redirect(url_for('task'))
        else:
            flash(u'错误的用户名或密码')
    return render_template('login.html', form=form)

@app.route('/task', methods=('POST','GET'))
def task():
    result = getUserTask()
    dates = []  
    for r in Task.query.all():
        if isinstance(r, Task):
            dates.append(r.get())
    if request.method == 'POST':
        requests = request.get_json()
#         if requests and 'finish' in requests:
#             print requests['finish']
# #             deleteUserTask(requests['finish'])
#             app.foo[task['userName']]={}
        if requests and 'change' in requests:
            taskName = re.match('\<a\>(\S+)\<\/a\>',requests['change'])
            if taskName:
                taskName = taskName.groups()[0]
                taskId = db.session.query(Task).filter(Task.task_name == taskName).first()
                result = getUserTask(taskId.id)
            return render_template('work.html', tasks=result['taskName'],
                                                details=result['details'],
                                                title=result['taskName'][0],
                                                pics=result['picpath'][0],
                                                path=result['picpath'],
                                                userName=result['userName'])
            
    return render_template('task.html', tasks=result['taskName'], 
                   dates=dates, 
                   details=config.task_details, 
                   userName=result['userName'])
  

@app.route('/add',methods=('POST','GET'))  
@admin_required  
def add():  
    form = AddTaskForm()
    if form.validate_on_submit():
        task = db.session.query(Task).filter(Task.task_name==form.taskName.data).all()
        if len(task) > 0:
            flash(u'当前已经存在有同名的任务名称，请重新命名')
            return render_template('add.html', userName=session['username'], form=form)

        t = Task(task_name=form.taskName.data,
                 pic_path=form.picList.data,
                 version_temp=form.taskTemplate.data,
                 user_id=str(form.users.data))
        db.session.add(t)
        db.session.commit()
        
        task = db.session.query(Task).filter(Task.task_name == form.taskName.data).first()
        
        for userId in form.users.data:
            user = db.session.query(Users).filter(Users.id == int(userId)).first()
            if user:
                user.task_id += '|%s' % str(task.id)
        return redirect(url_for('task')) 
    return render_template('add.html', userName=session['username'], form=form)

@app.route('/logout')  
@login_required  
def logout():  
    logout_user()
    try:
        print 'logout!'
        del app.foo[session['username']]
    except:
        pass
    return redirect(url_for('login'))  

@app.route('/result',methods=('POST','GET'))
@login_required
def result():
    g.foo = []
    task= getUserTask()
#     if task['userName'] not in list(app.foo):
#         app.foo[task['userName']] = {}
    try:
        for key in list(app.foo[task['userName']]):
            g.foo.append(app.foo[task['userName']][key])
    except:
            print id(app.foo)
    if request.method == 'POST':
        requests = request.get_json()
        if requests and 'finish' in requests:
            deleteUserTask(requests['finish'])
            app.foo[task['userName']] = {}
            print id(app.foo)
    return render_template('result.html', details=task['details'], dates=g.foo, userName=task['userName'], title= task['taskName'][0],)


@app.route('/work',methods=('POST','GET'))
@login_required 
def work():
    task = getUserTask()
    task['details'] = task['details'][1:]
    if request.method == 'POST':
        results = request.get_json()
        if results and 'dates' in results:
            app.foo[task['userName']][results['dates'][0]]=results['dates']
    try:
        return render_template('work.html', tasks=task['taskName'],
                                title= task['taskName'][0],
                                details=task['details'],
                                pics=task['picpath'][0],
                                path=task['picpath'], userName=task['userName'])
    except:
        abort(403)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)