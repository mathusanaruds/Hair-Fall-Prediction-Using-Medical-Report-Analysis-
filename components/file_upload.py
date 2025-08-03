import streamlit as st
from PIL import Image
import io
from typing import Optional
from config import Config
from services.data_manager import DataManager

class FileUploadComponent:
    """Component for handling file upload UI and logic"""
    
    def __init__(self):
        self.data_manager = DataManager()
    
    def render(self):
        """Render the file upload component"""
        
        # Check if file already uploaded
        completion_status = self.data_manager.get_completion_status()
        existing_file = self.data_manager.get_medical_file()
        
        if completion_status["medical_report"]:
            st.success("✅ Medical report uploaded successfully!")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("You can upload a different file if needed.")
            with col2:
                if st.button("🗑️ Remove File", use_container_width=True):
                    self.data_manager.save_medical_file(None)
                    st.session_state.medical_report_uploaded = False
                    st.rerun()
        
        # File upload instructions
        st.markdown("### 📄 Upload Your Medical Report")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **Supported file formats:**
            - 📄 **PDF files** - Laboratory reports, medical documents
            - 📝 **Text files** - Plain text medical reports
            - 🖼️ **Images** - Photos of medical reports (PNG, JPG, JPEG)
            
            **What to upload:**
            - Blood test results
            - Vitamin and mineral levels
            - Protein and keratin measurements
            - Liver function tests
            - Any relevant medical diagnostics
            """)
        
        with col2:
            st.markdown("""
            **File requirements:**
            - Max size: 16MB
            - Clear, readable text
            - Good image quality
            
            **Privacy:**
            - Files are processed temporarily
            - No permanent storage
            - Secure processing
            """)
        
        st.markdown("---")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a medical report file",
            type=Config.ALLOWED_FILE_TYPES,
            help="Upload PDF, TXT, or image files containing your medical report",
            key="medical_file_uploader"
        )
        
        if uploaded_file is not None:
            # Validate file
            validation_result = self._validate_file(uploaded_file)
            
            if validation_result["valid"]:
                # Display file information
                self._display_file_info(uploaded_file)
                
                # Preview file content
                self._preview_file(uploaded_file)
                
                # Save button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("💾 Save Medical Report", use_container_width=True, type="primary"):
                        # Reset file pointer
                        uploaded_file.seek(0)
                        self.data_manager.save_medical_file(uploaded_file)
                        st.rerun()
            else:
                st.error(f"❌ {validation_result['error']}")
        
        # Alternative input method
        st.markdown("---")
        st.markdown("### ✍️ Alternative: Manual Text Input")
        
        with st.expander("Enter medical report text manually"):
            manual_text = st.text_area(
                "Paste your medical report text here:",
                height=200,
                placeholder="Enter laboratory results, blood test values, vitamin levels, etc..."
            )
            
            if manual_text.strip():
                if st.button("💾 Save Manual Text", type="primary"):
                    # Create a text file object from the manual input
                    text_file = io.StringIO(manual_text)
                    text_file.name = "manual_input.txt"
                    self.data_manager.save_medical_file(text_file)
                    st.success("✅ Manual text saved successfully!")
                    st.rerun()
        
        # Current status
        if existing_file:
            st.markdown("---")
            st.markdown("### 📊 Current Upload Status")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                file_name = getattr(existing_file, 'name', 'Manual input')
                st.metric("File Name", file_name)
            
            with col2:
                file_type = self._get_file_type(existing_file)
                st.metric("File Type", file_type.upper())
            
            with col3:
                if hasattr(existing_file, 'size'):
                    file_size = f"{existing_file.size / 1024:.1f} KB"
                else:
                    file_size = "Unknown"
                st.metric("File Size", file_size)
    
    def _validate_file(self, file) -> dict:
        """Validate uploaded file"""
        if not file:
            return {"valid": False, "error": "No file provided"}
        
        # Check file size
        if hasattr(file, 'size') and file.size > Config.MAX_FILE_SIZE:
            return {"valid": False, "error": f"File size ({file.size / 1024 / 1024:.1f} MB) exceeds maximum allowed size (16 MB)"}
        
        # Check file type
        file_extension = file.name.split('.')[-1].lower() if '.' in file.name else ''
        if file_extension not in Config.ALLOWED_FILE_TYPES:
            return {"valid": False, "error": f"File type '{file_extension}' not supported. Allowed types: {', '.join(Config.ALLOWED_FILE_TYPES)}"}
        
        return {"valid": True}
    
    def _display_file_info(self, file):
        """Display file information"""
        st.markdown("#### 📋 File Information")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Name", file.name)
        
        with col2:
            file_type = self._get_file_type(file)
            st.metric("Type", file_type.upper())
        
        with col3:
            if hasattr(file, 'size'):
                size_mb = file.size / 1024 / 1024
                st.metric("Size", f"{size_mb:.2f} MB")
        
        with col4:
            st.metric("Status", "✅ Valid")
    
    def _preview_file(self, file):
        """Preview file content"""
        file_type = self._get_file_type(file)
        
        st.markdown("#### 👁️ File Preview")
        
        try:
            if file_type in ['png', 'jpg', 'jpeg']:
                # Image preview
                image = Image.open(file)
                
                # Resize for display
                max_width = 600
                if image.width > max_width:
                    ratio = max_width / image.width
                    new_height = int(image.height * ratio)
                    image = image.resize((max_width, new_height))
                
                st.image(image, caption="Uploaded medical report image")
                
                # Image info
                st.info(f"📏 Image dimensions: {image.width} x {image.height} pixels")
                
            elif file_type == 'txt':
                # Text preview
                file_content = file.read().decode('utf-8')
                file.seek(0)  # Reset file pointer
                
                preview_length = min(1000, len(file_content))
                preview_text = file_content[:preview_length]
                
                if len(file_content) > preview_length:
                    preview_text += "\n\n... (truncated)"
                
                st.text_area("Text content preview:", preview_text, height=200, disabled=True)
                st.info(f"📝 Text length: {len(file_content)} characters")
                
            elif file_type == 'pdf':
                # PDF preview (basic info only)
                st.info("📄 PDF file uploaded. Content will be extracted during processing.")
                st.warning("💡 Tip: Ensure the PDF contains clear, readable text for best results.")
                
        except Exception as e:
            st.warning(f"⚠️ Could not preview file: {str(e)}")
    
    def _get_file_type(self, file) -> str:
        """Get file type from file object"""
        if hasattr(file, 'name') and '.' in file.name:
            return file.name.split('.')[-1].lower()
        elif hasattr(file, 'type'):
            return file.type.split('/')[-1].lower()
        else:
            return 'unknown'