from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-5.4-mini"

def get_ui_layout(messages: list, stream_placeholder=None) -> str:
    """
    Call the LLM with streaming. Returns the full response text.
    Optionally updates a Streamlit placeholder with live streaming text.
    """
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
        temperature=0.3,  # lower = more consistent JSON
        max_completion_tokens=2000,
    )
    
    full_response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        full_response += delta
        if stream_placeholder:
            stream_placeholder.markdown(
                f'<div class="streaming-indicator">⚡ Generating interface... {len(full_response)} tokens</div>',
                unsafe_allow_html=True
            )
    
    return full_response


def build_messages(user_content: list) -> list:
    """
    Build the messages array for the API call.
    user_content is a list of OpenAI content blocks (text, image_url, etc.)
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content}
    ]