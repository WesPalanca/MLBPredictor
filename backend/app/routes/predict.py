import os
from flask import Blueprint, jsonify, request
import joblib
import pandas as pd

bp = Blueprint('predict', __name__)

@bp.route("/api/predict", methods=['POST'])
def predict():
    # Get the absolute path of the model file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, '..' ,'..', 'predict', 'best_game_predictor.pkl')
    
    # Print the path for debugging
    print(f"Loading model from: {model_path}")
    
    # Load the model
    model = joblib.load(model_path)
    
    # Extract data from the request
    data = request.get_json()
    team = data.get("team")
    opp = data.get("opp")
    rank = data.get("rank")
    wins = data.get('wins')
    losses = data.get('losses')

    
    # Encoding for 'h/a': assume 1 for home, 0 for away
    h_a = 1 if data.get("h/a") == "home" else 0
    
    # Map opponents to their numeric codes
    code_map = {
        'ARI': 0, 'ATL': 1, 'BAL': 2, 'BOS': 3, 'CHC': 4, 'CHW': 5, 'CIN': 6, 'CLE': 7, 'COL': 8, 'DET': 9,
        'MIA': 10, 'HOU': 11, 'KCR': 12, 'LAA': 13, 'LAD': 14, 'MIL': 15, 'MIN': 16, 'NYM': 17, 'NYY': 18,
        'OAK': 19, 'PHI': 20, 'PIT': 21, 'SDP': 22, 'SFG': 23, 'SEA': 24, 'STL': 25, 'TBR': 26, 'TEX': 27,
        'TOR': 28, 'WSN': 29
    }

    # Convert and team and opponent to its numeric code
    team_code = code_map.get(team, -1)
    opp_code = code_map.get(opp, -1)  # Use -1 for unknown opponents

    # Prepare the input data for the model
    input_data = pd.DataFrame([{
        'Tm': team_code,
        'Rank': rank,
        'h/a': h_a,
        'Opp': opp_code,
        'Wins': wins,
        'Losses': losses,
    }])

    # Make prediction
    prediction = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)

    # Convert the prediction to a readable format
    result = {
        'prediction': int(prediction[0]),
        'prediction_proba': prediction_proba[0].tolist()
    }

    return jsonify(result)
