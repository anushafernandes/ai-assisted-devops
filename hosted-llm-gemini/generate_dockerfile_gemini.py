import os
import re
from google import genai

API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.1-flash-lite"

PROMPT = """
Generate an ideal Dockerfile for {language} with best practices.

Return only the Dockerfile, without Markdown code fences or explanations.
Include:
- Appropriate base image
- Installing dependencies
- Setting working directory
- Adding source code
- Running the application
- Security and image-size best practices
"""

def generate_dockerfile(language):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=PROMPT.format(language=language),
    )

    if not response.text:
        raise RuntimeError("The model returned an empty response.")

    # Remove Markdown fences if the model includes them.
    dockerfile = response.text.strip()
    dockerfile = re.sub(r"^```(?:dockerfile)?\s*", "", dockerfile, flags=re.IGNORECASE)
    dockerfile = re.sub(r"\s*```$", "", dockerfile)

    return dockerfile.strip()


if __name__ == "__main__":
    language = input("Enter the programming language: ").strip()

    if not language:
        raise ValueError("Please enter a programming language.")

    try:
        dockerfile = generate_dockerfile(language)
        print("\nGenerated Dockerfile:\n")
        print(dockerfile)
    except Exception as error:
        print(f"Error generating Dockerfile: {error}")