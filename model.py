import cv2
import os
from PIL import Image
from ultralytics import YOLO

# 加載 YOLOv8 模型（使用 COCO 預訓練模型）
model = YOLO('yolov8l.pt')

# 圖片文件夾路徑和輸出文件夾路徑
input_folder = 'birds'
output_folder = 'birds_cropped'
os.makedirs(output_folder, exist_ok=True)

# 遍歷所有圖片文件
image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]

for img_file in image_files:
    img_path = os.path.join(input_folder, img_file)
    # 加載圖片
    img = cv2.imread(img_path)

    # 使用 YOLO 模型檢測圖片中的鳥類
    results = model(img)

    # 遍歷所有檢測到的對象
    for i, box in enumerate(results[0].boxes):  # results[0] 獲取第一個結果，boxes 是檢測到的框
        cls = int(box.cls)  # 獲取類別
        if cls == 14:  # 確保檢測到的是鳥類 (class ID 14 是鳥)
            # 獲取檢測框 (x1, y1, x2, y2)
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # 將框的座標轉換為整數

            # 裁剪圖片
            cropped_img = img[y1:y2, x1:x2]

            # 保存裁剪出的圖片
            crop_img = Image.fromarray(cropped_img)
            crop_img.save(os.path.join(output_folder, f"{img_file.split('.')[0]}_{i}.jpg"))

    print(f"{img_file} 處理完成")
