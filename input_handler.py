import base64
import pandas as pd

def handle_text_input(text: str) -> list:
    return [{"type": "text", "text": f"Analyze this and generate a UI:\n\n{text}"}]

def handle_image_input(uploaded_file) -> list:
    bytes_data = uploaded_file.read()
    b64 = base64.b64encode(bytes_data).decode("utf-8")
    mime = uploaded_file.type  # e.g. image/jpeg
    return [
        {
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{b64}"}
        },
        {
            "type": "text",
            "text": "Analyze this image and generate an appropriate UI layout based on what you see."
        }
    ]

def handle_file_input(uploaded_file) -> list:
    name = uploaded_file.name.lower()
    
    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        preview = df.head(50).to_string()
        summary = f"CSV file: {df.shape[0]} rows, {df.shape[1]} columns\nColumns: {list(df.columns)}\n\nPreview:\n{preview}"
        return [{"type": "text", "text": f"Analyze this data and generate an analytics UI:\n\n{summary}"}]
    
    elif name.endswith(".pdf"):
        try:
            import fitz  # pymupdf
            uploaded_file.seek(0)
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            text = text[:4000]  # limit tokens
            return [{"type": "text", "text": f"Analyze this document and generate a UI:\n\n{text}"}]
        except Exception as e:
            return [{"type": "text", "text": f"PDF file uploaded (could not extract text: {e}). Generate a generic document analysis UI."}]
    
    elif name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")[:4000]
        return [{"type": "text", "text": f"Analyze this text and generate a UI:\n\n{text}"}]
    
    else:
        return [{"type": "text", "text": f"File uploaded: {uploaded_file.name}. Generate an appropriate analysis UI."}]