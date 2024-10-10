import os
from rembg import remove
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

def process_single_image(file_path, output_folder):
    # 開啟圖片
    with open(file_path, 'rb') as file:
        input_image = file.read()

    # 去背
    output_image = remove(input_image)

    # 確保輸出資料夾存在
    os.makedirs(output_folder, exist_ok=True)

    # 生成新的圖片名稱 (取代 .jpg 為 .png)
    new_filename = os.path.join(output_folder, os.path.splitext(os.path.basename(file_path))[0] + '.png')
    
    # 將去背後的圖片存成 png
    with open(new_filename, 'wb') as file:
        file.write(output_image)

    # 匯報進度
    print(f'已去背並保存：{os.path.basename(file_path)} -> {os.path.basename(new_filename)}')

def process_images(folder_path, output_folder, max_workers=4):
    # 獲取所有要處理的 .jpg 檔案
    jpg_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]

    # 使用 ThreadPoolExecutor 進行並行處理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(lambda file_path: process_single_image(file_path, output_folder), jpg_files)

# 設定資料夾路徑
folder_path = 'extracted_images'
output_folder = 'removed_images'

# 執行圖片處理 (可調整 max_workers 來增加並行數量)
process_images(folder_path, output_folder, max_workers=8)
