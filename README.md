# BirdML

資工四 李易 111010512

## 步驟

### 資料分析

1. 前往 Macaulay Library 的[搜尋頁面](https://search.macaulaylibrary.org/catalog?regionCode=TW-KIN&beginYear=2023&endYear=2023&mediaType=photo&sort=obs_date_asc), 透過 Export 功能取得 `ML__2024-09-27T11-12_photo_TW-KIN.csv` 檔, 使用 `download.py` 下載圖片
2. 下載完畢後, 使用 `missing.py` 檢查是否有缺失的圖片
3. 下載完畢後, 使用 `duplicated.py` 檢查是否有重複的圖片
4. 檢查完畢後, 使用 `classes.py` 計算有多少種類
5. 檢查完畢後, 使用 `statics.py` 計算每種類有多少圖片

### 資料處理

1. ~~使用 `model.py` 將所有圖片中的鳥類擷取出來~~
2. ~~使用 `test.py` 將擷取出來的鳥類放進 test 資料夾~~
2. 將 Kaggle525 的 test 資料夾拉過來
3. 使用 `count.py` 計算圖片種類及數量
4. 使用 `indices.py` 生成 `class_indices.json` 檔
5. 使用 `predict.py` 進行單一預測
6. 使用 `main.py` 進行批量預測
7. 使用 `clear.py` 清理預測結果
8. 使用 `extract.py` 提取錯誤圖片
9. 使用 [remove.bg](https://www.remove.bg/windows-mac-linux/download) 去背錯誤圖片
10. 使用 `removed.py` 把去背圖片放進 test 資料夾
