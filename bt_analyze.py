# 用于BT分析的处理逻辑

import share_data

def analyze_bt():
    file_path = share_data.file_path
    dir_path = share_data.dir_path
    os_selection = share_data.os_selection
    dir_frame = share_data.dir_frame
    bt_text_list = share_data.bt_text_list  # 主界面 BT 页「已插入列表」
    print("BT 分析功能待实现", f"file_path={file_path!r} dir_path={dir_path!r} os={os_selection!r} list={bt_text_list!r}")
