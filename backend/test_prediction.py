import json
import urllib.request


url = "http://127.0.0.1:5000/predict"


customer = {
    "gender_Male": 1,
    "SeniorCitizen": 0,
    "Partner_Yes": 1,
    "Dependents_Yes": 0,
    "tenure": 12,
    "PhoneService_Yes": 1,
    "MultipleLines_Yes": 0,
    "InternetService_Fiber optic": 1,
    "OnlineSecurity_Yes": 0,
    "OnlineBackup_Yes": 1,
    "DeviceProtection_Yes": 0,
    "TechSupport_Yes": 0,
    "StreamingTV_Yes": 1,
    "StreamingMovies_Yes": 1,
    "Contract_One year": 0,
    "Contract_Two year": 0,
    "PaperlessBilling_Yes": 1,
    "PaymentMethod_Electronic check": 1,
    "PaymentMethod_Mailed check": 0,
    "PaymentMethod_Credit card (automatic)": 0,
    "PaymentMethod_Bank transfer (automatic)": 0,
    "MonthlyCharges": 80.0,
    "TotalCharges": 960.0
}


data = json.dumps(customer).encode("utf-8")


request = urllib.request.Request(
    url,
    data=data,
    headers={
        "Content-Type": "application/json"
    },
    method="POST"
)


try:

    with urllib.request.urlopen(request) as response:

        result = response.read().decode("utf-8")

        print("\nStatus code:", response.status)

        print("\nPrediction result:")

        print(json.dumps(
            json.loads(result),
            indent=4
        ))


except Exception as error:

    print("\nPrediction request failed:")
    print(error)