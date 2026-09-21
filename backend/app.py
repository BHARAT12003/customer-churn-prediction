from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import joblib

from pathlib import Path


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "model" / "churn_model.pkl"
SCALER_PATH = BASE_DIR / "model" / "scaler.pkl"
FEATURES_PATH = BASE_DIR / "model" / "feature_columns.pkl"


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_columns = joblib.load(FEATURES_PATH)


print("\n" + "=" * 60)
print("          CUSTOMER CHURN PREDICTION API")
print("=" * 60)

print("\nModel loaded successfully.")
print("Number of features:", len(feature_columns))


# ============================================================
# HOME
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Customer Churn Prediction API is running",
        "status": "success"
    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "model_loaded": True
    })


# ============================================================
# CREATE MODEL FEATURES
# ============================================================

def prepare_customer_data(data):

    # Start with an empty row containing all model features
    customer = pd.DataFrame(
        0,
        index=[0],
        columns=feature_columns
    )

    # --------------------------------------------------------
    # NUMERICAL FEATURES
    # --------------------------------------------------------

    customer["SeniorCitizen"] = int(
        data.get("senior_citizen", 0)
    )

    customer["tenure"] = float(
        data.get("tenure", 0)
    )

    customer["MonthlyCharges"] = float(
        data.get("monthly_charges", 0)
    )

    customer["TotalCharges"] = float(
        data.get("total_charges", 0)
    )

    # --------------------------------------------------------
    # CATEGORICAL FEATURES
    # --------------------------------------------------------

    categorical_mapping = {

        "gender": "gender_",

        "partner": "Partner_",

        "dependents": "Dependents_",

        "phone_service": "PhoneService_",

        "multiple_lines": "MultipleLines_",

        "internet_service": "InternetService_",

        "online_security": "OnlineSecurity_",

        "online_backup": "OnlineBackup_",

        "device_protection": "DeviceProtection_",

        "tech_support": "TechSupport_",

        "streaming_tv": "StreamingTV_",

        "streaming_movies": "StreamingMovies_",

        "contract": "Contract_",

        "paperless_billing": "PaperlessBilling_",

        "payment_method": "PaymentMethod_"
    }


    for input_name, feature_prefix in categorical_mapping.items():

        value = data.get(input_name)

        if value is None:
            continue

        feature_name = feature_prefix + str(value)

        if feature_name in customer.columns:

            customer.loc[0, feature_name] = 1


    return customer


# ============================================================
# PREDICTION
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ----------------------------------------------------
        # RECEIVE CUSTOMER DATA
        # ----------------------------------------------------

        data = request.get_json()

        if not data:

            return jsonify({
                "error": "No customer data received."
            }), 400


        # ----------------------------------------------------
        # PREPARE DATA
        # ----------------------------------------------------

        input_data = prepare_customer_data(data)


        # ----------------------------------------------------
        # SCALE DATA
        # ----------------------------------------------------

        input_scaled = scaler.transform(input_data)


        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        prediction = model.predict(input_scaled)[0]

        probability = model.predict_proba(
            input_scaled
        )[0][1]

        probability_percentage = probability * 100


        # ----------------------------------------------------
        # RISK LEVEL
        # ----------------------------------------------------

        if probability_percentage >= 70:

            risk_level = "High"

        elif probability_percentage >= 40:

            risk_level = "Medium"

        else:

            risk_level = "Low"


        # ----------------------------------------------------
        # RETENTION RECOMMENDATION
        # ----------------------------------------------------

        if risk_level == "High":

            recommendation = (
                "Offer a personalized retention plan, "
                "loyalty benefit, or targeted discount."
            )

        elif risk_level == "Medium":

            recommendation = (
                "Monitor the customer and provide "
                "personalized engagement or support."
            )

        else:

            recommendation = (
                "Maintain regular engagement and "
                "continue providing good service."
            )


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "prediction": int(prediction),

            "churn": (
                "Yes"
                if prediction == 1
                else "No"
            ),

            "churn_probability": round(
                probability_percentage,
                2
            ),

            "risk_level": risk_level,

            "recommendation": recommendation
        })


    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )