"""Automated Unit Test Generation CLI with AI."""
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

def _get_genai() -> Optional[object]:
    """Attempt to import the google.generativeai module lazily.

    Returns the imported module on success or None if it's not installed.
    """
    try:
        import google.generativeai as genai
        return genai
    except ModuleNotFoundError:
        return None

def generate_test_code(prompt: str) -> str:
    """Generate test code for a given function.

    Args:
        prompt (str): The prompt containing the function code and context.

    Returns:
        str: The generated test code.
    """

    genai = _get_genai()
    if genai is None:
        raise RuntimeError(
            "google-generative-ai is not installed. Install it with: `poetry add google-generative-ai` "
            "or `pip install google-generative-ai` to enable generation features."
        )

    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-flash-lite-latest')

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=2048,
        )
    )

    return response.text