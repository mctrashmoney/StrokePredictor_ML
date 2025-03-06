from flask import Flask, request, render_template
from pathlib import Path
import os
import pandas as pd
import joblib  # To load the model

# Get the directory of the current script
current_dir = Path(__file__).parent

# Construct the relative path to the model file
model_path = current_dir / "model" / "model_rf_new.pkl"

# Load the model
model = joblib.load(model_path)

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    app.logger.info("Home route accessed")  # Logs when this route is hit
    return render_template("index.html")

# Define the route for prediction
@app.route("/predict", methods=["GET", "POST"])
def predict():
    app.logger.info("Predict route accessed")  # <-- Add this here
    if request.method == "POST":
        try:
            # Collect user input from the form (assuming input names match)
            age = float(request.form["age"])
            gender = request.form["gender"]  # Male, Female, Other
            hypertension = int(request.form["hypertension"])  # 0 or 1
            heart_disease = int(request.form["heart_disease"])  # 0 or 1
            avg_glucose_level = float(request.form["avg_glucose_level"])
            bmi = float(request.form["bmi"])
            ever_married = request.form["ever_married"]  # Yes or No
            work_type = request.form["work_type"]  # e.g., Private, Self-employed, etc.
            residence_type = request.form["residence_type"]  # Urban or Rural
            smoking_status = request.form["smoking_status"]  # never smoked, formerly smoked, smokes, Unknown

            # Create a DataFrame for the input data
            input_data = pd.DataFrame({
                "age": [age],
                "hypertension": [hypertension],
                "heart_disease": [heart_disease],
                "avg_glucose_level": [avg_glucose_level],
                "bmi": [bmi],
                "gender_Female": [1 if gender == "Female" else 0],
                "gender_Male": [1 if gender == "Male" else 0],
                "gender_Other": [1 if gender == "Other" else 0],
                "ever_married_No": [1 if ever_married == "No" else 0],
                "ever_married_Yes": [1 if ever_married == "Yes" else 0],
                "work_type_Govt_job": [1 if work_type == "Govt_job" else 0],
                "work_type_Never_worked": [1 if work_type == "Never_worked" else 0],  # Added
                "work_type_Private": [1 if work_type == "Private" else 0],
                "work_type_Self-employed": [1 if work_type == "Self-employed" else 0],
                "work_type_children": [1 if work_type == "children" else 0],
                "Residence_type_Rural": [1 if residence_type == "Rural" else 0],
                "Residence_type_Urban": [1 if residence_type == "Urban" else 0],
                "smoking_status_Unknown": [1 if smoking_status == "Unknown" else 0],
                "smoking_status_formerly smoked": [1 if smoking_status == "formerly smoked" else 0],  # Fixed name
                "smoking_status_never smoked": [1 if smoking_status == "never smoked" else 0],  # Fixed name
                "smoking_status_smokes": [1 if smoking_status == "smokes" else 0]
            })

            # Make prediction
            prediction = model.predict(input_data)

            # Debugging: Print raw output
            print("Model Prediction Output:", prediction)  
            print("Input Data for Prediction:\n", input_data)

            # Return the result to the user
            if prediction[0] == 1:
                return render_template("index.html", prediction_text="The person is at risk of stroke.")
            else:
                return render_template("index.html", prediction_text="The person is not at risk of stroke.")
        
        except Exception as e:
            print("Error occurred:", str(e))  # Print the error message to the console
            print("Input Data Columns:", input_data.columns.tolist())  # Print feature names
            print("Input Data:\n", input_data)  # Print the actual input data
            return render_template("index.html", prediction_text=f"Error: {str(e)}. Check console logs for details.")
    
    return render_template("index.html")

#if __name__ == "__main__":
    #app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT not set
    app.run(host="0.0.0.0", port=port)
