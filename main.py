from input_handler import InputHandler
from PIL import Image
import requests
from io import BytesIO



def process_data(img_data,style_data):
    # load model
    image_url = img_data #"https://media.istockphoto.com/id/1182454657/photo/bohemian-living-room-interior-3d-render.jpg?s=612x612&w=0&k=20&c=qw37MGIiTL_jML3_Tbm4bM-jNLCrocSWj7DanhBr_bY="
    style = style_data

    I = InputHandler()
    op = I.get_suggestion(image_url,style)
    if op:
        image_data, suggestion = op
        output = I.get_output_image(image_data,suggestion)

        print(f"TO FRONTEND {output['output']['output_images'][0]}")
        return_to_frontend = output['output']['output_images'][0]
        return return_to_frontend,suggestion







