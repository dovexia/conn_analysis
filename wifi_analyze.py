# 用于WiFi分析的处理逻辑

import tkinter as tk

def analyze_wifi():
    win = tk.Toplevel()
    win.title("WiFi 分析")
    win.geometry("400x200")

    btn_frame = tk.Frame(win, padx=20, pady=20)
    btn_frame.pack(fill='both', expand=True)

    def make_cmd(i):
        def cmd():
            print(f"按钮 {i} 被点击")
        return cmd

    for i in range(1, 6):
        btn = tk.Button(btn_frame, text=f"按钮 {i}", command=make_cmd(i), width=12, height=1)
        btn.pack(pady=6, fill='x')
