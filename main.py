import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import share_data
from wifi_analyze import analyze_wifi
from bt_analyze import analyze_bt
from gps_analyze import analyze_gps

def on_button_click():
    print("按钮被点击了！")

root = tk.Tk()
root.title("无线分析")
root.geometry("960x600")  # 设置窗口大小

# 菜单栏
menubar = tk.Menu(root)
root.config(menu=menubar)

wifi_menu = tk.Menu(menubar, tearoff=0)
bt_menu = tk.Menu(menubar, tearoff=0)
gps_menu = tk.Menu(menubar, tearoff=0)

menubar.add_cascade(label="WiFi", menu=wifi_menu)
menubar.add_cascade(label="BT", menu=bt_menu)
menubar.add_cascade(label="GPS", menu=gps_menu)

wifi_menu.add_cascade(label="WiFi2")
bt_menu.add_cascade(label="BT2")
gps_menu.add_cascade(label="GPS2")

wifi3_menu = tk.Menu(wifi_menu, tearoff=0)
wifi_menu.add_cascade(label="WiFi3", menu=wifi3_menu)
wifi3_menu.add_command(label="WiFi3-1", command=on_button_click)

file_frame = tk.Frame(root)
file_frame.pack(padx=20, pady=10, fill='x')
file_label = tk.Label(file_frame, text="文件:")
file_label.pack(side='left')
def browse_file():
    file_path = filedialog.askopenfilename(title="选择文件")
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
file_btn = tk.Button(file_frame, text="浏览", command=browse_file)
file_btn.pack(side='left', padx=(0, 5))
file_entry = tk.Entry(file_frame, width=70)
file_entry.pack(side='left', fill='x', expand=True)

dir_frame = tk.Frame(root)
dir_frame.pack(padx=20, pady=10, fill='x')
dir_label = tk.Label(dir_frame, text="目录:")
dir_label.pack(side='left')
def browse_dir():
    dir_path = filedialog.askdirectory(title="选择目录")
    if dir_path:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, dir_path)
dir_btn = tk.Button(dir_frame, text="浏览", command=browse_dir)
dir_btn.pack(side='left')
dir_entry = tk.Entry(dir_frame, width=70)
dir_entry.pack(side='left', padx=5, fill='x', expand=True)
share_data.dir_frame = dir_frame

# BT 页：下拉选择框（平台）
os_var = tk.StringVar(value="Android")
os_frame = tk.Frame(root)
os_frame.pack(pady=10, anchor='w')
tk.Label(os_frame, text="平台:").pack(side='left', padx=(20, 8))
os_combo = ttk.Combobox(os_frame, textvariable=os_var, values=["Android", "Linux", "RTOS", "unknown"], state="readonly", width=12)
os_combo.pack(side='left')

def get_os_combo_selection():
    """返回 os_combo 当前选择，并在 log 中显示"""
    value = os_var.get()
    share_data.os_selection = value
    print(f"[OS选择] 当前平台: {value}")
    return value

os_combo.bind("<<ComboboxSelected>>", lambda e: get_os_combo_selection())

os_combo_index = os_combo.current()
share_data.os_selection = os_var.get()
print(f"[OS选择] 当前平台索引: {os_combo_index}")

# 三个 sheet 页（标签页）
notebook = ttk.Notebook(root)
notebook.pack(padx=20, pady=10, fill='both', expand=True)

sheet_wifi = tk.Frame(notebook, padx=20, pady=20)
sheet_bt = tk.Frame(notebook, padx=20, pady=20)
sheet_gps = tk.Frame(notebook, padx=20, pady=20)

notebook.add(sheet_wifi, text="WiFi")
notebook.add(sheet_bt, text="BT")
notebook.add(sheet_gps, text="GPS")

# WiFi sheet 页：多选框及选中状态（左列 + 右列）
tk.Label(sheet_wifi, text="WiFi 日志分析", font=("", 12)).pack(pady=10)
wifi_check_container = tk.Frame(sheet_wifi)
wifi_check_container.pack(pady=10, anchor='w')

wifi_check_vars = []  # 左列 4 个多选框的勾选状态
os_group = ttk.LabelFrame(wifi_check_container, text="OS")
os_group.pack(side='left', padx=(0, 40))
wifi_check_frame = tk.Frame(os_group)
wifi_check_frame.pack(padx=8, pady=8)
wifi_check_labels = ["Android", "Linux", "RTOS", "unknown"]
for i in range(4):
    var = tk.BooleanVar(value=False)
    wifi_check_vars.append(var)
    cb = tk.Checkbutton(wifi_check_frame, text=wifi_check_labels[i], variable=var, anchor='w')
    cb.pack(anchor='w', pady=2)

