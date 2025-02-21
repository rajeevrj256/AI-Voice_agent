import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_summary_from_llm(summary_text):
    """
    Uses Google Generative AI to extract structured details from a given summary.
    
    :param summary_text: The text summary from the voice API response.
    :return: JSON response with extracted date, time, and purpose.
    """
    model = genai.GenerativeModel("gemini-pro")  # Adjust model name if needed

    # K-Short Prompting: Give a clear instruction with an example
    prompt = f"""
    your are receptionist for appointment booking for botmast.
    Extract structured details (date, time, purpose) from the given summary.
    if date have contains today date then replace it with current date.and if date contains tomorrow date then replace it with tommorow date.
    Summary: "{summary_text}"
    
    Example Response Format:
    {{
        "date": "DD-MM-YYYY",
        "time": "HH:MM AM/PM",
        "purpose": "Appointment for [Person]",
        "email":"example@gmail.com"
    }}
    
    example:
    
    summary:The caller requested to book an important appointment for voiece agent at 6 PM tomorrow. The AI assistant asked for clarification on details and confirmed the booking, offering further assistance if needed.User provide email example@gmail.com
    response: {{
        "date": "21-02-2025",
        "time: "6:00 PM",
        "purpose": "Appointment for voice",
        "email":"example@gmail.com"
    }}
    """

    response = model.generate_content(prompt)
    
    # Extract response text and parse if needed
    return response.text if response else "No response received."

