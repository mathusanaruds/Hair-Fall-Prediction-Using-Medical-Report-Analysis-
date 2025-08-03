import streamlit as st
import plotly.graph_objects as go

def load_css():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Custom metric cards */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 0.5rem;
        border: 1px solid #1f77b4;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #0056b3;
        border-color: #0056b3;
    }
    
    /* Warning and info boxes */
    .stAlert {
        border-radius: 0.5rem;
    }
    
    /* File uploader */
    .uploadedFile {
        border-radius: 0.5rem;
        border: 2px dashed #1f77b4;
    }
    
    /* Custom headers */
    .custom-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Result cards */
    .result-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    
    /* Status indicators */
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    
    .status-danger {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def create_progress_bar(current_step: int, total_steps: int = 4):
    """Create a progress bar for the application steps"""
    progress = current_step / total_steps
    
    st.markdown(f"""
    <div style="background-color: #e9ecef; border-radius: 0.5rem; padding: 0.25rem; margin: 1rem 0;">
        <div style="background-color: #1f77b4; width: {progress * 100}%; height: 1rem; border-radius: 0.25rem; 
                    transition: width 0.3s ease-in-out;"></div>
    </div>
    <p style="text-align: center; margin-top: 0.5rem; color: #666;">
        Step {current_step} of {total_steps}
    </p>
    """, unsafe_allow_html=True)

def create_status_indicator(status: str, text: str):
    """Create a status indicator with icon and text"""
    icons = {
        "success": "✅",
        "warning": "⚠️", 
        "error": "❌",
        "info": "ℹ️",
        "pending": "⏳"
    }
    
    colors = {
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545", 
        "info": "#17a2b8",
        "pending": "#6c757d"
    }
    
    icon = icons.get(status, "ℹ️")
    color = colors.get(status, "#6c757d")
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; padding: 0.5rem; margin: 0.5rem 0;">
        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
        <span style="color: {color}; font-weight: bold;">{text}</span>
    </div>
    """, unsafe_allow_html=True)

def create_info_card(title: str, content: str, icon: str = "ℹ️"):
    """Create an information card"""
    st.markdown(f"""
    <div class="result-card">
        <h4 style="color: #1f77b4; margin-bottom: 1rem;">
            <span style="margin-right: 0.5rem;">{icon}</span>{title}
        </h4>
        <p style="margin: 0; line-height: 1.6;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, delta: str = None, color: str = "#1f77b4"):
    """Create a custom metric card"""
    delta_html = ""
    if delta:
        delta_html = f'<p style="color: #666; margin: 0.25rem 0 0 0; font-size: 0.875rem;">{delta}</p>'
    
    st.markdown(f"""
    <div style="background-color: white; padding: 1.5rem; border-radius: 0.5rem; 
                border-left: 4px solid {color}; box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);">
        <h3 style="color: {color}; margin: 0; font-size: 2rem; font-weight: bold;">{value}</h3>
        <p style="color: #666; margin: 0.25rem 0 0 0; font-weight: 500;">{title}</p>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def display_data_summary(questionnaire_completed: bool, medical_uploaded: bool):
    """Display data completion summary"""
    st.markdown("### 📊 Data Collection Progress")
    
    col1, col2 = st.columns(2)
    
    with col1:
        status = "success" if questionnaire_completed else "pending"
        text = "Completed" if questionnaire_completed else "Pending"
        create_status_indicator(status, f"Questionnaire: {text}")
    
    with col2:
        status = "success" if medical_uploaded else "pending"
        text = "Uploaded" if medical_uploaded else "Pending"
        create_status_indicator(status, f"Medical Report: {text}")
    
    # Overall progress
    progress = (questionnaire_completed + medical_uploaded) / 2
    st.progress(progress)
    
    if progress == 1.0:
        st.success("🎉 All data collected! Ready for prediction.")
    elif progress > 0:
        st.info("📋 Partial data available. You can proceed with prediction or add more data for better accuracy.")
    else:
        st.warning("⚠️ No data collected yet. Please complete questionnaire or upload medical report.")

def create_feature_comparison_chart(model1_features: dict, model2_features: dict):
    """Create a comparison chart for model features"""
    
    fig = go.Figure()
    
    # Model 1 features (normalized to 0-1 scale)
    if model1_features:
        feature_names = list(model1_features.keys())
        feature_values = list(model1_features.values())
        
        # Normalize values (simple min-max scaling)
        if feature_values:
            max_val = max(feature_values)
            min_val = min(feature_values)
            if max_val > min_val:
                normalized_values = [(v - min_val) / (max_val - min_val) for v in feature_values]
            else:
                normalized_values = [0.5] * len(feature_values)
            
            fig.add_trace(go.Bar(
                name='Biochemical Features',
                x=feature_names,
                y=normalized_values,
                marker_color='#1f77b4'
            ))
    
    fig.update_layout(
        title='Feature Contribution Analysis',
        xaxis_title='Features',
        yaxis_title='Normalized Value',
        showlegend=True,
        height=400
    )
    
    return fig

def format_confidence_level(confidence: float) -> tuple:
    """Format confidence level with color and description"""
    if confidence >= 0.8:
        return "High", "#28a745", "🎯"
    elif confidence >= 0.6:
        return "Medium", "#ffc107", "⚖️"
    else:
        return "Low", "#dc3545", "⚠️"

def create_timeline_component(steps_completed: list):
    """Create a timeline showing completion status"""
    steps = [
        {"name": "Start", "icon": "🏁"},
        {"name": "Questionnaire", "icon": "📋"},
        {"name": "Medical Report", "icon": "📄"},
        {"name": "Prediction", "icon": "🔬"},
        {"name": "Results", "icon": "📊"}
    ]
    
    st.markdown("### 🔄 Progress Timeline")
    
    cols = st.columns(len(steps))
    
    for i, (col, step) in enumerate(zip(cols, steps)):
        with col:
            status = "completed" if i in steps_completed else "pending"
            color = "#28a745" if status == "completed" else "#dee2e6"
            text_color = "white" if status == "completed" else "#6c757d"
            
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="background-color: {color}; color: {text_color}; 
                           width: 3rem; height: 3rem; border-radius: 50%; 
                           display: flex; align-items: center; justify-content: center; 
                           margin: 0 auto 0.5rem auto; font-size: 1.5rem;">
                    {step['icon']}
                </div>
                <p style="margin: 0; font-size: 0.875rem; color: {color};">
                    {step['name']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add connecting line (except for last item)
            if i < len(steps) - 1:
                line_color = "#28a745" if i in steps_completed and (i+1) in steps_completed else "#dee2e6"
                st.markdown(f"""
                <div style="height: 2px; background-color: {line_color}; 
                           margin: 1rem 0; position: relative; top: -2rem;"></div>
                """, unsafe_allow_html=True)