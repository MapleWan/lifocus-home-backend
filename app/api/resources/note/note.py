from flask_restx import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.models.note import Note
from app.api.models.tag import Tag  # 添加导入Tag模型
from app.api import notes_ns
from .note_api_model import note_list_response, note_info_request, note_response
from ...common.utils import api_response
from datetime import datetime

class NoteService(Resource):
    @jwt_required()
    @notes_ns.doc(description='获取所有笔记信息',
             responses={
                 200: '成功获取笔记列表',
                 401: '未授权访问',
                 500: '服务器内部错误'
             })
    @notes_ns.marshal_with(note_list_response)
    def get(self):
        # 获取当前用户的所有笔记
        current_user_id = get_jwt_identity()
        note_list = Note.findNotesByAccountId(current_user_id)
        result = [note.dict() for note in note_list]
        return {
            'success': True,
            'message': 'success',
            'data': result
        }, 200

    @jwt_required()
    @notes_ns.doc(description='创建新笔记',
             responses={
                 201: '成功创建笔记',
                 400: '请求参数错误',
                 401: '未授权访问',
                 500: '服务器内部错误'
             })
    @notes_ns.expect(note_info_request)
    @notes_ns.marshal_with(note_response)
    def post(self):
        # 解析请求参数
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=False, default='note', help='笔记类型')
        parser.add_argument('content', type=str, required=False, help='笔记内容')
        parser.add_argument('tags', type=str, required=False, help='标签')
        parser.add_argument('folder', type=str, required=False, help='笔记所属文件夹')
        parser.add_argument('isArchived', type=bool, required=False, default=False, help='是否已归档')
        parser.add_argument('isRecycle', type=bool, required=False, default=False, help='是否在回收站')
        parser.add_argument('isShare', type=bool, required=False, default=False, help='是否分享')
        parser.add_argument('sharePassword', type=str, required=False, help='分享密码')
        
        args = parser.parse_args()
        current_user_id = get_jwt_identity()

        # 处理标签
        tag_names = []
        if args['tags']:
            tag_names = [tag.strip() for tag in args['tags'].split(',') if tag.strip()]
            for tag_name in tag_names:
                # 检查标签是否已存在
                existing_tag = Tag.findTagByNameAndAccountId(tag_name, current_user_id)
                if not existing_tag:
                    # 如果标签不存在，则创建新标签
                    new_tag = Tag(
                        name=tag_name,
                        account_id=current_user_id
                    )
                    new_tag.addTag()

        # 创建新笔记
        new_note = Note(
            type=args['type'],
            content=args['content'],
            tags=args['tags'],
            folder=args['folder'],
            is_archived=args['isArchived'],
            is_recycle=args['isRecycle'],
            is_share=args['isShare'],
            share_password=args['sharePassword'],
            account_id=current_user_id
        )
        
        new_note.addNote()
        
        return {
            'success': True,
            'message': '笔记创建成功',
            'data': new_note.dict()
        }, 201

    @jwt_required()
    @notes_ns.doc(description='更新指定ID的笔记信息',
                  responses={
                      200: '成功更新笔记',
                      400: '请求参数错误',
                      401: '未授权访问',
                      404: '笔记不存在',
                      500: '服务器内部错误'
                  })
    @notes_ns.expect(note_info_request)
    @notes_ns.marshal_with(note_response)
    def put(self, note_id):
        current_user_id = get_jwt_identity()
        note = Note.findNoteByIdAndAccountId(note_id, current_user_id)

        if not note:
            return {
                'success': False,
                'message': '笔记不存在',
                'data': None
            }, 404

        # 解析请求参数
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=False, help='笔记类型')
        parser.add_argument('content', type=str, required=False, help='笔记内容')
        parser.add_argument('tags', type=str, required=False, help='标签')
        parser.add_argument('folder', type=str, required=False, help='笔记所属文件夹')
        parser.add_argument('isArchived', type=bool, required=False, help='是否已归档')
        parser.add_argument('isRecycle', type=bool, required=False, help='是否在回收站')
        parser.add_argument('isShare', type=bool, required=False, help='是否分享')
        parser.add_argument('sharePassword', type=str, required=False, help='分享密码')

        args = parser.parse_args()

        # 处理标签
        if args['tags'] is not None:
            tag_names = []
            if args['tags']:
                tag_names = [tag.strip() for tag in args['tags'].split(',') if tag.strip()]
                for tag_name in tag_names:
                    # 检查标签是否已存在
                    existing_tag = Tag.findTagByNameAndAccountId(tag_name, current_user_id)
                    if not existing_tag:
                        # 如果标签不存在，则创建新标签
                        new_tag = Tag(
                            name=tag_name,
                            account_id=current_user_id
                        )
                        new_tag.addTag()

        # 更新笔记属性
        if args['type'] is not None:
            note.type = args['type']
        if args['content'] is not None:
            note.content = args['content']
        if args['tags'] is not None:
            note.tags = args['tags']
        if args['folder'] is not None:
            note.folder = args['folder']
        if args['isArchived'] is not None:
            note.is_archived = args['isArchived']
        if args['isRecycle'] is not None:
            note.is_recycle = args['isRecycle']
        if args['isShare'] is not None:
            note.is_share = args['isShare']
        if args['sharePassword'] is not None:
            note.share_password = args['sharePassword']

        note.updated_at = datetime.now()
        note.updateNote()

        return {
            'success': True,
            'message': '笔记更新成功',
            'data': note.dict()
        }, 200

    @jwt_required()
    @notes_ns.doc(description='删除指定ID的笔记',
                  responses={
                      200: '成功删除笔记',
                      401: '未授权访问',
                      404: '笔记不存在',
                      500: '服务器内部错误'
                  })
    @notes_ns.marshal_with(api_response)
    def delete(self, note_id):
        current_user_id = get_jwt_identity()
        note = Note.findNoteByIdAndAccountId(note_id, current_user_id)

        if not note:
            return {
                'success': False,
                'message': '笔记不存在',
            }, 404

        note.deleteNote()

        return {
            'success': True,
            'message': '笔记删除成功',
        }, 200


