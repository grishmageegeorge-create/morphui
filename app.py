import streamlit as st
import time
from styles import CSS
from input_handler import handle_text_input, handle_image_input, handle_file_input
from llm_client import get_ui_layout, build_messages
from validators import parse_and_validate, get_fallback_layout
from ui_engine import render_layout

# ── Page config ──
st.set_page_config(
    page_title="MorphUI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CSS, unsafe_allow_html=True)
st.markdown("""
<script>
window.addEventListener('load', function() {
    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.display = 'block';
        sidebar.style.visibility = 'visible';
        sidebar.style.width = '300px';
        sidebar.style.transform = 'none';
    }
    const btn = window.parent.document.querySelector('[data-testid="collapsedControl"]');
    if (btn) btn.style.display = 'none';
});
</script>
""", unsafe_allow_html=True)

LOADING_MESSAGES = [
    "⚡ Analyzing multimodal inputs…",
    "🧠 Extracting semantic structure…",
    "🎨 Constructing adaptive interface…",
    "🔗 Mapping content to visual components…",
    "⚙️ Calibrating layout intelligence…",
    "✨ Rendering your personalized workspace…",
]

# ── Sidebar ──
with st.sidebar:
    st.markdown("## ⚡ MorphUI")
    st.markdown('<div style="font-size:11px;color:#5a5a7a;font-family:monospace;margin-bottom:1.5rem">AI Interface Engine v1.0</div>', unsafe_allow_html=True)

    st.markdown("### Input Type")
    input_mode = st.radio(
        "",
        ["📝 Text", "🖼️ Image", "📁 File (CSV/PDF/TXT)"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### Demo Scenarios")

    demo = st.selectbox(
        "",
        [
            "— pick a demo —",
            "📊 Sales CSV → Analytics",
            "📄 Resume → Skills Dashboard",
            "🧾 Invoice → Expense Insights",
            "💼 Business Plan → SWOT",
            "🏥 Medical Report → Summary",
            "🛍️ Product → Listing Form",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    show_json = st.toggle("Show raw JSON", value=False)

    st.markdown("---")
    st.markdown('<div style="font-size:10px;color:#3a3a5a;font-family:monospace">Built with MorphUI Engine<br>Powered by GPT-5.4-mini</div>', unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="morphui-header">
    <div class="morphui-logo">MorphUI</div>
    <div class="morphui-tagline">any input → intelligent interface · in real time</div>
</div>
""", unsafe_allow_html=True)

# ── Session state ──
if "history" not in st.session_state:
    st.session_state.history = []
if "last_raw_json" not in st.session_state:
    st.session_state.last_raw_json = ""
if "generated_layouts" not in st.session_state:
    st.session_state.generated_layouts = []
if "show_followups" not in st.session_state:
    st.session_state.show_followups = False
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False
if "last_input_text" not in st.session_state:
    st.session_state.last_input_text = ""  
if "text_value" not in st.session_state:
    st.session_state.text_value = ""
if "new_layout_added" not in st.session_state:
    st.session_state.new_layout_added = False


    

# ── Demo text presets ──
DEMO_TEXTS = {
    "💼 Business Plan → SWOT": """
        Company: TechFlow AI — B2B SaaS for workflow automation.
        Strengths: Proprietary NLP engine, strong founding team, 50 beta customers.
        Weaknesses: No brand recognition, limited funding ($500k), small team of 6.
        Opportunities: Remote work surge, $4B market growing 23% YoY, enterprise demand.
        Threats: Competitors like Zapier, Make.com; economic slowdown cutting SaaS budgets.
        Revenue: $12k MRR, targeting $100k MRR in 12 months.
        Key risks: Customer churn at 8%, hiring challenges.
    """,
    "🏥 Medical Report → Summary": """
        Patient: John Doe, 45M. Date: 2024-01-15.
        Blood Pressure: 148/95 mmHg (HIGH - normal: <120/80)
        Blood Glucose: 126 mg/dL (BORDERLINE HIGH - normal: <100)
        Cholesterol Total: 210 mg/dL (BORDERLINE - normal: <200)
        LDL: 145 mg/dL (HIGH - normal: <100)
        HDL: 42 mg/dL (LOW - normal: >40 for men)
        HbA1c: 6.1% (PREDIABETES - normal: <5.7%)
        BMI: 28.3 (OVERWEIGHT - normal: 18.5-24.9)
        Doctor notes: Patient advised dietary changes, exercise program, follow-up in 3 months.
    """,
    "🛍️ Product → Listing Form": """
        I have a product: Handmade ceramic coffee mug, 12oz capacity, artisan crafted,
        earth-tone glazing with speckled finish, microwave and dishwasher safe,
        made in Portugal, batch of 50 units available, cost to make: $8 each.
        Please generate an e-commerce product listing form for this.
    """,
    "📄 Resume → Skills Dashboard": """
        Name: Priya Sharma. Senior Full Stack Developer. 7 years experience.
        Skills: Python (Expert), React (Advanced), Node.js (Advanced), AWS (Intermediate),
        PostgreSQL (Advanced), Docker (Intermediate), TypeScript (Advanced).
        Experience: Google (2021-present) - Senior SWE, Meta (2019-2021) - SWE II,
        Startup (2017-2019) - Full Stack Developer.
        Education: B.Tech Computer Science, IIT Bombay, 2017.
        Projects: Led migration of monolith to microservices (50% latency reduction),
        built real-time analytics dashboard (100k users), open source contributor.
    """,
    "📊 Sales CSV → Analytics": """
    Monthly Sales Data:
    Jan: $12,000 | Feb: $18,500 | Mar: $22,000 | Apr: $15,000 | May: $30,000 | Jun: $28,000
    Top Products: Product A ($45k), Product B ($32k), Product C ($18k)
    Regions: North ($38k), South ($28k), East ($22k), West ($12k)
    Target: $25,000/month. Current avg: $20,916. Growth rate: 18% MoM.
""",
"🧾 Invoice → Expense Insights": """
    Invoice #INV-2024-089
    Vendor: CloudTech Solutions
    Date: January 15, 2024. Due: February 15, 2024.
    Items:
    - Cloud Hosting (Annual): $4,800
    - SSL Certificate: $120
    - Domain Registration: $45
    - Support Package: $600
    - Setup Fee: $250
    Total: $5,815. Tax (18%): $1,046.70. Grand Total: $6,861.70
    Status: Unpaid. Overdue risk: High.
""",
}

# ── Main input area ──
user_content = None
input_label = ""
if input_mode == "📝 Text":
    # Set demo text into session state when demo changes
    if demo in DEMO_TEXTS and not st.session_state.clear_input:
        st.session_state.text_value = DEMO_TEXTS[demo].strip()
    elif st.session_state.clear_input:
        st.session_state.text_value = ""
        st.session_state.clear_input = False

    text_input = st.text_area(
        "Paste text, describe a scenario, or pick a demo above",
        value=st.session_state.text_value,
        height=160,
        placeholder="e.g. paste a business plan, describe a product, write a scenario…",
        label_visibility="visible"
    )
    # Update session state as user types
    st.session_state.text_value = text_input
    
    if text_input.strip():
        user_content = handle_text_input(text_input)
        input_label = text_input
        st.session_state.last_input_text = text_input

elif input_mode == "🖼️ Image":
    img_file = st.file_uploader(
        "Upload any image — invoice, product photo, chart, document scan",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="visible"
    )
    if img_file:
        st.image(img_file, width=300)
        extra_text = st.text_area(
            "Add instructions (optional)",
            height=80,
            placeholder="e.g. This is an invoice, generate expense insights…"
        )
        image_content = handle_image_input(img_file)
        if extra_text.strip():
            image_content.append({"type": "text", "text": extra_text})
        user_content = image_content
        input_label = f"Image: {img_file.name}"

elif input_mode == "📁 File (CSV/PDF/TXT)":
    file = st.file_uploader(
        "Upload CSV, PDF, or TXT file",
        type=["csv", "pdf", "txt"],
        label_visibility="visible"
    )
    if file:
        extra_text = st.text_area(
            "Add instructions (optional)",
            height=80,
            placeholder="e.g. Focus on revenue trends, highlight risks…"
        )
        file_content = handle_file_input(file)
        if extra_text.strip():
            file_content[0]["text"] = file_content[0]["text"] + f"\n\nAdditional instructions: {extra_text}"
        user_content = file_content
        input_label = f"File: {file.name}"

# ── Buttons ──
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    generate_btn = st.button("⚡ Generate Interface", use_container_width=True)
with col2:
    clear_btn = st.button("✕ Clear", use_container_width=True)

# ── Clear ──
if clear_btn:
    st.session_state.generated_layouts = []
    st.session_state.last_raw_json = ""
    st.session_state.show_followups = False
    st.session_state.history = []
    st.session_state.clear_input = True
    st.session_state.input_key += 1
    st.rerun()

# ── Generation ──
if generate_btn and user_content:
    st.session_state.last_user_content = user_content
    st.session_state.last_input_text = input_label
    st.markdown("---")

    loading_placeholder = st.empty()
    stream_placeholder = st.empty()

    for msg in LOADING_MESSAGES:
        loading_placeholder.markdown(
            f'<div class="streaming-indicator">{msg}</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.6)

    try:
        messages = build_messages(user_content)
        raw_json = get_ui_layout(messages, stream_placeholder)
        st.session_state.last_raw_json = raw_json

        loading_placeholder.markdown(
            '<div class="streaming-indicator" style="color:#00d4aa;border-color:#00d4aa33;background:#00d4aa11">✓ Interface ready</div>',
            unsafe_allow_html=True
        )
        stream_placeholder.empty()
        time.sleep(0.4)
        loading_placeholder.empty()

        try:
            layout = parse_and_validate(raw_json)
        except Exception as e:
            layout = get_fallback_layout(str(e))

        # Add to layouts list (keeps all previous + new)
        st.session_state.generated_layouts.append({
            "label": input_label or "Generated UI",
            "layout": layout
        })
        st.session_state.show_followups = True

        st.session_state.history.append({
            "label": input_label or "Generated UI",
            "layout": layout
        })

    except Exception as e:
        loading_placeholder.empty()
        stream_placeholder.empty()
        st.markdown("""
        <div class="morphui-card" style="border-left:3px solid #ff4757;background:#ff475711">
            <div class="card-label" style="color:#ff4757">⚠ Something went wrong</div>
            <div class="text-content">Could not generate the interface. Please try again or rephrase your input.</div>
        </div>
        """, unsafe_allow_html=True)

elif generate_btn and not user_content:
    st.warning("Please provide an input first — type text, upload an image, or pick a demo scenario.")

# ── Render ALL accumulated layouts ──
if st.session_state.generated_layouts:
    for i, item in enumerate(st.session_state.generated_layouts):
        layout = item["layout"]
        if i > 0:
            st.markdown("---")
            st.markdown(f'<div style="font-size:11px;font-family:monospace;color:#5a5a7a;margin-bottom:8px">➕ {item["label"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-title">{layout.title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-subtitle">{layout.subtitle}</div>', unsafe_allow_html=True)
        render_layout(layout)
    st.session_state.new_layout_added = False

# ── Follow-up buttons — only show after generation ──
if st.session_state.show_followups:
    st.markdown("---")
    st.markdown('<div class="card-label" style="margin-bottom:10px">Suggested follow-ups</div>', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        if st.button("📋 Data Summary", use_container_width=True, key="btn_summary"):
            followup_content = handle_text_input(
                f"Based on this data: {st.session_state.last_input_text}\n\n"
                f"Generate a concise executive summary with key numbers, highlights, "
                f"and the 3 most important takeaways. Use metric cards and text components only. "
                f"Be specific to the actual data provided."
            )
            messages = build_messages(followup_content)
            with st.spinner("Generating summary..."):
                try:
                    raw_json = get_ui_layout(messages)
                    layout = parse_and_validate(raw_json)
                    st.session_state.generated_layouts.append({
                        "label": "Data Summary",
                        "layout": layout
                    })
                    st.session_state.new_layout_added = True
                    st.rerun()
                except Exception:
                    st.markdown("""
                    <div class="morphui-card" style="border-left:3px solid #ff4757">
                        <div class="card-label" style="color:#ff4757">⚠ Could not add section</div>
                        <div class="text-content">Please try again.</div>
                    </div>
                    """, unsafe_allow_html=True)

    with fc2:
        if st.button("🎯 Key Recommendations", use_container_width=True, key="btn_recommend"):
            followup_content = handle_text_input(
                f"Based on this specific content: {st.session_state.last_input_text}\n\n"
                f"Generate prioritized recommendations and next actions DIRECTLY related to this content. "
                f"Be specific — use actual names, skills, numbers from the original input. "
                f"Do not give generic advice. Use text, warning, and metric components."
            )
            messages = build_messages(followup_content)
            with st.spinner("Generating recommendations..."):
                try:
                    raw_json = get_ui_layout(messages)
                    layout = parse_and_validate(raw_json)
                    st.session_state.generated_layouts.append({
                        "label": "Key Recommendations",
                        "layout": layout
                    })
                    st.session_state.new_layout_added = True
                    st.rerun()
                except Exception:
                    st.markdown("""
                    <div class="morphui-card" style="border-left:3px solid #ff4757">
                        <div class="card-label" style="color:#ff4757">⚠ Could not add section</div>
                        <div class="text-content">Please try again.</div>
                    </div>
                    """, unsafe_allow_html=True)

    with fc3:
        if st.button("🔁 Regenerate", use_container_width=True, key="btn_regen"):
            if st.session_state.generated_layouts:
                st.session_state.generated_layouts = []
                st.session_state.show_followups = False
            st.rerun()

# ── Raw JSON toggle ──
if show_json and st.session_state.last_raw_json:
    st.markdown("---")
    st.markdown('<div class="card-label">Raw JSON from LLM</div>', unsafe_allow_html=True)
    st.code(st.session_state.last_raw_json, language="json")

# ── History in sidebar ──
if st.session_state.history:
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Recent Interfaces")
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            st.markdown(f'<div style="font-size:11px;color:#5a5a7a;padding:4px 0;font-family:monospace">↳ {item["label"][:35]}</div>', unsafe_allow_html=True)