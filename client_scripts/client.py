from server_connection import *
from go_board_recognition import b64image_to_string
import time
import base64
import random
import cv2

cam_port = 0

if __name__ == '__main__':
    client_id = str(random.randint(10000000, 99999999))
    client = init(client_id)
    time.sleep(5)
    while True:
        cam = cv2.VideoCapture(cam_port)
        result, image = cam.read()
        if result:
            result, buffer = cv2.imencode('.jpg', image)
            b64jpg = base64.b64encode(buffer)
            cam.release()
            position_string = b64image_to_string(b64jpg)
            data_publish(client, client_id, position_string)
            time.sleep(15)
