import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import share_data
import app_config
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


def build_wifi_tab(parent, initial=None):
    """构建 WiFi 标签页。initial 为上次保存的配置 dict，用于恢复勾选和列表。返回 get_state() 供保存配置。"""
    init = initial or {}
    tk.Label(parent, text="WiFi 日志分析", font=("", 12)).pack(pady=10)
    wifi_check_container = tk.Frame(parent)
    wifi_check_container.pack(pady=10, anchor='w')

    wifi_check_vars = []
    os_group = ttk.LabelFrame(wifi_check_container, text="OS")
    os_group.pack(side='left', padx=(0, 40))
    wifi_check_frame = tk.Frame(os_group)
    wifi_check_frame.pack(padx=8, pady=8)
    wifi_check_labels = ["Android", "Linux", "RTOS", "unknown"]
    left_init = init.get("left", [])
    for i in range(4):
        var = tk.BooleanVar(value=left_init[i] if i < len(left_init) else False)
        wifi_check_vars.append(var)
        cb = tk.Checkbutton(wifi_check_frame, text=wifi_check_labels[i], variable=var, anchor='w')
        cb.pack(anchor='w', pady=2)

    wifi_check_frame_right = tk.Frame(wifi_check_container, width=480, height=100)
    wifi_check_frame_right.pack(side='left')
    wifi_check_frame_right.pack_propagate(False)
    wifi_check_labels_right_android = ["Android0", "Android1", "Android2", "Android3", "ALL"]
    wifi_check_labels_right_linux = ["Linux0", "Linux1", "Linux2", "Linux3", "ALL"]
    wifi_check_labels_right_rtos = ["RTOS0", "RTOS1", "RTOS2", "RTOS3", "ALL"]
    wifi_check_labels_right_unknown = ["unknown0", "unknown1", "unknown2", "unknown3", "ALL"]

    def _list4(key):
        return init.get(key, [])[:4]

    android_check_vars = []
    linux_check_vars = []
    rtos_check_vars = []
    unknown_check_vars = []
    for i in range(4):
        v = _list4("android")
        var = tk.BooleanVar(value=v[i] if i < len(v) else False)
        android_check_vars.append(var)
        cb = tk.Checkbutton(wifi_check_frame_right, text=wifi_check_labels_right_android[i], variable=var, anchor='w')
        cb.place(x=0, y=i * 24)
    for i in range(4):
        v = _list4("linux")
        var = tk.BooleanVar(value=v[i] if i < len(v) else False)
        linux_check_vars.append(var)
        cb = tk.Checkbutton(wifi_check_frame_right, text=wifi_check_labels_right_linux[i], variable=var, anchor='w')
        cb.place(x=120, y=i * 24)
    for i in range(4):
        v = _list4("rtos")
        var = tk.BooleanVar(value=v[i] if i < len(v) else False)
        rtos_check_vars.append(var)
        cb = tk.Checkbutton(wifi_check_frame_right, text=wifi_check_labels_right_rtos[i], variable=var, anchor='w')
        cb.place(x=240, y=i * 24)
    for i in range(4):
        v = _list4("unknown")
        var = tk.BooleanVar(value=v[i] if i < len(v) else False)
        unknown_check_vars.append(var)
        cb = tk.Checkbutton(wifi_check_frame_right, text=wifi_check_labels_right_unknown[i], variable=var, anchor='w')
        cb.place(x=360, y=i * 24)

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

    wifi_right_frame = tk.Frame(parent)
    wifi_right_frame.pack(side='right', padx=20, pady=10, fill='both', expand=True)
    share_data.wifi_text_list = list(init.get("text_list", []))

    def wifi_add_text():
        s = wifi_entry.get().strip()
        if s:
            share_data.wifi_text_list.append(s)
            wifi_listbox.insert(tk.END, s)
            wifi_entry.delete(0, tk.END)

    def wifi_delete_selected():
        sel = wifi_listbox.curselection()
        if sel:
            i = sel[0]
            wifi_listbox.delete(i)
            share_data.wifi_text_list.pop(i)

    def wifi_clear_list():
        wifi_listbox.delete(0, tk.END)
        share_data.wifi_text_list.clear()

    wifi_entry_frame = tk.Frame(wifi_right_frame)
    wifi_entry_frame.pack(fill='x', pady=(0, 6))
    wifi_entry = tk.Entry(wifi_entry_frame, width=24)
    wifi_entry.pack(side='left', padx=(0, 8))
    tk.Button(wifi_entry_frame, text="Add", command=wifi_add_text, width=6).pack(side='left')
    tk.Label(wifi_right_frame, text="已插入列表:").pack(anchor='w')
    wifi_listbox = tk.Listbox(wifi_right_frame, height=8, width=30)
    wifi_listbox.pack(fill='both', expand=True, pady=4)
    for s in share_data.wifi_text_list:
        wifi_listbox.insert(tk.END, s)
    wifi_list_btn_frame = tk.Frame(wifi_right_frame)
    wifi_list_btn_frame.pack(fill='x')
    tk.Button(wifi_list_btn_frame, text="删除选中", command=wifi_delete_selected, width=8).pack(side='left', padx=(0, 8))
    tk.Button(wifi_list_btn_frame, text="清空", command=wifi_clear_list, width=6).pack(side='left')

    def on_wifi_analyze():
        sync_share_data()
        get_and_log_wifi_check_state()
        analyze_wifi()

    def get_wifi_state():
        return {
            "left": [wifi_check_vars[i].get() for i in range(4)],
            "android": [android_check_vars[i].get() for i in range(4)],
            "linux": [linux_check_vars[i].get() for i in range(4)],
            "rtos": [rtos_check_vars[i].get() for i in range(4)],
            "unknown": [unknown_check_vars[i].get() for i in range(4)],
            "text_list": list(share_data.wifi_text_list),
        }

    tk.Button(parent, text="WiFi 分析", command=on_wifi_analyze, width=12, height=2).pack(pady=20)
    return get_wifi_state


