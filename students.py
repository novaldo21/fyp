import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import uuid

# بيانات الجدول
schedules = []


def load_data():
    global schedules
    try:
        with open("schedules.json", "r", encoding="utf-8") as file:
            schedules = json.load(file)
    except FileNotFoundError:
        schedules = []


# تحديث الوقت والتاريخ
def update_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=now)
    root.after(1000, update_time)


# تحديث الجدول
def update_table():
    days = ["الاثنين", "الثلاثاء", "الاربعاء", "الخميس", "الجمعة", "السبت", "الاحد"]
    dayIndex = datetime.today().weekday()
    query = days[dayIndex]
    for row in tree.get_children():
        tree.delete(row)
    for schedule in schedules:
        if query.lower() in schedule["day"].lower():
            tree.insert(
                "",
                "end",
                values=(
                    schedule["day"],
                    schedule["course"],
                    schedule["room"],
                    schedule["time"],
                    schedule["status"],
                ),
            )


# إنشاء نافذة التطبيق
root = tk.Tk("اضافة مقررالى الجدول")
root.title("نظام إدارة جدول المحاضرات")
root.geometry("1080x600")
root.configure(bg="#1E1E1E", width=860)

# إطار العنوان والوقت
top_frame = tk.Frame(root, bg="#292929", pady=15)
top_frame.pack(fill="x")

label = tk.Label(
    top_frame,
    text="📅 جدول المحاضرات المتدربين مبنى الحاسب",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#292929",
)
label.pack(side="left", padx=20)

time_label = tk.Label(top_frame, font=("Arial", 14), fg="lightgray", bg="#292929")
time_label.pack(side="right", padx=20)
update_time()

# إطار الجدول
table_frame = tk.Frame(root, bg="#1E1E1E")
table_frame.pack(expand=True, fill="both", padx=30, pady=10)

columns = ("اليوم", "المادة", "القاعة", "الوقت", "الحالة")

tree = ttk.Treeview(table_frame, columns=columns, show="headings")
style = ttk.Style()
style.configure(
    "Treeview", font=("Arial", 14), rowheight=30, background="#333", foreground="white"
)
style.configure(
    "Treeview.Heading",
    font=("Arial", 16, "bold"),
    background="#444",
    foreground="black",
)

for idx, col in enumerate(columns):
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(expand=True, fill="both")

# إطار التحكم
control_frame = tk.Frame(root, bg="#292929", pady=10)
control_frame.pack(fill="x")


# تحميل البيانات وتحديث الجدول
load_data()
update_table()

# تشغيل التطبيق
root.mainloop()
