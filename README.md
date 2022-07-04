# AITemp
透過[YoloV5](https://github.com/ultralytics/yolov5)的AI影像辨識系統，先辨識到人的座標，再透過FLIR熱成像鏡頭偵測座標內的最大溫度，並將偵測到的溫度上傳到influxdb。
如超過37.5度時，將人拍照下來
