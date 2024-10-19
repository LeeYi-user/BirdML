import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

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

# 載入預訓練的 EfficientNetB0 模型，並解鎖所有權重
model = load_model('EfficientNetB0-525-(224 X 224)- 98.97.h5', custom_objects={'F1_score': F1_score})

# 解鎖所有層的權重
for layer in model.layers:
    layer.trainable = True

# 定義訓練數據的資料生成器 (假設你已經準備好資料集)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

train_generator = train_datagen.flow_from_directory(
    'train',  # 訓練資料路徑
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

# 定義驗證數據的資料生成器
val_datagen = ImageDataGenerator(rescale=1./255)

val_generator = val_datagen.flow_from_directory(
    'validation',  # 驗證資料路徑
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

# 編譯模型，設定優化器和損失函數
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy', F1_score])

# 訓練模型
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=val_generator,
    validation_steps=val_generator.samples // val_generator.batch_size,
    epochs=10)  # 設定你想要的 epoch 次數

# 儲存重新訓練的模型
model.save('efficientnetb0_finetuned.h5')

# 輸出訓練過程的歷史記錄
print("訓練完成，模型已儲存。")