wifi_check_vars_right = []  # 右列 4 个多选框的勾选状态
wifi_check_frame_right = tk.Frame(wifi_check_container, width=480, height=100)
wifi_check_frame_right.pack(side='left')
wifi_check_frame_right.pack_propagate(False)  # 保持宽高，否则 place 子控件时框架会缩成 0
##each layer name in os
wifi_check_labels_right_android = ["Android0", "Android1", "Android2", "Android3", "ALL"]
wifi_check_labels_right_linux = ["Linux0", "Linux1", "Linux2", "Linux3", "ALL"]
wifi_check_labels_right_rtos = ["RTOS0", "RTOS1", "RTOS2", "RTOS3", "ALL"]
wifi_check_labels_right_unknown = ["unknown0", "unknown1", "unknown2", "unknown3", "ALL"]

# 用 place(x=..., y=...) 指定每个 Checkbutton 的位置（像素）
android_check_vars = []
linux_check_vars = []
rtos_check_vars = []
unknown_check_vars = []
# 第 106 行：Android 列，位置 (x, y) 可改
for i in range(4):
    var = tk.BooleanVar(value=False)
    android_check_vars.append(var)
    cb = tk.Checkbutton(wifi_check_frame_right, text=wifi_check_labels_right_android[i], variable=var, anchor='w')
    cb.place(x=0, y=i * 24)  # Android 列：x=0 同一列，y 每行 24 像素

# 第 112 行：Linux 列
for i in range(4):
    var = tk.BooleanVar(value=False)
    linux_check_vars.append(var)
    cb = tk.Checkbutton(wifi_check_frame_right, text=wifi_check_labels_right_linux[i], variable=var, anchor='w')
    cb.place(x=120, y=i * 24)  # x=120 与 Android 列错开

for i in range(4):
    var = tk.BooleanVar(value=False)
    rtos_check_vars.append(var)
    cb = tk.Checkbutton(wifi_check_frame_right, text=wifi_check_labels_right_rtos[i], variable=var, anchor='w')
    cb.place(x=240, y=i * 24)

for i in range(4):
    var = tk.BooleanVar(value=False)
    unknown_check_vars.append(var)
    cb = tk.Checkbutton(wifi_check_frame_right, text=wifi_check_labels_right_unknown[i], variable=var, anchor='w')
    cb.place(x=360, y=i * 24)

# 打印每个 checkbox 的勾选状况
def get_and_log_wifi_check_state():
    print("--- 左列（平台） ---")
    for i, label in enumerate(wifi_check_labels):
        checked = wifi_check_vars[i].get()
        print(f"  {label}: {'勾选' if checked else '未勾选'}")
    print("--- 右列 Android ---")
    for i, label in enumerate(wifi_check_labels_right_android[:4]):
        checked = android_check_vars[i].get()
        print(f"  {label}: {'勾选' if checked else '未勾选'}")
    print("--- 右列 Linux ---")
    for i, label in enumerate(wifi_check_labels_right_linux[:4]):
        checked = linux_check_vars[i].get()
        print(f"  {label}: {'勾选' if checked else '未勾选'}")
    print("--- 右列 RTOS ---")
    for i, label in enumerate(wifi_check_labels_right_rtos[:4]):
        checked = rtos_check_vars[i].get()
        print(f"  {label}: {'勾选' if checked else '未勾选'}")
    print("--- 右列 unknown ---")
    for i, label in enumerate(wifi_check_labels_right_unknown[:4]):
        checked = unknown_check_vars[i].get()
        print(f"  {label}: {'勾选' if checked else '未勾选'}")

# WiFi 页右侧：文本输入 + 列表（可删除、清空）
wifi_right_frame = tk.Frame(sheet_wifi)
wifi_right_frame.pack(side='right', padx=20, pady=10, fill='both', expand=True)
wifi_text_list = []

def wifi_add_text():
    s = wifi_entry.get().strip()
    if s:
        wifi_text_list.append(s)
        wifi_listbox.insert(tk.END, s)
        wifi_entry.delete(0, tk.END)

def wifi_delete_selected():
    sel = wifi_listbox.curselection()
    if sel:
        i = sel[0]
        wifi_listbox.delete(i)
        wifi_text_list.pop(i)

def wifi_clear_list():
    wifi_listbox.delete(0, tk.END)
    wifi_text_list.clear()

wifi_entry_frame = tk.Frame(wifi_right_frame)
wifi_entry_frame.pack(fill='x', pady=(0, 6))
wifi_entry = tk.Entry(wifi_entry_frame, width=24)
wifi_entry.pack(side='left', padx=(0, 8))
tk.Button(wifi_entry_frame, text="Add", command=wifi_add_text, width=6).pack(side='left')
tk.Label(wifi_right_frame, text="已插入列表:").pack(anchor='w')
wifi_listbox = tk.Listbox(wifi_right_frame, height=8, width=30)
wifi_listbox.pack(fill='both', expand=True, pady=4)
wifi_list_btn_frame = tk.Frame(wifi_right_frame)
wifi_list_btn_frame.pack(fill='x')
tk.Button(wifi_list_btn_frame, text="删除选中", command=wifi_delete_selected, width=8).pack(side='left', padx=(0, 8))
tk.Button(wifi_list_btn_frame, text="清空", command=wifi_clear_list, width=6).pack(side='left')

