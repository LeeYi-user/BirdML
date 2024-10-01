import os
import hashlib

# 計算檔案的 MD5 哈希值
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# 檢查 birds 資料夾中的圖片是否不一樣，並統計重複數量
def check_unique_images(directory):
    image_hashes = {}
    duplicate_count = 0  # 用來統計重複圖片的數量

    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            file_path = os.path.join(directory, filename)
            file_hash = calculate_md5(file_path)
            
            if file_hash in image_hashes:
                print(f"Duplicate found: {filename} is the same as {image_hashes[file_hash]}")
                duplicate_count += 1
            else:
                image_hashes[file_hash] = filename

    if duplicate_count == 0:
        print("All images are unique!")
    else:
        print(f"Number of duplicate images: {duplicate_count}")

# 指定 birds 資料夾的路徑
directory = "birds"
check_unique_images(directory)
