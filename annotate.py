import os
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# 定義圖片資料夾路徑
extracted_folder = 'extracted_images'
removed_folder = 'removed_images'
pending_folder = 'pending_images'
progress_file = 'progress.txt'

# 初始化歷史記錄
history = []

# 讀取進度
def load_progress():
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0

# 儲存進度
def save_progress(index):
    with open(progress_file, 'w') as f:
        f.write(str(index))

# 獲取兩個資料夾中同名圖片對，按字母順序排列
def get_image_pairs():
    extracted_files = {os.path.splitext(f)[0]: f for f in os.listdir(extracted_folder) if os.path.isfile(os.path.join(extracted_folder, f))}
    removed_files = {os.path.splitext(f)[0]: f for f in os.listdir(removed_folder) if os.path.isfile(os.path.join(removed_folder, f))}

    common_files = sorted(extracted_files.keys() & removed_files.keys())
    return [(extracted_files[name], removed_files[name]) for name in common_files]

# 顯示圖片
def display_images(extracted_img_path, removed_img_path):
    try:
        img_extracted = Image.open(extracted_img_path)
        img_removed = Image.open(removed_img_path)
    except Exception as e:
        messagebox.showerror("圖片載入錯誤", f"無法載入圖片:\n{e}")
        return

    # 根據視窗大小調整圖片大小
    win_width = root.winfo_width() // 2
    win_height = root.winfo_height()

    # 防止 win_width 或 win_height 為零
    if win_width <= 0:
        win_width = 400  # 預設寬度
    if win_height <= 0:
        win_height = 300  # 預設高度

    # 向後相容性檢查
    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.LANCZOS

    img_extracted.thumbnail((win_width, win_height), resample)
    img_removed.thumbnail((win_width, win_height), resample)

    img_extracted_tk = ImageTk.PhotoImage(img_extracted)
    img_removed_tk = ImageTk.PhotoImage(img_removed)

    label_extracted.config(image=img_extracted_tk)
    label_extracted.image = img_extracted_tk
    label_removed.config(image=img_removed_tk)
    label_removed.image = img_removed_tk

# 跳到下一組圖片
def next_image():
    global image_index
    if image_index < len(image_pairs) - 1:
        image_index += 1
        history.append({'action': 'O'})
        update_display()
    else:
        messagebox.showinfo("完成", "已經到達最後一組圖片")

# 複製圖片到 pending_images 並跳到下一組
def copy_image():
    global image_index
    if 0 <= image_index < len(image_pairs):
        extracted_img_name = image_pairs[image_index][0]
        extracted_img_path = os.path.join(extracted_folder, extracted_img_name)
        pending_img_path = os.path.join(pending_folder, extracted_img_name)
        if not os.path.exists(pending_folder):
            os.makedirs(pending_folder)
        if os.path.exists(pending_img_path):
            messagebox.showwarning("警告", f"圖片 {extracted_img_name} 已經存在於 pending_images 中。")
            return
        try:
            shutil.copy(extracted_img_path, pending_folder)
            history.append({'action': 'P', 'image': extracted_img_name})
            image_index += 1
            update_display()
        except Exception as e:
            messagebox.showerror("複製錯誤", f"無法複製圖片:\n{e}")

# 倒退到上一組圖片
def back_image():
    global image_index
    if not history:
        messagebox.showinfo("提示", "已經在最開始的位置，無法再倒退。")
        return

    last_action = history.pop()

    if last_action['action'] == 'O':
        if image_index > 0:
            image_index -= 1
            update_display()
        else:
            messagebox.showinfo("提示", "已經在最開始的位置，無法再倒退。")
    elif last_action['action'] == 'P':
        if image_index > 0:
            image_index -= 1
            extracted_img_name = last_action['image']
            pending_img_path = os.path.join(pending_folder, extracted_img_name)
            if os.path.exists(pending_img_path):
                try:
                    os.remove(pending_img_path)
                except Exception as e:
                    messagebox.showerror("移除錯誤", f"無法移除圖片:\n{e}")
            update_display()
        else:
            messagebox.showinfo("提示", "已經在最開始的位置，無法再倒退。")
    else:
        messagebox.showerror("未知動作", "歷史記錄中存在未知的動作。")

# 更新圖片顯示
def update_display(event=None):
    if 0 <= image_index < len(image_pairs):
        extracted_img_path = os.path.join(extracted_folder, image_pairs[image_index][0])
        removed_img_path = os.path.join(removed_folder, image_pairs[image_index][1])
        display_images(extracted_img_path, removed_img_path)
        save_progress(image_index)
    else:
        messagebox.showinfo("完成", "沒有更多圖片可顯示。")

# 鍵盤事件處理
def on_key_press(event):
    key = event.char.lower()
    if key == 'o':
        next_image()
    elif key == 'p':
        copy_image()
    elif key == 'b':
        back_image()

# 處理視窗大小變更事件
def on_resize(event):
    update_display()

# 確保資料夾存在
for folder in [extracted_folder, removed_folder, pending_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 設定主視窗
root = tk.Tk()
root.title("Image Viewer")
root.geometry("800x400")

# 讀取圖片對並載入進度
image_pairs = get_image_pairs()
image_index = load_progress()

# 設定圖片顯示區域
label_extracted = tk.Label(root)
label_removed = tk.Label(root)
label_extracted.pack(side="left", fill="both", expand=True)
label_removed.pack(side="right", fill="both", expand=True)

# 綁定按鍵事件
root.bind("<Key>", on_key_press)

# 綁定視窗大小變更事件
root.bind("<Configure>", on_resize)

# 強制更新視窗，確保 win_width 和 win_height 正確
root.update_idletasks()

# 初始化顯示
update_display()

# 運行主程式
root.mainloop()
