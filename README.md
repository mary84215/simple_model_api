# Simple Machine Learning API

A demonstration of how to build and deploy a simple machine learning model as a RESTful API using Flask, Gunicorn, and Docker. This API predicts personality traits (Introvert/Extrovert) based on behavioral data.

## Features

- **Prediction Endpoint**: Accepts behavioral data and returns a personality prediction.
- **API Key Authentication**: Secures the endpoints with a simple API key check.
- **Logging**: Records request, response, and error information to a log file.
- **Log Download**: Provides an endpoint to download the application's log file.
- **Containerized**: Fully containerized with Docker for easy deployment and portability.

## Project Structure

```
.
├── data/                 # Contains the raw dataset
│   └── personality_dataset.csv
├── dev/                  # Development scripts and artifacts
│   ├── training.py       # Script to train the model
│   └── model.pkl         # The trained model (should be copied to prod/)
└── prod/                 # Production application code
    ├── app.py            # Flask application
    ├── main.py           # Core prediction logic
    ├── model.pkl         # The trained model used by the app
    ├── requirements.txt  # Python dependencies
    ├── Dockerfile        # Docker configuration
    └── test/             # Test data
```

## Prerequisites

- Docker installed on your machine.

## Setup and Running the Application

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mary84215/simple_model_api.git
    cd simple_model_api
    ```

2.  **Train the Model (Optional):**
    A pre-trained model `model.pkl` is included in the `dev` directory. To retrain the model, run the training script from the project root. This will create a new `model.pkl` in the `dev/` directory.
    ```bash
    python dev/training.py
    ```

3.  **Prepare for Production:**
    Copy the trained model from the `dev` directory to the `prod` directory so it can be included in the Docker image.
    ```bash
    # On macOS/Linux
    cp dev/model.pkl prod/model.pkl

    # On Windows
    copy dev\model.pkl prod\model.pkl
    ```

4.  **Build the Docker Image:**
    Navigate to the `prod` directory and build the Docker image.
    ```bash
    cd prod
    docker build -t personality-api .
    ```

5.  **Run the Docker Container:**
    Run the container, mapping port 5000 on your host to port 5000 in the container.
    ```bash
    docker run -d -p 5000:5000 --name personality-container personality-api
    ```
    The API will now be running and accessible at `http://localhost:5000`.

## API Usage

All endpoints require an `X-API-KEY` header for authentication. Valid keys include `abc123` or `mary84215`.

### 1. Predict Personality

- **Endpoint**: `/predict`
- **Method**: `POST`
- **Headers**:
  - `Content-Type: application/json`
  - `X-API-KEY: your_api_key`
- **Body**: A JSON array with one or more objects containing the feature data.

**Example `curl` request:**
```bash
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-H "X-API-KEY: abc123" \
-d '[{"Time_spent_Alone":10.0,"Stage_fear":1,"Social_event_attendance":3.0,"Going_outside":3.0,"Drained_after_socializing":1,"Friends_circle_size":5.0,"Post_frequency":3.0}]'
```

### 2. Download Logs

- **Endpoint**: `/log`
- **Method**: `GET`
- **Headers**:
  - `X-API-KEY: your_api_key`

**Example `curl` request:**

This command will download the `app.log` file to your current directory.
```bash
curl -X GET http://localhost:5000/log -H "X-API-KEY: abc123" -o app.log
```