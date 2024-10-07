import os

def list_test_directory(test_dir='test'):
    # 檢查test資料夾是否存在
    if not os.path.exists(test_dir):
        print(f"資料夾 '{test_dir}' 不存在。")
        return
    
    # 列出test資料夾下的所有項目
    items = os.listdir(test_dir)
    
    # 過濾出子資料夾
    subfolders = [item for item in items if os.path.isdir(os.path.join(test_dir, item))]
    
    # 計算子資料夾數量
    num_subfolders = len(subfolders)
    print(f"'{test_dir}' 資料夾下共有 {num_subfolders} 個子資料夾。")
    
    # 定義常見的圖片副檔名
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    
    total_images = 0
    # 遍歷每個子資料夾，計算圖片數量
    for folder in subfolders:
        folder_path = os.path.join(test_dir, folder)
        files = os.listdir(folder_path)
        # 過濾出圖片檔案
        images = [file for file in files if os.path.splitext(file)[1].lower() in image_extensions]
        num_images = len(images)
        total_images += num_images
        print(f"  子資料夾 '{folder}' 中有 {num_images} 張圖片。")
    
    print(f"總共有 {total_images} 張圖片在 '{test_dir}' 資料夾下的所有子資料夾中。")

if __name__ == "__main__":
    list_test_directory('test')
