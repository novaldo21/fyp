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


def save_data():
    with open("schedules.json", "w", encoding="utf-8") as file:
        json.dump(schedules, file, ensure_ascii=False, indent=4)


# تحديث الوقت والتاريخ
def update_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=now)
    root.after(1000, update_time)


# إضافة مادة جديدة
def add_schedule():
    new_schedule = {
        "id": str(uuid.uuid4()),
        "course": course_entry.get(),
        "time": time_entry.get(),
        "room": room_entry.get(),
        "status": status_entry.get(),
        "day": day_entry.get(),
    }
    schedules.append(new_schedule)
    update_table()
    save_data()
    input_window.destroy()


# حذف مادة
def delete_schedule():
    selected_item = tree.selection()
    if selected_item:
        schedules.pop(tree.index(selected_item[0]))
        update_table()
        save_data()


# تعديل مادة
def edit_schedule():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("تحذير", "يرجى تحديد مادة لتعديلها")
        return
    index = tree.index(selected_item[0])
    openInputWindow()
    course_entry.insert(0, schedules[index]["course"])
    time_entry.insert(0, schedules[index]["time"])
    room_entry.insert(0, schedules[index]["room"])
    status_entry.insert(0, schedules[index]["status"])
    day_entry.insert(0, schedules[index]["day"])
    schedules.pop(index)
    update_table()


def openInputWindow():
    course_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    room_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)
    day_entry.delete(0, tk.END)
    input_window.deiconify()


# تحديث الجدول
def update_table():
    for row in tree.get_children():
        tree.delete(row)
    for idx, _ in enumerate(schedules):
        tree.insert(
            "",
            "end",
            values=(
                schedules[idx]["day"],
                schedules[idx]["course"],
                schedules[idx]["room"],
                schedules[idx]["time"],
                schedules[idx]["status"],
            ),
        )


# البحث في الجدول
def search_schedule():
    query = search_entry.get().strip()
    for row in tree.get_children():
        tree.delete(row)
    for schedule in schedules:
        if query.lower() in schedule["course"].lower():
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

# شريط البحث
search_frame = tk.Frame(root, bg="#292929")
search_frame.pack(fill="x", padx=20, pady=5)

search_entry = tk.Entry(search_frame, font=("Arial", 14))
search_entry.pack(side="left", padx=10, expand=True, fill="x")
search_btn = tk.Button(
    search_frame,
    text="🔍 بحث",
    command=search_schedule,
    font=("Arial", 14),
    fg="black",
    bg="#007BFF",
)
search_btn.pack(side="right", padx=10)

# إطار الجدول
table_frame = tk.Frame(root, bg="#1E1E1E")
table_frame.pack(expand=True, fill="both", padx=30, pady=10)

columns = ("اليوم", "المادة", "القاعة", "الوقت", "الحالة")
columns_en = ("day", "course", "room", "time", "status")


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

delete_btn = tk.Button(
    control_frame,
    text="🗑 حذف المادة",
    command=delete_schedule,
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#AA0000",
    width=15,
)
delete_btn.pack(side="right", padx=10)

edit_btn = tk.Button(
    control_frame,
    text="✏️ تعديل المادة",
    command=edit_schedule,
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#FFC107",
    width=15,
)

edit_btn.pack(side="right", padx=10)

add_btn = tk.Button(
    control_frame,
    text="➕ إضافة مقرر",
    command=openInputWindow,
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#007BFF",
    width=15,
)

add_btn.pack(side="left", padx=10, pady=10)

# نافذة الإدخال

input_window = tk.Toplevel(root)
input_window.title("إضافة مادة جديدة")
input_window.geometry("600x600")
input_window.configure(bg="#292929")
input_window.protocol(
    "WM_DELETE_WINDOW", lambda: input_window.withdraw()
)  # للسماح بإخفاء النافذة

tk.Label(
    input_window, text="المادة", bg="#292929", fg="white", font=("Arial", 14)
).pack(pady=5)
course_entry = tk.Entry(input_window, font=("Arial", 14))
course_entry.pack(pady=5)

tk.Label(input_window, text="الوقت", bg="#292929", fg="white", font=("Arial", 14)).pack(
    pady=5
)
time_entry = tk.Entry(input_window, font=("Arial", 14))
time_entry.pack(pady=5)

tk.Label(input_window, text="اليوم", bg="#292929", fg="white", font=("Arial", 14)).pack(
    pady=5
)
day_entry = tk.Entry(input_window, font=("Arial", 14))
day_entry.pack(pady=5)

tk.Label(
    input_window, text="القاعة", bg="#292929", fg="white", font=("Arial", 14)
).pack(pady=5)
room_entry = tk.Entry(input_window, font=("Arial", 14))
room_entry.pack(pady=5)

tk.Label(
    input_window, text="الحالة", bg="#292929", fg="white", font=("Arial", 14)
).pack(pady=5)
status_entry = tk.Entry(input_window, font=("Arial", 14))
status_entry.pack(pady=5)

add_btn = tk.Button(
    input_window,
    text="➕ إضافة المادة",
    command=add_schedule,
    font=("Arial", 14, "bold"),
    fg="white",
    bg="#007BFF",
    width=20,
)

add_btn.pack(pady=15)


# تحميل البيانات وتحديث الجدول
load_data()
update_table()

# تشغيل التطبيق
root.mainloop()
