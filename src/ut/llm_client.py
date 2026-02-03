"""Automated Unit Test Generation CLI with AI."""
import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


def generate_test_code(prompt: str) -> str:
    """Generate test code for a given function.

    Args:
        prompt (str): The prompt containing the function code and context.

    Returns:
        str: The generated test code.
    """

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
