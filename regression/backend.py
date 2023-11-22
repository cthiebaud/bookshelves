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

    # Predict Y values
    Y_pred = model.predict(X)

    # Calculate residuals
    residuals = Y - Y_pred

    # Calculate standard deviation of residuals
    std_dev_residuals = np.std(residuals)

    # Create a meshgrid for the plane
    n_points = 10
    X1_plane = np.linspace(min(X1), max(X1), n_points)
    X2_plane = np.linspace(min(X2), max(X2), n_points)
    X1_plane, X2_plane = np.meshgrid(X1_plane, X2_plane)
    Y_plane = coefficients['intercept'] + coefficients['coef_X1'] * X1_plane + coefficients['coef_X2'] * X2_plane

    # Prepare results to send back to the frontend
    results = {
        'coefficients': coefficients,
        'meshgrid': {'X1': X1_plane.tolist(), 'X2': X2_plane.tolist(), 'Y': Y_plane.tolist()},
        'std_dev_residuals': std_dev_residuals
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
