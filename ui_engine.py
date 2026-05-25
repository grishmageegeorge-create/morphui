import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import time
import pandas as pd
from validators import UILayout, UIComponent

PLOTLY_TEMPLATE = "plotly_dark"
CARD_COLORS = {
    "green": "#00d4aa",
    "red": "#ff4757",
    "blue": "#4a9eff",
    "orange": "#ffa502",
    "default": "#a0a0b0"
}

def render_metric(comp: UIComponent):
    d = comp.data
    color = CARD_COLORS.get(d.get("color", "default"), "#a0a0b0")
    delta_html = f'<div class="metric-delta" style="color:{color}">{d.get("delta","")}</div>' if d.get("delta") else ""
    st.markdown(f"""
    <div class="morphui-card metric-card animate-in">
        <div class="card-label">{comp.title}</div>
        <div class="metric-value" style="color:{color}">{d.get("value","—")}</div>
        <div class="metric-label">{d.get("label","")}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def render_chart(comp: UIComponent):
    d = comp.data
    chart_type = d.get("chart_type", "bar")
    labels = d.get("labels", [])
    values = d.get("values", [])
    
    if not labels or not values:
        st.warning(f"No chart data for: {comp.title}")
        return
    
    if chart_type == "bar":
        fig = go.Figure(go.Bar(x=labels, y=values, marker_color="#4a9eff", marker_line_width=0))
    elif chart_type == "line":
        fig = go.Figure(go.Scatter(x=labels, y=values, mode="lines+markers",
                                   line=dict(color="#00d4aa", width=2),
                                   marker=dict(size=6)))
    elif chart_type in ("pie", "donut"):
        hole = 0.45 if chart_type == "donut" else 0
        fig = go.Figure(go.Pie(labels=labels, values=values, hole=hole,
                               marker=dict(colors=["#4a9eff","#00d4aa","#ffa502","#ff4757","#a855f7"])))
    else:
        fig = go.Figure(go.Bar(x=labels, y=values))
    
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=260,
        font=dict(color="#a0a0b0", size=11),
        showlegend=chart_type in ("pie","donut")
    )
    
    st.markdown(f'<div class="morphui-card animate-in"><div class="card-label">{comp.title}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=f"chart_{comp.title}_{id(fig)}_{time.time_ns()}")
    st.markdown('</div>', unsafe_allow_html=True)

def render_table(comp: UIComponent):
    d = comp.data
    headers = d.get("headers", [])
    rows = d.get("rows", [])
    if not headers:
        return
    try:
        df = pd.DataFrame(rows, columns=headers)
        st.markdown(f'<div class="card-label" style="margin-bottom:8px">{comp.title}</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True,
            column_config={col: st.column_config.TextColumn(col) for col in headers})
    except Exception:
        st.markdown(f'<div class="morphui-card animate-in"><div class="card-label">{comp.title}</div><div class="text-content">Could not render table.</div></div>', unsafe_allow_html=True)

def render_text(comp: UIComponent):
    d = comp.data
    style = d.get("style", "normal")
    content = d.get("content", "")
    border = {"highlight": "#4a9eff", "quote": "#00d4aa", "normal": "#2a2a3e"}.get(style, "#2a2a3e")
    st.markdown(f"""
    <div class="morphui-card animate-in" style="border-left: 3px solid {border};">
        <div class="card-label">{comp.title}</div>
        <div class="text-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def render_warning(comp: UIComponent):
    d = comp.data
    severity = d.get("severity", "medium")
    colors = {"low": "#ffa502", "medium": "#ff6b35", "high": "#ff4757"}
    color = colors.get(severity, "#ff6b35")
    icons = {"low": "⚠️", "medium": "🔶", "high": "🚨"}
    icon = icons.get(severity, "⚠️")
    st.markdown(f"""
    <div class="morphui-card warning-card animate-in" style="border-left: 3px solid {color}; background: {color}18;">
        <div class="card-label" style="color:{color}">{icon} {comp.title} · {severity.upper()}</div>
        <div class="text-content">{d.get("message","")}</div>
    </div>
    """, unsafe_allow_html=True)

def render_form(comp: UIComponent):
    d = comp.data
    fields = d.get("fields", [])
    unique = f"{comp.title}_{time.time_ns()}"
    st.markdown(f'<div class="morphui-card animate-in"><div class="card-label">{comp.title}</div>', unsafe_allow_html=True)
    for field in fields:
        ftype = field.get("type", "text")
        label = field.get("label", "")
        val = field.get("value", "")
        opts = field.get("options", [])
        key = f"form_{unique}_{label}"
        if ftype == "select" and opts:
            idx = opts.index(val) if val in opts else 0
            st.selectbox(label, opts, index=idx, key=key)
        elif ftype == "textarea":
            st.text_area(label, value=val, key=key)
        elif ftype == "number":
            st.number_input(label, value=float(val) if val else 0.0, key=key)
        else:
            st.text_input(label, value=val, key=key)
    st.markdown('</div>', unsafe_allow_html=True)

def render_tags(comp: UIComponent):
    d = comp.data
    items = d.get("items", [])
    tag_colors = {"blue":"#4a9eff22","green":"#00d4aa22","red":"#ff475722","orange":"#ffa50222","gray":"#ffffff11"}
    tag_text = {"blue":"#4a9eff","green":"#00d4aa","red":"#ff4757","orange":"#ffa502","gray":"#a0a0b0"}
    tags_html = " ".join([
        f'<span class="tag" style="background:{tag_colors.get(t.get("color","gray"),"#ffffff11")};color:{tag_text.get(t.get("color","gray"),"#a0a0b0")}">{t.get("label","")}</span>'
        for t in items
    ])
    st.markdown(f"""
    <div class="morphui-card animate-in">
        <div class="card-label">{comp.title}</div>
        <div class="tags-wrap">{tags_html}</div>
    </div>
    """, unsafe_allow_html=True)

def sanitize_progress_data(data):
    items = data.get("items", [])
    clean_items = []
    for item in items:
        label = item.get("label", "")
        value = item.get("value", 0)
        max_val = item.get("max", 100)
        color = item.get("color", "blue")
        if "<" in str(label) or "<" in str(value):
            continue
        try:
            value = float(str(value).replace('%',''))
        except:
            value = 0
        try:
            max_val = float(str(max_val))
        except:
            max_val = 100
        clean_items.append({
            "label": str(label),
            "value": value,
            "max": max_val,
            "color": str(color)
        })
    return {"items": clean_items}

def render_progress(comp: UIComponent):
    d = sanitize_progress_data(comp.data)
    items = d.get("items", [])
    
    COLOR_MAP = {
        "green": "#00d4aa", "success": "#00d4aa",
        "red": "#ff4757", "danger": "#ff4757",
        "orange": "#ffa502", "warning": "#ffa502",
        "blue": "#4a9eff", "info": "#4a9eff",
        "purple": "#a855f7", "gray": "#5a5a7a",
    }
    
    st.markdown(f'<div class="morphui-card animate-in"><div class="card-label">{comp.title}</div></div>', unsafe_allow_html=True)
    
    for item in items:
        pct = min(100, int((item.get("value", 0) / max(item.get("max", 100), 1)) * 100))
        raw_color = item.get("color", "blue")
        color = COLOR_MAP.get(raw_color, raw_color if str(raw_color).startswith("#") else "#4a9eff")
        label = item.get("label", "")
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f'<div style="font-size:12px;color:#a0a0c0;font-family:DM Mono,monospace;margin-bottom:4px">{label}</div>', unsafe_allow_html=True)
            st.progress(pct / 100, key=f"prog_{comp.title}_{label}_{time.time_ns()}")
        with col2:
            st.markdown(f'<div style="font-size:12px;color:{color};font-family:DM Mono,monospace;padding-top:20px;text-align:right">{pct}%</div>', unsafe_allow_html=True)

