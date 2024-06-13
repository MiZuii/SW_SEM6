from server_connection import *
import time
from ultralytics import YOLO
import os
import torchvision.transforms as transforms
from PIL import Image
from stringify_results import results_to_string
import cv2
import random

DIR = os.path.dirname(__file__)

cam_port = 0


if __name__ == "__main__":
    client_id = str(random.randint(10000000, 99999999))
    client = init(client_id)
    time.sleep(5)
    model = YOLO(f'{DIR}/yolo_go_model.pt')

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((640, 640), antialias=True)
    ])

    while True:
        cam = cv2.VideoCapture(cam_port)
        res, im = cam.read()

        if res:
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(im)
            im = transform(im).unsqueeze(0)

            cam.release()

            results = model(im)

            position = results_to_string(results)

            data_publish(client, client_id, position)
        time.sleep(10)