class NoteDetailService(Resource):
    @jwt_required()
    @notes_ns.doc(description='获取指定ID的笔记信息',
             responses={
                 200: '成功获取笔记信息',
                 401: '未授权访问',
                 404: '笔记不存在',
                 500: '服务器内部错误'
             })
    @notes_ns.marshal_with(note_response)
    def get(self, note_id):
        current_user_id = get_jwt_identity()
        note = Note.findNoteByIdAndAccountId(note_id, current_user_id)
        if note:
            return {
                'success': True,
                'message': 'success',
                'data': note.dict()
            }, 200
        else:
            return {
                'success': False,
                'message': '笔记不存在',
                'data': None
            }, 404

    @jwt_required()
    @notes_ns.doc(description='根据条件查询笔记',
             responses={
                 200: '成功获取笔记列表',
                 401: '未授权访问',
                 500: '服务器内部错误'
             })
    @notes_ns.expect(note_info_request)
    @notes_ns.marshal_with(note_list_response)
    def post(self):
        current_user_id = get_jwt_identity()
        
        # 解析请求参数
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=False, help='笔记类型')
        parser.add_argument('content', type=str, required=False, help='笔记内容')
        parser.add_argument('tags', type=str, required=False, help='标签')
        parser.add_argument('folder', type=str, required=False, help='笔记所属文件夹')
        parser.add_argument('isArchived', type=bool, required=False, help='是否已归档')
        parser.add_argument('isRecycle', type=bool, required=False, help='是否在回收站')
        parser.add_argument('isShare', type=bool, required=False, help='是否分享')
        
        args = parser.parse_args()
        
        # 构造查询条件
        conditions = {}
        if args['type'] is not None:
            conditions['type'] = args['type']
        if args['content'] is not None:
            conditions['content'] = args['content']
        if args['tags'] is not None:
            conditions['tags'] = args['tags']
        if args['folder'] is not None:
            conditions['folder'] = args['folder']
        if args['isArchived'] is not None:
            conditions['is_archived'] = args['isArchived']
        if args['isRecycle'] is not None:
            conditions['is_recycle'] = args['isRecycle']
        if args['isShare'] is not None:
            conditions['is_share'] = args['isShare']
            
        # 执行查询
        note_list = Note.findNotesByMultipleConditions(current_user_id, **conditions)
        result = [note.dict() for note in note_list]
        
        return {
            'success': True,
            'message': 'success',
            'data': result
        }, 200