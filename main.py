#!/usr/bin/env python3
# main.py - Mimi 風格金句工具箱
#
# 可用指令：
#   python main.py                   # 隨機印 1 句
#   python main.py 3                 # 隨機印 3 句
#   python main.py add "新金句"       # 新增自訂金句
#   python main.py list              # 列出全部金句
#   python main.py search 關鍵字      # 搜尋含關鍵字的金句
#   python main.py stats             # 顯示金句庫統計
#   python main.py export out.txt    # 匯出全部金句到檔案

from __future__ import annotations

import json
import os
import random
import sys
from pathlib import Path
from typing import Iterable

BASE_DIR = Path(__file__).resolve().parent
QUOTES_FILE = BASE_DIR / "quotes.json"

# 內建的 Mimi 風格金句清單
BUILTIN_QUOTES = [
    "有時候，最強的 alpha 就是耐心等 beta 爛掉。",
    "市場沒在等你成長，但米咪會陪你碎念。",
    "今天不犯蠢不配當交易員，犯完要記得成長。",
    "想抄底？不如抄起來讀書。",
    "樂觀的人看到機會，悲觀的人準備閃人，米咪在旁邊喝豆漿。",
    "你跟程式一樣，偶爾也要重開機。",
    "交易靠系統，人生成長靠碎念。",
    "有 Bug 沒關係，裝死是本事，修 Bug 是本能。",
    "市場不給答案，但米咪可以給金句。",
    "輸一次不丟臉，一直不學才真的該被嘲笑。",
]


def ensure_quotes_file() -> None:
    """若 quotes.json 不存在，建立一個空陣列檔。"""
    if not QUOTES_FILE.exists():
        save_custom_quotes([])


def normalize_quotes(items: Iterable[str]) -> list[str]:
    """清理空白並去掉空字串。"""
    cleaned: list[str] = []
    for item in items:
        text = str(item).strip()
        if text:
            cleaned.append(text)
    return cleaned


def load_custom_quotes() -> list[str]:
    """讀取 quotes.json 檔案，取出自訂金句陣列。"""
    ensure_quotes_file()
    try:
        with QUOTES_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return normalize_quotes(data)
    except Exception:
        print(f"[警告] 讀取 {QUOTES_FILE.name} 失敗，已忽略自訂金句。")
    return []


def save_custom_quotes(quotes: list[str]) -> None:
    """儲存自訂金句到 quotes.json。"""
    with QUOTES_FILE.open("w", encoding="utf-8") as f:
        json.dump(normalize_quotes(quotes), f, ensure_ascii=False, indent=2)


def get_all_quotes() -> list[str]:
    """回傳內建＋自訂金句，並去重。"""
    merged = BUILTIN_QUOTES + load_custom_quotes()
    deduped: list[str] = []
    for quote in merged:
        if quote not in deduped:
            deduped.append(quote)
    return deduped


def add_quote(new_quote: str) -> bool:
    """將新金句加入 quotes.json，若已存在會提示。"""
    new_quote = new_quote.strip()
    if not new_quote:
        print("[錯誤] 請輸入非空白的金句內容。")
        return False

    quotes = load_custom_quotes()
    all_quotes = BUILTIN_QUOTES + quotes
    if new_quote in all_quotes:
        print("[提示] 此金句已存在，不重複加。")
        return False

    quotes.append(new_quote)
    save_custom_quotes(quotes)
    print(f"已新增金句：{new_quote}")
    return True


def list_quotes() -> int:
    """列出全部金句。"""
    all_quotes = get_all_quotes()
    print("\n📚 全部金句：")
    for idx, quote in enumerate(all_quotes, start=1):
        source = "[builtin]" if quote in BUILTIN_QUOTES else "[custom]"
        print(f"{idx:02d}. {source} {quote}")
    print("")
    return 0


def search_quotes(keyword: str) -> int:
    """依關鍵字搜尋金句。"""
    keyword = keyword.strip()
    if not keyword:
        print("[錯誤] 請提供搜尋關鍵字。")
        return 1

    matched = [quote for quote in get_all_quotes() if keyword in quote]
    if not matched:
        print(f"\n🔎 沒有找到包含「{keyword}」的金句。\n")
        return 1

    print(f"\n🔎 搜尋結果（關鍵字：{keyword}）：")
    for idx, quote in enumerate(matched, start=1):
        print(f"{idx:02d}. {quote}")
    print("")
    return 0


def show_stats() -> int:
    """顯示金句庫統計。"""
    custom_quotes = load_custom_quotes()
    total = len(get_all_quotes())
    print("\n📊 金句庫統計：")
    print(f"- 內建金句：{len(BUILTIN_QUOTES)}")
    print(f"- 自訂金句：{len(custom_quotes)}")
    print(f"- 總金句數：{total}")
    print(f"- 儲存位置：{QUOTES_FILE}")
    print("")
    return 0


def export_quotes(output_path: str) -> int:
    """匯出全部金句到指定檔案。"""
    target = (BASE_DIR / output_path).resolve() if not os.path.isabs(output_path) else Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as f:
        for idx, quote in enumerate(get_all_quotes(), start=1):
            f.write(f"{idx:02d}. {quote}\n")
    print(f"已匯出 {len(get_all_quotes())} 句金句到：{target}")
    return 0


def random_quotes(count: int) -> int:
    """隨機印出 N 句金句。"""
    all_quotes = get_all_quotes()
    if not all_quotes:
        print("[警告] 無金句可用！")
        return 1

    count = max(1, count)
    selected_quotes = random.sample(all_quotes, min(count, len(all_quotes)))
    print("\n🐾 米咪金句：")
    for quote in selected_quotes:
        print(quote)
    print("")
    return 0


def print_help() -> int:
    print(__doc__ or "Mimi quote CLI")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) == 1:
        return random_quotes(1)

    command = argv[1]

    if command in {"-h", "--help", "help"}:
        return print_help()
    if command == "add":
        return 0 if add_quote(" ".join(argv[2:])) else 1
    if command == "list":
        return list_quotes()
    if command == "search":
        return search_quotes(" ".join(argv[2:]))
    if command == "stats":
        return show_stats()
    if command == "export":
        if len(argv) < 3:
            print("[錯誤] 請提供匯出檔名，例如：python main.py export out.txt")
            return 1
        return export_quotes(argv[2])

    try:
        return random_quotes(int(command))
    except ValueError:
        print(f"[錯誤] 不支援的指令：{command}\n")
        return print_help()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
