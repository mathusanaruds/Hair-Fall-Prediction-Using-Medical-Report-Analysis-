import streamlit as st
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from PIL import Image
import time
import traceback

# MUST be the first Streamlit command
st.set_page_config(
    page_title="🔬 Hair Fall Prediction System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Backend configuration
BACKEND_URL = "http://localhost:5000"

def inject_professional_css():
    """Inject complete professional medical-grade CSS styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Professional medical background */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }
    
    /* Professional header */
    .medical-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(30, 64, 175, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .medical-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .medical-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Connection status */
    .status-connected {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }
    
    .status-disconnected {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }
    
    /* Professional cards */
    .medical-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .medical-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-color: #cbd5e1;
    }
    
    .card-title {
        color: #1e293b;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-text {
        color: #64748b;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Question styling */
    .question-container {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #3b82f6;
    }
    
    .question-number {
        background: #3b82f6;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 0.75rem;
    }
    
    .question-text {
        color: #1e293b;
        font-weight: 500;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #1e293b;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    /* Result cards with medical colors */
    .result-excellent {
        border-left: 4px solid #059669;
        background: linear-gradient(90deg, #ecfdf5 0%, white 100%);
    }
    
    .result-good {
        border-left: 4px solid #0284c7;
        background: linear-gradient(90deg, #f0f9ff 0%, white 100%);
    }
    
    .result-warning {
        border-left: 4px solid #d97706;
        background: linear-gradient(90deg, #fffbeb 0%, white 100%);
    }
    
    .result-danger {
        border-left: 4px solid #dc2626;
        background: linear-gradient(90deg, #fef2f2 0%, white 100%);
    }
    
    /* Professional progress bar */
    .progress-container {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 4px;
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #3b82f6, #1e40af);
        border-radius: 8px;
        height: 12px;
        transition: width 0.6s ease;
        position: relative;
    }
    
    .progress-text {
        color: #475569;
        font-weight: 600;
        text-align: center;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    
    /* Professional buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1e40af);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
    }
    
    /* Section headers */
    .section-header {
        color: #1e293b;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .medical-title { font-size: 2rem; }
        .medical-subtitle { font-size: 1rem; }
        .metric-value { font-size: 2rem; }
        .medical-card { padding: 1.5rem; }
        .main .block-container { padding: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)

def check_backend_connection():
    """Check if backend is running with proper error handling"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        st.error(f"Backend connection error: {str(e)}")
        return False
    except Exception as e:
        st.error(f"Unexpected error checking backend: {str(e)}")
        return False

def make_prediction(form_data, uploaded_file=None):
    """Make prediction request to backend with improved error handling"""
    try:
        files = {}
        if uploaded_file:
            uploaded_file.seek(0)
            files['medical_report'] = (uploaded_file.name, uploaded_file, uploaded_file.type)
        
        response = requests.post(
            f"{BACKEND_URL}/predict", 
            data=form_data, 
            files=files, 
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "success": False, 
                "error": f"Server returned status {response.status_code}: {response.text}"
            }
            
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to backend server. Please ensure it's running."}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

def create_professional_gauge(value, title, max_value=100, color_scheme="blue"):
    """Create professional gauge chart with improved error handling"""
    try:
        if color_scheme == "blue":
            colors = ["#dbeafe", "#3b82f6", "#1e40af"]
        elif color_scheme == "green":
            colors = ["#dcfce7", "#16a34a", "#15803d"]
        elif color_scheme == "red":
            colors = ["#fee2e2", "#dc2626", "#b91c1c"]
        else:
            colors = ["#f1f5f9", "#64748b", "#475569"]
        
        # Ensure value is within bounds
        value = max(0, min(value, max_value))
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter'}},
            number = {'font': {'size': 28, 'color': '#1e293b', 'family': 'Inter'}},
            gauge = {
                'axis': {'range': [None, max_value], 'tickcolor': "#64748b", 'tickfont': {'color': '#64748b'}},
                'bar': {'color': colors[1], 'thickness': 0.7},
                'steps': [
                    {'range': [0, max_value*0.3], 'color': colors[0]},
                    {'range': [max_value*0.3, max_value*0.7], 'color': colors[0]},
                    {'range': [max_value*0.7, max_value], 'color': colors[0]}
                ],
                'threshold': {
                    'line': {'color': colors[2], 'width': 3},
                    'thickness': 0.75,
                    'value': max_value*0.8
                },
                'bgcolor': 'white',
                'bordercolor': '#e2e8f0'
            }
        ))
        
        fig.update_layout(
            height=280,
            font={'color': "#1e293b", 'family': "Inter"},
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating gauge chart: {str(e)}")
        return go.Figure()

def create_professional_stage_chart(current_stage):
    """Create professional stage chart with improved error handling"""
    try:
        stages = ['Stage 0', 'Stage 1', 'Stage 2', 'Stage 3', 'Stage 4', 'Stage 5']
        current_stage = max(0, min(current_stage, 5))  # Ensure stage is within bounds
        values = [1.0 if i == current_stage else 0.3 for i in range(6)]
        
        colors = []
        for i in range(6):
            if i == current_stage:
                if i <= 1:
                    colors.append('#16a34a')  # Green
                elif i <= 2:
                    colors.append('#0284c7')  # Blue
                elif i <= 3:
                    colors.append('#d97706')  # Orange
                else:
                    colors.append('#dc2626')  # Red
            else:
                colors.append('#e2e8f0')
        
        fig = go.Figure(data=[
            go.Bar(
                x=stages,
                y=values,
                marker=dict(
                    color=colors,
                    line=dict(color='#cbd5e1', width=1)
                ),
                text=[f"CURRENT" if i == current_stage else "" for i in range(6)],
                textposition="outside",
                textfont=dict(color='#1e293b', size=11, family='Inter')
            )
        ])
        
        fig.update_layout(
            title={
                'text': 'Hair Fall Stage Assessment',
                'x': 0.5,
                'font': {'size': 20, 'color': '#1e293b', 'family': 'Inter'}
            },
            xaxis=dict(
                title=dict(text="Stages", font=dict(color='#64748b', family='Inter')),
                tickfont=dict(color='#64748b', family='Inter'),
                gridcolor='#f1f5f9',
                showgrid=True
            ),
            yaxis=dict(
                title=dict(text="Level", font=dict(color='#64748b', family='Inter')),
                tickfont=dict(color='#64748b', family='Inter'),
                gridcolor='#f1f5f9',
                showgrid=True
            ),
            showlegend=False,
            height=350,
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=40, r=40, t=80, b=40)
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating stage chart: {str(e)}")
        return go.Figure()

def create_professional_model_chart(model1_conf, model2_conf):
    """Create professional model comparison chart with error handling"""
    try:
        models = ['Biochemical Analysis', 'Lifestyle Analysis']
        confidences = [
            max(0.0, min(1.0, model1_conf)),  # Ensure values are between 0 and 1
            max(0.0, min(1.0, model2_conf))
        ]
        colors = ['#3b82f6', '#8b5cf6']
        
        fig = go.Figure(data=[
            go.Bar(
                x=models,
                y=confidences,
                marker=dict(
                    color=colors,
                    line=dict(color='#cbd5e1', width=1)
                ),
                text=[f"{conf:.1%}" for conf in confidences],
                textposition="outside",
                textfont=dict(color='#1e293b', size=12, family='Inter')
            )
        ])
        
        fig.update_layout(
            title={
                'text': 'AI Model Confidence Analysis',
                'x': 0.5,
                'font': {'size': 20, 'color': '#1e293b', 'family': 'Inter'}
            },
            xaxis=dict(
                title=dict(text="Analysis Type", font=dict(color='#64748b', family='Inter')),
                tickfont=dict(color='#64748b', family='Inter'),
                gridcolor='#f1f5f9'
            ),
            yaxis=dict(
                title=dict(text="Confidence Level", font=dict(color='#64748b', family='Inter')),
                tickfont=dict(color='#64748b', family='Inter'),
                gridcolor='#f1f5f9',
                range=[0, 1]
            ),
            showlegend=False,
            height=350,
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=40, r=40, t=80, b=40)
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating model chart: {str(e)}")
        return go.Figure()

def display_professional_header():
    """Display professional medical header"""
    st.markdown("""
    <div class="medical-header">
        <div class="medical-title">🔬 Hair Fall Prediction System</div>
        <div class="medical-subtitle">Advanced AI-Powered Medical Analysis Platform</div>
    </div>
    """, unsafe_allow_html=True)

def display_connection_status():
    """Display professional connection status"""
    if check_backend_connection():
        st.markdown("""
        <div class="status-connected">
            ✅ AI Backend System Connected
        </div>
        """, unsafe_allow_html=True)
        return True
    else:
        st.markdown("""
        <div class="status-disconnected">
            ❌ AI Backend System Disconnected
        </div>
        """, unsafe_allow_html=True)
        st.error("🚨 Cannot connect to AI backend server. Please ensure the backend is running on http://localhost:5000")
        return False

def initialize_session_state():
    """Initialize session state variables"""
    if 'questionnaire_data' not in st.session_state:
        st.session_state.questionnaire_data = {}
    if 'medical_file' not in st.session_state:
        st.session_state.medical_file = None
    if 'prediction_results' not in st.session_state:
        st.session_state.prediction_results = None

def get_pss_score():
    """Calculate PSS score with error handling"""
    try:
        return sum(st.session_state.questionnaire_data.get(f"pss_{i}", 0) for i in range(1, 11))
    except Exception as e:
        st.error(f"Error calculating PSS score: {str(e)}")
        return 0

def render_health_assessment_tab():
    """Render the health assessment tab"""
    try:
        # Progress tracking
        completed_questions = len([k for k in st.session_state.questionnaire_data.keys() if k.startswith('pss_')])
        progress_percentage = (completed_questions / 10) * 100
        
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress_percentage}%;"></div>
        </div>
        <div class="progress-text">{progress_percentage:.0f}% Assessment Complete</div>
        """, unsafe_allow_html=True)
        
        # PSS Assessment
        st.markdown("""
        <div class="medical-card">
            <div class="card-title">🧠 Perceived Stress Scale (PSS) Assessment</div>
            <div class="card-text">
                The PSS is a globally validated psychological instrument for measuring stress perception. 
                Please rate how often you experienced these feelings during the <strong>last month</strong>.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # PSS Questions
        pss_questions = [
            "In the last month, how often have you been upset because of something that happened unexpectedly?",
            "In the last month, how often have you felt that you were unable to control the important things in your life?",
            "In the last month, how often have you felt nervous and stressed?",
            "In the last month, how often have you felt confident about your ability to handle your personal problems?",
            "In the last month, how often have you felt that things were going your way?",
            "In the last month, how often have you found that you could not cope with all the things that you had to do?",
            "In the last month, how often have you been able to control irritations in your life?",
            "In the last month, how often have you felt that you were on top of things?",
            "In the last month, how often have you been angered because of things that happened that were outside of your control?",
            "In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?"
        ]
        
        pss_options = ["Never", "Almost Never", "Sometimes", "Fairly Often", "Very Often"]
        
        for i, question in enumerate(pss_questions, 1):
            st.markdown(f"""
            <div class="question-container">
                <div class="question-number">{i}</div>
                <div class="question-text">{question}</div>
            </div>
            """, unsafe_allow_html=True)
            
            response = st.select_slider(
                f"Question {i} Response",
                options=pss_options,
                key=f"pss_{i}",
                label_visibility="collapsed"
            )
            
            # Apply reverse scoring for questions 4, 5, 7, 8
            if i in [4, 5, 7, 8]:
                st.session_state.questionnaire_data[f"pss_{i}"] = 4 - pss_options.index(response)
            else:
                st.session_state.questionnaire_data[f"pss_{i}"] = pss_options.index(response)
        
        # Lifestyle Assessment
        st.markdown("""
        <div class="medical-card">
            <div class="card-title">👤 Clinical History & Lifestyle Assessment</div>
            <div class="card-text">
                These clinical factors help our AI system understand your medical profile and risk factors.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Lifestyle questions in organized sections
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p class="section-header">🧬 Genetic & Family History</p>', unsafe_allow_html=True)
            genetics = st.radio("Family History of Hair Loss:", ["No", "Yes"], key="genetics")
            st.session_state.questionnaire_data["genetics"] = 1 if genetics == "Yes" else 0
            
            st.markdown('<p class="section-header">🚬 Lifestyle Factors</p>', unsafe_allow_html=True)
            smoking = st.radio("Tobacco Use:", ["No", "Yes"], key="smoking")
            st.session_state.questionnaire_data["smoking"] = 1 if smoking == "Yes" else 0
            
            st.markdown('<p class="section-header">💇‍♀️ Hair Care Practices</p>', unsafe_allow_html=True)
            hair_care = st.radio("Difficulty Maintaining Hair Health:", ["No", "Yes"], key="hair_care")
            st.session_state.questionnaire_data["hair_care"] = 1 if hair_care == "Yes" else 0
        
        with col2:
            st.markdown('<p class="section-header">🌍 Environmental Exposure</p>', unsafe_allow_html=True)
            environment = st.radio("Environmental Stressors (Pollution, Extreme Weather):", ["No", "Yes"], key="environment")
            st.session_state.questionnaire_data["environment"] = 1 if environment == "Yes" else 0
            
            st.markdown('<p class="section-header">⚖️ Hormonal Status</p>', unsafe_allow_html=True)
            hormonal = st.radio("Hormonal Changes (Pregnancy, Menopause, Thyroid):", ["No", "Yes"], key="hormonal_changes")
            st.session_state.questionnaire_data["hormonal_changes"] = 1 if hormonal == "Yes" else 0
            
            st.markdown('<p class="section-header">📉 Recent Health Changes</p>', unsafe_allow_html=True)
            weight_loss = st.radio("Significant Weight Loss Recently:", ["No", "Yes"], key="weight_loss")
            st.session_state.questionnaire_data["weight_loss"] = 1 if weight_loss == "Yes" else 0
        
        # Age input
        st.markdown('<p class="section-header">🎂 Demographics</p>', unsafe_allow_html=True)
        age = st.number_input("Age (years)", min_value=1, max_value=100, value=30, key="age")
        st.session_state.questionnaire_data["age"] = age
        
        # Assessment Results
        pss_score = get_pss_score()
        
        st.markdown('<p class="section-header">📊 Assessment Summary</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{pss_score}</div>
                <div class="metric-label">PSS Score (0-40)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if pss_score <= 13:
                stress_level, stress_class = "Low Risk", "result-excellent"
                stress_icon = "🟢"
            elif pss_score <= 26:
                stress_level, stress_class = "Moderate Risk", "result-warning"
                stress_icon = "🟡"
            else:
                stress_level, stress_class = "High Risk", "result-danger"
                stress_icon = "🔴"
            
            st.markdown(f"""
            <div class="metric-card {stress_class}">
                <div class="metric-value">{stress_icon}</div>
                <div class="metric-label">{stress_level}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            completion = (completed_questions / 10) * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{completion:.0f}%</div>
                <div class="metric-label">Completion</div>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error in health assessment: {str(e)}")
        st.error(f"Traceback: {traceback.format_exc()}")

def render_medical_report_tab():
    """Render the medical report tab"""
    try:
        st.markdown("""
        <div class="medical-card">
            <div class="card-title">📋 Medical Report Upload & Analysis</div>
            <div class="card-text">
                Upload your laboratory reports for comprehensive biomarker analysis. Our AI system extracts key clinical data 
                including protein levels, vitamins, minerals, and liver function markers to enhance diagnostic accuracy.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # File upload section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Select Medical Report",
                type=["pdf", "txt", "png", "jpg", "jpeg"],
                help="Supported formats: PDF, TXT, PNG, JPG, JPEG (Maximum: 16MB)"
            )
            
            if uploaded_file:
                st.session_state.medical_file = uploaded_file
                st.success(f"✅ Medical report uploaded successfully: {uploaded_file.name}")
                
                # File information display
                file_col1, file_col2, file_col3 = st.columns(3)
                
                with file_col1:
                    st.markdown(f"""
                    <div class="medical-card">
                        <div class="card-title">📄 Document Name</div>
                        <div class="card-text">{uploaded_file.name}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with file_col2:
                    st.markdown(f"""
                    <div class="medical-card">
                        <div class="card-title">📊 File Size</div>
                        <div class="card-text">{uploaded_file.size / 1024:.1f} KB</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with file_col3:
                    file_type = uploaded_file.name.split('.')[-1].upper()
                    st.markdown(f"""
                    <div class="medical-card">
                        <div class="card-title">🔖 Format</div>
                        <div class="card-text">{file_type}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="medical-card">
                <div class="card-title">💡 Clinical Guidelines</div>
                <div class="card-text">
                    <ul style="color: #64748b; line-height: 1.8; margin: 0; padding-left: 1rem;">
                        <li>🔍 Ensure text is legible and high-resolution</li>
                        <li>🩸 Include complete blood chemistry panels</li>
                        <li>💊 Add vitamin and mineral profiles</li>
                        <li>🧬 Include protein and keratin measurements</li>
                        <li>🫀 Add hepatic function indicators</li>
                        <li>⚗️ Include hormonal markers if available</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error in medical report tab: {str(e)}")

def render_ai_analysis_tab():
    """Render the AI analysis tab"""
    try:
        # Data readiness assessment
        has_questionnaire = len(st.session_state.questionnaire_data) > 0
        has_medical = st.session_state.medical_file is not None
        
        st.markdown("""
        <div class="medical-card">
            <div class="card-title">🔬 AI-Powered Clinical Analysis Engine</div>
            <div class="card-text">
                Our advanced dual-model artificial intelligence system combines neural networks with ensemble learning 
                to provide comprehensive hair loss risk assessment based on clinical biomarkers and lifestyle factors.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Clinical data status
        status_col1, status_col2 = st.columns(2)
        
        with status_col1:
            if has_questionnaire:
                pss_completed = sum(1 for i in range(1, 11) if f"pss_{i}" in st.session_state.questionnaire_data)
                st.markdown(f"""
                <div class="medical-card result-excellent">
                    <div class="card-title">✅ Clinical Assessment Complete</div>
                    <div class="card-text">
                        📊 PSS Assessment: {pss_completed}/10 questions completed<br>
                        👤 Lifestyle Factors: All factors assessed<br>
                        🎯 System Status: Ready for AI analysis
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="medical-card result-warning">
                    <div class="card-title">⚠️ Clinical Assessment Required</div>
                    <div class="card-text">Please complete the health assessment questionnaire to proceed</div>
                </div>
                """, unsafe_allow_html=True)
        
        with status_col2:
            if has_medical:
                st.markdown(f"""
                <div class="medical-card result-excellent">
                    <div class="card-title">✅ Laboratory Report Available</div>
                    <div class="card-text">
                        📄 Document: {st.session_state.medical_file.name}<br>
                        🔍 OCR Engine: Ready for text extraction<br>
                        🧪 Biomarker Analysis: Enabled
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="medical-card result-good">
                    <div class="card-title">📋 Laboratory Report (Optional)</div>
                    <div class="card-text">Upload laboratory reports for enhanced biomarker analysis and improved diagnostic accuracy</div>
                </div>
                """, unsafe_allow_html=True)
        
        if not has_questionnaire:
            st.warning("⚠️ Clinical assessment required. Please complete the health questionnaire to proceed with AI analysis.")
            return
        
        # AI Analysis execution
        if st.button("🚀 Initiate AI Clinical Analysis", type="primary", use_container_width=True):
            
            # Professional progress animation
            progress_container = st.empty()
            status_container = st.empty()
            
            analysis_stages = [
                (20, "🤖 Initializing neural network models..."),
                (40, "🧠 Processing clinical assessment data..."),
                (60, "📄 Extracting biomarkers from medical reports..."),
                (80, "🔬 Executing dual-model predictions..."),
                (95, "📊 Compiling comprehensive analysis..."),
                (100, "✅ Clinical analysis complete!")
            ]
            
            for progress, status in analysis_stages:
                progress_container.markdown(f"""
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress}%;"></div>
                </div>
                """, unsafe_allow_html=True)
                
                status_container.markdown(f"""
                <div class="medical-card">
                    <div class="card-text" style="text-align: center; font-weight: 600; color: #3b82f6;">
                        {status}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(0.6)
            
            # Execute prediction
            form_data = st.session_state.questionnaire_data.copy()
            result = make_prediction(form_data, st.session_state.medical_file)
            
            progress_container.empty()
            status_container.empty()
            
            if result.get("success"):
                st.session_state.prediction_results = result
                predictions = result.get("predictions", {})
                
                st.success("🎉 AI Clinical Analysis Successfully Completed!")
                
                # Extract clinical results with safe defaults
                stage = predictions.get("stage", 0)
                condition = predictions.get("condition", "No")
                confidence = predictions.get("confidence", 0.0)
                
                # Ensure values are within expected ranges
                stage = max(0, min(stage, 5))
                confidence = max(0.0, min(confidence, 1.0))
                
                # Clinical results display
                result_col1, result_col2, result_col3 = st.columns(3)
                
                with result_col1:
                    if stage <= 1:
                        stage_class, stage_icon = "result-excellent", "🟢"
                        stage_severity = "Minimal"
                    elif stage <= 2:
                        stage_class, stage_icon = "result-good", "🔵"
                        stage_severity = "Mild"
                    elif stage <= 3:
                        stage_class, stage_icon = "result-warning", "🟡"
                        stage_severity = "Moderate"
                    else:
                        stage_class, stage_icon = "result-danger", "🔴"
                        stage_severity = "Significant"
                    
                    st.markdown(f"""
                    <div class="metric-card {stage_class}">
                        <div class="metric-value">{stage_icon} {stage}</div>
                        <div class="metric-label">Hair Loss Stage<br><small>{stage_severity} Severity</small></div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with result_col2:
                    condition_class = "result-danger" if condition == "Yes" else "result-excellent"
                    condition_icon = "⚠️" if condition == "Yes" else "✅"
                    condition_status = "Positive" if condition == "Yes" else "Negative"
                    
                    st.markdown(f"""
                    <div class="metric-card {condition_class}">
                        <div class="metric-value">{condition_icon}</div>
                        <div class="metric-label">Clinical Finding<br><small>{condition_status} for Hair Loss</small></div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with result_col3:
                    if confidence >= 0.8:
                        conf_class, conf_icon = "result-excellent", "🎯"
                        conf_level = "High"
                    elif confidence >= 0.6:
                        conf_class, conf_icon = "result-warning", "⚖️"
                        conf_level = "Moderate"
                    else:
                        conf_class, conf_icon = "result-danger", "⚠️"
                        conf_level = "Low"
                    
                    st.markdown(f"""
                    <div class="metric-card {conf_class}">
                        <div class="metric-value">{conf_icon}</div>
                        <div class="metric-label">Diagnostic Confidence<br><small>{confidence:.1%} ({conf_level})</small></div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Clinical interpretation
                interpretation = predictions.get("interpretation", "")
                if interpretation:
                    st.markdown(f"""
                    <div class="medical-card">
                        <div class="card-title">🤖 AI Clinical Interpretation</div>
                        <div class="card-text" style="font-size: 1rem; line-height: 1.7; font-weight: 500;">
                            {interpretation}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Clinical recommendations based on stage
                render_clinical_recommendations(stage)
                
                # Technical analysis details
                render_technical_analysis(predictions)
            
            else:
                st.error(f"❌ AI Analysis Failed: {result.get('error', 'Unknown system error occurred')}")
                
    except Exception as e:
        st.error(f"Error in AI analysis tab: {str(e)}")
        st.error(f"Traceback: {traceback.format_exc()}")

def render_clinical_recommendations(stage):
    """Render clinical recommendations based on stage"""
    try:
        st.markdown('<p class="section-header">💡 Clinical Recommendations</p>', unsafe_allow_html=True)
        
        if stage <= 1:
            st.markdown("""
            <div class="medical-card result-excellent">
                <div class="card-title">🎉 Excellent Hair Health Profile</div>
                <div class="card-text">
                    <strong>Preventive Care Protocol:</strong>
                    <ul style="line-height: 1.8; margin-top: 1rem;">
                        <li>✅ <strong>Maintenance:</strong> Continue current hair care regimen</li>
                        <li>🥗 <strong>Nutrition:</strong> Maintain protein-rich diet with biotin and essential vitamins</li>
                        <li>💧 <strong>Hydration:</strong> Ensure adequate fluid intake (2-3L daily)</li>
                        <li>😌 <strong>Stress Management:</strong> Continue effective stress reduction practices</li>
                        <li>🏃 <strong>Circulation:</strong> Regular cardiovascular exercise for scalp health</li>
                        <li>🌙 <strong>Sleep Hygiene:</strong> Maintain 7-8 hours quality sleep for cellular regeneration</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif stage <= 2:
            st.markdown("""
            <div class="medical-card result-good">
                <div class="card-title">💙 Good Hair Health with Monitoring Required</div>
                <div class="card-text">
                    <strong>Early Intervention Protocol:</strong>
                    <ul style="line-height: 1.8; margin-top: 1rem;">
                        <li>👀 <strong>Monitoring:</strong> Monthly self-assessment and photographic documentation</li>
                        <li>🧴 <strong>Hair Care:</strong> Transition to gentle, sulfate-free formulations</li>
                        <li>💊 <strong>Supplementation:</strong> Consider biotin (5mg), vitamin D3, omega-3 fatty acids</li>
                        <li>🧘 <strong>Stress Reduction:</strong> Implement mindfulness practices and relaxation techniques</li>
                        <li>🌙 <strong>Sleep Optimization:</strong> Establish consistent sleep-wake cycle</li>
                        <li>🥬 <strong>Nutritional Support:</strong> Increase antioxidant-rich foods and lean proteins</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif stage <= 3:
            st.markdown("""
            <div class="medical-card result-warning">
                <div class="card-title">⚠️ Moderate Hair Loss - Medical Consultation Recommended</div>
                <div class="card-text">
                    <strong>Medical Intervention Protocol:</strong>
                    <ul style="line-height: 1.8; margin-top: 1rem;">
                        <li>👨‍⚕️ <strong>Specialist Referral:</strong> Consultation with dermatologist or trichologist</li>
                        <li>🔬 <strong>Laboratory Assessment:</strong> Complete metabolic panel, thyroid function, iron studies</li>
                        <li>🚫 <strong>Avoid:</strong> Chemical treatments, excessive heat styling, tight hairstyles</li>
                        <li>💊 <strong>Targeted Therapy:</strong> Medical-grade nutritional supplementation</li>
                        <li>🌿 <strong>Topical Care:</strong> Gentle scalp massage, rosemary oil, minoxidil consideration</li>
                        <li>📊 <strong>Progress Tracking:</strong> Weekly hair count and monthly photographic assessment</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="medical-card result-danger">
                <div class="card-title">🚨 Significant Hair Loss - Immediate Medical Intervention Required</div>
                <div class="card-text">
                    <strong>Urgent Treatment Protocol:</strong>
                    <ul style="line-height: 1.8; margin-top: 1rem;">
                        <li>🏥 <strong>Emergency Consultation:</strong> Immediate evaluation by hair restoration specialist</li>
                        <li>🔬 <strong>Comprehensive Workup:</strong> Full hormonal panel, autoimmune markers, nutritional assessment</li>
                        <li>💉 <strong>Medical Therapy:</strong> FDA-approved treatments (minoxidil, finasteride, dutasteride)</li>
                        <li>📋 <strong>Monitoring Protocol:</strong> Bi-weekly follow-ups with progress documentation</li>
                        <li>🧬 <strong>Genetic Testing:</strong> Androgenetic alopecia genetic markers</li>
                        <li>🔄 <strong>Advanced Therapies:</strong> PRP, microneedling, low-level laser therapy, transplantation consultation</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error rendering clinical recommendations: {str(e)}")

def render_technical_analysis(predictions):
    """Render technical analysis details"""
    try:
        with st.expander("🔬 Technical Model Analysis"):
            detailed = predictions.get("detailed_results", {})
            
            tech_col1, tech_col2 = st.columns(2)
            
            with tech_col1:
                st.markdown("#### 🧪 Biochemical Analysis Model")
                st.metric("Stage Prediction", f"Stage {detailed.get('model1_stage', 0)}")
                st.metric("Neural Network Confidence", f"{detailed.get('model1_confidence', 0):.1%}")
                st.info("🔬 Analyzes protein levels, vitamins, minerals, stress biomarkers, and hepatic function")
            
            with tech_col2:
                st.markdown("#### 👤 Lifestyle Risk Model")
                condition_val = "Positive" if detailed.get('model2_condition', 0) == 1 else "Negative"
                st.metric("Risk Assessment", condition_val)
                st.metric("Random Forest Confidence", f"{detailed.get('model2_confidence', 0):.1%}")
                st.info("🎯 Evaluates genetic factors, stress levels, environmental exposures, and health history")
    except Exception as e:
        st.error(f"Error rendering technical analysis: {str(e)}")

def render_dashboard_tab():
    """Render the clinical dashboard tab"""
    try:
        if st.session_state.prediction_results:
            predictions = st.session_state.prediction_results.get("predictions", {})
            
            st.markdown("""
            <div class="medical-card">
                <div class="card-title">📊 Clinical Analytics Dashboard</div>
                <div class="card-text">
                    Comprehensive visualization and statistical analysis of your hair health assessment results.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Clinical dashboard charts
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # Stage assessment chart
                stage = predictions.get("stage", 0)
                fig1 = create_professional_stage_chart(stage)
                st.plotly_chart(fig1, use_container_width=True)
                
                # Overall confidence gauge
                confidence = predictions.get("confidence", 0.0)
                fig3 = create_professional_gauge(confidence * 100, "Overall Diagnostic Confidence", 100, "blue")
                st.plotly_chart(fig3, use_container_width=True)
            
            with chart_col2:
                # Model performance comparison
                detailed = predictions.get("detailed_results", {})
                model1_conf = detailed.get("model1_confidence", 0)
                model2_conf = detailed.get("model2_confidence", 0)
                fig2 = create_professional_model_chart(model1_conf, model2_conf)
                st.plotly_chart(fig2, use_container_width=True)
                
                # PSS stress assessment gauge
                pss_score = get_pss_score()
                fig4 = create_professional_gauge(pss_score, "PSS Stress Assessment", 40, "red")
                st.plotly_chart(fig4, use_container_width=True)
            
            # Clinical data export
            st.markdown('<p class="section-header">📁 Clinical Data Export</p>', unsafe_allow_html=True)
            
            export_col1, export_col2, export_col3 = st.columns(3)
            
            with export_col1:
                if st.button("📄 Generate Clinical Report", use_container_width=True):
                    st.info("📋 Clinical PDF report generation feature in development")
            
            with export_col2:
                if st.button("📊 Export Analysis Data", use_container_width=True):
                    json_data = json.dumps(st.session_state.prediction_results, indent=2)
                    st.download_button(
                        label="📥 Download Clinical Data (JSON)",
                        data=json_data,
                        file_name=f"clinical_hair_analysis_{int(time.time())}.json",
                        mime="application/json",
                        use_container_width=True
                    )
            
            with export_col3:
                if st.button("🔄 New Clinical Assessment", use_container_width=True):
                    # Use a confirmation dialog
                    if st.button("✅ Confirm Data Reset", key="confirm_reset"):
                        st.session_state.questionnaire_data = {}
                        st.session_state.medical_file = None
                        st.session_state.prediction_results = None
                        st.rerun()
        
        else:
            st.markdown("""
            <div class="medical-card">
                <div class="card-title" style="text-align: center;">📊 Clinical Analytics Dashboard</div>
                <div class="card-text" style="text-align: center;">
                    Complete your clinical assessment and execute AI analysis to access comprehensive 
                    interactive visualizations, statistical trends, and detailed clinical insights.
                </div>
                <div style="text-align: center; margin: 3rem 0;">
                    <div style="font-size: 4rem; color: #cbd5e1;">📈📊📉</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error in dashboard tab: {str(e)}")

def main():
    """Main application with professional medical UI and improved error handling"""
    try:
        # Inject professional CSS
        inject_professional_css()
        
        # Professional header
        display_professional_header()
        
        # Connection status
        if not display_connection_status():
            return
        
        # Initialize session state
        initialize_session_state()
        
        # Professional tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🧠 Health Assessment", 
            "📋 Medical Report", 
            "🔬 AI Analysis", 
            "📊 Clinical Dashboard"
        ])
        
        with tab1:
            render_health_assessment_tab()
        
        with tab2:
            render_medical_report_tab()
        
        with tab3:
            render_ai_analysis_tab()
        
        with tab4:
            render_dashboard_tab()
            
    except Exception as e:
        st.error(f"Critical application error: {str(e)}")
        st.error(f"Traceback: {traceback.format_exc()}")
        st.info("Please refresh the page and try again. If the problem persists, contact support.")

if __name__ == "__main__":
    main()