# Stroke Risk Prediction API

This project is a Flask-based web API for predicting stroke risk using machine learning. The backend is powered by a trained Random Forest model and is deployed on Render.

## Project Structure

/Stroke-Risk-Prediction │-- app.py # Flask API for stroke prediction │-- Stroke_Risk_Prediction.ipynb # Jupyter notebook with ML model training │-- requirements.txt # Python dependencies │-- Procfile # Render deployment command │-- /model │ ├── model_rf_new.pkl # Trained ML model (Random Forest) │-- /templates │ ├── index.html # UI for interacting with the API │-- /static # CSS/JS files (if needed)

## Features

- Accepts user health data such as age, gender, glucose level, BMI, and other relevant parameters.
  
- Uses a pre-trained Random Forest model for prediction.
  
- Returns whether a person is at risk of stroke or not.
  
- Provides a web-based interface for easy interaction.
  
- Deployed on Render for public access.

## Installation and Setup

### 1. Clone the Repository

```bash

git clone https://github.com/your-username/Stroke-Risk-Prediction.git

cd Stroke-Risk-Prediction

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Run the Flask Application

python app.py

The app will be available at http://127.0.0.1:5000/.

### API Endpoints

1. Home Page

•	GET / → Loads the web UI (index.html)

2. Stroke Risk Prediction

•	POST /predict → Accepts user data and returns stroke risk prediction.

•	Input Format (JSON or Form Data):
{
  "age": 50,
  "gender": "Male",
  "hypertension": 1,
  "heart_disease": 0,
  "avg_glucose_level": 85.6,
  "bmi": 25.4,
  "ever_married": "Yes",
  "work_type": "Private",
  "residence_type": "Urban",
  "smoking_status": "never smoked"
}

•	Example Response:

{
  "prediction": "The person is at risk of stroke."
}

### Deploying to Render

1. Push the Code to GitHub

git add .

git commit -m "Initial commit"

git push origin main

2. Deploy on Render

1.	Go to Render.

2.	Click New + → Web Service.

3.	Connect your GitHub repository.

4.	Set Build Command:

pip install -r requirements.txt

5.	Set Start Command:

gunicorn app:app

6.	Click "Deploy" and wait for deployment to complete.

### Troubleshooting

Getting a 404 Error?

•	Ensure index.html exists in the templates/ folder.

Model Not Found?

•	Make sure model_rf_new.pkl is inside the /model/ directory.

Deployment Failing on Render?

Try triggering a redeploy:

git commit --allow-empty -m "Trigger redeploy"

git push origin main
Contributing
Contributions are welcome! If you would like to contribute, feel free to submit a pull request.
License
This project is open-source under the MIT License.


