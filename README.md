# Mimi Demo Repo

一個用 Python 寫的 **Mimi 金句 CLI 小工具**。

目前功能：
- 隨機抽一句或多句金句
- 新增自訂金句到 `quotes.json`
- 列出全部金句
- 關鍵字搜尋
- 顯示金句庫統計
- 匯出全部金句到文字檔
- 基本自動化測試（`test_main.py`）

## 快速開始

```bash
python3 main.py
python3 main.py 3
python3 main.py add "保持紀律，別跟爛單談戀愛。"
python3 main.py list
python3 main.py search 市場
python3 main.py stats
python3 main.py export exports/quotes.txt
```

## 測試

這個專案目前使用 Python 內建 `unittest`，不用另外安裝套件：

```bash
python3 -m unittest -v
```

## 專案檔案

- `main.py`：主程式
- `quotes.json`：自訂金句庫
- `test_main.py`：CLI 基本測試

之後可以再往下擴成 API、TUI、Web UI 或金句分類系統。
