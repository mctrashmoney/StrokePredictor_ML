import os
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from flask import Flask, request, render_template
from pathlib import Path

# Initialize Flask app
app = Flask(__name__)

# Get the directory of the current script
current_dir = Path(__file__).parent

# Path to the model and scaler files
model_path = current_dir / "model" / "VotingClassifier_LR_RF_SVM_model.pkl"
# model_path = current_dir / "model" / "xgboost_model.pkl"
# model_path = current_dir / "model" / "model_rf_new.pkl"
scaler_path = current_dir / "model" / "scaler.pkl"

# Step to create the scaler.pkl if it doesn't exist
def create_and_save_scaler():
    if not scaler_path.exists():
        print("Scaler file not found, creating scaler...")

        # Create a sample dataset (this should ideally be your training dataset)
        # For demonstration, we'll assume the dataset is a CSV with the same columns
        #data = pd.read_csv('C:/Gayatri/UnivOfTexas_Bootcamp/classes/Assignment/project4/stroke_risk/dataset1/6march_4_57PM/df_cleaned_export.csv')
        dataset_path = current_dir / "df_cleaned_export.csv"
        data = pd.read_csv(dataset_path)
        # List of columns that need to be scaled
        columns_to_scale = [
            'age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi',
            'gender_Female', 'gender_Male', 'gender_Other', 'ever_married_No',
            'ever_married_Yes', 'work_type_Govt_job', 'work_type_Never_worked',
            'work_type_Private', 'work_type_Self-employed', 'work_type_children',
            'Residence_type_Rural', 'Residence_type_Urban',
            'smoking_status_Unknown', 'smoking_status_formerly smoked',
            'smoking_status_never smoked', 'smoking_status_smokes'
        ]

        # Extract the features to be scaled
        features = data[columns_to_scale]

        # Initialize the scaler and fit it to the data
        scaler = StandardScaler()
        scaler.fit(features)

        # Save the scaler to the file
        joblib.dump(scaler, scaler_path)
        print(f"Scaler saved to {scaler_path}")

# Call the function to create the scaler if it doesn't exist
create_and_save_scaler()

# Load the model and scaler
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # Collect user input from the form
            age = int(request.form["age"])
            gender = request.form["gender"]
            hypertension = int(request.form["hypertension"])
            heart_disease = int(request.form["heart_disease"])
            avg_glucose_level = float(request.form["avg_glucose_level"])
            bmi = float(request.form["bmi"])
            ever_married = request.form["ever_married"]
            work_type = request.form["work_type"]
            residence_type = request.form["residence_type"]
            smoking_status = request.form["smoking_status"]

            # One-hot encode the categorical variables
            gender_encoded = [1 if gender == "Male" else 0, 1 if gender == "Female" else 0, 1 if gender == "Other" else 0]
            ever_married_encoded = [1 if ever_married == "Yes" else 0, 1 if ever_married == "No" else 0]
            residence_encoded = [1 if residence_type == "Urban" else 0, 1 if residence_type == "Rural" else 0]
            smoking_status_encoded = [1 if smoking_status == "Unknown" else 0,
                                      1 if smoking_status == "formerly smoked" else 0, 
                                      1 if smoking_status == "never smoked" else 0, 
                                      1 if smoking_status == "smokes" else 0
                                      ]
            work_type_encoded = [1 if work_type == "Govt_job" else 0,
                                 1 if work_type == "Never_worked" else 0,
                                 1 if work_type == "Private" else 0,
                                 1 if work_type == "Self-employed" else 0,
                                 1 if work_type == "children" else 0]

            # Prepare the input data as an array
            input_data = [
                age, hypertension, heart_disease, avg_glucose_level, bmi
            ] + gender_encoded + ever_married_encoded + work_type_encoded + residence_encoded + smoking_status_encoded

            # Convert input data into a DataFrame for scaling
            input_df = pd.DataFrame([input_data], columns=[
                'age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi',
                'gender_Female', 'gender_Male', 'gender_Other', 'ever_married_No',
                'ever_married_Yes', 'work_type_Govt_job', 'work_type_Never_worked',
                'work_type_Private', 'work_type_Self-employed', 'work_type_children',
                'Residence_type_Rural', 'Residence_type_Urban',
                'smoking_status_Unknown', 'smoking_status_formerly smoked',
                'smoking_status_never smoked', 'smoking_status_smokes'
            ])

            # Standardize the user input using the loaded scaler
            input_data_scaled = scaler.transform(input_df)

            # Make the prediction
            prediction = model.predict(input_data_scaled)

            # Return the prediction result
            if prediction[0] == 1:
                return render_template("index.html", prediction_text="The person is at risk of stroke.")
            else:
                return render_template("index.html", prediction_text="The person is not at risk of stroke.")

        except Exception as e:
            return render_template("index.html", prediction_text=f"Error: {str(e)}. Check console logs for details.")

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT not set
    app.run(host="0.0.0.0", port=port)
