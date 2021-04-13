from dataclasses import dataclass, field
from typing import List


@dataclass
class BountiesItem:

    csv_meta = {
        "name": "bounties",
        "keys": ['item_id', 'title', 'description', 'categories', 'keywords', 'value_in_usdt', 'token_name', 'value_in_token', 'expires_date', 'status', 'issue_type', 'project_type', 'time_commitment', 'experience_level', 'url']
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
    url: str = ""

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
            self.experience_level,
            self.url
        ]


@dataclass
class GrantsItem:

    csv_meta = {
        "name": "grants",
        "keys": ['item_id', 'title', 'description', 'reference_url', 'twitter', 'github_project_url', 'region', 'tenants', 'amount_received', 'url']
    }

    item_id: int = "" # id
    title: str = "" # 标题
    description: str = ""
    reference_url: str = ""
    twitter: str = ""
    github_project_url: str = ""
    region: str = ""
    tenants: List[str] = field(default_factory=list)
    amount_received: str = ""
    url: str = ""

    def to_csv_row(self):
        return [
            self.item_id, 
            self.title, 
            self.description,
            self.reference_url, 
            self.twitter,
            self.github_project_url,
            self.region,
            ",".join(self.tenants),
            self.amount_received,
            self.url
        ]
