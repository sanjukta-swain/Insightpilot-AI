import os
from google import genai

def configure_gemini(api_key):
    client = genai.Client(api_key=api_key)
    return client

def generate_insights(client, data_summary):
    prompt = f"""
You are a Business Data Analyst.

Analyze the following business dataset summary and provide:

1. Executive Summary
2. Key Insights
3. Business Risks
4. Recommendations
5. Growth Opportunities

Dataset:
{data_summary}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text