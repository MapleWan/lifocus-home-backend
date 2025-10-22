from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.models.tag import Tag
from app.api import notes_ns
from .tag_api_model import tag_list_response, tag_info_request, tag_response
from ...common.utils import api_response

class TagListService(Resource):
    @jwt_required()
    @notes_ns.doc(description='获取所有标签信息',
                  responses={
                      200: '成功获取标签列表',
                      401: '未授权访问',
                      500: '服务器内部错误'
                  })
    @notes_ns.marshal_with(tag_list_response)
    def get(self):
        """获取当前用户的所有标签"""
        current_user_id = get_jwt_identity()
        tag_list = Tag.findTagsByAccountId(current_user_id)
        result = [tag.dict() for tag in tag_list]
        return {
            'success': True,
            'message': 'success',
            'data': result
        }, 200

    @jwt_required()
    @notes_ns.doc(description='创建新标签',
                  responses={
                      201: '成功创建标签',
                      400: '请求参数错误',
                      401: '未授权访问',
                      500: '服务器内部错误'
                  })
    @notes_ns.expect(tag_info_request)
    @notes_ns.marshal_with(tag_response)
    def post(self):
        """创建新标签"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='标签名称不能为空')
        args = parser.parse_args()

        current_user_id = get_jwt_identity()

        # 检查标签是否已存在
        existing_tag = Tag.findTagByNameAndAccountId(args['name'], current_user_id)
        if existing_tag:
            return {
                'success': False,
                'message': '标签已存在',
                'data': None
            }, 400

        # 创建新标签
        new_tag = Tag(
            name=args['name'],
            account_id=current_user_id
        )

        new_tag.addTag()

        return {
            'success': True,
            'message': '标签创建成功',
            'data': new_tag.dict()
        }, 201


class TagService(Resource):
    @jwt_required()
    @notes_ns.doc(description='获取指定ID的标签信息',
                  responses={
                      200: '成功获取标签信息',
                      401: '未授权访问',
                      404: '标签不存在',
                      500: '服务器内部错误'
                  })
    @notes_ns.marshal_with(tag_response)
    def get(self, tag_id):
        """获取指定标签详情"""
        current_user_id = get_jwt_identity()
        tag = Tag.findTagById(tag_id)

        if not tag or tag.account_id != current_user_id:
            return {
                'success': False,
                'message': '标签不存在',
                'data': None
            }, 404

        return {
            'success': True,
            'message': 'success',
            'data': tag.dict()
        }, 200

    @jwt_required()
    @notes_ns.doc(description='更新指定ID的标签信息',
                  responses={
                      200: '成功更新标签',
                      400: '请求参数错误',
                      401: '未授权访问',
                      404: '标签不存在',
                      500: '服务器内部错误'
                  })
    @notes_ns.expect(tag_info_request)
    @notes_ns.marshal_with(tag_response)
    def put(self, tag_id):
        """更新指定标签"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='标签名称不能为空')
        args = parser.parse_args()
        print(args)

        current_user_id = int(get_jwt_identity())
        tag = Tag.findTagById(tag_id)
        if not tag or tag.account_id != current_user_id:
            return {
                'success': False,
                'message': '标签不存在',
                'data': None
            }, 404

        # 检查新名称是否与其他标签冲突
        existing_tag = Tag.findTagByNameAndAccountId(args['name'], current_user_id)
        if existing_tag and existing_tag.id != tag_id:
            return {
                'success': False,
                'message': '标签名称已存在',
                'data': None
            }, 400

        # 更新标签
        tag.name = args['name']
        tag.updateTag()

        return {
            'success': True,
            'message': '标签更新成功',
            'data': tag.dict()
        }, 200

    @jwt_required()
    @notes_ns.doc(description='删除指定ID的标签',
                  responses={
                      200: '成功删除标签',
                      401: '未授权访问',
                      404: '标签不存在',
                      500: '服务器内部错误'
                  })
    @notes_ns.marshal_with(api_response)
    def delete(self, tag_id):
        """删除指定标签"""
        current_user_id = int(get_jwt_identity())
        tag = Tag.findTagById(tag_id)

        if not tag or tag.account_id != current_user_id:
            return {
                'success': False,
                'message': '标签不存在',
            }, 404

        tag.deleteTag()

        return {
            'success': True,
            'message': '标签删除成功',
        }, 200