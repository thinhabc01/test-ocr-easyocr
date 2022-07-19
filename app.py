#@title **Run server**
from flask import Flask, request, jsonify
import easyocr
import pickle

import numpy as np
import cv2
import base64


app = Flask(__name__)

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
        
def load_object(filename):
    with open(filename, 'rb') as inp:
        reader = pickle.load(inp)
    return reader
        
def solutionCaptcha(captcha):
    reader = load_object("model.pkl")
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
def solutionCaptcha_process():
    captchaResult = []
    captchabase64 = request.form.get('captchabase64')
    captcha = chuyen_base64_sang_anh(captchabase64)
    captchaResult = solutionCaptcha(captcha)
    return jsonify(captchaResult)

@app.route('/')
def hello_world():
    reader = easyocr.Reader(['en'], gpu=False)
    save_object(reader, "model.pkl")
    return " Server OK"

# Start Backend

if __name__ == '__main__':
    app.run()
