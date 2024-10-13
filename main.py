import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
import os
import json
import shutil
from sklearn.metrics import accuracy_score, f1_score

# 自訂 F1_score 函數
def F1_score(y_true, y_pred):
    # 將預測值轉換為整數類別
    y_pred = tf.argmax(y_pred, axis=-1)
    y_true = tf.argmax(y_true, axis=-1)
    
    # 計算 TP, FP, FN
    TP = tf.reduce_sum(tf.cast(y_true * y_pred, 'float32'))
    FP = tf.reduce_sum(tf.cast((1 - y_true) * y_pred, 'float32'))
    FN = tf.reduce_sum(tf.cast(y_true * (1 - y_pred), 'float32'))
    
    # 計算 precision 和 recall
    precision = TP / (TP + FP + tf.keras.backend.epsilon())
    recall = TP / (TP + FN + tf.keras.backend.epsilon())
    
    # 計算 F1 score
    f1 = 2 * precision * recall / (precision + recall + tf.keras.backend.epsilon())
    return f1

# 載入模型
model = tf.keras.models.load_model('EfficientNetB0-525-(224 X 224)- 98.97.h5', custom_objects={'F1_score': F1_score})

# 載入類別映射
with open('class_indices.json', 'r') as f:
    class_indices = json.load(f)

# 創建 index 到 class 的映射，將鍵轉為整數
idx_to_class = {int(k): v for k, v in class_indices.items()}
class_to_idx = {v: int(k) for k, v in class_indices.items()}  # 用於將類別轉為索引

# 單張圖片預測函數
def predict_single_image(img_path):
    # 檢查圖片是否存在
    if not os.path.exists(img_path):
        print(f"圖片路徑不存在: {img_path}")
        return None
    
    try:
        # 載入圖片，並轉換為224x224大小
        img = image.load_img(img_path, target_size=(224, 224))
    except Exception as e:
        print(f"載入圖片失敗: {img_path}, 錯誤: {e}")
        return None
    
    # 將圖片轉換為數組，並擴展維度為 (1, 224, 224, 3)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # 使用 EfficientNet 的預處理函數
    img_array = preprocess_input(img_array)
    
    # 使用模型進行預測
    prediction = model.predict(img_array)
    
    # 取得預測結果的類別索引
    predicted_index = np.argmax(prediction, axis=-1)[0]
    
    # 將索引轉換回類別標籤
    predicted_class = idx_to_class.get(predicted_index, "Unknown")
    
    # 取得預測的置信度
    confidence = prediction[0][predicted_index]
    
    return predicted_class, confidence

# 初始化結果儲存路徑
results_dir = 'results'
true_dir = os.path.join(results_dir, 'true')
false_dir = os.path.join(results_dir, 'false')

# 創建結果目錄，如果不存在的話
os.makedirs(true_dir, exist_ok=True)
os.makedirs(false_dir, exist_ok=True)

# 遍歷 test 資料夾下的所有子資料夾和圖片
test_dir = 'test'
y_true = []
y_pred = []

for class_name in os.listdir(test_dir):
    class_path = os.path.join(test_dir, class_name)
    if not os.path.isdir(class_path):
        continue  # 跳過非資料夾項目
    
    # 創建對應的子資料夾在 results/true 和 results/false 中
    true_class_dir = os.path.join(true_dir, class_name)
    false_class_dir = os.path.join(false_dir, class_name)
    os.makedirs(true_class_dir, exist_ok=True)
    os.makedirs(false_class_dir, exist_ok=True)
    
    for img_name in os.listdir(class_path):
        img_path = os.path.join(class_path, img_name)
        if not img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            continue  # 跳過非圖片文件
        
        # 預測圖片
        result = predict_single_image(img_path)
        if result is None:
            continue  # 跳過預測失敗的圖片
        
        predicted_class, confidence = result
        y_pred.append(predicted_class)
        
        # 真實標籤為資料夾名稱
        y_true.append(class_name)
        
        print(f"圖片: {img_path} | 預測類別: {predicted_class} | 置信度: {confidence:.4f}")
        
        # 決定將圖片複製到 true 或 false 資料夾的對應子資料夾
        if predicted_class == class_name and confidence >= 0.9:
            dest_dir_specific = true_class_dir
        else:
            dest_dir_specific = false_class_dir
        
        # 複製圖片到目的地資料夾
        try:
            shutil.copy(img_path, dest_dir_specific)
        except Exception as e:
            print(f"複製圖片失敗: {img_path} 到 {dest_dir_specific}, 錯誤: {e}")

# 計算準確率
accuracy = accuracy_score(y_true, y_pred)
print(f"\n最終準確率: {accuracy * 100:.2f}%")

# （可選）計算 F1 分數和其他評估指標
# 將類別轉換為數字索引
y_true_idx = [class_to_idx.get(label, -1) for label in y_true]
y_pred_idx = [class_to_idx.get(label, -1) for label in y_pred]

# 移除無法映射的樣本
filtered = [(t, p) for t, p in zip(y_true_idx, y_pred_idx) if t != -1 and p != -1]
if filtered:
    y_true_filtered, y_pred_filtered = zip(*filtered)
    f1 = f1_score(y_true_filtered, y_pred_filtered, average='weighted')
    print(f"F1 Score (加權平均): {f1:.4f}")
else:
    print("沒有有效的樣本來計算 F1 分數和分類報告。")
