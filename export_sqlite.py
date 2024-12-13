import sqlite3

# 連接到 SQLite 資料庫
conn = sqlite3.connect('db_final.db')

# 導出資料庫內容
with open('db_dump.sql', 'w', encoding='utf-8') as f:  # 指定 UTF-8 編碼
    for line in conn.iterdump():
        f.write(f'{line}\n')

conn.close()
print("Database dump exported to db_dump.sql")
