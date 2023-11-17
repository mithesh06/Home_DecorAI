import constants as C
from yolo_obj import OBJ_DETECTOR 
import time
from LLM_handler import LLM_Interface as L
import os
import requests
import json



class InputHandler:
    def __init__(self) -> None:
        self.yolo_model = OBJ_DETECTOR()
        self.LLM = L()

    def get_suggestion(self,image_url,style):

        object_detection_result = self.yolo_model.get_objs(image_url)
        
        if (object_detection_result):
            object_string, (width,height) = object_detection_result
            print(object_string)
            suggestion = self.LLM.suggest(object_string,height,width,style)
            return image_url, suggestion
        return None
    
    def get_output_image(self,url,suggestion):

        response = requests.get(url)
        with open("image.jpg", "wb") as f:
            f.write(response.content)

        files = [("input_image", open("image.jpg", "rb"))]
        # "selected_model": "openjourney_2",
        payload = {
            "text_prompt": suggestion,
            "selected_model": "sd_1_5",
            "selected_controlnet_model": [],
            "negative_prompt": "",
            "num_outputs": 1,
            "quality": 70,
            "output_width": 768,
            "output_height": 512,
            "guidance_scale": 23,
            "prompt_strength": 0.55,
            "controlnet_conditioning_scale": [0.6],
            "seed": 3929441273,
            "image_guidance_scale": 1.2,
        }

        response = requests.post(
            "https://api.gooey.ai/v2/Img2Img/form/?run_id=1fxo2ieg&uid=KfaQ2zd7zShkUZftCMkbjhwmokF3",
            headers={
                "Authorization": "Bearer " + os.environ["sk-WuuXCCW1Yjp7cEHfCUIChtkFGJB81w0wKN8DNXuzCveS7qQ6"],
            },
            files=files,
            data={"json": json.dumps(payload)},
        )
        assert response.ok, response.content

        result = response.json()

        return result