from PIL import Image, ImageDraw
from io import BytesIO
import requests


def get_image(params):
    img = Image.new('RGB', params['size'], params['rgb'])
    if params['store']:
        response = requests.get(
            f"http://ahriknow.oss-cn-beijing.aliyuncs.com/store/{params['store'][0]}/{params['store'][1]}.jpg")
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img = img.resize(params['size'], Image.ANTIALIAS)
    draw = ImageDraw.Draw(img)
    for i in params['lines']:
        draw.line(i[0], i[1])
    for i in params['ellipses']:
        draw.ellipse(i[0], i[1], i[2])
    for i in params['rectangles']:
        draw.rectangle(i[0], i[1], i[2])
    for i in params['texts']:
        draw.text(i[0], i[1], i[2], i[3])
    if params['point']:
        img = img.point(lambda p: p * params['point'])
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    f.close()
    return data
