import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def convert_medical_report_to_friendly(report_text, api_key):
    """
    Converts a medical report into patient-friendly language using Google's Generative AI.
    """
    if not api_key:
        raise ValueError("API key is required")
    if not report_text:
        raise ValueError("Report text is required")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        """
    You are a helpful medical assistant tasked with converting technical medical information into patient-friendly language. 
    Please explain the following medical report in simple, clear terms that a patient can easily understand.
    
    Guidelines:
    1. Use everyday language instead of medical terminology
    2. Break down complex concepts into simple explanations
    3. Organize information into clear sections
    4. Highlight important points the patient should know
    5. Include supportive and encouraging language
    6. Return the response in JSON format with appropriate sections
    
    Format the response as a JSON object with these sections:
    {
        "summary": "A brief overview in simple terms",
        "vital_signs_explained": {"blood_pressure": "explanation", ...},
        "current_health": "Simple explanation of current condition",
        "medication_instructions": [{"medication": "name", "instructions": "simple instructions"}],
        "next_steps": ["list of what patient needs to do"],
        "lifestyle_recommendations": ["clear, actionable recommendations"],
        "important_warnings": ["any critical points to watch for"],
        "follow_up_plan": "When and why to follow up"
    }
    
    Medical Report:
    """
        + report_text
    )

    response = model.generate_content(prompt)
    response_text = response.text

    emergency_keywords = [
        "severe pain",
        "chest pain",
        "shortness of breath",
        "difficulty breathing",
        "emergency",
        "immediate attention",
    ]

    result = {"mode": "friendly", "ai_converted_report": response_text}

    if any(keyword in report_text.lower() for keyword in emergency_keywords):
        result["emergency_warning"] = {
            "warning": "⚠️ IMPORTANT: If you experience severe chest pain or other "
            "emergency symptoms, call 911 immediately.",
            "medication_note": "Use your nitroglycerin as prescribed for chest pain.",
        }

    return result

def test_converter():
    sample_report = """
            Clinical Evaluation Report
            Patient: John Davis
            Date of Service: 09/30/2024
            Provider: Jane Smith, MD, FACC
            Department: Cardiology

            Chief Complaint: Patient presents with intermittent episodes of substernal chest discomfort associated with physical exertion.

            History of Present Illness: 64-year-old male with known coronary artery disease presents for routine follow-up and management of stable angina pectoris. Patient reports experiencing intermittent episodes of retrosternal pressure during moderate physical exertion, rated 4/10 on pain scale, alleviating with rest within 5-7 minutes. Denies radiation of pain, diaphoresis, or associated autonomic symptoms. No episodes of rest angina or crescendo pattern noted.

            Physical Examination:
            Vital Signs:
                BP: 142/88 mmHg
                HR: 76 bpm, regular rhythm
                RR: 16/min
                O2 Saturation: 98% on room air
                BMI: 28.4 kg/m²

            Laboratory Findings:
                Total Cholesterol: 210 mg/dL
                LDL: 138 mg/dL
                HDL: 42 mg/dL
                Triglycerides: 150 mg/dL
                HbA1c: 5.8%
                Troponin I: <0.04 ng/mL (negative)
                BNP: 85 pg/mL

            Medications:
                - Aspirin 81mg daily
                - Atorvastatin 40mg daily
                - Metoprolol 25mg BID
                - Nitroglycerin 0.4mg sublingual PRN

            Plan:
                1. Continue current medications
                2. Schedule coronary angiography for October 5, 2024
                3. Lifestyle Modifications:
                    - Sodium-restricted diet (<2g/day)
                    - DASH diet principles
                    - Smoking cessation
                    - Cardiac rehabilitation program
                4. Follow-up in 2 weeks post-angiography
        """
    try:
        api_key = os.environ.get("API_KEY")
        result = convert_medical_report_to_friendly(sample_report, api_key)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    test_converter()
