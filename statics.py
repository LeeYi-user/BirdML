import csv
from collections import Counter

# 設定檔案路徑
file_path = 'ML__2024-09-27T11-12_photo_TW-KIN.csv'

# 初始化計數器
name_counter = Counter()

# 讀取CSV檔案
with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    # 迭代每一行，統計Scientific Name的出現次數，並保留Common Name
    for row in reader:
        scientific_name = row['Scientific Name']
        common_name = row['Common Name']
        name_counter[(scientific_name, common_name)] += 1

# 根據出現次數從高到低排序並打印
for (scientific_name, common_name), count in name_counter.most_common():
    print(f"Scientific Name: {scientific_name}, Common Name: {common_name}, Count: {count}")
