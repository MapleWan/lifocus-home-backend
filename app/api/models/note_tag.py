from . import db

# 多对多关系中间表
note_tags = db.Table('note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.PrimaryKeyConstraint('note_id', 'tag_id')  # 复合主键，防止重复关联
)