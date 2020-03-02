import sqlite3
from flask import Flask, make_response, redirect, request
from Image.Create import get_image
from Image.Analysis import analysis

app = Flask(__name__)


@app.route('/')
def index():
    try:
        params = analysis(request.args)
        img = get_image(params)
        resp = make_response(img)
        resp.headers["Content-Type"] = "image/png"
        return resp
    except Exception as ex:
        print(ex)
        return redirect('/500')


@app.route('/image')
def image():
    try:
        params = analysis(request.args)
        img = get_image(params)
        resp = make_response(img)
        resp.headers["Content-Type"] = "image/png"
        return resp
    except Exception as ex:
        print(ex)
        return redirect('/500')


@app.route('/image/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "GET":
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload</title>
    <style>
        body {
            width: 100%;
        }

        .form {
            height: 300px;
            width: 500px;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 0 5px #999;
            margin: 100px auto;
            padding: 20px;
        }

        label {
            width: 100%;
            margin: 20px 0;
        }
    </style>
</head>
<body>
<form class="form" action="/image/upload" method="post" enctype="multipart/form-data">
    <label>库名
        <input type="text" name="store">
    </label>
    <label>序号
        <input type="text" name="index">
    </label>
    <label>图片
        <input type="file" name="file">
    </label>
    <label>上传
        <input type="submit" value="上传"/>
    </label>
</form>
</body>
</html>
        """
        return html
    else:
        try:
            file = request.files.get('file').read()
            conn = sqlite3.connect('./Image/db.sqlite3')
            c = conn.cursor()
            msql = '''INSERT INTO store(`name`, `index`, `image`) VALUES (?, ?, ?)'''
            para = (request.form['store'], request.form['index'], file)
            c.execute(msql, para)
            conn.commit()
            conn.close()
            return """成功 <a href="/image/upload">继续</a>"""
        except Exception as ex:
            print(str(ex))
            return """失败 <a href="/image/upload">继续</a>"""


@app.errorhandler(404)
def page_not_found(error):
    return redirect('/404')


@app.route('/404')
def page_404():
    return "<h1>404</h1>"


@app.route('/500')
def page_500():
    return "<h1>500</h1>"


# def createdb(dbname):
#     conn = sqlite3.connect(dbname)
#     c = conn.cursor()
#     c.execute('''CREATE TABLE store
#         (`id` INTEGER PRIMARY KEY  AUTOINCREMENT,
#         `name`          TEXT    ,
#         `index`          int   ,
#         `image`          blob
#
#          );''')
#     conn.commit()
#     conn.close()
#     return 'ok'


if __name__ == '__main__':
    app.run()
