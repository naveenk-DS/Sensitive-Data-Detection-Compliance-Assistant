import streamlit as st
import os
import uuid
import json
import pandas as pd
import plotly.express as px
from datetime import datetime

# Import custom modules
from config import UPLOADS_DIR, OUTPUTS_DIR, VECTOR_DB_DIR
from document_parser import parse_document
from detector import detect_sensitive_data
from risk import calculate_risk
from redactor import redact_document
from summary import generate_compliance_summary
from qa import answer_question
from rag import create_vector_store
from utils import log_scan, get_all_logs

st.set_page_config(
    page_title="AI Compliance Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Theme and Modern UI
st.markdown("""
<style>
    .reportview-container {
        background: #121212;
    }
    .sidebar .sidebar-content {
        background: #1e1e1e;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .risk-high { color: #ff4b4b; font-weight: bold; }
    .risk-medium { color: #ffa500; font-weight: bold; }
    .risk-low { color: #00fa9a; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ AI-Powered Sensitive Data Detection & Compliance Assistant")

# Session State Initialization
if "current_docs" not in st.session_state:
    st.session_state.current_docs = {}

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    ollama_url = st.text_input("Ollama Base URL", value=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"))
    ollama_model = st.text_input("Ollama Model", value=os.environ.get("OLLAMA_MODEL", "llama3"))
    
    if ollama_url:
        os.environ["OLLAMA_BASE_URL"] = ollama_url
    if ollama_model:
        os.environ["OLLAMA_MODEL"] = ollama_model
            
    st.markdown("---")
    st.header("📈 Live Risk Monitor")
    
    # Live mini-chart
    logs_df = get_all_logs()
    if not logs_df.empty:
        # We only plot the last 15 scans to make it look like a live heartbeat monitor
        recent_logs = logs_df.tail(15)
        fig_monitor = px.line(
            recent_logs, x='id', y='risk_score',
            markers=True, line_shape='spline',
            color_discrete_sequence=['#00FF66']
        )
        fig_monitor.update_traces(
            fill='tozeroy', 
            fillcolor='rgba(0, 255, 102, 0.1)', 
            line=dict(width=3)
        )
        fig_monitor.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=5, b=5, l=5, r=5),
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            height=120, hovermode="x unified",
            showlegend=False
        )
        st.plotly_chart(fig_monitor, use_container_width=True)
    else:
        st.info("Awaiting scans...")
        
    st.markdown("- **0–5**: <span class='risk-low'>Low Risk</span>", unsafe_allow_html=True)
    st.markdown("- **6–15**: <span class='risk-medium'>Medium Risk</span>", unsafe_allow_html=True)
    st.markdown("- **16+**: <span class='risk-high'>High Risk</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("Developed by AI Assistant\nVersion 1.0.0")

# --- MAIN TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📤 Upload & Scan", "📊 Dashboard", "📝 Compliance Report", "💬 Q&A", "📜 Audit Logs"
])

with tab1:
    st.header("Document Upload")
    uploaded_files = st.file_uploader(
        "Upload Documents (PDF, TXT, CSV)", 
        type=['pdf', 'txt', 'csv'], 
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("🚀 Analyze Documents"):
            with st.spinner("Analyzing documents..."):
                for file in uploaded_files:
                    doc_id = str(uuid.uuid4())
                    file_path = os.path.join(UPLOADS_DIR, f"{doc_id}_{file.name}")
                    
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                        
                    # Parse
                    text, page_data = parse_document(file_path)
                    
                    # Detect
                    sensitive_items = detect_sensitive_data(text)
                    
                    # Risk
                    risk_score, risk_level = calculate_risk(sensitive_items)
                    
                    # Store in session state
                    st.session_state.current_docs[file.name] = {
                        "id": doc_id,
                        "path": file_path,
                        "text": text,
                        "page_data": page_data,
                        "sensitive_items": sensitive_items,
                        "risk_score": risk_score,
                        "risk_level": risk_level,
                        "summary": None # Generated on demand
                    }
                    
                    # Log
                    log_scan(file.name, len(sensitive_items), risk_level, risk_score)
                    
                    # Vector DB for RAG
                    try:
                        create_vector_store(text, doc_id)
                    except Exception as e:
                        st.warning(f"Could not create vector store for {file.name}: {e}")
                        
                st.success("Analysis Complete!")
                st.rerun()

    # Display current docs
    if st.session_state.current_docs:
        st.subheader("Detected Data")
        selected_file = st.selectbox("Select File to View", list(st.session_state.current_docs.keys()))
        doc_data = st.session_state.current_docs[selected_file]
        
        st.write(f"**Risk Level:** {doc_data['risk_level']} ({doc_data['risk_score']})")
        
        if doc_data["sensitive_items"]:
            df = pd.DataFrame(doc_data["sensitive_items"])
            st.dataframe(df, use_container_width=True)
            
            # Export options
            col1, col2, col3 = st.columns(3)
            with col1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, "detection_report.csv", "text/csv")
            with col2:
                json_str = df.to_json(orient='records')
                st.download_button("Download JSON", json_str, "detection_report.json", "application/json")
            with col3:
                # Redaction
                if selected_file.endswith(".pdf"):
                    mask_mode = st.selectbox("Masking Mode", ["Full Black Box", "Partial Mask", "Blur Sensitive Data", "Highlight Before Masking"])
                    if st.button("Generate Masked PDF"):
                        with st.spinner("Redacting..."):
                            out_path = os.path.join(OUTPUTS_DIR, f"masked_{selected_file}")
                            redact_document(doc_data["path"], out_path, doc_data["page_data"], doc_data["sensitive_items"], mask_mode)
                            with open(out_path, "rb") as f:
                                st.download_button("Download Masked PDF", f, f"masked_{selected_file}", "application/pdf")
        else:
            st.info("No sensitive data detected.")

with tab2:
    st.header("📊 Global Risk Dashboard")
    if st.session_state.current_docs:
        all_items = []
        doc_risks = []
        for filename, doc in st.session_state.current_docs.items():
            all_items.extend(doc["sensitive_items"])
            doc_risks.append({"Document": filename, "Risk Score": doc["risk_score"]})
            
        if all_items:
            df_all = pd.DataFrame(all_items)
            df_docs = pd.DataFrame(doc_risks)
            
            # --- TOP KPIs ---
            st.markdown("### 📈 Executive Summary")
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.metric(label="Total Documents Scanned", value=len(doc_risks))
            with kpi2:
                st.metric(label="Total Sensitive Items", value=len(all_items))
            with kpi3:
                st.metric(label="Average Risk Score", value=f"{df_docs['Risk Score'].mean():.1f}")
                
            st.markdown("<hr style='border: 1px solid #333;'>", unsafe_allow_html=True)
            
            # --- CHARTS ROW 1 ---
            col1, col2 = st.columns(2)
            counts = df_all['Category'].value_counts().reset_index()
            counts.columns = ['Category', 'Count']
            
            custom_colors = ['#00F0FF', '#FF0055', '#7000FF', '#00FF66', '#FFD700', '#FF8C00']
            
            with col1:
                st.markdown("#### 🎯 Data Distribution")
                fig_donut = px.pie(
                    counts, values='Count', names='Category', hole=0.5,
                    color_discrete_sequence=custom_colors
                )
                fig_donut.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#121212', width=2)))
                fig_donut.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"), showlegend=False, margin=dict(t=20, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_donut, use_container_width=True)
                
            with col2:
                st.markdown("#### 📦 Category Hierarchy")
                fig_tree = px.treemap(
                    counts, path=[px.Constant("All Data"), 'Category'], values='Count',
                    color='Count', color_continuous_scale='Purp'
                )
                fig_tree.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"), margin=dict(t=20, b=20, l=20, r=20)
                )
                fig_tree.update_traces(marker=dict(cornerradius=5))
                st.plotly_chart(fig_tree, use_container_width=True)
                
            # --- CHARTS ROW 2 ---
            st.markdown("#### 🚨 Risk Score by Document")
            fig_bar = px.bar(
                df_docs, x="Risk Score", y="Document", orientation='h',
                color="Risk Score", color_continuous_scale="Reds",
                text="Risk Score"
            )
            fig_bar.update_traces(textposition='outside')
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"), margin=dict(t=20, b=20, l=20, r=20),
                xaxis=dict(showgrid=True, gridcolor="#333"),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        else:
            st.info("No data to visualize.")
    else:
        st.info("Upload documents to see the dashboard.")

with tab3:
    st.header("📝 AI Compliance Report")
    if st.session_state.current_docs:
        selected_file_rep = st.selectbox("Select File for Report", list(st.session_state.current_docs.keys()), key="rep_select")
        doc_data = st.session_state.current_docs[selected_file_rep]
        
        if st.button("Generate Report"):
            with st.spinner("Generating AI Report with Ollama..."):
                try:
                    report = generate_compliance_summary(
                        doc_data["text"], 
                        doc_data["sensitive_items"],
                        doc_data["risk_level"],
                        doc_data["risk_score"]
                    )
                    doc_data["summary"] = report
                    st.session_state.current_docs[selected_file_rep] = doc_data
                except Exception as e:
                    st.error(f"Error generating report: {e}")
                        
        if doc_data.get("summary"):
            st.markdown(doc_data["summary"])
            # Simple text download for report
            st.download_button("Download Report (TXT)", doc_data["summary"], f"report_{selected_file_rep}.txt")
    else:
        st.info("Upload documents first.")

with tab4:
    st.header("💬 Document Q&A")
    if st.session_state.current_docs:
        selected_file_qa = st.selectbox("Select File to Ask About", list(st.session_state.current_docs.keys()), key="qa_select")
        doc_data = st.session_state.current_docs[selected_file_qa]
        
        question = st.text_input("Ask a question about the document:")
        if st.button("Ask"):
            if question:
                with st.spinner("Searching for answer using Ollama..."):
                    try:
                        answer = answer_question(question, doc_data["text"], doc_data["id"])
                        st.success("Answer:")
                        st.write(answer)
                    except Exception as e:
                        st.error(f"Error answering question: {e}")
    else:
        st.info("Upload documents first.")

with tab5:
    st.header("📜 Audit Logs")
    logs_df = get_all_logs()
    if not logs_df.empty:
        st.dataframe(logs_df, use_container_width=True)
        csv = logs_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Audit Logs", csv, "audit_logs.csv", "text/csv")
    else:
        st.info("No logs available yet.")
