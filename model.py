#!/usr/bin/python
# -*- coding:UTF-8 -*-

# from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
# import json
# import uuid

# PROFILE_FILE = "profiles.json"

class User(UserMixin):
    def __init__(self, username):
        self.username = username
#         self.password_hash = self.get_password_hash()
        self.id = self.get_id()
   
#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')
#      
#     @password.setter
#     def password(self, password):
#         """save user name, id and password hash to json file"""
#         self.password_hash = generate_password_hash(password)
#         with open(PROFILE_FILE, 'w+') as f:
#             try:
#                 profiles = json.load(f)
#             except ValueError:
#                 profiles = {}
#             profiles[self.username] = [self.password_hash, self.id]
#             f.write(json.dumps(profiles))
 
    def verify_password(self, password):
        if password == 'admin':
            return True
        return False
    
#     def get_password_hash(self):
#         try:
#             with open(PROFILE_FILE) as f:
#                 user_profiles = json.load(f)
#                 user_info = user_profiles.get(self.username, None)
#                 if user_info is not None:
#                     return user_info[0]
#         except IOError,ValueError:
#             return None
#         return None
 
#     def get_id(self):
#         if self.username is not None:
#             try:
#                 with open(PROFILE_FILE) as f:
#                     user_profiles = json.load(f)
#                     if self.username in user_profiles:
#                         return user_profiles[self.username][1]
#             except:
#                 pass
#         return unicode(uuid.uuid4())
    
    def get_id(self):
        return '1'
 
    @staticmethod
    def get(user_id):
        return User('admin')
#         if not user_id:
#             return None
#         try:
#             with open(PROFILE_FILE) as f:
#                 user_profiles = json.load(f)
#                 for user_name, profile in user_profiles.iteritems():
#                     if profile[1] == user_id:
#                         return User(user_name)
#         except:
#             return None
#         return None