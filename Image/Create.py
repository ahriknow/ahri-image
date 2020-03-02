import sqlite3
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
            img = img.resize(params['size'], Image.ANTIALIAS)

    # if params['store']:
    #     response = requests.get(
    #         f"http://ahriknow.oss-cn-beijing.aliyuncs.com/store/{params['store'][0]}/{params['store'][1]}.jpg")
    #     if response.status_code == 200:
    #         img = Image.open(BytesIO(response.content))
    #         img = img.resize(params['size'], Image.ANTIALIAS)
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
