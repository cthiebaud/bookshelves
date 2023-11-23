from sklearn.preprocessing import StandardScaler
from flask import Flask, jsonify, render_template, request
import numpy as np
from sklearn.linear_model import LinearRegression
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    n_points = 16
    X1_plane = np.linspace(0, 255, n_points)
    X2_plane = np.linspace(0, 255, n_points)
    X1_plane, X2_plane = np.meshgrid(X1_plane, X2_plane)
    Y_plane = coefficients['intercept'] + coefficients['coef_X1'] * X1_plane + coefficients['coef_X2'] * X2_plane

    # Coerce z-coordinates onto the regression plane
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Calculate coerced z-coordinates for the second scatter plot
    Z_coerced_second = coefficients['intercept'] + coefficients['coef_X1'] * X_scaled[:, 0] + coefficients['coef_X2'] * X_scaled[:, 1]

    # Reshape coerced z-coordinates for the second scatter plot
    Z_coerced_second = np.array(Z_coerced_second).reshape(np.array(Y).shape)

    # Prepare results to send back to the frontend
    results = {
        'coefficients': coefficients,
        'meshgrid': {'X1': X1_plane.tolist(), 'X2': X2_plane.tolist(), 'Y': Y_plane.tolist()},
        'std_dev_residuals': std_dev_residuals,
        'coercedZ_second': Z_coerced_second.tolist()  # Add coerced z-coordinates for the second scatter plot to results
    }

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