def render_swot(comp: UIComponent):
    d = comp.data
    def quadrant(title, items, color):
        items_html = "".join([f"<li>{i}</li>" for i in items])
        return f'<div class="swot-quad" style="border-top:2px solid {color}"><div class="swot-title" style="color:{color}">{title}</div><ul class="swot-list">{items_html}</ul></div>'
    
    html = f"""
    <div class="morphui-card animate-in">
        <div class="card-label">{comp.title}</div>
        <div class="swot-grid">
            {quadrant("Strengths", d.get("strengths",[]), "#00d4aa")}
            {quadrant("Weaknesses", d.get("weaknesses",[]), "#ff4757")}
            {quadrant("Opportunities", d.get("opportunities",[]), "#4a9eff")}
            {quadrant("Threats", d.get("threats",[]), "#ffa502")}
        </div>
    </div>"""
    st.markdown(html, unsafe_allow_html=True)

SIZE_COLS = {"small": 1, "medium": 1, "large": 2, "full": 3}

def render_layout(layout: UILayout):
    renderers = {
        "metric": render_metric,
        "chart": render_chart,
        "table": render_table,
        "text": render_text,
        "warning": render_warning,
        "form": render_form,
        "tags": render_tags,
        "progress": render_progress,
        "swot": render_swot,
    }

    i = 0
    components = layout.components
    while i < len(components):
        comp = components[i]
        try:
            if comp.size == "full":
                renderers.get(comp.type, render_text)(comp)
                i += 1
            elif comp.size == "large":
                cols = st.columns([2, 1]) if i + 1 < len(components) and components[i+1].size in ("small","medium") else st.columns(1)
                with cols[0]:
                    renderers.get(comp.type, render_text)(comp)
                if len(cols) > 1 and i + 1 < len(components):
                    i += 1
                    with cols[1]:
                        renderers.get(components[i].type, render_text)(components[i])
                i += 1
            else:
                group = []
                while i < len(components) and components[i].size in ("small","medium") and len(group) < 3:
                    group.append(components[i])
                    i += 1
                cols = st.columns(len(group))
                for col, c in zip(cols, group):
                    with col:
                        try:
                            renderers.get(c.type, render_text)(c)
                        except Exception:
                            st.markdown('<div class="morphui-card animate-in"><div class="card-label" style="color:#ff4757">⚠ Component Error</div><div class="text-content">This section could not be rendered.</div></div>', unsafe_allow_html=True)
        except Exception:
            st.markdown('<div class="morphui-card animate-in"><div class="card-label" style="color:#ff4757">⚠ Component Error</div><div class="text-content">This section could not be rendered.</div></div>', unsafe_allow_html=True)
            i += 1