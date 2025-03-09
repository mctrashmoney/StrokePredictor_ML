import os
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from flask import Flask, request, render_template
from pathlib import Path

# Get the directory of the current script
current_dir = Path(__file__).parent


# Define the model directory and scaler file path
model_dir = current_dir / "model"
scaler_path = model_dir / "scaler.pkl"

# Ensure the model directory exists
model_dir.mkdir(parents=True, exist_ok=True)

# Load the dataset
df = pd.read_csv(current_dir / "healthcare-dataset-stroke-data.csv")

# Data cleaning and preprocessing (mimicking the steps from your notebook)
df_cleaned = df.dropna(subset=['bmi', 'smoking_status'])
df_cleaned = pd.get_dummies(df_cleaned)

# Define features (remove 'id' and 'stroke' columns, 'stroke' is the target)
X = df_cleaned.copy()
X.drop(columns=["stroke", "id"], axis=1, inplace=True)

# Initialize StandardScaler
scaler = StandardScaler()

# Fit the scaler to the data (using the same features you would use for prediction)
X_scaled = scaler.fit_transform(X)

# Save the scaler to a file

joblib.dump(scaler, scaler_path)

print(f"Scaler saved to {scaler_path}")

# Initialize Flask app
app = Flask(__name__)




# Path to the model and scaler files
model_path = current_dir / "model" / "xgboost_model.pkl"
scaler_path = current_dir / "model" / "scaler.pkl"

# Load the model and scaler
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Feature columns for one-hot encoding and standardization
feature_columns = [
    'age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi',
    'gender_Female', 'gender_Male', 'gender_Other',
    'ever_married_No', 'ever_married_Yes',
    'work_type_Govt_job', 'work_type_Never_worked', 'work_type_Private', 'work_type_Self-employed', 'work_type_children',
    'Residence_type_Rural', 'Residence_type_Urban',    
    'smoking_status_Unknown', 'smoking_status_formerly smoked', 'smoking_status_never smoked', 'smoking_status_smokes'
]

# Web App Title
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
           

            ########################################
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
            gender_encoded = [1 if gender == "Female" else 0, 1 if gender == "Male" else 0, 1 if gender == "Other" else 0]
            print(f"Encoded gender: {gender_encoded}")  # Debugging

            ever_married_encoded = [1 if ever_married == "No" else 0, 1 if ever_married == "Yes" else 0]
            residence_encoded = [1 if residence_type == "Rural" else 0, 1 if residence_type == "Urban" else 0]
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

            # Convert input data into a DataFrame to apply the same scaler
            input_df = pd.DataFrame([input_data], columns=feature_columns)

            # Ensure all columns are present (in case any category is missing)
            for col in feature_columns:
                if col not in input_df.columns:
                    input_df[col] = 0

            # Reorder columns to match the training order
            input_df = input_df[feature_columns]

            # Standardize the user input using the loaded scaler
            input_data_scaled = scaler.transform(input_df)

            # Predict the probability of stroke risk
            #risk_score = model.predict_proba(input_data_scaled)[0][1]
            #risk_percentage = risk_score * 100

            # Make the prediction
            prediction = model.predict(input_data_scaled)

            # Return the prediction result
            if prediction[0] == 1:
                return render_template("index.html", prediction_text="The person is at risk of stroke.")
                #return render_template("index.html", prediction_text=f"The person is at risk of stroke with {risk_percentage:.2f}% risk.")
            else:
                return render_template("index.html", prediction_text="The person is not at risk of stroke.")

        except Exception as e:
            return render_template("index.html", prediction_text=f"Error: {str(e)}. Check console logs for details.")

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT not set
    app.run(host="0.0.0.0", port=port)
