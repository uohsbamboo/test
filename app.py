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
from scipy.signal import spectrogram,stft
from scipy.signal.windows import hann
from scipy.fftpack import fftfreq

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

@app.route("/FFT", methods=["GET","POST"])
def FFT():
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
		tmp_df_2 = tmp_df_2.drop('timestamp',axis=1)

		dt = 0.1 # サンプリング間隔
		M = 512 #FFTサイズ
		win = hann(M) #窓関数
		acf = 1/(sum(win)/M)
		overlap = 0.5 #オーバラップ
		overlap_samples = int(round(M*overlap)) # overlap in samples

		# 周波数スケール作成
		freq = fftfreq(M, dt)[1:int(M//2.56)]

		df = pd.DataFrame({'freq':freq})
		collist = list(tmp_df_2.columns)

		for colname in collist:
			x = tmp_df_2[colname].values
    		#振幅
			t, f, S = stft(x, fs=10, window=win, nperseg=M, noverlap=overlap_samples, padded=False, return_onesided=False,boundary=None)
			SS = acf*np.abs(S)
			avg_SS =np.mean(SS,axis=1)
			SSS = pd.Series(data=avg_SS[1:int(M//2.56)],name=colname, dtype='float')
			df = pd.concat([df, SSS], axis=1)
		FFT = df.to_json(orient='table')
		return FFT
	except:
		return "error"

@app.route("/FFT_para", methods=["GET","POST"])
def FFT_para():
	try:    
		aa = request.get_data()
		bb = aa.decode('UTF-8')
		cc = json.loads(bb)
		
		Json_Samp = cc["Samp"]
		Json_Sz = cc["Sz"]
		Json_rows = cc["rows"]
		Json_Overlap = cc["OLR"]
	    
		Norm_rows = json_normalize(Json_rows)
		df_lst = Norm_rows.columns.tolist()
		df_lst.remove('timestamp')
		df_lst.insert(0, 'timestamp')
		tmp_df_1 = Norm_rows[df_lst]
		tmp_df_2 = tmp_df_1.dropna(how='any').dropna(how='all', axis=1)
		df = tmp_df_2.drop('timestamp',axis=1)

		dt = 1/Json_Samp # サンプリング間隔
		M = Json_Sz #FFTサイズ
		win = hann(M) #窓関数
		acf = 1/(sum(win)/M)
		overlap = Json_Overlap #オーバラップ
		overlap_samples = int(round(M*overlap)) # overlap in samples

		# 周波数スケール作成
		freq = fftfreq(M, dt)[1:int(M//2.56)]

		df_FFT = pd.DataFrame({'freq':freq})
		collist = list(df.columns)

		for colname in collist:
			x = df[colname].values
    		#振幅
			t, f, S = stft(x, fs=Json_Samp, window=win, nperseg=M, noverlap=overlap_samples, padded=False, return_onesided=False,boundary=None)
			SS = acf*np.abs(S)
			avg_SS =np.mean(SS,axis=1)
			SSS = pd.Series(data=avg_SS[1:int(M//2.56)],name=colname, dtype='float')
			df_FFT = pd.concat([df_FFT, SSS], axis=1)
		FFT = df_FFT.to_json(orient='table')
		return FFT
	except:
		return "error"

@app.route("/Return",methods=["GET","POST"])
def Return():
	aa = request.get_data()
	bb = aa.decode('UTF-8')
	return str(bb)

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
		plt.figsize=(14,12)
		fig = sns.heatmap(tmp_df_2.astype(float).corr(),linewidths=0.1,vmax=1.0, square=True, cmap='RdBu', linecolor='white').get_figure()
		buf = io.BytesIO()
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