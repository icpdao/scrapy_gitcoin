from dataclasses import dataclass, field
from typing import List


@dataclass
class BountiesItem:

    csv_meta = {
        "name": "bounties",
        "keys": ['item_id', 'title', 'description', 'categories', 'keywords', 'value_in_usdt', 'token_name', 'value_in_token', 'expires_date', 'status', 'issue_type', 'project_type', 'time_commitment', 'experience_level']
    }

    item_id: int = "" # id
    title: str = "" # 标题
    description: str = "" # 项目描述
    categories: List[str] = field(default_factory=list) # 标签
    keywords: List[str] = field(default_factory=list) # 技能标签
    value_in_usdt: str = 0 # 价格
    token_name: str = ""
    value_in_token: str = ""
    expires_date: str = ""  # expires_date
    status: str = "" # 状态
    issue_type: str = ""
    project_type: str = ""
    time_commitment: str = ""
    experience_level: str = ""

    def to_csv_row(self):
        return [
            self.item_id, 
            self.title, 
            self.description, 
            ",".join(self.categories),
            ",".join(self.keywords),
            self.value_in_usdt,
            self.token_name,
            self.value_in_token,
            self.expires_date,
            self.status,
            self.issue_type,
            self.project_type,
            self.time_commitment,
            self.experience_level
        ]
