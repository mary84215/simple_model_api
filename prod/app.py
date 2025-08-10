# prod/app.py

import os
#os.chdir(os.path.join(os.getcwd(),'prod'))
import logging
from flask import Flask, request, jsonify, send_file, abort
from main import predict
import pandas as pd
import time
from datetime import datetime

VALID_API_KEYS = {"abc123", "secret456",'mary84215'}

app = Flask(__name__)
# 應用根目錄
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#APP_ROOT = os.path.join(os.getcwd())

# 設定 log
LOG_PATH = os.path.join(APP_ROOT, "app.log")

logging.basicConfig(
    level=logging.INFO, #多少以上的層級要被記錄到log
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_PATH), #將log記錄到file
        logging.StreamHandler() #將log輸出到終端機
        ]
)

""" logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
) """


""" import json
with open('test/input/input1.json', 'r') as f:
    data = json.load(f)  # 注意：是 json.load，不是 json.loads
 """


@app.before_request #Flask提供的 hook，在每個請求開始前呼叫
def log_request_info():
    app.logger.info(f"------ request from: {request.remote_addr}; method: {request.method}; route: {request.path} ------")

@app.before_request #兩個before request要分開寫
def check_api_key():
    api_key = request.headers.get("X-API-KEY")
    if api_key not in VALID_API_KEYS:
        app.logger.info(f"request was aborted since invalid or missing API key")
        abort(401, description="invalid or missing API key") # abort要寫在最後面

# Route 1: 預測 API
@app.route('/predict', methods=['POST'])
def model_predict():
    start_time = time.time()

    try:        
        input_json = request.get_json()
        app.logger.info(f"received input")
        input_data = pd.DataFrame(input_json)

        result_df = predict(input_data)
        app.logger.info(f"complete output")
        result = result_df.to_dict(orient='records')

        end_time = time.time()
        duration = round(end_time - start_time, 3)

        app.logger.info(f"prediction time used: {duration} seconds")
        
        return jsonify({"prediction": result})

    except Exception as e:
        app.logger.exception(f"prediction failed:") # 在 except 區塊內使用，會自動記錄完整 traceback 和錯誤上下文，適合在發生例外時使用。
        # 跟logger.error差異：logger.error需要指定exc_info=True才會紀錄traceback，是用在簡單且知道情境的log
        #return jsonify({"error": str(e)}), 500

# Route 2: 下載 log 檔
@app.route('/log', methods=['GET'])
def get_log():
    if os.path.exists(LOG_PATH):
        return send_file(LOG_PATH, as_attachment=True)
    else:
        return jsonify({"error": "log file not found"}), 404
    
@app.after_request
def log_response_info(response):
    app.logger.info(f"------ response status: {response.status} ------")
    return response

@app.errorhandler(Exception) # 全域異常處理log註冊處理所有未捕捉的例外錯誤，例如如果某個route出錯 log會記錄這段 
def handle_exception(e):
    app.logger.exception(f"unhandled exception: {str(e)}")
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
    #app.run()
    #app.run(host='localhost', port=5000, debug=True)



