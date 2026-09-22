// =========================================================
// CHURNGUARD - FRONTEND PREDICTION LOGIC
// =========================================================

// Flask API URL
const API_URL = "https://customer-churn-api-etzn.onrender.com/predict";

// Get HTML elements
const predictionForm = document.getElementById("predictionForm");

const initialState = document.getElementById("initialState");
const loadingState = document.getElementById("loadingState");
const resultState = document.getElementById("resultState");

const probability = document.getElementById("probability");
const riskBadge = document.getElementById("riskBadge");
const churnResult = document.getElementById("churnResult");
const recommendation = document.getElementById("recommendation");
const predictionStatus =
    document.getElementById("predictionStatus");
const riskScoreText = document.getElementById("riskScoreText");
const riskScoreFill = document.getElementById("riskScoreFill");

const riskFactors = document.getElementById("riskFactors");
const riskFactorList = document.getElementById("riskFactorList");

const predictionValue = document.getElementById("predictionValue");
const riskValue = document.getElementById("riskValue");

const probabilityCircle =
    document.querySelector(".probability-circle");


// =========================================================
// FORM SUBMISSION
// =========================================================

predictionForm.addEventListener("submit", async function (event) {

    // Prevent page refresh
    event.preventDefault();

    // Show loading state
    initialState.classList.add("hidden");
    resultState.classList.add("hidden");
    loadingState.classList.remove("hidden");
    // =====================================================
// INPUT VALIDATION
// =====================================================

const tenureInput = Number(
    document.getElementById("tenure").value
);

const monthlyChargesInput = Number(
    document.getElementById("monthly_charges").value
);

const totalChargesInput = Number(
    document.getElementById("total_charges").value
);

if (isNaN(tenureInput) || tenureInput < 0 || tenureInput > 100) {
    alert("Please enter a valid tenure between 0 and 100 months.");
    loadingState.classList.add("hidden");
    initialState.classList.remove("hidden");
    return;
}

if (isNaN(monthlyChargesInput) || monthlyChargesInput < 0) {
    alert("Please enter a valid monthly charge.");
    loadingState.classList.add("hidden");
    initialState.classList.remove("hidden");
    return;
}

if (isNaN(totalChargesInput) || totalChargesInput < 0) {
    alert("Please enter a valid total charge.");
    loadingState.classList.add("hidden");
    initialState.classList.remove("hidden");
    return;
}

    // Collect customer information
    const customerData = {

        gender:
            document.getElementById("gender").value,

        senior_citizen:
            Number(
                document.getElementById("senior_citizen").value
            ),

        partner:
            document.getElementById("partner").value,

        dependents:
            document.getElementById("dependents").value,

        tenure: tenureInput,

        phone_service:
            document.getElementById("phone_service").value,

        multiple_lines:
            document.getElementById("multiple_lines").value,

        internet_service:
            document.getElementById("internet_service").value,

        online_security:
            document.getElementById("online_security").value,

        online_backup:
            document.getElementById("online_backup").value,

        device_protection:
            document.getElementById("device_protection").value,

        tech_support:
            document.getElementById("tech_support").value,

        streaming_tv:
            document.getElementById("streaming_tv").value,

        streaming_movies:
            document.getElementById("streaming_movies").value,

        contract:
            document.getElementById("contract").value,

        paperless_billing:
            document.getElementById("paperless_billing").value,

        payment_method:
            document.getElementById("payment_method").value,

        monthly_charges: monthlyChargesInput,

        total_charges: totalChargesInput
    };


    // =====================================================
    // SEND DATA TO FLASK
    // =====================================================

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(customerData)
        });


        // Convert response to JSON
        const data = await response.json();


        // Check API response
        if (!response.ok) {

            throw new Error(
                data.error || "Prediction request failed."
            );
        }


        // Display prediction
        displayPrediction(data);


    } catch (error) {

        console.error("Prediction error:", error);

        loadingState.classList.add("hidden");
        resultState.classList.add("hidden");
        initialState.classList.remove("hidden");

        alert(
            "Unable to connect to the prediction server.\n\n" +
            "Make sure Flask is running at:\n" +
            "http://127.0.0.1:5000"
        );
    }

});


// =========================================================
// DISPLAY PREDICTION
// =========================================================

