from flask_restx import fields
from app.api import notes_ns

# 标签信息模型
tag_info_request = notes_ns.model('TagInfoRequest', {
    'name': fields.String(required=True, description='标签名称'),
})

tag_info_response = notes_ns.model('TagInfoResponse', {
    'id': fields.Integer(description='标签ID'),
    'name': fields.String(description='标签名称'),
    'createdAt': fields.String(description='创建时间'),
    'updatedAt': fields.String(description='更新时间'),
    'accountId': fields.Integer(description='账户ID')
})

tag_list_response = notes_ns.model('TagListResponse', {
    'success': fields.Boolean(description='操作是否成功'),
    'message': fields.String(description='响应消息'),
    'data': fields.List(fields.Nested(tag_info_response), description='标签列表')
})

tag_response = notes_ns.model('TagResponse', {
    'success': fields.Boolean(description='操作是否成功'),
    'message': fields.String(description='响应消息'),
    'data': fields.Nested(tag_info_response, description='标签详情')
})