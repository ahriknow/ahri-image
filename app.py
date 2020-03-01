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


@app.errorhandler(404)
def page_not_found(error):
    return redirect('/404')


@app.route('/404')
def page_404():
    return "<h1>404</h1>"


@app.route('/500')
def page_500():
    return "<h1>500</h1>"


if __name__ == '__main__':
    app.run()