function displayPrediction(data) {

    // Hide loading
    loadingState.classList.add("hidden");

    // Show result
    resultState.classList.remove("hidden");
    predictionStatus.textContent =
    "✓ AI Prediction Completed";


    // Get values
    const churnProbability =
        Number(data.churn_probability);

    const riskLevel =
        data.risk_level;

    const churn =
        data.churn;


    // =====================================================
    // PROBABILITY
    // =====================================================

    probability.textContent =
        `${churnProbability.toFixed(2)}%`;
        // Update risk score bar
riskScoreText.textContent =
    `${churnProbability.toFixed(2)}%`;

riskScoreFill.style.width =
    `${churnProbability}%`;


    // Convert percentage to circle degrees
    const degrees =
        (churnProbability / 100) * 360;


    probabilityCircle.style.background =
        `conic-gradient(
            #6366f1 ${degrees}deg,
            #e8eaf1 ${degrees}deg
        )`;


    // =====================================================
    // RISK LEVEL
    // =====================================================

    riskBadge.textContent =
        `${riskLevel.toUpperCase()} RISK`;
        riskBadge.classList.remove("high", "medium", "low");

if (data.risk_level === "High") {
    riskBadge.classList.add("high");
} else if (data.risk_level === "Medium") {
    riskBadge.classList.add("medium");
} else {
    riskBadge.classList.add("low");
}

    riskValue.textContent =
        riskLevel;


    // Remove previous risk classes
    riskBadge.classList.remove(
        "risk-high",
        "risk-medium",
        "risk-low"
    );


    // Apply correct risk style
    if (riskLevel === "High") {

        riskBadge.classList.add("risk-high");

    } else if (riskLevel === "Medium") {

        riskBadge.classList.add("risk-medium");

    } else {

        riskBadge.classList.add("risk-low");
    }


    // =====================================================
    // CHURN RESULT
    // =====================================================

    predictionValue.textContent =
        churn;


    if (churn === "Yes") {

        churnResult.textContent =
            "Customer May Churn";

    } else {

        churnResult.textContent =
            "Customer Likely to Stay";
    }


    // =====================================================
    // RECOMMENDATION
    // =====================================================

    recommendation.textContent =
        data.recommendation;

// Generate customer risk factors
const factors = [];

const tenure = Number(document.getElementById("tenure").value);
const monthlyCharges = Number(
    document.getElementById("monthly_charges").value
);
const contract = document.getElementById("contract").value;
const internetService = document.getElementById("internet_service").value;
const onlineSecurity = document.getElementById("online_security").value;
const techSupport = document.getElementById("tech_support").value;
const paymentMethod = document.getElementById("payment_method").value;

if (contract === "Month-to-month") {
    factors.push("Month-to-month contract may indicate higher churn risk.");
}

if (tenure <= 12) {
    factors.push("Short customer tenure indicates an early-stage customer.");
}

if (monthlyCharges >= 70) {
    factors.push("Higher monthly charges may increase churn risk.");
}

if (internetService === "Fiber optic") {
    factors.push("Fiber optic customers show a notable churn pattern in the dataset.");
}

if (onlineSecurity === "No") {
    factors.push("Customer does not have online security service.");
}

if (techSupport === "No") {
    factors.push("Customer does not have technical support service.");
}

if (paymentMethod === "Electronic check") {
    factors.push("Electronic check payment method is associated with higher churn in the dataset.");
}

// Show factors
riskFactorList.innerHTML = "";


if (factors.length === 0) {
    riskFactorList.innerHTML = `
        <div class="risk-factor-item">
            <span>✓</span>
            <p>No major risk factors identified from the customer profile.</p>
        </div>
    `;
} else {
    factors.forEach(factor => {
        riskFactorList.innerHTML += `
            <div class="risk-factor-item">
                <span>⚠</span>
                <p>${factor}</p>
            </div>
        `;
    });
}

riskFactors.classList.remove("hidden");
// Generate retention actions based on risk level
const retentionActions = document.getElementById("retentionActions");

let actions = [];

if (data.risk_level === "High") {

    actions = [
        {
            icon: "💰",
            title: "Personalized Retention Offer",
            text: "Provide a targeted discount or loyalty benefit to reduce churn risk."
        },
        {
            icon: "📞",
            title: "Immediate Customer Outreach",
            text: "Contact the customer proactively and understand their concerns."
        },
        {
            icon: "🎁",
            title: "Loyalty Benefit",
            text: "Offer an additional service benefit or exclusive customer incentive."
        },
        {
            icon: "🔄",
            title: "Contract Upgrade",
            text: "Consider offering a suitable long-term contract with additional benefits."
        }
    ];

} else if (data.risk_level === "Medium") {

    actions = [
        {
            icon: "📞",
            title: "Proactive Engagement",
            text: "Contact the customer and provide personalized service support."
        },
        {
            icon: "🎁",
            title: "Loyalty Benefit",
            text: "Offer a small loyalty benefit to strengthen customer engagement."
        },
        {
            icon: "🔄",
            title: "Contract Recommendation",
            text: "Consider recommending a longer-term contract with suitable benefits."
        }
    ];

} else {

    actions = [
        {
            icon: "⭐",
            title: "Maintain Engagement",
            text: "Continue providing reliable service and regular customer engagement."
        },
        {
            icon: "💬",
            title: "Customer Satisfaction",
            text: "Maintain good communication and monitor customer satisfaction."
        },
        {
            icon: "🎁",
            title: "Loyalty Building",
            text: "Consider suitable loyalty benefits to maintain long-term engagement."
        }
    ];
}

retentionActions.innerHTML = actions.map(action => `
    <div class="retention-action">
        <span class="action-icon">${action.icon}</span>
        <div>
            <strong>${action.title}</strong>
            <p>${action.text}</p>
        </div>
    </div>
`).join("");

retentionPlan.classList.remove("hidden");
}