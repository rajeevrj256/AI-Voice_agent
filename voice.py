import requests
import json
import os
from dotenv import load_dotenv
from LLM import get_summary_from_llm
from google_sheet import log_call_to_sheets,is_duplicate
from flask import Flask, request, jsonify

app = Flask(__name__)
load_dotenv()

vapi_token = os.environ.get("VAPI_TOKEN")

@app.route('/call', methods=['GET', 'POST'])
def list_calls():
    response = requests.get(
        "https://api.vapi.ai/call",
        headers={"Authorization": f"Bearer {vapi_token}"},
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return jsonify({"error": "Error fetching calls"}), response.status_code

    data = response.json()

    if not isinstance(data, list) or len(data) == 0:
        print("Empty or unexpected response format:", data)
        return jsonify({"error": "No calls found"}), 400

    processed_calls = []

    for item in data:
        call_id = item.get("id", "N/A")
        if is_duplicate(call_id):
            print(f"Duplicate detected: Call ID {call_id} already logged.")
            continue
        summary = item.get("summary", "").strip()
        if not summary:
            print("Warning: Missing or empty summary in call data")
            continue  # Skip this item if summary is missing

        print("New Summary:", summary)
        llm_response = get_summary_from_llm(summary)

        if not llm_response or llm_response.strip() == "":
            print("Warning: Empty response from LLM")
            continue  # Skip processing if LLM response is empty

        try:
            llm_data = json.loads(llm_response)  # Ensure valid JSON response
            print(llm_data)
            log_call_to_sheets(item, llm_data)
            processed_calls.append(llm_data)
        except json.JSONDecodeError as e:
            print("Error parsing LLM response JSON:", e)
            print("LLM Response:", llm_response)  # Debugging output
            continue

    return jsonify({"calls": processed_calls}), 200

if __name__ == "__main__":
    app.run(port=5000)
