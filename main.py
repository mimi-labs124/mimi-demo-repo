# main.py - Mimi 風格金句隨機顯示器（支援自訂金句）
# 執行方式：
#   python main.py N                # 隨機印 N 句
#   python main.py add "新金句"       # 新增自訂金句

import random
import sys
import json
import os

# 內建的 Mimi 風格金句清單
builtin_quotes = [
    "有時候，最強的 alpha 就是耐心等 beta 爛掉。",
    "市場沒在等你成長，但米咪會陪你碎念。",
    "今天不犯蠢不配當交易員，犯完要記得成長。",
    "想抄底？不如抄起來讀書。",
    "樂觀的人看到機會，悲觀的人準備閃人，米咪在旁邊喝豆漿。",
    "你跟程式一樣，偶爾也要重開機。",
    "交易靠系統，人生成長靠碎念。",
    "有 Bug 沒關係，裝死是本事，修 Bug 是本能。",
    "市場不給答案，但米咪可以給金句。",
    "輸一次不丟臉，一直不學才真的該被嘲笑。"
]

QUOTES_FILE = "quotes.json"

def load_custom_quotes():
    """讀取 quotes.json 檔案，取出自訂金句陣列"""
    if os.path.exists(QUOTES_FILE):
        try:
            with open(QUOTES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            print(f"[警告] 讀取 {QUOTES_FILE} 失敗，已忽略自訂金句。")
    return []

def save_custom_quotes(quotes):
    """儲存自訂金句到 quotes.json"""
    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

def add_quote(new_quote):
    """將新金句加入 quotes.json，若已存在會提示。"""
    quotes = load_custom_quotes()
    if new_quote in builtin_quotes or new_quote in quotes:
        print("[提示] 此金句已存在，不重複加。")
        return False
    quotes.append(new_quote)
    save_custom_quotes(quotes)
    print(f"已新增金句：{new_quote}")
    return True

if __name__ == "__main__":
    # 若參數為 add，預期格式：python main.py add "新金句"
    if len(sys.argv) > 2 and sys.argv[1] == "add":
        new_quote = sys.argv[2].strip()
        if new_quote:
            add_quote(new_quote)
        else:
            print("[錯誤] 請輸入非空白的金句內容。")
        sys.exit(0)

    # 正常流程：隨機印 N 句
    try:
        count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
        if count < 1:
            count = 1
    except ValueError:
        count = 1
    all_quotes = builtin_quotes + load_custom_quotes()
    if not all_quotes:
        print("[警告] 無金句可用！")
        sys.exit(1)
    selected_quotes = random.sample(all_quotes, min(count, len(all_quotes)))
    print("\n🐾 米咪金句：")
    for q in selected_quotes:
        print(q)
    print("")
