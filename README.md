# Stroke Risk Prediction API

This project is a Flask-based web API for predicting stroke risk using machine learning. The backend is powered by a trained Random Forest model and is deployed on Render.

## Project Structure

Project4_MachineLearning/
│
├── healthcare-dataset-stroke-data  # Your dataset     
│             
├── Stroke_Risk_Prediction.ipynb  # Jupyter notebook for exploring the model              
│   
│
├── model/                  
│   ├── model_rf_new.pkl    # Saved Random Forest model
│   └── model_SVM.pkl      # Saved SVM model
│   └── stroke_logistic_reg_model.pkl 
│
├── static/                 
│   └── style.css           # CSS file for styling your web app
│
├──├ templates/             
│   └── index.html          # HTML template for your web app's homepage          
│
├── app.py                  # Main file to run your Flask/Django web app
├── Procfile                # For deployment (e.g., on Heroku)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation  

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

```
### 2. Install Dependencies

pip install -r requirements.txt

### 3. Run the Flask Application

python app.py

The app will be available at http://127.0.0.1:5000/.

### 4. API Endpoints

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

### 5. Deploying to Render

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

## Troubleshooting

Getting a 404 Error?

•	Ensure index.html exists in the templates/ folder.

Model Not Found?

•	Make sure model_rf_new.pkl is inside the /model/ directory.

Deployment Failing on Render?

Try triggering a redeploy:

git commit --allow-empty -m "Trigger redeploy"

git push origin main

## Contributing

Contributions are welcome! If you would like to contribute, feel free to submit a pull request.

## License

This project is open-source under the MIT License.


