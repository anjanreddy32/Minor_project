# app.py
from flask import *
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
with open('model_loan.pkl', 'rb') as file:
    classifier = pickle.load(file)

@app.route('/')
def home():
    return render_template('home.html')

# Login Page Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            return redirect(url_for('prediction'))
        else:
            error = 'Invalid credentials'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/predict', methods=['GET', 'POST'])
def prediction():
    return render_template('index.html')



@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        features = [float(x) for x in request.form.values()]
        # Reshape the data for prediction
        features_array = np.array(features).reshape(1, -1)
        # Predict
        prediction = classifier.predict(features_array)
        if prediction[0] == 0:
            result = "Loan not approved."
        else:
            result = "Loan approved."
    
        return render_template('result.html', prediction_text=result)  # Change predicted_text to prediction_text
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True,port=5003)
