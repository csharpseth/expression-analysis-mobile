from flask import Flask, request

import numpy as np
import urllib.request as urllib
import cv2 as cv

from expression_analysis import *
from IGNORE import BASEURL

app = Flask(__name__)

def url_to_image(url):
    res = urllib.urlopen(url)
    img = np.asarray(bytearray(res.read()), dtype="uint8")
    img = cv.imdecode(img, cv.IMREAD_COLOR)
    return img

@app.post("/process/image")
def process_image():
    data = request.get_json()
    url = f"{BASEURL}/{data['fileName']}"
    img = url_to_image(url)
    sentiment = PredictSentiment(img)

    return { "sentiment": sentiment }, 200

    
