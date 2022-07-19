#@title **Run server**
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin 
import easyocr

import numpy as np
import cv2
import base64



app = Flask(__name__)
reader = easyocr.Reader(['en'], gpu=False)
# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_SORT_KEYS'] = False


def solutionCaptcha(captcha):
    result = reader.readtext(captcha, detail=0)
    return result

def chuyen_base64_sang_anh(anh_base64):
    try:
        anh_base64 = np.fromstring(base64.b64decode(anh_base64), dtype=np.uint8)
        anh_base64 = cv2.imdecode(anh_base64, cv2.IMREAD_ANYCOLOR)
    except:
        return None
    return anh_base64

@app.route('/s', methods=['POST'] )
@cross_origin(origin='*')
def solutionCaptcha_process():
    captchaResult = []
    captchabase64 = request.form.get('captchabase64')
    captcha = chuyen_base64_sang_anh(captchabase64)
    captchaResult = solutionCaptcha(captcha)
    return jsonify(captchaResult)

@app.route('/')
@cross_origin(origin='*')
def hello_world():
    return " Server OK"

# Start Backend

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
