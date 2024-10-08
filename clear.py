import os

def remove_empty_folders(path):
    # 遍歷資料夾
    for foldername, subfolders, filenames in os.walk(path, topdown=False):
        # 如果資料夾是空的，則刪除
        if not subfolders and not filenames:
            try:
                os.rmdir(foldername)
                print(f"Deleted empty folder: {foldername}")
            except OSError as e:
                print(f"Error deleting folder {foldername}: {e}")

# 指定要清理的資料夾路徑
results_folder = "results"
remove_empty_folders(results_folder)
