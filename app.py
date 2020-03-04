import sqlite3
from flask import Flask, make_response, redirect, request, jsonify
from Image.Create import get_image
from Image.Analysis import analysis
import pytesseract
from PIL import Image
import hashlib

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/image/generate')


@app.route('/image/generate')
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


@app.route('/image/ocr', methods=['POST'])
def ocr():
    try:
        file = request.files.get('file')
        lang = request.form['lang']
        md5 = hashlib.md5(file.read()).hexdigest()
        conn = sqlite3.connect('./Image/db.sqlite3')
        c = conn.cursor()
        c.execute('''select `text` from `ocr` where `md5`=? and `lang`=?''', (md5, lang))
        values = c.fetchone()
        if values:
            return jsonify({'code': 200, 'msg': 'success', 'data': values[0]})
        img = Image.open(file)
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        text = pytesseract.image_to_string(img, lang=lang)

        c.execute('''insert into `ocr`(`md5`, `text`, `lang`) values(?, ?, ?)''', (md5, text, lang))
        c.close()
        conn.commit()
        conn.close()
        return jsonify({'code': 200, 'msg': 'success', 'data': text})
    except Exception as ex:
        print(ex)
        return jsonify({'code': 500, 'msg': 'fail', 'data': None})


@app.route('/image/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file').read()
        conn = sqlite3.connect('./Image/db.sqlite3')
        c = conn.cursor()
        msql = '''INSERT INTO store(`name`, `index`, `image`) VALUES (?, ?, ?)'''
        para = (request.form['store'], request.form['index'], file)
        c.execute(msql, para)
        conn.commit()
        conn.close()
        return jsonify({'code': 200, 'msg': 'success', 'data': None})
    except Exception as ex:
        print(str(ex))
        return jsonify({'code': 500, 'msg': 'fail', 'data': None})


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
