"""Example script to demonstrate requirements.txt auto-generation."""

import requests
from flask import Flask, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route("/data")
def get_data():
    response = requests.get("https://api.example.com/data")
    df = pd.DataFrame(response.json())
    arr = np.array(df.values)
    return jsonify({"mean": float(arr.mean())})


if __name__ == "__main__":
    app.run(debug=True)
