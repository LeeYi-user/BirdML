import os
from rembg import new_session, remove

# 定義資料夾路徑
input_folder = 'extracted_images'
output_folder = 'removed_images'

# 如果輸出資料夾不存在，則建立資料夾
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

model_name = "birefnet-general"
rembg_session = new_session(model_name)

# 逐一處理 input_folder 中的圖片
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)

    # 確保只處理圖片文件
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        with open(input_path, 'rb') as img_file:
            img = img_file.read()
            output = remove(img, session=rembg_session)  # 指定模型

            # 儲存去背後的圖片
            output_path = os.path.join(output_folder, filename)
            with open(output_path, 'wb') as out_file:
                out_file.write(output)

            print(f'已去背並保存：{os.path.basename(input_path)} -> {os.path.basename(output_path)}')

print("圖片去背完成！")
