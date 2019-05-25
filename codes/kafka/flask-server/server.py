from flask import Flask,request
import json
from Lstm import Lstm
from PredictMC import PredictMC
from PredictHMM import PredictHMM


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route("/predict", methods=['POST'])
def predict():    
    l = []
    if  request.headers.get('Content-Type') == 'application/json; charset=UTF-8':             
        sequence = request.get_json()['seq']
        l = lstm_model.predict(sequence)
        m = mc_model.predict(sequence)
        h = mc_model.predict(sequence)     
    
    predictions = {}
    predictions['lstm_prediction'] = [l[0]]
    predictions['mc_prediction'] = [m]
    predictions['hmm_prediction'] = [h]
    
    return json.dumps(predictions) 


if __name__ == '__main__':    
    lstm_model = Lstm()
    mc_model = PredictMC()
    hmm_model = PredictHMM()
    app.run()


    