import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any
from config import Config

class ResultsDisplay:
    """Component for displaying prediction results"""
    
    def __init__(self):
        pass
    
    def render(self, results: Dict[str, Any]):
        """Render prediction results"""
        
        if not results.get("success"):
            st.error(f"❌ Prediction failed: {results.get('error', 'Unknown error')}")
            return
        
        predictions = results.get("predictions", {})
        
        # Main results header
        st.markdown("## 🎯 Hair Fall Prediction Results")
        
        # Key metrics
        self._display_key_metrics(predictions)
        
        # Detailed analysis
        self._display_detailed_analysis(predictions)
        
        # Visualization
        self._display_visualizations(predictions)
        
        # Recommendations
        self._display_recommendations(predictions)
        
        # Processing information
        self._display_processing_info(results)
        
        # Export options
        self._display_export_options(results)
    
    def _display_key_metrics(self, predictions: Dict[str, Any]):
        """Display key prediction metrics"""
        
        stage = predictions.get("stage", 0)
        condition = predictions.get("condition", "No")
        confidence = predictions.get("confidence", 0.0)
        
        st.markdown("### 📊 Key Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Hair fall stage
            stage_color = Config.STAGE_COLORS.get(stage, "#666666")
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border: 2px solid {stage_color}; border-radius: 10px;">
                <h2 style="color: {stage_color}; margin: 0;">Stage {stage}</h2>
                <p style="margin: 0.5rem 0;">{Config.STAGE_DESCRIPTIONS.get(stage, 'Unknown stage')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Hair fall condition
            condition_color = "#dc3545" if condition == "Yes" else "#28a745"
            condition_icon = "⚠️" if condition == "Yes" else "✅"
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border: 2px solid {condition_color}; border-radius: 10px;">
                <h2 style="color: {condition_color}; margin: 0;">{condition_icon} {condition}</h2>
                <p style="margin: 0.5rem 0;">Hair Fall Condition</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Confidence score
            confidence_color = "#28a745" if confidence > 0.8 else "#ffc107" if confidence > 0.6 else "#dc3545"
            confidence_text = "High" if confidence > 0.8 else "Medium" if confidence > 0.6 else "Low"
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border: 2px solid {confidence_color}; border-radius: 10px;">
                <h2 style="color: {confidence_color}; margin: 0;">{confidence:.1%}</h2>
                <p style="margin: 0.5rem 0;">Confidence ({confidence_text})</p>
            </div>
            """, unsafe_allow_html=True)
    
    def _display_detailed_analysis(self, predictions: Dict[str, Any]):
        """Display detailed analysis"""
        
        st.markdown("---")
        st.markdown("### 🔍 Detailed Analysis")
        
        detailed_results = predictions.get("detailed_results", {})
        interpretation = predictions.get("interpretation", "")
        
        # Model breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Model 1 (Biochemical Analysis)")
            model1_stage = detailed_results.get("model1_stage", 0)
            model1_conf = detailed_results.get("model1_confidence", 0.0)
            
            st.metric("Predicted Stage", f"Stage {model1_stage}")
            st.metric("Model Confidence", f"{model1_conf:.1%}")
            st.progress(model1_conf)
            
            st.markdown("""
            *Based on biochemical markers:*
            - Protein levels
            - Vitamin & mineral content
            - Stress indicators
            - Liver function data
            """)
        
        with col2:
            st.markdown("#### Model 2 (Lifestyle Analysis)")
            model2_condition = detailed_results.get("model2_condition", 0)
            model2_conf = detailed_results.get("model2_confidence", 0.0)
            condition_text = "Yes" if model2_condition == 1 else "No"
            
            st.metric("Hair Fall Risk", condition_text)
            st.metric("Model Confidence", f"{model2_conf:.1%}")
            st.progress(model2_conf)
            
            st.markdown("""
            *Based on lifestyle factors:*
            - Genetic predisposition
            - Stress levels
            - Environmental factors
            - Health conditions
            """)
        
        # Interpretation
        if interpretation:
            st.markdown("#### 💡 Clinical Interpretation")
            st.info(interpretation)
    
    def _display_visualizations(self, predictions: Dict[str, Any]):
        """Display visualizations"""
        
        st.markdown("---")
        st.markdown("### 📈 Visual Analysis")
        
        tab1, tab2, tab3 = st.tabs(["Stage Distribution", "Model Comparison", "Confidence Analysis"])
        
        with tab1:
            # Stage progression chart
            self._create_stage_chart(predictions)
        
        with tab2:
            # Model comparison
            self._create_model_comparison_chart(predictions)
        
        with tab3:
            # Confidence analysis
            self._create_confidence_chart(predictions)
    
    def _create_stage_chart(self, predictions: Dict[str, Any]):
        """Create stage progression chart"""
        
        current_stage = predictions.get("stage", 0)
        
        # Create data for all stages
        stages = list(range(6))  # 0-5
        stage_labels = [f"Stage {i}" for i in stages]
        colors = [Config.STAGE_COLORS.get(i, "#666666") for i in stages]
        
        # Highlight current stage
        bar_colors = ["lightgray" if i != current_stage else colors[i] for i in stages]
        
        fig = go.Figure(data=[
            go.Bar(
                x=stage_labels,
                y=[1 if i == current_stage else 0.3 for i in stages],
                marker_color=bar_colors,
                text=[Config.STAGE_DESCRIPTIONS.get(i, "") for i in stages],
                textposition="outside"
            )
        ])
        
        fig.update_layout(
            title="Hair Fall Stage Assessment",
            xaxis_title="Stages",
            yaxis_title="Current Level",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _create_model_comparison_chart(self, predictions: Dict[str, Any]):
        """Create model comparison chart"""
        
        detailed_results = predictions.get("detailed_results", {})
        
        models = ["Model 1 (Biochemical)", "Model 2 (Lifestyle)"]
        confidences = [
            detailed_results.get("model1_confidence", 0.0),
            detailed_results.get("model2_confidence", 0.0)
        ]
        weights = [
            detailed_results.get("ensemble_weights", {}).get("model1", 0.67),
            detailed_results.get("ensemble_weights", {}).get("model2", 0.33)
        ]
        
        fig = go.Figure(data=[
            go.Bar(name='Confidence', x=models, y=confidences, yaxis='y', offsetgroup=1),
            go.Bar(name='Weight', x=models, y=weights, yaxis='y2', offsetgroup=2)
        ])
        
        fig.update_layout(
            title='Model Performance Comparison',
            xaxis=dict(domain=[0, 1]),
            yaxis=dict(title='Confidence', side='left'),
            yaxis2=dict(title='Ensemble Weight', side='right', overlaying='y'),
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _create_confidence_chart(self, predictions: Dict[str, Any]):
        """Create confidence analysis chart"""
        
        confidence = predictions.get("confidence", 0.0)
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = confidence * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Prediction Confidence"},
            delta = {'reference': 80},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 60], 'color': "lightgray"},
                    {'range': [60, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Confidence interpretation
        if confidence > 0.8:
            st.success("🎯 High confidence prediction - Results are highly reliable")
        elif confidence > 0.6:
            st.warning("⚖️ Medium confidence prediction - Results are moderately reliable")
        else:
            st.error("⚠️ Low confidence prediction - Consider additional testing")
    
    def _display_recommendations(self, predictions: Dict[str, Any]):
        """Display recommendations based on results"""
        
        st.markdown("---")
        st.markdown("### 💡 Recommendations")
        
        stage = predictions.get("stage", 0)
        condition = predictions.get("condition", "No")
        confidence = predictions.get("confidence", 0.0)
        
        recommendations = []
        
        # Stage-based recommendations
        if stage == 0:
            recommendations.extend([
                "✅ Continue current hair care routine",
                "🥗 Maintain balanced nutrition",
                "💧 Stay hydrated",
                "😌 Manage stress levels"
            ])
        elif stage <= 2:
            recommendations.extend([
                "👀 Monitor hair health regularly",
                "🧴 Use gentle hair care products",
                "💊 Consider vitamin supplements",
                "🧘 Practice stress management"
            ])
        elif stage <= 4:
            recommendations.extend([
                "👨‍⚕️ Consult a dermatologist",
                "🔬 Consider additional medical tests",
                "💊 Evaluate nutritional deficiencies",
                "🚫 Avoid harsh hair treatments"
            ])
        else:
            recommendations.extend([
                "🚨 Seek immediate medical consultation",
                "🏥 Consider specialist referral",
                "💉 Explore treatment options",
                "📋 Regular medical monitoring"
            ])
        
        # Confidence-based recommendations
        if confidence < 0.6:
            recommendations.append("🔄 Consider retaking assessment with more detailed information")
        
        # Display recommendations
        col1, col2 = st.columns(2)
        
        mid_point = len(recommendations) // 2
        
        with col1:
            for rec in recommendations[:mid_point]:
                st.markdown(f"- {rec}")
        
        with col2:
            for rec in recommendations[mid_point:]:
                st.markdown(f"- {rec}")
        
        # Disclaimer
        st.warning("""
        ⚠️ **Important Disclaimer:**
        This is an AI-based prediction system for educational purposes. 
        Always consult qualified healthcare professionals for medical advice, 
        diagnosis, and treatment decisions.
        """)
    
    def _display_processing_info(self, results: Dict[str, Any]):
        """Display processing information"""
        
        with st.expander("🔧 Processing Details"):
            
            messages = results.get("messages", [])
            medical_processed = results.get("medical_report_processed", False)
            questionnaire_processed = results.get("questionnaire_processed", False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Data Sources:**")
                st.write(f"✅ Medical Report: {'Processed' if medical_processed else 'Not provided'}")
                st.write(f"✅ Questionnaire: {'Processed' if questionnaire_processed else 'Not provided'}")
            
            with col2:
                st.markdown("**Processing Messages:**")
                for message in messages:
                    st.write(f"• {message}")
    
    def _display_export_options(self, results: Dict[str, Any]):
        """Display export options"""
        
        st.markdown("---")
        st.markdown("### 📁 Export Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Download PDF Report", use_container_width=True):
                st.info("PDF export feature coming soon!")
        
        with col2:
            if st.button("📊 Export Data (JSON)", use_container_width=True):
                import json
                json_data = json.dumps(results, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name="hair_fall_prediction_results.json",
                    mime="application/json"
                )
        
        with col3:
            if st.button("🔄 New Analysis", use_container_width=True):
                if st.confirm("Clear all data and start new analysis?"):
                    from services.data_manager import DataManager
                    data_manager = DataManager()
                    data_manager.clear_all_data()
                    st.rerun()