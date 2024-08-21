from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging

import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

def scale(payload):
    """Scales Payload"""

    LOG.info("Scaling Payload: %s payload")
    scaler = StandardScaler().fit(payload)
    scaled_adhoc_predict = scaler.transform(payload)
    return scaled_adhoc_predict

@app.route("/")
def home():
    html = "<h3>Sklearn Prediction Home</h3>"
    return html.format(format)

@app.route("/hello")
def hello():
    html = "<h1>Hello world!!!</h1>"
    return html.format(format)

# TO DO:  Log out the prediction value
@app.route("/predict", methods=['POST'])
def predict():
    # Performs an sklearn prediction
    LOG.info("JSON payload: %s", request.json)

    try:
        # Load pretrained model as clf. Try any one model. 
        clf = joblib.load("./LinearRegression.joblib")
        # clf = joblib.load("./StochasticGradientDescent.joblib")
        # clf = joblib.load("./GradientBoostingRegressor.joblib")
    except Exception as e:
        LOG.error(repr(e))
        return "Model not loaded"

    json_payload = request.json
    LOG.info("JSON payload: %s json_payload")
    inference_payload = pd.DataFrame(json_payload)
    LOG.info("inference payload DataFrame: %s inference_payload")
    scaled_payload = scale(inference_payload)
    prediction = list(clf.predict(scaled_payload))
    return jsonify({'prediction': prediction})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
