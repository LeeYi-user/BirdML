import numpy as np
import tensorflow as tf
import pandas as pd
import os
from sklearn.metrics import f1_score
from keras.preprocessing.image import ImageDataGenerator

SEED = 53

data = {"imgpaths": [] , "labels": []}
paths = os.listdir('test')

for folders in paths:
    paths_folders = os.path.join('test', folders)
    filelist = os.listdir(paths_folders)
    for files in filelist:
        paths_folders_files = os.path.join(paths_folders, files)
        data["imgpaths"].append(paths_folders_files)
        data["labels"].append(folders)

test_df = pd.DataFrame(data , index=range(len(data['imgpaths'])))

BatchSiz = 40
ImgSiz = (224, 224)
generator = ImageDataGenerator()

# Dataframe --> Preprocessed Image data

test_images = generator.flow_from_dataframe(
    dataframe = test_df,
    x_col = 'imgpaths',
    y_col = 'labels',
    target_size = ImgSiz,
    color_mode = 'rgb',
    class_mode = 'categorical',
    batch_size = BatchSiz,
    shuffle = False,
    seed = SEED
)

# When loading a whole model using 'load_model'

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

model = tf.keras.models.load_model('EfficientNetB0-525-(224 X 224)- 98.97.h5', custom_objects={'F1_score': F1_score})

y_test = test_images.classes
y_pred = np.argmax(model.predict(test_images), axis = 1)

# Compute F1 Score (A value related to Recall and Precision)
f1 = f1_score(y_test, y_pred, average='macro')
print("F1 Score:", f1)
