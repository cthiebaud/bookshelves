from flask import Flask, jsonify, render_template, request
import numpy as np
from sklearn.linear_model import LinearRegression
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

def perform_regression_and_get_std_dev_and_model(X1, X2, Y):
    # Reshape the data for sklearn
    X = np.column_stack((X1, X2))

    # Perform linear regression
    model = LinearRegression()
    model.fit(X, Y)

    # Predict Y values
    Y_pred = model.predict(X)

    # Calculate residuals
    residuals = Y - Y_pred

    # Calculate standard deviation of residuals
    std_dev_residuals = np.std(residuals)

    # print(f"std_dev_residuals: {std_dev_residuals}")

    return std_dev_residuals, model

@app.route('/perform_regression', methods=['POST'])
def perform_regression():
    data = request.get_json()

    # Extract data
    xyz = [
        data['x'],
        data['y'],
        data['z']
    ]

    permutations = [
        [0,1,2],
        [2,1,0],
        [0,2,1],    
    ]

    # Calculate std_dev_residuals and get the model for the original data
    res = [perform_regression_and_get_std_dev_and_model(xyz[p[0]], xyz[p[1]], xyz[p[2]]) for p in permutations]

    # print(res)

    # Find the permutation with the lowest std_dev_residuals
    p, best_permutation = min(
        enumerate(res),
        key=lambda x: x[1][0]
    )
    P = permutations[p]
    std_dev_residuals = best_permutation[0]
    model = best_permutation[1]
    
    # print(P, "model.coef_", model.coef_, "model.intercept_", model.intercept_)

    # Create a meshgrid for the plane
    n_points = 16
    X1_plane = np.linspace(0, 256, n_points)
    X2_plane = np.linspace(0, 256, n_points)
    X1_plane, X2_plane = np.meshgrid(X1_plane, X2_plane)
    Y_plane = model.intercept_ + model.coef_[0] * X1_plane + model.coef_[1] * X2_plane

    planes = [X1_plane.tolist(), X2_plane.tolist(), Y_plane.tolist()]
    coeffs = [model.coef_[0], model.coef_[1], -1]

    coefficients = {'intercept': model.intercept_, 'x': coeffs[P[0]], 'y': coeffs[P[1]], 'z': coeffs[P[2]]}
    meshgrid =  {'x': planes[P[0]], 'y': planes[P[1]], 'z': planes[P[2]]}

    # Prepare results to send back to the frontend
    results = {
        'coefficients': coefficients,
        'meshgrid': meshgrid,
        'std_dev_residuals': std_dev_residuals
    }

    print(f"{data['image']}:\n\tstd_dev: {std_dev_residuals}")

    # Return results to the frontend
    return jsonify(results)

@app.route('/perform_regression2d', methods=['POST'])
def perform_regression2d():
    data = request.get_json()

    # Extract data
    X = data['X']
    Y = data['Y']

    # Reshape the data for sklearn
    X = np.array(X).reshape(-1, 1)

    # Perform simple linear regression
    model = LinearRegression()
    model.fit(X, Y)

    # Get coefficients
    coefficients = {'intercept': model.intercept_, 'coef_X': model.coef_[0]}

    # Predict Y values
    Y_pred = model.predict(X)

    # Calculate residuals
    residuals = Y - Y_pred

    # Calculate standard deviation of residuals
    std_dev_residuals = np.std(residuals)

    # Prepare results to send back to the frontend
    results = {
        'coefficients': coefficients,
        'std_dev_residuals': std_dev_residuals
    }

    # Return results to the frontend
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=4321)
