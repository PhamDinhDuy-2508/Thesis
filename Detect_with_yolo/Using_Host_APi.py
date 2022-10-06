import io
import cv2
import numpy
import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder


def using_API():
    print("ddd")

    # image = cv2.cv2.cvtColor(img, cv2.cv2.COLOR_BGR2RGB)
    # pilImage = Image.fromarray(image)

    # # Convert to JPEG Buffer
    # buffered = io.BytesIO()
    # pilImage.save(buffered, quality=100, format="JPEG")

    # # Build multipart form and post request
    # m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})

    # response = requests.post("https://detect.roboflow.com/steel_shape_c/1?api_key=5CTrdY2PU4A5uX2kn35g", data=m,
    #                          headers={'Content-Type': m.content_type})

    # print(response)
    # print(response.json())


if __name__ == '__main__':
    print("hello")



