# 用于BT分析的处理逻辑

import tkinter as tk
import share_data

def analyze_bt_hfp(text_widget):
    text_widget.insert(tk.END, "hfp select\n")

def analyze_bt_a2dp(text_widget):
    text_widget.insert(tk.END, "a2dp select\n")

def analyze_bt_le(text_widget):
    text_widget.insert(tk.END, "le select\n")

def analyze_bt():
    file_path = share_data.file_path
    dir_path = share_data.dir_path
    os_selection = share_data.os_selection
    dir_frame = share_data.dir_frame
    bt_text_list = share_data.bt_text_list  # 主界面 BT 页「已插入列表」

    # 先新建结果窗口，供各子分析函数输出
    win = tk.Toplevel()
    win.title("BT 分析结果")
    win.geometry("500x400")
    text_frame = tk.Frame(win, padx=10, pady=10)
    text_frame.pack(fill="both", expand=True)
    text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10))
    text_widget.pack(fill="both", expand=True)

    if share_data.bt_hfp:
        analyze_bt_hfp(text_widget)
    if share_data.bt_a2dp:
        analyze_bt_a2dp(text_widget)
    if share_data.bt_le:
        analyze_bt_le(text_widget)

    print("BT 分析功能实现", f"file_path={file_path!r} dir_path={dir_path!r} os={os_selection!r} list={bt_text_list!r}")
