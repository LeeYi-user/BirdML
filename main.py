import pandas as pd
import os
import requests

# 讀取 CSV 檔案
csv_file = 'ML__2024-09-27T11-12_photo_TW-KIN.csv'
df = pd.read_csv(csv_file)

# 創建一個資料夾來儲存圖片
os.makedirs('birds', exist_ok=True)

# 下載圖片並存檔
for index, row in df.iterrows():
    catalog_number = row['目錄編號']  # 目錄編號欄位
    url = f'https://cdn.download.ams.birds.cornell.edu/api/v2/asset/{catalog_number}/1200'
    image_path = os.path.join('birds', f'{catalog_number}.jpg')

    # 下載圖片
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"圖片 {catalog_number} 已下載並儲存到 {image_path}")
    else:
        print(f"下載 {catalog_number} 失敗，狀態碼: {response.status_code}")
