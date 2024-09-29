import pandas as pd
import os

# 讀取CSV檔案
csv_file = 'ML__2024-09-27T11-12_photo_TW-KIN.csv'
df = pd.read_csv(csv_file)

# 取得目錄編號欄位
catalog_numbers = df['目錄編號'].astype(str)

# 指定圖片資料夾
image_folder = 'birds'

# 建立一個空的列表來儲存沒有對應圖片的目錄編號
missing_images = []

# 檢查每個目錄編號是否有對應的.jpg檔案
for catalog_number in catalog_numbers:
    image_file = f"{catalog_number}.jpg"
    image_path = os.path.join(image_folder, image_file)
    
    if not os.path.isfile(image_path):
        missing_images.append(catalog_number)

# 輸出沒有對應圖片的目錄編號
if missing_images:
    print("以下目錄編號缺少對應的圖片檔案:")
    for missing in missing_images:
        print(missing)
else:
    print("所有目錄編號都有對應的圖片檔案。")
