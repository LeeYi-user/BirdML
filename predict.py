import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
import os
import json
from sklearn.metrics import f1_score

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

# 單張圖片預測函數
def predict_single_image(img_path):
    # 檢查圖片是否存在
    if not os.path.exists(img_path):
        print(f"圖片路徑不存在: {img_path}")
        return None
    
    # 載入圖片，並轉換為224x224大小
    img = image.load_img(img_path, target_size=(224, 224))
    
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

# 測試單張圖片的預測
img_path = 'test/ABBOTTS BABBLER/1.jpg'  # 替換為你的圖片路徑
predicted_class, confidence = predict_single_image(img_path)
if predicted_class is not None:
    print(f"Predicted class: {predicted_class} with confidence {confidence:.4f}")
