import os
import shutil

def organize_images(source_folder, destination_folder):
    # 檢查目標資料夾是否存在，若不存在則創建
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 遍歷 source_folder 下的所有圖片
    for file in os.listdir(source_folder):
        if "_" in file:
            # 分離類別名稱與編號
            category, number = file.rsplit("_", 1)
            number = os.path.splitext(number)[0]  # 去掉編號後的副檔名
            
            # 檢查目標子資料夾是否存在，若不存在則創建
            category_folder = os.path.join(destination_folder, category)
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)
            
            # 原始圖片路徑
            file_path = os.path.join(source_folder, file)

            # 新的檔案名稱
            new_file_name = f"{number}{os.path.splitext(file)[1]}"  # 保留原始副檔名
            new_file_path = os.path.join(category_folder, new_file_name)

            # 複製圖片到目標資料夾並重新命名
            shutil.copy(file_path, new_file_path)
            print(f"圖片 {file} 已儲存至 {new_file_path}")

# 設定來源與目標資料夾
source_folder = 'removed_images/'
destination_folder = 'test/'

# 執行圖片分類與命名
organize_images(source_folder, destination_folder)
