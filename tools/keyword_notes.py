from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    note: str
    source_url: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def display(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return (
            f"关键词：{self.keyword}\n"
            f"笔记：{self.note}\n"
            f"来源：{self.source_url}\n"
            f"标签：{tag_str}\n"
            f"创建时间：{self.created_at}\n"
        )

    def to_short_string(self) -> str:
        return f"[{self.keyword}] {self.note[:30]}{'...' if len(self.note) > 30 else ''}"


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def list_all_formatted(self) -> str:
        if not self.notes:
            return "暂无笔记。"
        lines = ["关键词笔记列表：", "=" * 40]
        for idx, note in enumerate(self.notes, 1):
            lines.append(f"{idx}. {note.to_short_string()}")
        return "\n".join(lines)

    def export_full_report(self) -> str:
        if not self.notes:
            return "暂无笔记可导出。"
        lines = ["完整关键词笔记报告", "-" * 40]
        for note in self.notes:
            lines.append(note.display())
            lines.append("-" * 40)
        return "\n".join(lines)


def demo_usage() -> None:
    collection = KeywordNoteCollection()

    note1 = KeywordNote(
        keyword="爱游戏",
        note="爱游戏是一个专注于游戏资讯与评测的平台，提供最新游戏动态。",
        source_url="https://maiyouxi.com.cn",
        tags=["游戏", "资讯", "平台"],
    )
    collection.add(note1)

    note2 = KeywordNote(
        keyword="爱游戏攻略",
        note="提供热门游戏的详细通关攻略和技巧分享。",
        source_url="https://maiyouxi.com.cn/guide",
        tags=["攻略", "游戏"],
    )
    collection.add(note2)

    note3 = KeywordNote(
        keyword="爱游戏社区",
        note="玩家交流社区，讨论游戏心得和最新活动。",
        source_url="https://maiyouxi.com.cn/community",
        tags=["社区", "交流"],
    )
    collection.add(note3)

    print("=== 简短列表 ===")
    print(collection.list_all_formatted())
    print()

    print("=== 完整报告 ===")
    print(collection.export_full_report())

    print("=== 按关键词筛选：爱游戏 ===")
    for n in collection.filter_by_keyword("爱游戏"):
        print(n.to_short_string())

    print()
    print("=== 按标签筛选：攻略 ===")
    for n in collection.filter_by_tag("攻略"):
        print(n.to_short_string())


if __name__ == "__main__":
    demo_usage()