# BT 页右侧：文本输入 + 列表（可删除、清空）
bt_right_frame = tk.Frame(sheet_bt)
bt_right_frame.pack(side='right', padx=20, pady=10, fill='both', expand=True)
bt_text_list = []  # 存储插入的文本列表

def bt_add_text():
    s = bt_entry.get().strip()
    if s:
        bt_text_list.append(s)
        bt_listbox.insert(tk.END, s)
        bt_entry.delete(0, tk.END)

def bt_delete_selected():
    sel = bt_listbox.curselection()
    if sel:
        i = sel[0]
        bt_listbox.delete(i)
        bt_text_list.pop(i)

def bt_clear_list():
    bt_listbox.delete(0, tk.END)
    bt_text_list.clear()

bt_entry_frame = tk.Frame(bt_right_frame)
bt_entry_frame.pack(fill='x', pady=(0, 6))
bt_entry = tk.Entry(bt_entry_frame, width=24)
bt_entry.pack(side='left', padx=(0, 8))
tk.Button(bt_entry_frame, text="Add", command=bt_add_text, width=6).pack(side='left')
tk.Label(bt_right_frame, text="已插入列表:").pack(anchor='w')
bt_listbox = tk.Listbox(bt_right_frame, height=8, width=30)
bt_listbox.pack(fill='both', expand=True, pady=4)
bt_btn_frame = tk.Frame(bt_right_frame)
bt_btn_frame.pack(fill='x')
tk.Button(bt_btn_frame, text="删除选中", command=bt_delete_selected, width=8).pack(side='left', padx=(0, 8))
tk.Button(bt_btn_frame, text="清空", command=bt_clear_list, width=6).pack(side='left')

# GPS 页右侧：文本输入 + 列表（可删除、清空）
gps_right_frame = tk.Frame(sheet_gps)
gps_right_frame.pack(side='right', padx=20, pady=10, fill='both', expand=True)
gps_text_list = []

def gps_add_text():
    s = gps_entry.get().strip()
    if s:
        gps_text_list.append(s)
        gps_listbox.insert(tk.END, s)
        gps_entry.delete(0, tk.END)

def gps_delete_selected():
    sel = gps_listbox.curselection()
    if sel:
        i = sel[0]
        gps_listbox.delete(i)
        gps_text_list.pop(i)

def gps_clear_list():
    gps_listbox.delete(0, tk.END)
    gps_text_list.clear()

gps_entry_frame = tk.Frame(gps_right_frame)
gps_entry_frame.pack(fill='x', pady=(0, 6))
gps_entry = tk.Entry(gps_entry_frame, width=24)
gps_entry.pack(side='left', padx=(0, 8))
tk.Button(gps_entry_frame, text="Add", command=gps_add_text, width=6).pack(side='left')
tk.Label(gps_right_frame, text="已插入列表:").pack(anchor='w')
gps_listbox = tk.Listbox(gps_right_frame, height=8, width=30)
gps_listbox.pack(fill='both', expand=True, pady=4)
gps_btn_frame = tk.Frame(gps_right_frame)
gps_btn_frame.pack(fill='x')
tk.Button(gps_btn_frame, text="删除选中", command=gps_delete_selected, width=8).pack(side='left', padx=(0, 8))
tk.Button(gps_btn_frame, text="清空", command=gps_clear_list, width=6).pack(side='left')

def get_and_log_bt_check_state():
    print("--- BT 左列（平台） ---")


def get_and_log_gps_check_state():
    print("--- GPS 左列（平台） ---")

def sync_share_data():
    share_data.file_path = file_entry.get().strip()
    share_data.dir_path = dir_entry.get().strip()
    share_data.os_selection = os_var.get()

def run_wifi_analyze():
    sync_share_data()
    get_and_log_wifi_check_state()
    analyze_wifi()

def run_bt_analyze():
    sync_share_data()
    get_and_log_bt_check_state()
    analyze_bt()

def run_gps_analyze():
    sync_share_data()
    get_and_log_gps_check_state()
    analyze_gps()

wifi_btn = tk.Button(sheet_wifi, text="WiFi 分析", command=run_wifi_analyze, width=12, height=2)
wifi_btn.pack(pady=20)

bt_btn = tk.Button(sheet_bt, text="BT 分析", command=run_bt_analyze, width=12, height=2)
bt_btn.pack(pady=20)
tk.Label(sheet_bt, text="蓝牙日志分析", font=("", 12)).pack(pady=10)

gps_btn = tk.Button(sheet_gps, text="GPS 分析", command=run_gps_analyze, width=12, height=2)
gps_btn.pack(pady=20)
tk.Label(sheet_gps, text="GPS 日志分析", font=("", 12)).pack(pady=10)

root.mainloop()
