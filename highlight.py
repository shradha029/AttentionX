import google.generativeai as genai
import json

# 🔑 Paste your API key here
genai.configure(api_key="api")

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")


def get_highlights(transcript_data: dict):
    """
    Input: transcript from Whisper
    Output: list of highlights with start, end, hook
    """

    full_text = transcript_data["text"]

    prompt = f"""
Find 3 highly engaging or emotional segments from this transcript.

Rules:
- Each segment should be 30 to 60 seconds
- Return timestamps in SECONDS (integer)
- Output ONLY JSON in this format:

[
  {{"start": 10, "end": 50, "hook": "This will change your mindset"}}
]

Transcript:
{full_text}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Extract JSON safely
    start = text.find("[")
    end = text.rfind("]") + 1
    json_str = text[start:end]

    highlights = json.loads(json_str)

    return highlights


# 🔥 Quick test
if __name__ == "__main__":
    test_data = {
        "text": "Success comes from discipline. Most people quit early. Stay focused and results will come."
    }

    print(get_highlights(test_data))