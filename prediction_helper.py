
import pandas as pd
import joblib

# Load artifacts once when the module is imported
try:
    model_young = joblib.load("artifacts/model_young.joblib")
    model_rest = joblib.load("artifacts/model_rest.joblib")
    scaler_young_obj = joblib.load("artifacts/scaler_young.joblib")
    scaler_rest_obj = joblib.load("artifacts/scaler_rest.joblib")
except FileNotFoundError:
    # Handle case where artifacts are not found
    # This is important for robustness, e.g., in a cloud environment
    print("Error: Model or scaler artifacts not found. Make sure the 'artifacts' directory is correct.")
    model_young = model_rest = scaler_young_obj = scaler_rest_obj = None


def calculate_normalized_risk(medical_history):
    """Calculates a normalized risk score based on medical history."""
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }
    diseases = medical_history.lower().split(" & ")
    total_risk_score = sum(risk_scores.get(disease, 0) for disease in diseases)
    max_possible_score = 14  # heart disease (8) + diabetes/high blood pressure (6)

    # Avoid division by zero if max_possible_score is 0
    if max_possible_score == 0:
        return 0.0

    normalized_risk_score = total_risk_score / max_possible_score
    return normalized_risk_score


def preprocess_input(input_dict):
    """
    Transforms the user input dictionary into a DataFrame ready for the model.
    This involves one-hot encoding, column standardization, and feature calculation.
    """
    # Create a DataFrame from the input dictionary
    df = pd.DataFrame([input_dict])

    # --- Feature Engineering ---
    # 1. Calculate Normalized Risk Score
    df['normalized_risk_score'] = df['medical_history'].apply(calculate_normalized_risk)

    # 2. Encode Insurance Plan
    insurance_plan_encoding = {'Bronze': 1, 'Silver': 2, 'Gold': 3}
    df['insurance_plan'] = df['insurance_plan'].map(insurance_plan_encoding)

    # --- One-Hot Encoding for Categorical Features ---
    # Use pd.get_dummies for robust encoding. It's much cleaner than if/elif chains.
    categorical_cols = [
        'gender', 'region', 'marital_status', 'bmi_category',
        'smoking_status', 'employment_status'
    ]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # --- Column Alignment ---
    # Define all columns the model was trained on to ensure consistency
    model_columns = [
        'age', 'number_of_dependants', 'income_lakhs', 'insurance_plan',
        'genetical_risk', 'normalized_risk_score', 'gender_Male',
        'region_Northwest', 'region_Southeast', 'region_Southwest',
        'marital_status_Unmarried', 'bmi_category_Obesity',
        'bmi_category_Overweight', 'bmi_category_Underweight',
        'smoking_status_Occasional', 'smoking_status_Regular',
        'employment_status_Salaried', 'employment_status_Self-Employed'
    ]

    # Add any missing columns from the model_columns list and fill with 0
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0

    # Ensure the order of columns matches the training data
    df = df[model_columns]

    return df


def handle_scaling(age, df):
    """Applies the correct scaler to the numerical columns."""
    if age <= 25:
        scaler_obj = scaler_young_obj
    else:
        scaler_obj = scaler_rest_obj

    # Extract the scaler from the loaded object
    scaler = scaler_obj['scaler']

    # FIX: Trust the scaler's internal feature names as the source of truth,
    # as the error message indicates it's inconsistent with other metadata.
    if hasattr(scaler, 'feature_names_in_'):
        cols_to_scale = scaler.feature_names_in_
    else:
        # Fallback for older scikit-learn versions or different object types
        print("Warning: Scaler object has no 'feature_names_in_'. Falling back to saved column list.")
        cols_to_scale = scaler_obj['cols_to_scale']

    # We can only scale columns that are present in the input DataFrame
    valid_cols_to_scale = [col for col in cols_to_scale if col in df.columns]

    if not valid_cols_to_scale:
        print("Warning: No valid columns for scaling were found in the DataFrame.")
        return df

    # This transform should now succeed because we are providing the exact columns
    # in the exact format that the scaler was trained on.
    df[valid_cols_to_scale] = scaler.transform(df[valid_cols_to_scale])

    return df


def predict(input_dict):
    """
    Main prediction function that orchestrates preprocessing, scaling, and prediction.
    """
    if not all([model_young, model_rest, scaler_young_obj, scaler_rest_obj]):
        raise RuntimeError("Model or scaler artifacts are not loaded. Cannot perform prediction.")

    # 1. Preprocess the raw input
    input_df = preprocess_input(input_dict)

    # 2. Scale the numerical features
    input_df = handle_scaling(input_dict['age'], input_df)

    # 3. Predict using the appropriate model
    if input_dict['age'] <= 25:
        prediction = model_young.predict(input_df)
    else:  # Corrected logic for age > 25
        prediction = model_rest.predict(input_df)

    # The model predicts an array, so we return the first element.
    return int(prediction[0])

