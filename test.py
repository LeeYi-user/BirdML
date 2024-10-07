import os
import pandas as pd
from PIL import Image

# 讀取CSV檔案
ml_data = pd.read_csv('ML__2024-09-27T11-12_photo_TW-KIN.csv')
birds_data = pd.read_csv('birds.csv')

# 把欄位轉為大寫，以便比對
ml_data['Scientific Name'] = ml_data['Scientific Name'].str.upper()
birds_data['scientific name'] = birds_data['scientific name'].str.upper()

# 找出同時存在於兩個CSV中的Scientific Name
common_names = set(ml_data['Scientific Name']).intersection(set(birds_data['scientific name']))

# 創建test資料夾下的子資料夾並紀錄Scientific Name和labels的對應關係
name_to_label = {}

for name in common_names:
    # 從birds.csv中找對應的label
    label = birds_data.loc[birds_data['scientific name'] == name, 'labels'].values[0]
    
    # 創建對應的子資料夾
    folder_path = os.path.join('test', label)
    os.makedirs(folder_path, exist_ok=True)
    
    # 記錄Scientific Name和label的對應
    name_to_label[name] = label

# 定義圖片尺寸
target_size = (224, 224)

# 複製符合條件的圖片到對應的子資料夾並調整圖片大小
for name in common_names:
    # 找到在 ml_data 中對應的所有列
    ml_rows = ml_data[ml_data['Scientific Name'] == name]

     # 遍歷對應的目錄編號，並尋找對應的圖片
    for _, row in ml_rows.iterrows():
        # 找到ML__2024-09-27T11-12_photo_TW-KIN.csv中對應的目錄編號
        directory_number = str(row['目錄編號'])

        # 找出birds_cropped資料夾下所有以目錄編號開頭的.jpg圖片
        for file_name in os.listdir('birds_cropped'):
            if file_name.startswith(str(directory_number)) and file_name.endswith('.jpg'):
                # 取得對應的label子資料夾
                label_folder = name_to_label[name]
                target_folder = os.path.join('test', label_folder)
                
                # 定義來源檔案和目標檔案
                source_file = os.path.join('birds_cropped', file_name)
                target_file = os.path.join(target_folder, file_name)
                
                # 打開圖片並調整大小
                img = Image.open(source_file)
                img = img.resize(target_size)
                
                # 複製圖片到對應的子資料夾，並保存調整後的圖片
                img.save(target_file)

print("處理完成，圖片已複製並調整大小到對應子資料夾。")
