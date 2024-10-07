import os
import json

def create_class_indices(test_dir='test', output_file='class_indices.json'):
    """
    讀取指定的測試資料夾，並生成類別映射的 JSON 文件，將索引作為 key，類別名稱作為 value。

    Args:
        test_dir (str): 測試資料夾的路徑，預設為 'test'。
        output_file (str): 輸出的 JSON 文件名稱，預設為 'class_indices.json'。

    Returns:
        dict: 類別映射的字典。
    """
    if not os.path.isdir(test_dir):
        raise ValueError(f"The directory '{test_dir}' does not exist.")

    # 取得所有子資料夾名稱
    class_names = [d for d in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, d))]

    if not class_names:
        raise ValueError(f"No subdirectories found in '{test_dir}'.")

    # 排序子資料夾名稱，確保類別索引的一致性
    class_names.sort()

    # 創建類別映射，從 0 開始
    class_indices = {str(idx): class_name for idx, class_name in enumerate(class_names)}

    # 保存為 JSON 文件
    with open(output_file, 'w') as f:
        json.dump(class_indices, f, indent=4, ensure_ascii=False)

    print(f"類別映射已保存至 '{output_file}'。")
    print("類別映射如下：")
    for idx, class_name in class_indices.items():
        print(f"  {idx}: {class_name}")

    return class_indices

if __name__ == "__main__":
    # 你可以根據需要修改 'test' 資料夾的路徑或輸出文件名稱
    create_class_indices(test_dir='test', output_file='class_indices.json')
