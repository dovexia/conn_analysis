# 主界面与各分析模块共享的数据
# main.py 写入，wifi_analyze / bt_analyze / gps_analyze 等读取

# 文件路径（选择文件输入框的当前值）
file_path = ""

# 目录路径（选择目录输入框的当前值）
dir_path = ""

# 目录所在 Frame 的引用（若分析模块需要访问目录相关控件可用）
dir_frame = None

# 平台下拉框当前选中的文本（Android / Linux / RTOS / unknown）
os_selection = ""

# 各标签页「已插入列表」的文本列表，供对应 analyze 模块读取
wifi_text_list = []
bt_text_list = []
gps_text_list = []

# BT 页协议多选框状态（点击 BT 分析时由 main 同步）
bt_hfp = False
bt_a2dp = False
bt_le = False
