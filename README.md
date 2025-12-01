# Simple Machine Learning API（性格預測服務）

此專案示範如何以 Flask + Gunicorn 建立簡單的機器學習推論 API，並透過 Docker 封裝成容易部署的服務。API 會根據使用者的行為特徵預測其人格傾向（內向／外向），同時支援 API Key 驗證與伺服器端記錄。

## 特色

- **RESTful 推論端點**：`/predict` 接收 JSON 陣列並回傳模型預測結果。
- **API Key 驗證**：所有端點都需提供 `X-API-KEY`，避免未授權存取。
- **完整記錄**：使用 `app.log` 追蹤 request/response、例外狀況與執行時間。
- **Log 下載**：`/log` 端點可直接下載伺服器端日誌。
- **Docker 化**：在 `prod/Dockerfile` 內建置，方便與任何環境整合。

## 專案結構

```
.
├── data/
│   └── personality_dataset.csv   # 模型訓練資料
├── dev/
│   ├── training.py               # 建模腳本，輸出 model.pkl 與測試資料
│   └── model.pkl                 # 訓練完成的模型（需複製到 prod/）
└── prod/
    ├── app.py                    # Flask + Gunicorn API 入口
    ├── main.py                   # 載入模型並提供 predict 函式
    ├── model.pkl                 # 服務使用的模型權重
    ├── requirements.txt          # 執行所需套件
    ├── Dockerfile                # Docker 建置檔
    ├── app.log                   # 執行期 log
    └── test/
        ├── input/input1.*        # 範例輸入
        └── output/output1.*      # 預期輸出
```

## 先決條件

- 已安裝 Docker。
- 若要重新訓練模型，請在本機具備 Python 3.10+ 及 `pip`。

## 建置與部署

1. **取得程式碼**
   ```bash
   git clone https://github.com/mary84215/simple_model_api.git
   cd simple_model_api
   ```

2. **（選用）重新訓練模型**
   ```bash
   python dev/training.py
   ```
   - 會讀取 `data/personality_dataset.csv`，訓練 Logistic Regression 並輸出 `dev/model.pkl`。
   - 也會同步產生 `prod/test/input` 與 `prod/test/output` 的範例檔案。

3. **準備推論模型**
   ```bash
   cp dev/model.pkl prod/model.pkl   # macOS / Linux
   # 或者
   copy dev\model.pkl prod\model.pkl # Windows
   ```

4. **（選用）本機執行以便除錯**
   ```bash
   cd prod
   pip install -r requirements.txt
   python app.py
   ```
   - 預設 Flask 會在 `http://localhost:5001` 執行，可用於快速驗證。

5. **使用 Docker 建置與啟動**
   ```bash
   cd prod
   docker build -t personality-api .
   docker run -d -p 5000:5000 --name personality-container personality-api
   ```
   - Gunicorn 服務會綁定 `0.0.0.0:5000`，可透過 `http://localhost:5000` 存取。

## API 使用方式

- 每個請求都必須帶上 `X-API-KEY`（預設可用：`abc123`、`secret456`、`mary84215`）。
- 請求與回應皆會被記錄在 `prod/app.log`，可透過 `/log` 下載。

### `/predict`

- 方法：`POST`
- Header：`Content-Type: application/json` 與 `X-API-KEY`
- Body：JSON 陣列（可一次傳多筆），欄位需與訓練資料一致

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: abc123" \
  -d '[{"Time_spent_Alone":10.0,"Stage_fear":1,"Social_event_attendance":3.0,"Going_outside":3.0,"Drained_after_socializing":1,"Friends_circle_size":5.0,"Post_frequency":3.0}]'
```

範例輸出：

```json
{
  "prediction": [
    {"IF_INTROVERTED": 1}
  ]
}
```

### `/log`

- 方法：`GET`
- Header：`X-API-KEY`
- 作用：下載 `app.log`

```bash
curl -X GET http://localhost:5000/log \
  -H "X-API-KEY: abc123" \
  -o app.log
```

## 開發與除錯建議

- `prod/app.py` 內已實作 `before_request` 與 `after_request` hook，可快速追蹤請求週期。
- 若更新 `.gitignore` 不生效，請確認檔案是否已被 Git 追蹤（必要時使用 `git rm --cached <file>`）。
- 若要擴充欄位或替換模型，只需更新 `dev/training.py` 並重新輸出 `model.pkl`。