import pandas as pd

# 讀取 CSV 檔案
file_path = 'ML__2024-09-27T11-12_photo_TW-KIN.csv'
data = pd.read_csv(file_path)

# 找出 "Scientific Name" 欄位的不同值
unique_scientific_names = data['Scientific Name'].unique()

# 列出每個不同的值及其數量
print("每個不同的 'Scientific Name' 值:")
for name in unique_scientific_names:
    print(name)
print(f"\n不同的 'Scientific Name' 數量:\n{len(unique_scientific_names)}")

# 計算總行數
total_rows = len(data)

# 計算總行數除以不同的 'Scientific Name' 數量
result = total_rows / len(unique_scientific_names)
print(f"\nCSV 檔案中的總行數:\n{total_rows}")
print(f"\n總行數除以不同 'Scientific Name' 數量的結果:\n{result}")
