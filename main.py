# main.py - Mimi 風格金句隨機顯示器
# 執行方式：python main.py N（N 可選，一次要印幾句）

import random
import sys

# 內建的 Mimi 風格金句清單
mimi_quotes = [
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

# 取得命令列參數 N，預設為 1
try:
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if count < 1:
        count = 1
except ValueError:
    count = 1

selected_quotes = random.sample(mimi_quotes, min(count, len(mimi_quotes)))

print("\n🐾 米咪金句：")
for q in selected_quotes:
    print(q)
print("")
