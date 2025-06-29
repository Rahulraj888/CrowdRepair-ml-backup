# app.py

import config
from flask import Flask, request, jsonify
from flask_cors import CORS
from clustering.clusterer import run_dbscan

app = Flask(__name__)
CORS(app)  # enable CORS for all origins


@app.route('/predict_hotspots', methods=['POST'])
def predict_hotspots():
    """
    Expects JSON: { "reports": [ { "latitude": ..., "longitude": ... }, … ] }
    Returns a GeoJSON FeatureCollection of clustered polygons.
    """
    payload = request.get_json(force=True)
    reports = payload.get('reports', [])

    # Delegate all the clustering work to our clusterer
    feature_collection = run_dbscan(reports)
    return jsonify(feature_collection), 200


if __name__ == '__main__':
    app.run(port=config.FLASK_PORT)
