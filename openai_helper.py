import openai
import logging

# Replace this with your actual OpenAI API key
OPENAI_API_KEY = 'sk'
openai.api_key = OPENAI_API_KEY
logger = logging.getLogger(__name__)

def generate_text(prompt, max_tokens=150):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or the latest model
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        message = response.choices[0].text.strip()
        return message
    except Exception as e:
        logger.error(f"Error while calling OpenAI API: {e}")
        return None
