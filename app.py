#@title **Run server**
from flask import *
from paddleocr import PaddleOCR,draw_ocr
import pickle

import numpy as np
import cv2
import base64
import os
import platform

app = Flask(__name__)

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
        
def load_object(filename):
    with open(filename, 'rb') as inp:
        reader = pickle.load(inp)
    return reader
        
def solutionCaptcha(captcha):
    reader = PaddleOCR(use_angle_cls=True, lang='en')
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
    return " Server OK"

@app.route('/ini-model')
def iniModel():
    reader = easyocr.Reader(['en'], gpu=False)
    save_object(reader, "model.pkl")
    return " Server OK"

#===========================download file================================
@app.route('/return-files', methods=['GET'])
def return_files_tut():
    file = str(request.args.get('file'))
    try:
        return send_file(file, attachment_filename=file)
    except Exception as e:
        return str(e)
    
@app.route('/getinfo')
def getinfo():
	s = ""
	arr = os.listdir(os.path.normpath(os.getcwd()))
	for i in arr :
		s += f"<h1>{str(i)}</h1>\n"
	return s
# Start Backend

if __name__ == '__main__':
    app.run()
