import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox
import json
from data import Safty_Data
import random
import string
from os import getenv
from dotenv import load_dotenv
import pyperclip
load_dotenv()


# 列名的字符串常量
COLUMN_1 = "平台"
COLUMN_2 = "帳號"
COLUMN_3 = "密碼"
COLUMN_4 = "備註"

database = Safty_Data('data.db', getenv('password'))

data = []

# 創建主視窗
root = tk.Tk()
root.title("密碼資料庫")

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=13)
root.option_add("*Font", default_font)

tree_style = ttk.Style()
tree_style.configure("Treeview", background="white", foreground="black")  # 设置表格背景和前景颜色
tree_style.configure("Treeview.Heading", font=("Arial", 12, "bold"))  # 设置表头的字体和样式
tree_style.map("Treeview", background=[("selected", "#A3A3A3")])  # 设置选中行的背景颜色


# 創建表格
tree = ttk.Treeview(root, columns=(COLUMN_1, COLUMN_2, COLUMN_3, COLUMN_4), show="headings")
tree.heading(COLUMN_1, text=COLUMN_1)
tree.heading(COLUMN_2, text=COLUMN_2)
tree.heading(COLUMN_3, text=COLUMN_3)
tree.heading(COLUMN_4, text=COLUMN_4)
tree.pack()

def load_data():
    global data, tree
    data = database.load(entry6.get())
    tree.delete(*tree.get_children())
        # 初始化表格中的數據
    for row_data in data:
        tree.insert('', 'end', values=row_data)

# 創建一個框架來容納輸入框和添加按鈕
input_frame = tk.Frame(root)
input_frame.pack(pady=10)  # 增加垂直間距

# 創建輸入框
label1 = tk.Label(input_frame, text=f"{COLUMN_1}:")
label1.grid(row=0, column=0, padx=5)  # 增加水平間距
entry1 = tk.Entry(input_frame)
entry1.grid(row=0, column=1, padx=5)  # 增加水平間距

label2 = tk.Label(input_frame, text=f"{COLUMN_2}:")
label2.grid(row=0, column=2, padx=5)  # 增加水平間距
entry2 = tk.Entry(input_frame)
entry2.grid(row=0, column=3, padx=5)  # 增加水平間距

label3 = tk.Label(input_frame, text=f"{COLUMN_3}:")
label3.grid(row=0, column=4, padx=5)  # 增加水平間距
entry3 = tk.Entry(input_frame)
entry3.grid(row=0, column=5, padx=5)  # 增加水平間距

label4 = tk.Label(input_frame, text=f"{COLUMN_4}:")
label4.grid(row=0, column=6, padx=5)  # 增加水平間距
entry4 = tk.Entry(input_frame)
entry4.grid(row=0, column=7, padx=5)  # 增加水平間距

def on_entry_change(*args):
    database.password = entry5.get()
    load_data()

label5 = tk.Label(input_frame, text=f"密碼")
label5.grid(row=1, column=0, padx=5)  # 增加水平間距
entry_text = tk.StringVar()
entry_text.trace("w", on_entry_change)
entry5 = tk.Entry(input_frame, show="*", textvariable=entry_text)
entry5.grid(row=1, column=1, padx=5)  # 增加水平間距

def on_keyword_change(*args):
    load_data()

label6 = tk.Label(input_frame, text=f"關鍵字")
label6.grid(row=1, column=3, padx=5)  # 增加水平間距
entry_text2 = tk.StringVar()
entry_text2.trace("w", on_keyword_change)
entry6 = tk.Entry(input_frame, show="*", textvariable=entry_text2)
entry6.grid(row=1, column=4, padx=5)  # 增加水平間距

def set_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    entry_text.set(password)
    pyperclip.copy(password)
    messagebox.showinfo('密碼隨機生成', '密碼已儲存到剪貼簿，請妥善保存')
    

# 添加行的按鈕
random_password_button = tk.Button(input_frame, text="隨機生成", command=set_random_password)
random_password_button.grid(row=1, column=2, padx=5)  # 增加水平間距

# 添加行的函數
def add_row():
    if entry5.get().strip() == '': return
    value1 = entry1.get().strip()
    value2 = entry2.get().strip()
    value3 = entry3.get().strip()
    value4 = entry4.get().strip()

    if value1 and value2 and value3:  # 檢查是否都有輸入值
        database.add(value1, value2, value3, value4)
    else:
        # 輸入欄位為空或只有空白字符，不儲存資料
        entry1.delete(0, 'end')
        entry2.delete(0, 'end')
        entry3.delete(0, 'end')
        entry4.delete(0, 'end')

    load_data()

# 刪除行的函數
def delete_row():
    for id in tree.selection():
        selected = tree.item(id)
        selected.get("values")[0]
        database.delete(selected.get("values")[0], selected.get("values")[1])
    
    load_data()

# 添加行的按鈕
add_button = tk.Button(input_frame, text="添加行", command=add_row)
add_button.grid(row=0, column=8, padx=5)  # 增加水平間距

# 刪除行的按鈕
delete_button = tk.Button(input_frame, text="刪除選定行", command=delete_row)
delete_button.grid(row=0, column=9, padx=5)  # 增加水平間距

load_data()

# 啟動應用程序的主迴圈
root.mainloop()
