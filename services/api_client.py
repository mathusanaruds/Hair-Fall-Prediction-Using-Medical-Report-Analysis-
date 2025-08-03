# Frontend API Client Fixes

# In services/api_client.py, update the make_prediction method:

def make_prediction(self, questionnaire_data: Optional[Dict] = None, 
                   medical_file: Optional[Any] = None) -> Dict[str, Any]:
    """Make prediction using backend API"""
    try:
        url = f"{self.base_url}{Config.ENDPOINTS['predict']}"
        
        # Prepare form data
        form_data = {}
        files = {}
        
        print(f"Making prediction request to: {url}")
        print(f"Questionnaire data: {questionnaire_data is not None}")
        print(f"Medical file: {medical_file is not None}")
        
        # Add questionnaire data if available
        if questionnaire_data:
            form_data.update(questionnaire_data)
            print(f"Form data keys: {list(form_data.keys())}")
        
        # Add medical file if available
        if medical_file:
            # Reset file pointer if it's a file object
            if hasattr(medical_file, 'seek'):
                medical_file.seek(0)
            
            # Handle different file types
            if hasattr(medical_file, 'read'):
                # It's a file-like object
                file_content = medical_file.read()
                if hasattr(medical_file, 'seek'):
                    medical_file.seek(0)
                
                files['medical_report'] = (
                    getattr(medical_file, 'name', 'uploaded_file'),
                    file_content,
                    getattr(medical_file, 'content_type', 'application/octet-stream')
                )
            else:
                # It's already file content
                files['medical_report'] = medical_file
            
            print(f"File prepared for upload: {list(files.keys())}")
        
        # Make request
        print(f"Sending request with {len(form_data)} form fields and {len(files)} files")
        
        if files:
            response = self.session.post(url, data=form_data, files=files)
        else:
            response = self.session.post(url, data=form_data)
        
        print(f"Response status: {response.status_code}")
        
        # Handle response
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction successful: {result.get('success', False)}")
            return result
        else:
            error_detail = "Unknown error"
            try:
                error_response = response.json()
                error_detail = error_response.get('error', 'Server error')
                print(f"Error response: {error_response}")
            except:
                error_detail = f"HTTP {response.status_code}: {response.text}"
            
            return {
                "success": False,
                "error": error_detail,
                "status_code": response.status_code
            }
            
    except requests.RequestException as e:
        error_msg = f"Request failed: {str(e)}"
        print(f"Request exception: {error_msg}")
        return {"success": False, "error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"Unexpected exception: {error_msg}")
        return {"success": False, "error": error_msg}

# Add a method to test questionnaire-only predictions:

def make_questionnaire_prediction(self, questionnaire_data: Dict) -> Dict[str, Any]:
    """Make prediction using only questionnaire data"""
    try:
        url = f"{self.base_url}/predict-questionnaire"
        
        print(f"Making questionnaire-only prediction to: {url}")
        print(f"Data: {questionnaire_data}")
        
        response = self.session.post(url, data=questionnaire_data)
        
        if response.status_code == 200:
            return response.json()
        else:
            try:
                error_response = response.json()
                return {"success": False, "error": error_response.get('error', 'Server error')}
            except:
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
    except Exception as e:
        return {"success": False, "error": str(e)}

# Add a method to test file uploads:

def test_file_upload(self, medical_file: Any) -> Dict[str, Any]:
    """Test file upload functionality"""
    try:
        url = f"{self.base_url}/test-upload"
        
        files = {}
        if hasattr(medical_file, 'read'):
            file_content = medical_file.read()
            if hasattr(medical_file, 'seek'):
                medical_file.seek(0)
            
            files['medical_report'] = (
                getattr(medical_file, 'name', 'test_file'),
                file_content,
                getattr(medical_file, 'content_type', 'application/octet-stream')
            )
        
        response = self.session.post(url, files=files)
        return response.json()
        
    except Exception as e:
        return {"success": False, "error": str(e)}