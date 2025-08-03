"""Frontend Configuration for Hair Fall Prediction System"""

class Config:
    # Backend API Configuration
    BACKEND_BASE_URL = "http://localhost:5000"
    
    # API Endpoints
    ENDPOINTS = {
        "health": "/health",
        "questionnaire": "/questionnaire", 
        "predict": "/predict"
    }
    
    # File Upload Settings
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    ALLOWED_FILE_TYPES = ["pdf", "txt", "png", "jpg", "jpeg"]
    
    # UI Configuration
    PAGE_TITLE = "Hair Fall Prediction System"
    PAGE_ICON = "🔬"
    LAYOUT = "wide"
    
    # Styling
    PRIMARY_COLOR = "#1f77b4"
    BACKGROUND_COLOR = "#f8f9fa"
    SECONDARY_COLOR = "#ff7f0e"
    
    # Session State Keys
    SESSION_KEYS = {
        "questionnaire_data": "questionnaire_responses",
        "medical_file": "uploaded_medical_file",
        "prediction_results": "prediction_results",
        "current_step": "current_step"
    }
    
    # Application Steps
    STEPS = [
        {"name": "Home", "icon": "🏠"},
        {"name": "Questionnaire", "icon": "📋"},
        {"name": "Medical Report", "icon": "📄"},
        {"name": "Prediction", "icon": "🔬"},
        {"name": "About", "icon": "ℹ️"}
    ]
    
    # PSS Questions Configuration
    PSS_SCALE = ["Never", "Almost Never", "Sometimes", "Fairly Often", "Very Often"]
    PSS_VALUES = [0, 1, 2, 3, 4]
    
    # Result Interpretation
    STAGE_DESCRIPTIONS = {
        0: "No significant hair fall detected",
        1: "Very mild hair fall indicators", 
        2: "Mild hair fall detected",
        3: "Moderate hair fall confirmed",
        4: "Significant hair fall detected",
        5: "Severe hair fall confirmed"
    }
    
    STAGE_COLORS = {
        0: "#28a745",  # Green
        1: "#6c757d",  # Gray
        2: "#ffc107",  # Yellow
        3: "#fd7e14",  # Orange
        4: "#dc3545",  # Red
        5: "#6f42c1"   # Purple
    }