from . import db
from datetime import datetime
from ..common.utils import format_datetime_to_json
from .note_tag import note_tags

class Note(db.Model):
    __tablename__ = 'note' # 表名 与 数据库中的表名一一对应
    
    # 主键 id
    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True, comment='主键ID')
    # 类型
    type = db.Column(db.String(20), nullable=False, default='note', comment='笔记类型')
    # 标题
    title = db.Column(db.String(255), comment='笔记标题')
    # 内容
    content = db.Column(db.Text(), comment='笔记内容')
    # 存储文件夹
    folder = db.Column(db.String(255), comment='存储文件夹')
    # 是否已归档
    is_archived = db.Column(db.Boolean(), nullable=False, default=False, comment='是否已归档')
    # 是否在回收站
    is_recycle = db.Column(db.Boolean(), nullable=False, default=False, comment='是否在回收站')
    # 是否分享
    is_share = db.Column(db.Boolean(), nullable=False, default=False, comment='是否分享')
    # 分享密码
    share_password = db.Column(db.String(255), comment='分享密码')
    # 创建时间
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    # 更新时间
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    # 账户ID (外键)
    account_id = db.Column(db.Integer(), db.ForeignKey('user.id'), comment='账户ID')
    
    # 多对多关系：标签
    tags = db.relationship('Tag', secondary=note_tags, back_populates='notes', lazy='dynamic')

    # 新增笔记
    def addNote(self):
        db.session.add(self)
        db.session.commit()

    # 更新笔记
    def updateNote(self):
        db.session.add(self)
        db.session.commit()

    # 删除笔记
    def deleteNote(self):
        db.session.delete(self)
        db.session.commit()

    # 笔记信息
    def dict(self):
        # 获取标签名称列表和ID列表
        tag_names = [tag.name for tag in self.tags]
        tag_ids = [str(tag.id) for tag in self.tags]
        
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'content': self.content,
            'tags': ','.join(tag_names),  # 返回标签名称，而不是ID
            'tagIds': ','.join(tag_ids),  # 返回标签ID
            'folder': self.folder,
            'isArchived': self.is_archived,
            'isRecycle': self.is_recycle,
            'isShare': self.is_share,
            'sharePassword': self.share_password,
            'createdAt': format_datetime_to_json(self.created_at),
            'updatedAt': format_datetime_to_json(self.updated_at),
            'accountId': self.account_id
        }
    
    # 按 ID 查询笔记
    @classmethod
    def findNoteById(cls, id):
        result = db.session.execute(db.select(cls).filter_by(id=id)).first()
        if result:
            return result[0] if hasattr(result, '__getitem__') else result
        return None

    # 按 ID 和 Account ID 查询笔记
    @classmethod
    def findNoteByIdAndAccountId(cls, id, account_id):
        result = db.session.execute(db.select(cls).filter_by(id=id, account_id=account_id)).first()
        if result:
            return result[0] if hasattr(result, '__getitem__') else result
        return None

    # 按 Account ID 查询笔记
    @classmethod
    def findNotesByAccountId(cls, account_id):
        return db.session.query(cls).filter_by(account_id=account_id).all()
    
    # 根据多个属性条件查询笔记
    @classmethod
    def findNotesByMultipleConditions(cls, account_id, **kwargs):
        query = db.session.query(cls).filter_by(account_id=account_id)
        
        # 根据传入的条件动态构建查询
        if 'type' in kwargs and kwargs['type'] is not None:
            query = query.filter_by(type=kwargs['type'])
        if 'content' in kwargs and kwargs['content'] is not None:
            query = query.filter(cls.content.like(f"%{kwargs['content']}%"))
        if 'title' in kwargs and kwargs['title'] is not None:
            query = query.filter(cls.title.like(f"%{kwargs['title']}%"))
        if 'tags' in kwargs and kwargs['tags'] is not None:
            # 根据标签名称查询笔记
            tag_names = [tag.strip() for tag in kwargs['tags'].split(',') if tag.strip()]
            if tag_names:
                # 使用多对多关系进行查询
                query = query.join(cls.tags).filter(Tag.name.in_(tag_names))
        if 'folder' in kwargs and kwargs['folder'] is not None:
            query = query.filter_by(folder=kwargs['folder'])
        if 'is_archived' in kwargs and kwargs['is_archived'] is not None:
            query = query.filter_by(is_archived=kwargs['is_archived'])
        if 'is_recycle' in kwargs and kwargs['is_recycle'] is not None:
            query = query.filter_by(is_recycle=kwargs['is_recycle'])
        if 'is_share' in kwargs and kwargs['is_share'] is not None:
            query = query.filter_by(is_share=kwargs['is_share'])
            
        return query.all()

# 导入Tag模型以避免循环导入
from .tag import Tag