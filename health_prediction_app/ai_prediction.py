import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def fallback_prediction(glucose, haemoglobin, cholesterol):
    glucose = float(glucose)
    haemoglobin = float(haemoglobin)
    cholesterol = float(cholesterol)

    risks = []

    if glucose > 140:
        risks.append("elevated glucose level")
    if haemoglobin < 12:
        risks.append("low haemoglobin level")
    if cholesterol > 240:
        risks.append("high cholesterol level")

    if not risks:
        return "The given values are within a generally acceptable range. Maintain a healthy lifestyle and regular checkups."

    return "Possible health risk due to " + ", ".join(risks) + ". Please consult a healthcare professional for proper evaluation."


def predict_health(glucose, haemoglobin, cholesterol):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return fallback_prediction(glucose, haemoglobin, cholesterol)

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are a health prediction assistant.

        Analyze the following blood test values:
        Glucose: {glucose}
        Haemoglobin: {haemoglobin}
        Cholesterol: {cholesterol}

        Write a short, simple health-risk remark in 2 lines.
        Do not provide a final diagnosis.
        Recommend medical consultation if the values look abnormal.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception:
        return fallback_prediction(glucose, haemoglobin, cholesterol)
