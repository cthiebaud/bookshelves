from flask import Flask, jsonify, render_template, request
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perform_regression', methods=['POST'])
def perform_regression():
    data = request.get_json()

    # Extract data
    X1 = data['X1']
    X2 = data['X2']
    Y = data['Y']

    # Reshape the data for sklearn
    X = np.column_stack((X1, X2))

    # Perform linear regression
    model = LinearRegression()
    model.fit(X, Y)

    # Get coefficients
    coefficients = {'intercept': model.intercept_, 'coef_X1': model.coef_[0], 'coef_X2': model.coef_[1]}

    return jsonify(coefficients)

if __name__ == '__main__':
    app.run(debug=True)
