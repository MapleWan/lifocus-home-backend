from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 导入所有模型以确保它们被正确注册
from .user import User
from .note import Note
from .revoked_token import RevokedToken
from .tag import Tag
from .timeline import Timeline
from .note_tag import note_tags