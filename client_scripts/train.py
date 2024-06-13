from ultralytics import YOLO
import os

if __name__ == '__main__':
    DIR = os.path.dirname(__file__)

    model = YOLO('./runs/detect/train8/weights/best.pt')

    model.train(data=f'{DIR}/yaml/yolo_go.yaml', imgsz=640, batch=-1, time=2)