from . import db
from datetime import datetime
from ..common.utils import format_datetime_to_json

class Tag(db.Model):
    __tablename__ = 'tag'  # 表名 与 数据库中的表名一一对应
    
    # 主键 id
    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True, comment='主键ID')
    # 标签名称
    name = db.Column(db.String(100), nullable=False, comment='标签名称')
    # 创建时间
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    # 更新时间
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    # 账户ID (外键)
    account_id = db.Column(db.Integer(), db.ForeignKey('user.id'), comment='账户ID')

    # 新增标签
    def addTag(self):
        db.session.add(self)
        db.session.commit()

    # 更新标签
    def updateTag(self):
        db.session.add(self)
        db.session.commit()

    # 删除标签
    def deleteTag(self):
        db.session.delete(self)
        db.session.commit()

    # 标签信息
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'createdAt': format_datetime_to_json(self.created_at),
            'updatedAt': format_datetime_to_json(self.updated_at),
            'accountId': self.account_id
        }
    
    # 按 ID 查询标签
    @classmethod
    def findTagById(cls, id):
        result = db.session.execute(db.select(cls).filter_by(id=id)).first()
        if result:
            return result[0] if hasattr(result, '__getitem__') else result
        return None

    # 按名称和 Account ID 查询标签
    @classmethod
    def findTagByNameAndAccountId(cls, name, account_id):
        result = db.session.execute(db.select(cls).filter_by(name=name, account_id=account_id)).first()
        if result:
            return result[0] if hasattr(result, '__getitem__') else result
        return None

    # 按 Account ID 查询标签
    @classmethod
    def findTagsByAccountId(cls, account_id):
        return db.session.query(cls).filter_by(account_id=account_id).all()