def sync_share_data():
    share_data.file_path = file_entry.get().strip()
    share_data.dir_path = dir_entry.get().strip()
    share_data.os_selection = os_var.get()


def build_bt_tab(parent, initial=None):
    """构建 BT 标签页。initial 为上次保存的配置。返回 get_state() 供保存配置。"""
    init = initial or {}
    tk.Label(parent, text="蓝牙日志分析", font=("", 12)).pack(pady=10)
    bt_right_frame = tk.Frame(parent)
    bt_right_frame.pack(side='right', padx=20, pady=10, fill='both', expand=True)
    share_data.bt_text_list = list(init.get("text_list", []))

    def bt_add_text():
        s = bt_entry.get().strip()
        if s:
            share_data.bt_text_list.append(s)
            bt_listbox.insert(tk.END, s)
            bt_entry.delete(0, tk.END)

    def bt_delete_selected():
        sel = bt_listbox.curselection()
        if sel:
            i = sel[0]
            bt_listbox.delete(i)
            share_data.bt_text_list.pop(i)

    def bt_clear_list():
        bt_listbox.delete(0, tk.END)
        share_data.bt_text_list.clear()

    bt_entry_frame = tk.Frame(bt_right_frame)
    bt_entry_frame.pack(fill='x', pady=(0, 6))
    bt_entry = tk.Entry(bt_entry_frame, width=24)
    bt_entry.pack(side='left', padx=(0, 8))
    tk.Button(bt_entry_frame, text="Add", command=bt_add_text, width=6).pack(side='left')
    tk.Label(bt_right_frame, text="已插入列表:").pack(anchor='w')
    bt_listbox = tk.Listbox(bt_right_frame, height=8, width=30)
    bt_listbox.pack(fill='both', expand=True, pady=4)
    for s in share_data.bt_text_list:
        bt_listbox.insert(tk.END, s)
    bt_btn_frame = tk.Frame(bt_right_frame)
    bt_btn_frame.pack(fill='x')
    tk.Button(bt_btn_frame, text="删除选中", command=bt_delete_selected, width=8).pack(side='left', padx=(0, 8))
    tk.Button(bt_btn_frame, text="清空", command=bt_clear_list, width=6).pack(side='left')

    def get_and_log_bt_check_state():
        print("--- BT 左列（平台） ---")

    def on_bt_analyze():
        share_data.bt_hfp = bt_hfp_var.get()
        share_data.bt_a2dp = bt_a2dp_var.get()
        share_data.bt_le = bt_le_var.get()
        sync_share_data()
        get_and_log_bt_check_state()
        analyze_bt()

    tk.Button(parent, text="BT 分析", command=on_bt_analyze, width=12, height=2).pack(pady=20)

    # BT 按钮下方：HFP / A2DP / LE 多选框
    bt_profile_frame = ttk.LabelFrame(parent, text="协议/配置")
    bt_profile_frame.pack(pady=10, anchor='w', padx=20, fill='x')
    bt_hfp_var = tk.BooleanVar(value=init.get("hfp", False))
    bt_a2dp_var = tk.BooleanVar(value=init.get("a2dp", False))
    bt_le_var = tk.BooleanVar(value=init.get("le", False))
    tk.Checkbutton(bt_profile_frame, text="HFP", variable=bt_hfp_var, anchor='w').pack(side='left', padx=12, pady=6)
    tk.Checkbutton(bt_profile_frame, text="A2DP", variable=bt_a2dp_var, anchor='w').pack(side='left', padx=12, pady=6)
    tk.Checkbutton(bt_profile_frame, text="LE", variable=bt_le_var, anchor='w').pack(side='left', padx=12, pady=6)

    def get_bt_state():
        return {
            "text_list": list(share_data.bt_text_list),
            "hfp": bt_hfp_var.get(),
            "a2dp": bt_a2dp_var.get(),
            "le": bt_le_var.get(),
        }

    return get_bt_state


