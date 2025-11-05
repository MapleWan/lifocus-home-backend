from . import db
from datetime import datetime
from ..common.utils import format_datetime_to_json

class Timeline(db.Model):
    __tablename__ = 'timeline'
    
    # 主键 id
    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True, comment='主键ID')
    # 事件标题
    title = db.Column(db.String(255), nullable=False, comment='事件标题')
    # 事件描述
    description = db.Column(db.Text(), comment='事件描述')
    # 事件类型（work, study, rest, exercise, social, other）
    event_type = db.Column(db.String(50), nullable=False, default='other', comment='事件类型')
    # 事件开始时间
    start_time = db.Column(db.DateTime(), nullable=False, comment='事件开始时间')
    # 事件结束时间
    end_time = db.Column(db.DateTime(), comment='事件结束时间')
    # 事件持续时长（分钟）
    duration = db.Column(db.Integer(), comment='事件持续时长（分钟）')
    # 事件标签（用于分类和筛选）
    tags = db.Column(db.String(255), comment='事件标签，逗号分隔')
    # 重要性级别（1-5，5为最重要）
    importance = db.Column(db.Integer(), nullable=False, default=3, comment='重要性级别')
    # 完成状态
    is_completed = db.Column(db.Boolean(), nullable=False, default=True, comment='是否已完成')
    # 是否已包含在日报中
    is_summarized = db.Column(db.Boolean(), nullable=False, default=False, comment='是否已总结到日报')
    # 创建时间
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, comment='创建时间')
    # 更新时间
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    # 账户ID (外键)
    account_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False, comment='账户ID')

    # 新增时间线事件
    def addTimeline(self):
        db.session.add(self)
        db.session.commit()

    # 更新时间线事件
    def updateTimeline(self):
        db.session.add(self)
        db.session.commit()

    # 删除时间线事件
    def deleteTimeline(self):
        db.session.delete(self)
        db.session.commit()

    # 计算事件时长
    def calculate_duration(self):
        if self.start_time and self.end_time:
            duration_delta = self.end_time - self.start_time
            self.duration = int(duration_delta.total_seconds() / 60)  # 转换为分钟
        return self.duration

    # 时间线事件信息
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'eventType': self.event_type,
            'startTime': format_datetime_to_json(self.start_time),
            'endTime': format_datetime_to_json(self.end_time) if self.end_time else None,
            'duration': self.duration,
            'tags': self.tags,
            'importance': self.importance,
            'isCompleted': self.is_completed,
            'isSummarized': self.is_summarized,
            'createdAt': format_datetime_to_json(self.created_at),
            'updatedAt': format_datetime_to_json(self.updated_at),
            'accountId': self.account_id
        }

    # 按 ID 查询时间线事件
    @classmethod
    def findTimelineById(cls, id):
        result = db.session.execute(db.select(cls).filter_by(id=id)).first()
        if result:
            return result[0] if hasattr(result, '__getitem__') else result
        return None

    # 按 ID 和 Account ID 查询时间线事件
    @classmethod
    def findTimelineByIdAndAccountId(cls, id, account_id):
        result = db.session.execute(db.select(cls).filter_by(id=id, account_id=account_id)).first()
        if result:
            return result[0] if hasattr(result, '__getitem__') else result
        return None

    # 按 Account ID 查询时间线事件
    @classmethod
    def findTimelinesByAccountId(cls, account_id):
        return db.session.query(cls).filter_by(account_id=account_id).all()

    # 按日期范围查询时间线事件
    @classmethod
    def findTimelinesByDateRange(cls, account_id, start_date, end_date):
        return db.session.query(cls).filter(
            cls.account_id == account_id,
            cls.start_time >= start_date,
            cls.start_time <= end_date
        ).order_by(cls.start_time.asc()).all()

    # 查询未总结的时间线事件
    @classmethod
    def findUnsummarizedTimelines(cls, account_id, date):
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        return db.session.query(cls).filter(
            cls.account_id == account_id,
            cls.start_time >= start_of_day,
            cls.start_time <= end_of_day,
            cls.is_summarized == False
        ).order_by(cls.start_time.asc()).all()

    # 标记事件为已总结
    def mark_as_summarized(self):
        self.is_summarized = True
        self.updateTimeline()