
import tkinter as tk
from tkinter import filedialog
from wifi_analyze import analyze_wifi

def on_button_click():
    print("按钮被点击了！")

root = tk.Tk()
root.title("无线log分析")
root.geometry("600x400")  # 设置窗口大小

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
file_entry = tk.Entry(file_frame, width=40)
file_entry.pack(side='left')

dir_frame = tk.Frame(root)
dir_frame.pack(padx=20, pady=10, fill='x')
dir_label = tk.Label(dir_frame, text="目录:")
dir_label.pack(side='left')
dir_entry = tk.Entry(dir_frame, width=40)
dir_entry.pack(side='left', padx=5)
def browse_dir():
    dir_path = filedialog.askdirectory(title="选择目录")
    if dir_path:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, dir_path)
dir_btn = tk.Button(dir_frame, text="浏览", command=browse_dir)
dir_btn.pack(side='left')


# 直接用 place 固定底部按钮
wifi_btn = tk.Button(root, text="WiFi", command=analyze_wifi, width=12, height=2)
wifi_btn.place(x=80, y=340, width=100, height=40)
bt_btn = tk.Button(root, text="BT", width=12, height=2)
bt_btn.place(x=250, y=340, width=100, height=40)
gps_btn = tk.Button(root, text="GPS", width=12, height=2)
gps_btn.place(x=420, y=340, width=100, height=40)

root.mainloop()
