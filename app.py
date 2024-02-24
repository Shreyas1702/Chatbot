from flask import Flask, request, jsonify
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
from flask_cors import CORS 
app = Flask(__name__)
CORS(app)
df = pd.read_csv("api_endpoints.csv")  

def get_response(user_input):
    
    endpoint_ratios = process.extract(user_input, df['Endpoint'], scorer=fuzz.token_set_ratio)
    best_match = max(endpoint_ratios, key=lambda x: x[1])[0]  

    
    response = df[df['Endpoint'] == best_match][['Endpoint','Purpose', 'Functionality']].iloc[0]

    return response.to_dict()


@app.route('/bot', methods=['POST'])
def chatbot():
    data = request.get_json()
    print(data)
    user_input = data['inpt']
    response = get_response(user_input)
    print(response)
    return jsonify(response)

@app.route('/', methods=['GET'])
def namesefg():
    return "Helllo"

if __name__ == "__main__":
    app.run(debug=True)