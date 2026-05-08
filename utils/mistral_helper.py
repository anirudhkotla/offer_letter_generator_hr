import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

MODEL = "mistral-small-latest"


def get_client() -> Mistral:
    api_key = os.getenv("MISTRAL_API_KEY", "")
    if not api_key or api_key == "your_mistral_api_key_here":
        raise ValueError("MISTRAL_API_KEY not set in .env file.")
    return Mistral(api_key=api_key)


def generate_internship_responsibilities(role: str, short_description: str, duration: str) -> str:
    prompt = f"""You are an HR professional writing an internship offer letter for Tericsoft Technology Solutions Pvt. Ltd.

Role: {role}
Duration: {duration}
Short Description: {short_description}

Write a professional 2-3 sentence responsibility paragraph for the offer letter.
- In second person ("Your internship will include...")
- No bullet points, flowing prose only
- Formal tone suitable for an offer letter
Return ONLY the paragraph text."""

    client = get_client()
    res = client.chat.complete(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content.strip()


def generate_fulltime_responsibilities(role: str, short_description: str) -> str:
    prompt = f"""You are an HR professional writing a full-time offer letter for Tericsoft Technology Solutions Pvt. Ltd., Hyderabad, India.

Role: {role}
Short Description: {short_description}

Generate professional role responsibilities. Use this EXACT format:

[Area Name 1]:
• [task]
• [task]
• [task]
• [task]

[Area Name 2]:
• [task]
• [task]
• [task]
• [task]

Beyond the specific mentioned core areas, the role also includes the following expectations:
• Be an active contributor to Tericsoft's culture.
• Collaborate closely with other team members.
• Provide support in varied areas beyond the job description, as needed.

Use plain bullet character •. No markdown bold. Return ONLY the responsibilities text."""

    client = get_client()
    res = client.chat.complete(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content.strip()


def refine_section(section_text: str, instruction: str) -> str:
    prompt = f"""You are an HR professional refining an offer letter for Tericsoft Technology Solutions Pvt. Ltd.

Current text:
{section_text}

Instruction: {instruction}

Rewrite according to the instruction. Keep a formal, professional tone for an Indian corporate offer letter.
Return ONLY the rewritten text."""

    client = get_client()
    res = client.chat.complete(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content.strip()