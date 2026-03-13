# 用于WiFi分析的处理逻辑

import tkinter as tk
import share_data

def analyze_wifi():
    # 从 main 共享的状态读取：文件路径、目录路径、平台选择
    file_path = share_data.file_path
    dir_path = share_data.dir_path
    os_selection = share_data.os_selection
    dir_frame = share_data.dir_frame  # 主界面目录所在 Frame 的引用（可选使用）

    win = tk.Toplevel()
    win.title("WiFi 分析")
    win.geometry("400x200")

    btn_frame = tk.Frame(win, padx=20, pady=20)
    btn_frame.pack(fill='both', expand=True)

    # 示例：在窗口顶部显示当前共享状态
    info = f"文件: {file_path or '(未选)'}\n目录: {dir_path or '(未选)'}\n平台: {os_selection}"
    tk.Label(btn_frame, text=info, justify="left").pack(anchor="w", pady=(0, 10))

    def make_cmd(i):
        def cmd():
            print(f"按钮 {i} 被点击 | file_path={file_path!r} dir_path={dir_path!r} os={os_selection!r}")
        return cmd

    for i in range(1, 6):
        btn = tk.Button(btn_frame, text=f"按钮 {i}", command=make_cmd(i), width=12, height=1)
        btn.pack(pady=6, fill='x')
