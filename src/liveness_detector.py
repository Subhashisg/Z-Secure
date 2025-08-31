import cv2
import numpy as np
import mediapipe as mp
import time
from typing import Tuple, Dict, List, Optional
import math

class LivenessDetector:
    """Advanced liveness detection service to prevent spoofing attacks"""
    
    def __init__(self):
        # Initialize MediaPipe components
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face_detection = mp.solutions.face_detection
        
        # Face mesh for detailed analysis
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Face detection for basic checks
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.7
        )
        
        # Liveness check parameters
        self.blink_threshold = 0.2
        self.head_turn_threshold = 15  # degrees
        self.texture_variance_threshold = 50
        self.min_face_size = 100
        
        # Eye aspect ratio landmarks (for blink detection)
        self.LEFT_EYE_IDXS = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]
        self.RIGHT_EYE_IDXS = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        
    def calculate_eye_aspect_ratio(self, landmarks: List, eye_idxs: List[int]) -> float:
        """Calculate Eye Aspect Ratio (EAR) for blink detection"""
        try:
            # Get eye landmarks
            eye_points = []
            for idx in eye_idxs:
                if idx < len(landmarks):
                    point = landmarks[idx]
                    eye_points.append([point.x, point.y])
            
            if len(eye_points) < 6:
                return 0.0
            
            eye_points = np.array(eye_points)
            
            # Calculate distances
            # Vertical distances
            v1 = np.linalg.norm(eye_points[1] - eye_points[5])
            v2 = np.linalg.norm(eye_points[2] - eye_points[4])
            
            # Horizontal distance
            h = np.linalg.norm(eye_points[0] - eye_points[3])
            
            # Eye aspect ratio
            if h > 0:
                ear = (v1 + v2) / (2.0 * h)
                return ear
            
            return 0.0
            
        except Exception as e:
            print(f"Error calculating EAR: {e}")
            return 0.0
    
    def detect_blink(self, image: np.ndarray) -> Dict[str, any]:
        """Detect eye blink for liveness verification"""
        try:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_image)
            
            blink_data = {
                'blink_detected': False,
                'left_ear': 0.0,
                'right_ear': 0.0,
                'avg_ear': 0.0
            }
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Calculate EAR for both eyes
                    left_ear = self.calculate_eye_aspect_ratio(face_landmarks.landmark, self.LEFT_EYE_IDXS)
                    right_ear = self.calculate_eye_aspect_ratio(face_landmarks.landmark, self.RIGHT_EYE_IDXS)
                    
                    avg_ear = (left_ear + right_ear) / 2.0
                    
                    blink_data.update({
                        'left_ear': left_ear,
                        'right_ear': right_ear,
                        'avg_ear': avg_ear,
                        'blink_detected': avg_ear < self.blink_threshold
                    })
                    
                    break  # Process only first face
            
            return blink_data
            
        except Exception as e:
            print(f"Error in blink detection: {e}")
            return {'blink_detected': False, 'left_ear': 0.0, 'right_ear': 0.0, 'avg_ear': 0.0}
    
    def detect_head_movement(self, image: np.ndarray) -> Dict[str, any]:
        """Detect head movement for liveness verification"""
        try:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_image)
            
            movement_data = {
                'head_pose': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0},
                'movement_detected': False
            }
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Key points for pose estimation
                    landmarks = face_landmarks.landmark
                    
                    # Nose tip (1), chin (18), left eye corner (33), right eye corner (263)
                    nose_tip = landmarks[1]
                    chin = landmarks[18]
                    left_eye = landmarks[33]
                    right_eye = landmarks[263]
                    
                    # Calculate head pose angles
                    # Yaw (left-right rotation)
                    eye_center_x = (left_eye.x + right_eye.x) / 2
                    nose_x = nose_tip.x
                    yaw = (nose_x - eye_center_x) * 180  # Rough estimation
                    
                    # Pitch (up-down rotation)
                    nose_y = nose_tip.y
                    eye_center_y = (left_eye.y + right_eye.y) / 2
                    pitch = (nose_y - eye_center_y) * 180  # Rough estimation
                    
                    # Roll (tilt)
                    eye_slope = (right_eye.y - left_eye.y) / (right_eye.x - left_eye.x + 1e-6)
                    roll = math.atan(eye_slope) * 180 / math.pi
                    
                    movement_data['head_pose'] = {
                        'pitch': pitch,
                        'yaw': yaw,
                        'roll': roll
                    }
                    
                    # Check if significant movement detected
                    movement_detected = (
                        abs(yaw) > self.head_turn_threshold or
                        abs(pitch) > self.head_turn_threshold or
                        abs(roll) > self.head_turn_threshold
                    )
                    
                    movement_data['movement_detected'] = movement_detected
                    break
            
            return movement_data
            
        except Exception as e:
            print(f"Error in head movement detection: {e}")
            return {'head_pose': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0}, 'movement_detected': False}
    
    def analyze_texture_variance(self, image: np.ndarray) -> Dict[str, any]:
        """Analyze texture variance to detect printed photos or screens"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect face region
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(rgb_image)
            
            texture_data = {
                'variance': 0.0,
                'is_real': False,
                'face_detected': False
            }
            
            if results.detections:
                for detection in results.detections:
                    # Get face bounding box
                    bbox = detection.location_data.relative_bounding_box
                    h, w = image.shape[:2]
                    
                    x = int(bbox.xmin * w)
                    y = int(bbox.ymin * h)
                    width = int(bbox.width * w)
                    height = int(bbox.height * h)
                    
                    # Extract face region
                    face_region = gray[y:y+height, x:x+width]
                    
                    if face_region.size > 0:
                        # Calculate Laplacian variance (texture measure)
                        laplacian = cv2.Laplacian(face_region, cv2.CV_64F)
                        variance = laplacian.var()
                        
                        texture_data.update({
                            'variance': float(variance),
                            'is_real': variance > self.texture_variance_threshold,
                            'face_detected': True
                        })
                    
                    break  # Process only first detection
            
            return texture_data
            
        except Exception as e:
            print(f"Error in texture analysis: {e}")
            return {'variance': 0.0, 'is_real': False, 'face_detected': False}
    
    def check_face_quality(self, image: np.ndarray) -> Dict[str, any]:
        """Check face quality and size for liveness detection"""
        try:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(rgb_image)
            
            quality_data = {
                'face_detected': False,
                'face_size': 0,
                'face_area_ratio': 0.0,
                'quality_sufficient': False,
                'brightness_ok': False
            }
            
            if results.detections:
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    h, w = image.shape[:2]
                    
                    face_width = int(bbox.width * w)
                    face_height = int(bbox.height * h)
                    face_size = min(face_width, face_height)
                    
                    # Calculate face area ratio
                    face_area = face_width * face_height
                    image_area = w * h
                    face_area_ratio = face_area / image_area
                    
                    # Check brightness in face region
                    x = int(bbox.xmin * w)
                    y = int(bbox.ymin * h)
                    face_region = image[y:y+face_height, x:x+face_width]
                    
                    if face_region.size > 0:
                        avg_brightness = np.mean(cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY))
                        brightness_ok = 50 < avg_brightness < 200  # Good brightness range
                    else:
                        brightness_ok = False
                    
                    quality_data.update({
                        'face_detected': True,
                        'face_size': face_size,
                        'face_area_ratio': face_area_ratio,
                        'quality_sufficient': face_size >= self.min_face_size and face_area_ratio >= 0.1,
                        'brightness_ok': brightness_ok
                    })
                    
                    break
            
            return quality_data
            
        except Exception as e:
            print(f"Error in face quality check: {e}")
            return {'face_detected': False, 'face_size': 0, 'face_area_ratio': 0.0, 'quality_sufficient': False, 'brightness_ok': False}
    
    def comprehensive_liveness_check(self, image: np.ndarray) -> Dict[str, any]:
        """Perform comprehensive liveness check"""
        try:
            # Run all liveness checks
            blink_result = self.detect_blink(image)
            movement_result = self.detect_head_movement(image)
            texture_result = self.analyze_texture_variance(image)
            quality_result = self.check_face_quality(image)
            
            # Calculate liveness score
            liveness_score = 0.0
            checks_passed = 0
            total_checks = 4
            
            # Blink detection (25% weight)
            if blink_result['blink_detected'] or blink_result['avg_ear'] > 0.15:
                liveness_score += 0.25
                checks_passed += 1
            
            # Head movement (25% weight)
            if movement_result['movement_detected']:
                liveness_score += 0.25
                checks_passed += 1
            
            # Texture analysis (25% weight)
            if texture_result['is_real']:
                liveness_score += 0.25
                checks_passed += 1
            
            # Face quality (25% weight)
            if quality_result['quality_sufficient'] and quality_result['brightness_ok']:
                liveness_score += 0.25
                checks_passed += 1
            
            # Determine if liveness check passed
            # Require at least 2 out of 4 checks to pass, or score >= 0.5
            liveness_passed = checks_passed >= 2 or liveness_score >= 0.5
            
            # Compile comprehensive result
            result = {
                'liveness_passed': liveness_passed,
                'liveness_score': liveness_score,
                'checks_passed': checks_passed,
                'total_checks': total_checks,
                'blink_detection': blink_result,
                'head_movement': movement_result,
                'texture_analysis': texture_result,
                'face_quality': quality_result,
                'timestamp': time.time()
            }
            
            return result
            
        except Exception as e:
            print(f"Error in comprehensive liveness check: {e}")
            return {
                'liveness_passed': False,
                'liveness_score': 0.0,
                'checks_passed': 0,
                'total_checks': 4,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def process_image_for_liveness(self, image_data_b64: str) -> Dict[str, any]:
        """Process base64 image data for liveness detection"""
        try:
            import base64
            from PIL import Image
            import io
            
            # Handle data URL format
            if ',' in image_data_b64:
                image_data = base64.b64decode(image_data_b64.split(',')[1])
            else:
                image_data = base64.b64decode(image_data_b64)
            
            # Load image
            pil_image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Perform liveness check
            liveness_result = self.comprehensive_liveness_check(opencv_image)
            
            return liveness_result
            
        except Exception as e:
            print(f"Error processing image for liveness: {e}")
            return {
                'liveness_passed': False,
                'liveness_score': 0.0,
                'checks_passed': 0,
                'total_checks': 4,
                'error': f'Image processing error: {str(e)}',
                'timestamp': time.time()
            }