def build_gps_tab(parent, initial=None):
    """构建 GPS 标签页。initial 为上次保存的配置。返回 get_state() 供保存配置。"""
    init = initial or {}
    tk.Label(parent, text="GPS 日志分析", font=("", 12)).pack(pady=10)
    gps_right_frame = tk.Frame(parent)
    gps_right_frame.pack(side='right', padx=20, pady=10, fill='both', expand=True)
    share_data.gps_text_list = list(init.get("text_list", []))

    def gps_add_text():
        s = gps_entry.get().strip()
        if s:
            share_data.gps_text_list.append(s)
            gps_listbox.insert(tk.END, s)
            gps_entry.delete(0, tk.END)

    def gps_delete_selected():
        sel = gps_listbox.curselection()
        if sel:
            i = sel[0]
            gps_listbox.delete(i)
            share_data.gps_text_list.pop(i)

    def gps_clear_list():
        gps_listbox.delete(0, tk.END)
        share_data.gps_text_list.clear()

    gps_entry_frame = tk.Frame(gps_right_frame)
    gps_entry_frame.pack(fill='x', pady=(0, 6))
    gps_entry = tk.Entry(gps_entry_frame, width=24)
    gps_entry.pack(side='left', padx=(0, 8))
    tk.Button(gps_entry_frame, text="Add", command=gps_add_text, width=6).pack(side='left')
    tk.Label(gps_right_frame, text="已插入列表:").pack(anchor='w')
    gps_listbox = tk.Listbox(gps_right_frame, height=8, width=30)
    gps_listbox.pack(fill='both', expand=True, pady=4)
    for s in share_data.gps_text_list:
        gps_listbox.insert(tk.END, s)
    gps_btn_frame = tk.Frame(gps_right_frame)
    gps_btn_frame.pack(fill='x')
    tk.Button(gps_btn_frame, text="删除选中", command=gps_delete_selected, width=8).pack(side='left', padx=(0, 8))
    tk.Button(gps_btn_frame, text="清空", command=gps_clear_list, width=6).pack(side='left')

    def get_and_log_gps_check_state():
        print("--- GPS 左列（平台） ---")

    def on_gps_analyze():
        sync_share_data()
        get_and_log_gps_check_state()
        analyze_gps()

    def get_gps_state():
        return {"text_list": list(share_data.gps_text_list)}

    tk.Button(parent, text="GPS 分析", command=on_gps_analyze, width=12, height=2).pack(pady=20)
    return get_gps_state


# 加载上次配置并构建各标签页
_saved_config = app_config.load_config()

file_entry.insert(0, _saved_config.get("file_path", ""))
dir_entry.insert(0, _saved_config.get("dir_path", ""))
_os = _saved_config.get("os_selection", "Android")
if _os in ("Android", "Linux", "RTOS", "unknown"):
    os_var.set(_os)

get_wifi_state = build_wifi_tab(sheet_wifi, _saved_config.get("wifi"))
get_bt_state = build_bt_tab(sheet_bt, _saved_config.get("bt"))
get_gps_state = build_gps_tab(sheet_gps, _saved_config.get("gps"))


def _on_closing():
    config = {
        "file_path": file_entry.get().strip(),
        "dir_path": dir_entry.get().strip(),
        "os_selection": os_var.get(),
        "wifi": get_wifi_state(),
        "bt": get_bt_state(),
        "gps": get_gps_state(),
    }
    app_config.save_config(config)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", _on_closing)
root.mainloop()
