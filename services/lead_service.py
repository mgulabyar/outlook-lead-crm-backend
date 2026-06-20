import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()

class LeadService:
    @staticmethod
    async def process_email_to_lead(email_body, sender_email):
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        system_prompt = """
        You are a Sales Intelligence Specialist. Extract Lead details from the email text.
        Determine 'Lead Score' (0-100) based on purchase intent.
        Determine 'Priority' (Hot, Warm, Cold).
        
        Return JSON ONLY:
        {
            "name": "Full Name",
            "company": "Company Name",
            "phone": "Phone Number",
            "designation": "Job Title",
            "lead_score": 0,
            "priority": "Hot/Warm/Cold",
            "intent_summary": "One line summary of their interest"
        }
        """

        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Sender: {sender_email}\nEmail: {email_body}",
                },
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)