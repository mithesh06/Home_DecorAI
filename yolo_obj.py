from ultralytics import YOLO
import numpy as np
from io import BytesIO
import requests
from PIL import Image


# YOlO model Version
YMV = "yolov8n.pt"


def get_image_dimensions(url):
    response = requests.get(url)
    image_data = BytesIO(response.content)
    image = Image.open(image_data)
    width, height = image.size
    return width, height, image


class OBJ_DETECTOR:
    def __init__(self) -> None:
        self.last_img = None

        self.model = YOLO(YMV)# set model parameters
        self.model.overrides['conf'] = 0.25  # NMS confidence threshold
        self.model.overrides['iou'] = 0.45  # NMS IoU threshold
        self.model.overrides['agnostic_nms'] = False  # NMS class-agnostic
        self.model.overrides['max_det'] = 1000  # maximum number of detections per image
    
    def get_objs(self, URL):
        width, height, image = get_image_dimensions(URL)
        if width and height:
            print(f"Image dimensions: {width}x{height}")
            results = self.model.predict(image)
            result = results[0]
            names = result.names
            boxes = result.boxes.xyxy # x1, y1, x2, y2
            categories = result.boxes.cls 

            # UNUSED
            scores = result.boxes.conf
            scores = result.probs # for classification models
            masks = result.masks # for segmentation models


            ret = "" # Return Query
            for i,(b,c) in enumerate(zip(boxes,categories)):
                ret += f"{i}. location {b.numpy()}, class: {names[c.item()]} \n"

            if ret:
                return ret, (width,height)
            else:
                return None

        else:
            return None









