import streamlit as st
from typing import Dict, Any
from config import Config
from services.data_manager import DataManager

class QuestionnaireComponent:
    """Component for handling questionnaire UI and logic"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.pss_questions = self._get_pss_questions()
        self.lifestyle_questions = self._get_lifestyle_questions()
    
    def _get_pss_questions(self) -> list:
        """Get PSS questionnaire questions"""
        return [
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
    
    def _get_lifestyle_questions(self) -> Dict[str, Dict]:
        """Get lifestyle questions"""
        return {
            "genetics": {
                "question": "Do your parents or siblings have hair fall problems?",
                "type": "binary"
            },
            "smoking": {
                "question": "Do you have a smoking habit?",
                "type": "binary"
            },
            "hair_care": {
                "question": "Is it difficult to maintain your hair in good condition?",
                "type": "binary"
            },
            "environment": {
                "question": "Is your environment polluted or do you experience extreme weather conditions or radiological problems?",
                "type": "binary"
            },
            "hormonal_changes": {
                "question": "Are you experiencing hormonal changes (pregnancy, menopause, thyroid issues)?",
                "type": "binary"
            },
            "weight_loss": {
                "question": "Have you experienced significant weight loss recently?",
                "type": "binary"
            },
            "age": {
                "question": "What is your age?",
                "type": "number",
                "min": 1,
                "max": 100
            }
        }
    
    def render(self):
        """Render the questionnaire component"""
        
        # Load existing data if available
        existing_data = self.data_manager.get_questionnaire_data() or {}
        
        # Progress tracking
        completion_status = self.data_manager.get_completion_status()
        
        if completion_status["questionnaire"]:
            st.success("✅ Questionnaire completed!")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("You can modify your responses and save again if needed.")
            with col2:
                if st.button("🗑️ Clear Responses", use_container_width=True):
                    self.data_manager.save_questionnaire_data({})
                    st.rerun()
        
        # Create tabs for different sections
        tab1, tab2 = st.tabs(["📊 Stress Assessment (PSS)", "👤 Lifestyle Factors"])
        
        questionnaire_data = {}
        
        with tab1:
            st.markdown("### Perceived Stress Scale (PSS)")
            st.markdown("*Please rate how often you felt or thought a certain way during the **last month**.*")
            
            # PSS Questions
            for i, question in enumerate(self.pss_questions, 1):
                st.markdown(f"**Question {i}:**")
                st.markdown(question)
                
                key = f"pss_{i}"
                default_value = existing_data.get(key, 0)
                
                response = st.select_slider(
                    f"Response to Question {i}",
                    options=Config.PSS_SCALE,
                    value=Config.PSS_SCALE[default_value],
                    key=key,
                    label_visibility="collapsed"
                )
                
                # Convert response to numeric value
                questionnaire_data[key] = Config.PSS_SCALE.index(response)
                
                st.markdown("---")
        
        with tab2:
            st.markdown("### Lifestyle & Health Factors")
            st.markdown("*Please answer the following questions about your lifestyle and health history.*")
            
            # Lifestyle Questions
            for key, question_data in self.lifestyle_questions.items():
                question = question_data["question"]
                question_type = question_data["type"]
                
                st.markdown(f"**{question}**")
                
                if question_type == "binary":
                    default_value = existing_data.get(key, 0)
                    response = st.radio(
                        question,
                        options=["No", "Yes"],
                        index=default_value,
                        key=key,
                        horizontal=True,
                        label_visibility="collapsed"
                    )