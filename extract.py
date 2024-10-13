import os
import shutil

def extract_and_rename_images(source_folder, destination_folder):
    # 支援的圖片格式
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    # 檢查目標資料夾是否存在，若不存在則創建
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # 遍歷 false 資料夾底下的所有子資料夾
    for root, dirs, files in os.walk(source_folder):
        # 取得子資料夾名稱
        subfolder_name = os.path.basename(root)
        
        for file in files:
            # 檢查文件是否是圖片
            if any(file.lower().endswith(ext) for ext in supported_extensions):
                # 原始圖片路徑
                file_path = os.path.join(root, file)
                
                # 新的檔案名稱格式：false子資料夾名稱_原始名稱
                new_filename = f"{subfolder_name}_{file}"
                new_file_path = os.path.join(destination_folder, new_filename)
                
                # 複製並重新命名圖片到目標資料夾
                shutil.copy(file_path, new_file_path)
                print(f"圖片 {file} 已提取並重新命名為 {new_filename}")

# 設定來源與目標資料夾
source_folder = 'test'
destination_folder = 'extracted_images/'

# 執行提取與重新命名
extract_and_rename_images(source_folder, destination_folder)
