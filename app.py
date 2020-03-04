from flask import Flask
from flask import request
import pandas as pd
import numpy as np
import json
import base64
import io
import random
import os
from pandas.io.json import json_normalize
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return "Hello world"

@app.route("/CSV", methods=["GET","POST"])
def CSV():
	try:
		aa = request.get_data()
		bb = aa.decode('UTF-8')
		cc = json.loads(bb)
		dd = cc["rows"]
		ee = json_normalize(dd)
		lst = ee.columns.tolist()
		lst.remove('timestamp')
		lst.insert(0, 'timestamp')
		tmp_df_1 = ee[lst]
		tmp_df_2 = tmp_df_1.dropna(how='any').dropna(how='all', axis=1)
		tmp_df_2.to_csv('ff.csv')
		return "Success"
	except:
		return "error"

@app.route("/Seaborn", methods=["GET","POST"])
def SNS():
	try:
		aa = request.get_data()
		bb = aa.decode('UTF-8')
		cc = json.loads(bb)
		dd = cc["rows"]
		ee = json_normalize(dd)
		lst = ['Ch2','Ch3','Ch5','Ch6','Ch7','Ch9','DR_Ch2','DR_Ch3','DR_Ch4','DR_Ch5','DR_Ch6','DR_Ch7','DR_Ch8','DR_Ch9']
		tmp_df_1 = ee[lst]
		tmp_df_2 = tmp_df_1.dropna(how='any').dropna(how='all', axis=1)
		fig = sns.heatmap(tmp_df_2.astype(float).corr(),linewidths=0.2,vmax=1.0, square=True, cmap='RdBu', linecolor='white', annot=True).get_figure()
		buf = io.BytesIO()
		plt.figsize=(14,12)
		fig.savefig(buf,format='png',bbox_inches="tight")
		buf.seek(0)
		pic = base64.b64encode(buf.read())
		return pic
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