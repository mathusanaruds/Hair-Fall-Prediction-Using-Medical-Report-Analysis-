import streamlit as st
from typing import Dict, Any, Optional
from config import Config

class DataManager:
    """Manage session data and state"""
    
    def __init__(self):
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        for key in Config.SESSION_KEYS.values():
            if key not in st.session_state:
                st.session_state[key] = None
        
        # Initialize step tracking
        if "current_step" not in st.session_state:
            st.session_state.current_step = 0
        
        # Initialize completion flags
        if "questionnaire_completed" not in st.session_state:
            st.session_state.questionnaire_completed = False
        
        if "medical_report_uploaded" not in st.session_state:
            st.session_state.medical_report_uploaded = False
    
    def save_questionnaire_data(self, data: Dict[str, Any]):
        """Save questionnaire responses"""
        st.session_state[Config.SESSION_KEYS["questionnaire_data"]] = data
        st.session_state.questionnaire_completed = True
        st.success("✅ Questionnaire responses saved!")
    
    def get_questionnaire_data(self) -> Optional[Dict[str, Any]]:
        """Get questionnaire responses"""
        return st.session_state.get(Config.SESSION_KEYS["questionnaire_data"])
    
    def save_medical_file(self, file_data: Any):
        """Save uploaded medical file"""
        st.session_state[Config.SESSION_KEYS["medical_file"]] = file_data
        st.session_state.medical_report_uploaded = True
        st.success("✅ Medical report uploaded successfully!")
    
    def get_medical_file(self) -> Optional[Any]:
        """Get uploaded medical file"""
        return st.session_state.get(Config.SESSION_KEYS["medical_file"])
    
    def save_prediction_results(self, results: Dict[str, Any]):
        """Save prediction results"""
        st.session_state[Config.SESSION_KEYS["prediction_results"]] = results
    
    def get_prediction_results(self) -> Optional[Dict[str, Any]]:
        """Get prediction results"""
        return st.session_state.get(Config.SESSION_KEYS["prediction_results"])
    
    def clear_all_data(self):
        """Clear all session data"""
        for key in Config.SESSION_KEYS.values():
            st.session_state[key] = None
        
        st.session_state.questionnaire_completed = False
        st.session_state.medical_report_uploaded = False
        st.session_state.current_step = 0
        
        st.success("✅ All data cleared!")
    
    def get_completion_status(self) -> Dict[str, bool]:
        """Get completion status of different steps"""
        return {
            "questionnaire": st.session_state.get("questionnaire_completed", False),
            "medical_report": st.session_state.get("medical_report_uploaded", False),
            "prediction": st.session_state.get(Config.SESSION_KEYS["prediction_results"]) is not None
        }
    
    def update_current_step(self, step: int):
        """Update current step"""
        st.session_state.current_step = step
    
    def get_current_step(self) -> int:
        """Get current step"""
        return st.session_state.get("current_step", 0)
    
    def is_ready_for_prediction(self) -> bool:
        """Check if ready to make prediction"""
        questionnaire_data = self.get_questionnaire_data()
        medical_file = self.get_medical_file()
        
        return (questionnaire_data is not None) or (medical_file is not None)
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of available data"""
        questionnaire_data = self.get_questionnaire_data()
        medical_file = self.get_medical_file()
        
        summary = {
            "has_questionnaire": questionnaire_data is not None,
            "has_medical_report": medical_file is not None,
            "questionnaire_questions_answered": 0,
            "medical_file_name": None,
            "ready_for_prediction": False
        }
        
        if questionnaire_data:
            # Count PSS questions answered
            pss_count = sum(1 for key in questionnaire_data.keys() if key.startswith("pss_"))
            summary["questionnaire_questions_answered"] = pss_count
        
        if medical_file:
            summary["medical_file_name"] = getattr(medical_file, 'name', 'Unknown file')
        
        summary["ready_for_prediction"] = self.is_ready_for_prediction()
        
        return summary