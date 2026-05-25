from pydantic import BaseModel, validator
from typing import List, Optional, Any, Literal
import json

class UIComponent(BaseModel):
    type: Literal["metric", "chart", "table", "text", "warning", "form", "tags", "progress", "swot"]
    title: str
    size: Literal["small", "medium", "large", "full"] = "medium"
    data: Any

class UILayout(BaseModel):
    title: str
    subtitle: str = ""
    theme: Literal["light", "dark"] = "dark"
    components: List[UIComponent]

def parse_and_validate(raw_json: str) -> UILayout:
    # Strip markdown fences if model wraps response
    cleaned = raw_json.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()
    
    data = json.loads(cleaned)
    return UILayout(**data)

def get_fallback_layout(error_msg: str) -> UILayout:
    return UILayout(
        title="Processing Error",
        subtitle="The AI returned an unexpected response format.",
        theme="dark",
        components=[
            UIComponent(
                type="warning",
                title="Parse Error",
                size="full",
                data={"message": f"Could not render UI: {error_msg}", "severity": "medium"}
            ),
            UIComponent(
                type="text",
                title="What to try",
                size="full",
                data={"content": "Try rephrasing your input, or use a more structured document (CSV, clear text). The AI sometimes needs clearer input to generate a valid interface.", "style": "normal"}
            )
        ]
    )
