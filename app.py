from flask import Flask
from flask import request
import pandas as pd
import numpy as np
import json
import io
import random
import os

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return "Hello world"

@app.route("/Testjs", methods=["GET","POST"])
def Test():
	try:
		aa = request.get_data()
		bb = aa.decode('UTF-8')
		cc = json.loads(bb)
		dd = cc["rows"][1]

		return str(dd)
	except:
		return "error"

@app.route("/Sample", methods=["GET","POST"])
def sample_post():
	if request.method == "POST":
		return request.get_data()
	else:
		return "vvv"

if __name__ == '__main__':
	app.secret_key = os.urandom(10)
	app.run(debug= True)