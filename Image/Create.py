import sqlite3

import requests
from PIL import Image, ImageDraw
from io import BytesIO


def get_image(params):
    img = Image.new('RGB', params['size'], params['rgb'])

    if params['store']:
        conn = sqlite3.connect('./Image/db.sqlite3')
        c = conn.cursor()
        msql = '''select `image` from `store` where `name`=? and `index`=?'''
        para = (params['store'][0], params['store'][1])
        c.execute(msql, para)
        values = c.fetchone()
        c.close()
        conn.close()
        if values:
            img = Image.open(BytesIO(values[0]))
            if params['original'] and params['original'] == 'false':
                img = img.resize(params['size'], Image.ANTIALIAS)
    elif params['album']:
        url = f"http://ahri-image.ahriknow.com/{params['album'][0]}/{params['album'][1]}.png"
        if response := requests.get(url):
            img = Image.open(BytesIO(response.content))
            if params['original'] and params['original'] == 'false':
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
    if data := params['colour']:
        if data[0] == 2:
            step_r = (data[2][0] - data[1][0]) / params['size'][1]
            step_g = (data[2][1] - data[1][1]) / params['size'][1]
            step_b = (data[2][2] - data[1][2]) / params['size'][1]
            for y in range(0, params['size'][1]):
                bg_r = round(data[1][0] + step_r * y)
                bg_g = round(data[1][1] + step_g * y)
                bg_b = round(data[1][2] + step_b * y)
                for x in range(0, params['size'][0]):
                    draw.point((x, y), fill=(bg_r, bg_g, bg_b))
        elif data[0] == 4:
            step_r = (data[2][0] - data[1][0]) / params['size'][0]
            step_g = (data[2][1] - data[1][1]) / params['size'][0]
            step_b = (data[2][2] - data[1][2]) / params['size'][0]
            for x in range(0, params['size'][0]):
                bg_r = round(data[1][0] + step_r * (params['size'][0] - x))
                bg_g = round(data[1][1] + step_g * (params['size'][0] - x))
                bg_b = round(data[1][2] + step_b * (params['size'][0] - x))
                for y in range(0, params['size'][1]):
                    draw.point((x, y), fill=(bg_r, bg_g, bg_b))
    if params['point']:
        img = img.point(lambda p: p * params['point'])
    if params['opacity']:
        img = img.convert('RGBA')
        x, y = img.size
        for i in range(x):
            for j in range(y):
                color = img.getpixel((i, j))
                color = color[:-1] + (params['opacity'],)
                img.putpixel((i, j), color)
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    f.close()
    return data
