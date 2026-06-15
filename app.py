import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import sys
import os
from fpdf import FPDF
from datetime import datetime

sys.path.append("src")
from history import init_db, log_scan, get_history
from explainability import plot_shap_waterfall

st.set_page_config(
    page_title="Advanced CyberShield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize DB
init_db()

# Custom CSS for Cybersecurity Theme
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #c9d1d9; }
    h1, h2, h3 { color: #58a6ff !important; }
    .stAlert { background-color: #161b22; border: 1px solid #30363d; }
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Advanced CyberShield")
st.markdown("**Enterprise AI Phishing Detection Platform**")

@st.cache_resource
def load_model():
    if os.path.exists("advanced_email_model.pkl"):
        return joblib.load("advanced_email_model.pkl")
    return None

model = load_model()

def create_gauge(confidence, is_phishing):
    score = confidence * 100 if is_phishing else (1 - confidence) * 100
    color = "red" if score > 75 else "orange" if score > 40 else "green"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': "Threat Level (%)"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 40], 'color': "rgba(0,255,0,0.1)"},
                {'range': [40, 75], 'color': "rgba(255,165,0,0.1)"},
                {'range': [75, 100], 'color': "rgba(255,0,0,0.1)"}
            ]
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    return fig

def generate_pdf_report(text, prediction, confidence):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=16)
    
    pdf.cell(200, 10, txt="Email Threat Analysis Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("DejaVu", size=12)
    pdf.cell(200, 10, txt=f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(200, 10, txt=f"Prediction: {prediction}", ln=True)
    pdf.cell(200, 10, txt=f"Confidence: {confidence:.2%}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("DejaVu", size=14)
    pdf.cell(200, 10, txt="Analyzed Content:", ln=True)
    pdf.set_font("DejaVu", size=10)
    
    pdf.multi_cell(0, 10, txt=text[:2000])
    
    pdf.output("threat_report.pdf")

tabs = st.tabs(["Scanner", "Explainable AI (SHAP)", "Historical Scans"])

with tabs[0]:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Email Analysis Engine")
        
        # Sample Buttons
        btn_col1, btn_col2 = st.columns(2)
        if btn_col1.button("Load Phishing Sample"):
            st.session_state.email_text = "URGENT: Your PayPal account has been suspended due to unauthorized activity. Please verify your identity immediately at http://paypal-security-auth.com/login.exe"
        if btn_col2.button("Load Safe Sample"):
            st.session_state.email_text = "Hi Team, let's schedule a meeting for tomorrow at 10 AM to discuss the new project requirements. Best, John."
            
        email_text = st.text_area("Raw Email Content", height=250, value=st.session_state.get('email_text', ''))
        st.session_state.email_text = email_text
        
        if st.button("Run Threat Scan", type="primary"):
            if not email_text:
                st.warning("Please enter email text.")
            elif model is None:
                st.error("Model not trained yet. Please run `src/train.py`.")
            else:
                with st.spinner("Analyzing NLP features and handcrafted indicators..."):
                    pred = model.predict([email_text])[0]
                    prob = model.predict_proba([email_text])[0]
                    conf = max(prob)
                    is_phishing = (pred == 1)
                    
                    label = "🚨 PHISHING" if is_phishing else "✅ SAFE"
                    log_scan(email_text, label, conf)
                    
                    st.session_state.scan_result = {
                        "text": email_text, "label": label, "conf": conf, "is_phishing": is_phishing
                    }
                    
                    # Generate SHAP
                    try:
                        plot_shap_waterfall(model, email_text)
                        st.session_state.shap_ready = True
                        st.session_state.shap_error = None
                    except Exception as e:
                        st.session_state.shap_ready = False
                        st.session_state.shap_error = str(e)
                    
                    # Generate PDF
                    generate_pdf_report(email_text, label, conf)
                    st.session_state.pdf_ready = True
                    
    with col2:
        st.subheader("Threat Metrics")
        if 'scan_result' in st.session_state:
            res = st.session_state.scan_result
            st.markdown(f"### {res['label']}")
            st.plotly_chart(create_gauge(res['conf'], res['is_phishing']), use_container_width=True)
            
            if st.session_state.get("pdf_ready"):
                with open("threat_report.pdf", "rb") as f:
                    st.download_button(
                        label="📄 Download Threat Report",
                        data=f,
                        file_name="threat_report.pdf",
                        mime="application/pdf"
                    )

with tabs[1]:
    st.subheader("Explainable AI (SHAP Waterfall)")
    if st.session_state.get("shap_error"):
        st.error(f"SHAP failed to generate: {st.session_state.shap_error}")
    elif st.session_state.get("shap_ready"):
        st.info("This waterfall plot shows how the AI arrived at its decision by pushing the probability higher (red) or lower (blue).")
        if os.path.exists("shap_waterfall.png"):
            st.image("shap_waterfall.png", use_container_width=True)
    else:
        st.write("Run a scan to generate SHAP explanations.")

with tabs[2]:
    st.subheader("Historical Scan Records")
    history = get_history()
    if history:
        df_hist = pd.DataFrame(history, columns=["Timestamp", "Snippet", "Prediction", "Confidence"])
        st.dataframe(df_hist, use_container_width=True)
    else:
        st.write("No scans logged yet.")