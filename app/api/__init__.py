from flask import Blueprint
from flask_restx import Api, Namespace

# 创建API蓝图
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# 创建Flask-RESTX的Api实例
api = Api(
    api_blueprint,
    version='1.0',
    title='LiFocus API',
    description='LiFocus的RESTful API',
    doc='/docs/',  # Swagger文档路径
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Token格式: Bearer <token>'
        }
    },
    security='Bearer'
)

auth_ns = Namespace('auth', description='认证相关接口', path='/auth')
users_ns = Namespace('users', description='用户管理接口', path='/users')
notes_ns = Namespace('article', description='笔记管理接口', path='/article')
tags_ns = Namespace('tags', description='标签管理接口', path='/tags')

from app.api.resources.auth.login import Login
from app.api.resources.auth.logout import Logout
from app.api.resources.auth.register import Register
from app.api.resources.user.user import UserService
from app.api.resources.note.note import NoteService, NoteDetailService
from app.api.resources.tag.tag import TagListService, TagService

# 登录注册
auth_ns.add_resource(Register, '/register')
auth_ns.add_resource(Login, '/login')
auth_ns.add_resource(Logout, '/logout')

# 用户测试 TODO
users_ns.add_resource(UserService, '/profile')

# 笔记相关
notes_ns.add_resource(NoteService, '/note', '/note/<int:note_id>')
notes_ns.add_resource(NoteDetailService, '/note-detail', '/note-detail/<int:note_id>')

# 标签相关
tags_ns.add_resource(TagListService, '/tags')
tags_ns.add_resource(TagService, '/tags/<int:tag_id>')

# 注册命名空间到API
api.add_namespace(auth_ns)
api.add_namespace(users_ns)
api.add_namespace(notes_ns)
api.add_namespace(tags_ns)