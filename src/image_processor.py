import os
import mimetypes
from PIL import Image
import numpy as np
import struct

class ImageProcessor:
    """Image processing and detection service"""
    
    def __init__(self):
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
        self.max_file_size = 16 * 1024 * 1024  # 16MB
    
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def detect_encryption(self, file_path):
        """Detect if image is encrypted using Z-secure algorithm"""
        try:
            # Check file size first
            if os.path.getsize(file_path) > self.max_file_size:
                return False
            
            # Read first few bytes to check for Z-secure signature
            with open(file_path, 'rb') as f:
                header = f.read(4)
            
            # Check for Z-secure signature
            if header == b'ZSEC':
                return True
            
            # Try to open as image to verify it's a normal image
            try:
                with Image.open(file_path) as img:
                    # If we can open it as an image, it's not encrypted
                    return False
            except Exception:
                # If we can't open it as an image but no Z-secure signature,
                # it might be corrupted or encrypted with different method
                return True
                
        except Exception as e:
            print(f"Error detecting encryption: {e}")
            return False
    
    def validate_image(self, file_path):
        """Validate image file integrity"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False, "File does not exist"
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return False, "File is empty"
            
            if file_size > self.max_file_size:
                return False, "File too large"
            
            # Check MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type or not mime_type.startswith('image/'):
                # Could be encrypted, check for Z-secure signature
                with open(file_path, 'rb') as f:
                    header = f.read(4)
                if header != b'ZSEC':
                    return False, "Invalid image file"
            
            return True, "Valid"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def get_image_info(self, file_path):
        """Get basic image information"""
        try:
            # Check if it's encrypted first
            if self.detect_encryption(file_path):
                return {
                    'encrypted': True,
                    'format': 'Z-Secure Encrypted',
                    'size': os.path.getsize(file_path),
                    'dimensions': None
                }
            
            # Get normal image info
            with Image.open(file_path) as img:
                return {
                    'encrypted': False,
                    'format': img.format,
                    'mode': img.mode,
                    'size': os.path.getsize(file_path),
                    'dimensions': img.size,
                    'has_transparency': img.mode in ('RGBA', 'LA', 'P')
                }
                
        except Exception as e:
            return {
                'error': str(e),
                'encrypted': 'unknown'
            }
    
    def optimize_image(self, file_path, quality=85):
        """Optimize image for processing"""
        try:
            with Image.open(file_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if too large
                max_dimension = 2048
                if max(img.size) > max_dimension:
                    ratio = max_dimension / max(img.size)
                    new_size = tuple(int(dim * ratio) for dim in img.size)
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Save optimized version
                optimized_path = file_path.replace('.', '_optimized.')
                img.save(optimized_path, 'JPEG', quality=quality, optimize=True)
                
                return optimized_path
                
        except Exception as e:
            print(f"Error optimizing image: {e}")
            return file_path
    
    def create_thumbnail(self, file_path, size=(150, 150)):
        """Create thumbnail for image preview"""
        try:
            if self.detect_encryption(file_path):
                # Can't create thumbnail for encrypted image
                return None
            
            with Image.open(file_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Save thumbnail
                thumbnail_path = file_path.replace('.', '_thumb.')
                img.save(thumbnail_path, 'JPEG', quality=80)
                
                return thumbnail_path
                
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return None
    
    def compare_images(self, img1_path, img2_path):
        """Compare two images for similarity"""
        try:
            # Skip comparison if either is encrypted
            if self.detect_encryption(img1_path) or self.detect_encryption(img2_path):
                return None
            
            with Image.open(img1_path) as img1, Image.open(img2_path) as img2:
                # Convert to same mode and size for comparison
                img1 = img1.convert('RGB').resize((64, 64))
                img2 = img2.convert('RGB').resize((64, 64))
                
                # Convert to arrays
                arr1 = np.array(img1)
                arr2 = np.array(img2)
                
                # Calculate MSE
                mse = np.mean((arr1 - arr2) ** 2)
                
                # Calculate similarity percentage
                max_mse = 255 ** 2
                similarity = max(0, 100 - (mse / max_mse * 100))
                
                return similarity
                
        except Exception as e:
            print(f"Error comparing images: {e}")
            return None
    
    def extract_metadata(self, file_path):
        """Extract metadata from image file"""
        try:
            if self.detect_encryption(file_path):
                # Try to extract Z-secure metadata
                return self._extract_zsecure_metadata(file_path)
            
            with Image.open(file_path) as img:
                metadata = {
                    'filename': os.path.basename(file_path),
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'file_size': os.path.getsize(file_path)
                }
                
                # Extract EXIF data if available
                if hasattr(img, '_getexif') and img._getexif():
                    metadata['exif'] = dict(img._getexif())
                
                return metadata
                
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_zsecure_metadata(self, file_path):
        """Extract metadata from Z-secure encrypted file"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            if not data.startswith(b'ZSEC'):
                return {'error': 'Not a Z-secure encrypted file'}
            
            # Extract metadata length
            metadata_length = struct.unpack('>I', data[4:8])[0]
            metadata_bytes = data[8:8+metadata_length]
            
            import json
            metadata = json.loads(metadata_bytes.decode('utf-8'))
            metadata['file_size'] = len(data)
            metadata['encrypted_size'] = len(data) - 8 - metadata_length
            
            return metadata
            
        except Exception as e:
            return {'error': f'Error extracting Z-secure metadata: {str(e)}'}
