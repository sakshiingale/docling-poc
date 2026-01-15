import os
from pathlib import Path
from dotenv import load_dotenv

try:
    from openai import AzureOpenAI
except Exception:
    AzureOpenAI = None


# =========================
# Azure OpenAI Config
# =========================

load_dotenv()

AZ_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZ_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZ_DEPLOY = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZ_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

if not (AZ_ENDPOINT and AZ_KEY and AZ_DEPLOY and AzureOpenAI):
    raise RuntimeError("Azure OpenAI configuration missing")

client = AzureOpenAI(
    azure_endpoint=AZ_ENDPOINT,
    api_key=AZ_KEY,
    api_version=AZ_API_VERSION,
)


# =========================
# PROMPT (LLM DOES THE WORK)
# =========================

SYSTEM_PROMPT = """
You are cleaning a legal document extracted from a PDF.

Your task:
- REMOVE the index / arrangement of sections part completely.
- The index typically appears as a list like:
  1.
  2.
  3.
  4.
  5.
  ...
  without actual section content.
- REMOVE any table of contents or arrangement headings.

START the document from the ACTUAL content, such as:
- "1. Short title, extent and commencement"
- "2. Definitions"
- "3. ..."

Keep:
- All real sections
- All clauses and sub-clauses
- All legal text after the real Section 1 begins

Do NOT:
- Add new content
- Invent missing sections
- Change numbering

Output:
- Clean Markdown only
- No explanations
- No headings like "Cleaned Output"
"""


# =========================
# Main Logic
# =========================

def main():
    input_path = Path("output/structured_pages.md")
    output_path = Path("output/clean_structured_pages.md")

    if not input_path.exists():
        raise FileNotFoundError(f"{input_path} not found")

    raw_text = input_path.read_text(encoding="utf-8")

    response = client.chat.completions.create(
        model=AZ_DEPLOY,
        temperature=0.0,
        max_tokens=8000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text},
        ],
    )

    cleaned_text = response.choices[0].message.content.strip()

    output_path.write_text(cleaned_text, encoding="utf-8")

    print("✅ Noise cleanup completed")
    print(f"📄 Cleaned file saved to: {output_path}")


if __name__ == "__main__":
    main()
