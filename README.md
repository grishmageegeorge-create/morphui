# ⚡ MorphUI

> AI-powered generative UI engine — transforms any document, image, or text into a dynamic interface in real-time.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red) ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--5.4--mini-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

<!-- ADD YOUR DEMO GIF HERE -->

## What is this?
MorphUI is an AI interface engine that accepts any multimodal input — text, PDF, image, CSV — and generates a fully custom interactive dashboard in real time. The LLM acts as a UI architect, outputting structured JSON that the rendering engine turns into real charts, forms, metrics, and widgets — not plain text.

## Features
- 🖼️ Multimodal input: text, image (GPT Vision), PDF, CSV, TXT
- ⚡ Generative JSON layout — every interface is unique to the input
- 🔄 Streaming responses with animated loading states
- 🎯 6 built-in demo scenarios
- 🛡️ Pydantic validation with graceful error handling
- 🌙 Dark-themed animated UI with custom CSS

## Architecture
User Input → Input Parser → Prompt Builder → GPT-5.4-mini → JSON Validator (Pydantic) → UI Renderer → Animated Dashboard

## Project Structure
morphui/
├── app.py              # Main Streamlit app
├── llm_client.py       # OpenAI API + streaming
├── ui_engine.py        # JSON → widget renderer
├── validators.py       # Pydantic schema validation
├── input_handler.py    # Multimodal input processing
├── prompts.py          # System prompt engineering
├── styles.py           # Custom CSS theme
├── .env.example        # Environment variables template
└── requirements.txt

## Setup
```bash
git clone https://github.com/YOUR_USERNAME/morphui.git
cd morphui
pip install -r requirements.txt
cp .env.example .env   # add your API key
streamlit run app.py
```

## Demo Scenarios
| Input | Output |
|-------|--------|
| 📄 Resume PDF | Skills dashboard with progress bars |
| 🧾 Invoice image | Expense table + donut chart |
| 📊 Sales CSV | KPI metrics + trend charts |
| 💼 Business plan text | SWOT grid + action cards |
| 🏥 Medical report | Warning cards + health metrics |
| 🛍️ Product image | E-commerce listing form |

## Follow-up Actions
After generating any interface, use the suggested follow-ups:
- **📋 Data Summary** — Executive summary with key takeaways
- **🎯 Key Recommendations** — Prioritized action items
- **🔁 Regenerate** — Fresh interface from same input

## Future Enhancements
- Voice input via Whisper API
- PDF export of generated dashboards
- Multi-page layouts
- Drag-and-drop widget reordering
- Team collaboration mode

## License
MIT