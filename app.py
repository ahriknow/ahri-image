import sqlite3
from flask import Flask, make_response, redirect, request, jsonify
from Image.Create import get_image
from Image.Analysis import analysis

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/image')


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
        return redirect('/image/500')


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
    return redirect('/image/404')


@app.route('/image/404')
def page_404():
    return "<h1>Image : 404</h1>"


@app.route('/image/500')
def page_500():
    return "<h1>Image : 500</h1>"


if __name__ == '__main__':
    app.run()
