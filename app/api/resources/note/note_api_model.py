from flask_restx import fields
from app.api import notes_ns

# 笔记信息模型
note_info_request = notes_ns.model('NoteInfo', {
    # 'id': fields.Integer(description='笔记ID'),
    'type': fields.String(description='笔记类型'),
    'title': fields.String(description='笔记标题'),
    'content': fields.String(description='笔记内容'),
    'tags': fields.String(description='笔记标签'),
    'folder': fields.String(description='笔记所属文件夹'),
    'isArchived': fields.Boolean(description='是否已归档'),
    'isRecycle': fields.Boolean(description='是否在回收站'),
    'isShare': fields.Boolean(description='是否分享'),
    'sharePassword': fields.String(description='分享密码'),
    'createdAt': fields.String(description='创建时间'),
    'updatedAt': fields.String(description='更新时间'),
    'accountId': fields.Integer(description='账户ID')
})

note_info_response = notes_ns.model('NoteInfo', {
    'id': fields.Integer(description='笔记ID'),
    'type': fields.String(description='笔记类型'),
    'title': fields.String(description='笔记标题'),
    'content': fields.String(description='笔记内容'),
    'tags': fields.String(description='笔记标签'),
    'tagIds': fields.String(description='笔记标签IDs'),
    'folder': fields.String(description='笔记所属文件夹'),
    'isArchived': fields.Boolean(description='是否已归档'),
    'isRecycle': fields.Boolean(description='是否在回收站'),
    'isShare': fields.Boolean(description='是否分享'),
    'sharePassword': fields.String(description='分享密码'),
    'createdAt': fields.String(description='创建时间'),
    'updatedAt': fields.String(description='更新时间'),
    'accountId': fields.Integer(description='账户ID')
})

note_list_response = notes_ns.model('NoteListResponse', {
    'success': fields.Boolean(description='操作是否成功'),
    'message': fields.String(description='响应消息'),
    'data': fields.List(fields.Nested(note_info_response), description='笔记列表')
})

note_response = notes_ns.model('NoteResponse', {
    'success': fields.Boolean(description='操作是否成功'),
    'message': fields.String(description='响应消息'),
    'data': fields.Nested(note_info_response, description='笔记详情')
})