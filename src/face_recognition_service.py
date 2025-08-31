import cv2
import numpy as np
import face_recognition
import pickle
import os
import base64
import json
from PIL import Image
import io

class FaceRecognitionService:
    """Advanced face recognition service for authentication"""
    
    def __init__(self):
        self.face_data_dir = 'face_data'
        self.tolerance = 0.4  # More strict tolerance for better security
        self.min_face_size = 50  # Minimum face size in pixels
        os.makedirs(self.face_data_dir, exist_ok=True)
    
    def process_face_data(self, face_data_b64):
        """Process base64 encoded face data and extract encoding"""
        try:
            print("Processing face data...")
            
            # Handle data URL format (data:image/jpeg;base64,...)
            if ',' in face_data_b64:
                image_data = base64.b64decode(face_data_b64.split(',')[1])
            else:
                image_data = base64.b64decode(face_data_b64)
            
            print(f"Decoded image data size: {len(image_data)} bytes")
            
            # Load image
            image = Image.open(io.BytesIO(image_data))
            print(f"Original image size: {image.size}, mode: {image.mode}")
            
            # Convert to RGB array
            if image.mode == 'RGBA':
                # Convert RGBA to RGB
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
                image = background
            elif image.mode not in ['RGB', 'L']:
                image = image.convert('RGB')
            
            image_array = np.array(image)
            print(f"Image array shape: {image_array.shape}")
            
            # Ensure RGB format
            if len(image_array.shape) == 2:
                # Grayscale to RGB
                image_array = np.stack([image_array] * 3, axis=-1)
            elif len(image_array.shape) == 3 and image_array.shape[2] == 4:
                # RGBA to RGB (shouldn't happen after PIL conversion, but just in case)
                image_array = image_array[:, :, :3]
            
            print(f"Final image array shape: {image_array.shape}")
            
            # Enhance image quality for better face detection
            image_array = self.enhance_image_quality(image_array)
            
            # Detect faces with both models for better accuracy
            face_locations_hog = face_recognition.face_locations(image_array, model='hog')
            face_locations_cnn = face_recognition.face_locations(image_array, model='cnn') if len(face_locations_hog) == 0 else []
            
            face_locations = face_locations_hog if len(face_locations_hog) > 0 else face_locations_cnn
            
            print(f"Detected {len(face_locations)} face(s)")
            
            if not face_locations:
                print("No faces detected in image")
                return None
            
            # Validate face size and quality
            for face_location in face_locations:
                top, right, bottom, left = face_location
                face_width = right - left
                face_height = bottom - top
                
                # Check minimum face size
                if face_width < self.min_face_size or face_height < self.min_face_size:
                    print(f"Face too small: {face_width}x{face_height}, minimum required: {self.min_face_size}x{self.min_face_size}")
                    return None
                
                # Check face aspect ratio (should be roughly square for a frontal face)
                aspect_ratio = face_width / face_height
                if aspect_ratio < 0.7 or aspect_ratio > 1.5:
                    print(f"Invalid face aspect ratio: {aspect_ratio}")
                    return None
            
            # Get face encodings with large model for better accuracy
            face_encodings = face_recognition.face_encodings(image_array, face_locations, model='large', num_jitters=2)
            
            print(f"Generated {len(face_encodings)} face encoding(s)")
            
            if not face_encodings:
                print("No face encodings generated")
                return None
            
            # Return the first face encoding
            encoding = face_encodings[0]
            print(f"Face encoding shape: {encoding.shape}")
            return encoding
            
        except Exception as e:
            print(f"Error processing face data: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_face_encoding(self, user_id, face_encoding):
        """Save face encoding to file"""
        try:
            face_file = os.path.join(self.face_data_dir, f"user_{user_id}.pkl")
            with open(face_file, 'wb') as f:
                pickle.dump(face_encoding, f)
            return True
        except Exception as e:
            print(f"Error saving face encoding: {e}")
            return False
    
    def load_face_encoding(self, user_id):
        """Load face encoding from file"""
        try:
            face_file = os.path.join(self.face_data_dir, f"user_{user_id}.pkl")
            if not os.path.exists(face_file):
                return None
            
            with open(face_file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading face encoding: {e}")
            return None
    
    def verify_face(self, user_id, face_data_b64):
        """Verify face against stored encoding"""
        try:
            print(f"Starting face verification for user {user_id}")
            
            # Load stored encoding from database first, then try file fallback
            stored_encoding = None
            
            # Try to get from database first
            try:
                from database_manager import DatabaseManager
                db_manager = DatabaseManager()
                stored_encoding = db_manager.get_face_encoding(user_id)
                print(f"Loaded face encoding from database: {stored_encoding is not None}")
            except Exception as db_error:
                print(f"Database error, trying file fallback: {db_error}")
                # Fallback to file storage
                stored_encoding = self.load_face_encoding(user_id)
                print(f"Loaded face encoding from file: {stored_encoding is not None}")
            
            if stored_encoding is None:
                print("No stored face encoding found")
                return False
            
            # Process current face data
            current_encoding = self.process_face_data(face_data_b64)
            if current_encoding is None:
                print("Failed to process current face data")
                return False
            
            print(f"Stored encoding shape: {stored_encoding.shape if hasattr(stored_encoding, 'shape') else 'No shape'}")
            print(f"Current encoding shape: {current_encoding.shape if hasattr(current_encoding, 'shape') else 'No shape'}")
            
            # Compare faces with distance calculation for debugging
            distances = face_recognition.face_distance([stored_encoding], current_encoding)
            distance = distances[0] if len(distances) > 0 else 1.0
            print(f"Face distance: {distance} (threshold: {self.tolerance})")
            
            # Additional security checks
            # 1. Check if distance is reasonable (not too close, indicating potential spoofing)
            if distance < 0.1:
                print("Warning: Distance too close, potential spoofing attempt")
                return False
            
            # 2. Verify encoding quality
            if not self._is_valid_encoding(stored_encoding) or not self._is_valid_encoding(current_encoding):
                print("Invalid encoding detected")
                return False
            
            # Compare faces with strict tolerance
            matches = face_recognition.compare_faces([stored_encoding], current_encoding, tolerance=self.tolerance)
            result = matches[0] if matches else False
            
            # Additional validation: even if match is True, reject if distance is too high
            if result and distance > self.tolerance * 0.8:  # 80% of tolerance as additional check
                print(f"Match rejected due to high distance: {distance}")
                result = False
            
            print(f"Face verification result: {result}")
            return result
            
        except Exception as e:
            print(f"Error verifying face: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_face_distance(self, user_id, face_data_b64):
        """Get face distance for additional security metrics"""
        try:
            stored_encoding = self.load_face_encoding(user_id)
            current_encoding = self.process_face_data(face_data_b64)
            
            if stored_encoding is None or current_encoding is None:
                return None
            
            distances = face_recognition.face_distance([stored_encoding], current_encoding)
            return distances[0] if len(distances) > 0 else None
            
        except Exception as e:
            print(f"Error calculating face distance: {e}")
            return None
    
    def update_face_encoding(self, user_id, new_face_data_b64):
        """Update face encoding for a user"""
        try:
            new_encoding = self.process_face_data(new_face_data_b64)
            if new_encoding is None:
                return False
            
            return self.save_face_encoding(user_id, new_encoding)
            
        except Exception as e:
            print(f"Error updating face encoding: {e}")
            return False
    
    def delete_face_data(self, user_id):
        """Delete face data for a user"""
        try:
            face_file = os.path.join(self.face_data_dir, f"user_{user_id}.pkl")
            if os.path.exists(face_file):
                os.remove(face_file)
            return True
        except Exception as e:
            print(f"Error deleting face data: {e}")
            return False
    
    def enhance_image_quality(self, image_array):
        """Enhance image quality for better face recognition"""
        try:
            # Apply histogram equalization
            if len(image_array.shape) == 3:
                # Convert to LAB color space
                lab = cv2.cvtColor(image_array, cv2.COLOR_RGB2LAB)
                l, a, b = cv2.split(lab)
                
                # Apply CLAHE to L channel
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                l = clahe.apply(l)
                
                # Merge channels and convert back to RGB
                enhanced = cv2.merge([l, a, b])
                enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
            else:
                # Grayscale image
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                enhanced = clahe.apply(image_array)
            
            return enhanced
        except Exception as e:
            print(f"Error enhancing image: {e}")
            return image_array
    
    def _is_valid_encoding(self, encoding):
        """Validate face encoding quality"""
        try:
            if encoding is None:
                return False
            
            # Check encoding shape
            if not hasattr(encoding, 'shape') or encoding.shape != (128,):
                return False
            
            # Check for all zeros or all ones (invalid encodings)
            if np.all(encoding == 0) or np.all(encoding == 1):
                return False
            
            # Check for reasonable variance (valid face encodings should have some variance)
            if np.var(encoding) < 0.001:
                return False
            
            # Check for extreme values
            if np.any(np.abs(encoding) > 5.0):
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating encoding: {e}")
            return False
